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
import requests
import asyncio

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

WEAPON_CLASSES = {
    0: 'person',
    24: 'backpack',
    26: 'handbag',
    43: 'knife',  # Add knife class if available
    44: 'scissors',  # Scissors can be weapon-like
    67: 'cell phone'
}

class Detection(BaseModel):
    class_name: str
    confidence: float
    bbox: List[float]

class DetectionResult(BaseModel):
    detections: List[Detection]
    total_count: int
    has_weapon: bool
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

# Telegram configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
ALERT_PHONE_NUMBER = os.getenv('ALERT_PHONE_NUMBER', '9167937612')

# Track last alert time to avoid spam
last_alert_time = None
ALERT_COOLDOWN = 10  # seconds between alerts

async def send_telegram_alert(weapon_type: str, confidence: float, timestamp: str):
    """Send Telegram notification when weapon is detected"""
    global last_alert_time
    
    # Check cooldown to avoid spam
    now = datetime.now(timezone.utc)
    if last_alert_time:
        time_diff = (now - last_alert_time).total_seconds()
        if time_diff < ALERT_COOLDOWN:
            logger.info(f"Alert cooldown active. Skipping notification.")
            return
    
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logger.warning("Telegram credentials not configured")
        return
    
    try:
        message = f"""
🚨 *WEAPON DETECTED ALERT* 🚨

⚠️ *Type:* {weapon_type}
📊 *Confidence:* {confidence}%
📱 *Alert Number:* {ALERT_PHONE_NUMBER}
⏰ *Time:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🎯 *System:* ThreatEYE Detection System

⚡ Immediate attention required!
        """
        
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        # Send asynchronously without blocking
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: requests.post(url, json=payload, timeout=5)
        )
        
        if response.status_code == 200:
            logger.info(f"Telegram alert sent successfully for {weapon_type}")
            last_alert_time = now
        else:
            logger.error(f"Telegram alert failed: {response.text}")
            
    except Exception as e:
        logger.error(f"Error sending Telegram alert: {e}")

def load_model():
    global model
    try:
        if not MODEL_PATH.exists():
            logger.info("Downloading YOLOv8n model...")
            model = YOLO('yolov8n.pt')
            model.save(str(MODEL_PATH))
        else:
            logger.info("Loading existing YOLOv8n model...")
            model = YOLO(str(MODEL_PATH))
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        model = YOLO('yolov8n.pt')

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
        
        # Use lower confidence for knife detection to catch more instances
        results = model(img_array, conf=0.25, verbose=False)
        
        detections = []
        has_weapon = False
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                
                class_name = model.names[cls_id]
                
                # Expanded weapon keywords for better detection
                weapon_keywords = ['knife', 'gun', 'pistol', 'rifle', 'weapon', 'sword', 'blade', 'scissors']
                is_weapon = any(keyword in class_name.lower() for keyword in weapon_keywords)
                
                # Check if it's a knife class (class 43 in some COCO variations)
                is_knife = cls_id == 43 or 'knife' in class_name.lower() or 'scissors' in class_name.lower()
                
                # For knife detection, accept lower confidence threshold
                if is_knife and conf >= 0.2:
                    is_weapon = True
                
                if cls_id in WEAPON_CLASSES or is_weapon or cls_id == 67:
                    detection = Detection(
                        class_name=class_name,
                        confidence=conf,
                        bbox=[x1, y1, x2, y2]
                    )
                    detections.append(detection)
                    
                    if is_weapon:
                        has_weapon = True
                        # Send Telegram alert for weapon detection
                        asyncio.create_task(
                            send_telegram_alert(
                                weapon_type=class_name,
                                confidence=round(conf * 100, 1),
                                timestamp=datetime.now(timezone.utc).isoformat()
                            )
                        )
        
        detection_doc = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'detections': [d.model_dump() for d in detections],
            'has_weapon': has_weapon
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

@api_router.post("/test-telegram")
async def test_telegram_notification():
    """Test endpoint to verify Telegram notifications work"""
    try:
        await send_telegram_alert(
            weapon_type="TEST - System Check",
            confidence=100.0,
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        return {"status": "success", "message": "Test notification sent to Telegram"}
    except Exception as e:
        logger.error(f"Test notification error: {e}")
        return {"status": "error", "message": str(e)}

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