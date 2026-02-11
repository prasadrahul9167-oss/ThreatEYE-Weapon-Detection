from fastapi import FastAPI, APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone
import cv2
import numpy as np
from ultralytics import YOLO
import base64
import io
from PIL import Image

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI()
api_router = APIRouter(prefix="/api")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

model = None
MODEL_PATH = ROOT_DIR / 'yolov8n.pt'
face_cascade = None
eye_cascade = None

WEAPON_CLASSES = {
    0: 'person',
    24: 'backpack',
    26: 'handbag',
    67: 'cell phone'
}

class Detection(BaseModel):
    class_name: str
    confidence: float
    bbox: List[float]
    attributes: Optional[List[str]] = []

class DetectionResult(BaseModel):
    detections: List[Detection]
    total_count: int
    has_weapon: bool
    suspicious_person: bool
    timestamp: str

class DetectionRequest(BaseModel):
    image: str

class SystemStats(BaseModel):
    total_detections: int
    gun_count: int
    knife_count: int
    phone_count: int
    uptime: str

app_start_time = datetime.now(timezone.utc)

def load_model():
    global model, face_cascade, eye_cascade
    try:
        if not MODEL_PATH.exists():
            logger.info("Downloading YOLOv8n model...")
            model = YOLO('yolov8n.pt')
            model.save(str(MODEL_PATH))
        else:
            logger.info("Loading existing YOLOv8n model...")
            model = YOLO(str(MODEL_PATH))
        logger.info("Model loaded successfully")
        
        # Load face and eye cascade classifiers
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        logger.info("Face detection classifiers loaded")
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        model = YOLO('yolov8n.pt')

def detect_face_attributes(img_array, person_bbox):
    """Detect if person has face covered or wearing sunglasses"""
    attributes = []
    
    try:
        x1, y1, x2, y2 = [int(coord) for coord in person_bbox]
        
        # Ensure bbox is within image bounds
        h, w = img_array.shape[:2]
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        
        if x2 <= x1 or y2 <= y1:
            return attributes
            
        # Extract person region
        person_img = img_array[y1:y2, x1:x2]
        
        if person_img.size == 0:
            return attributes
        
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(person_img, cv2.COLOR_RGB2GRAY)
        
        # Detect faces in person region
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            # No face detected - likely face is covered
            attributes.append("FACE_COVERED")
        else:
            # Face detected, check for eyes
            for (fx, fy, fw, fh) in faces:
                face_roi_gray = gray[fy:fy+fh, fx:fx+fw]
                eyes = eye_cascade.detectMultiScale(face_roi_gray, 1.1, 3)
                
                if len(eyes) == 0:
                    # Face visible but no eyes detected - likely wearing sunglasses or face partially covered
                    attributes.append("SUNGLASSES")
                elif len(eyes) < 2:
                    # Only one eye detected - partially covered
                    attributes.append("PARTIAL_COVER")
    
    except Exception as e:
        logger.error(f"Error detecting face attributes: {e}")
    
    return attributes

load_model()

@api_router.get("/")
async def root():
    return {"message": "Weapon Detection System API", "status": "active"}

@api_router.post("/detect", response_model=DetectionResult)
async def detect_weapons(request: DetectionRequest):
    try:
        image_data = base64.b64decode(request.image.split(',')[1] if ',' in request.image else request.image)
        image = Image.open(io.BytesIO(image_data))
        img_array = np.array(image)
        
        if img_array.shape[2] == 4:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)
        
        results = model(img_array, conf=0.3, verbose=False)
        
        detections = []
        has_weapon = False
        suspicious_person = False
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                
                class_name = model.names[cls_id]
                
                weapon_keywords = ['knife', 'gun', 'pistol', 'rifle', 'weapon']
                is_weapon = any(keyword in class_name.lower() for keyword in weapon_keywords)
                
                # Detect face attributes for persons
                attributes = []
                if cls_id == 0:  # Person class
                    attributes = detect_face_attributes(img_array, [x1, y1, x2, y2])
                    if any(attr in attributes for attr in ["FACE_COVERED", "SUNGLASSES", "PARTIAL_COVER"]):
                        suspicious_person = True
                
                if cls_id in WEAPON_CLASSES or is_weapon or cls_id == 67:
                    detection = Detection(
                        class_name=class_name,
                        confidence=conf,
                        bbox=[x1, y1, x2, y2],
                        attributes=attributes
                    )
                    detections.append(detection)
                    
                    if is_weapon:
                        has_weapon = True
        
        detection_doc = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'detections': [d.model_dump() for d in detections],
            'has_weapon': has_weapon,
            'suspicious_person': suspicious_person
        }
        await db.detections.insert_one(detection_doc)
        
        return DetectionResult(
            detections=detections,
            total_count=len(detections),
            has_weapon=has_weapon,
            timestamp=detection_doc['timestamp']
        )
    
    except Exception as e:
        logger.error(f"Detection error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/stats", response_model=SystemStats)
async def get_stats():
    try:
        total = await db.detections.count_documents({})
        
        gun_count = await db.detections.count_documents({
            'detections.class_name': {'$regex': 'gun|pistol|rifle|weapon', '$options': 'i'}
        })
        
        knife_count = await db.detections.count_documents({
            'detections.class_name': {'$regex': 'knife', '$options': 'i'}
        })
        
        phone_count = await db.detections.count_documents({
            'detections.class_name': {'$regex': 'phone|cell', '$options': 'i'}
        })
        
        uptime = str(datetime.now(timezone.utc) - app_start_time).split('.')[0]
        
        return SystemStats(
            total_detections=total,
            gun_count=gun_count,
            knife_count=knife_count,
            phone_count=phone_count,
            uptime=uptime
        )
    except Exception as e:
        logger.error(f"Stats error: {e}")
        return SystemStats(
            total_detections=0,
            gun_count=0,
            knife_count=0,
            phone_count=0,
            uptime="0:00:00"
        )

@api_router.get("/recent-detections")
async def get_recent_detections(limit: int = 10):
    try:
        detections = await db.detections.find(
            {},
            {"_id": 0}
        ).sort("timestamp", -1).limit(limit).to_list(limit)
        return {"detections": detections}
    except Exception as e:
        logger.error(f"Recent detections error: {e}")
        return {"detections": []}

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()