import React, { useRef, useEffect, useState } from 'react';
import { Camera, CameraOff, AlertTriangle } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

export default function VideoFeed({ isActive, setIsActive, onDetection, setFps }) {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);
  const detectionIntervalRef = useRef(null);
  const [error, setError] = useState(null);
  const [hasWeapon, setHasWeapon] = useState(false);
  const [suspiciousPerson, setSuspiciousPerson] = useState(false);
  const lastFrameTimeRef = useRef(Date.now());

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: 1280, height: 720 }
      });
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        streamRef.current = stream;
        setIsActive(true);
        setError(null);
        startDetection();
      }
    } catch (err) {
      console.error('Camera error:', err);
      setError('Unable to access camera. Please check permissions.');
    }
  };

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
    if (detectionIntervalRef.current) {
      clearInterval(detectionIntervalRef.current);
    }
    setIsActive(false);
    setHasWeapon(false);
    setSuspiciousPerson(false);
  };

  const captureFrame = () => {
    const video = videoRef.current;
    const canvas = document.createElement('canvas');
    
    if (!video || video.readyState !== 4) return null;
    
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0);
    
    return canvas.toDataURL('image/jpeg', 0.8);
  };

  const startDetection = () => {
    if (detectionIntervalRef.current) {
      clearInterval(detectionIntervalRef.current);
    }

    detectionIntervalRef.current = setInterval(async () => {
      const frameData = captureFrame();
      if (!frameData) return;

      const now = Date.now();
      const fps = Math.round(1000 / (now - lastFrameTimeRef.current));
      setFps(fps);
      lastFrameTimeRef.current = now;

      try {
        const response = await fetch(`${BACKEND_URL}/api/detect`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ image: frameData })
        });

        const result = await response.json();
        drawDetections(result.detections);
        setHasWeapon(result.has_weapon);
        
        if (result.detections.length > 0) {
          onDetection(result);
        }
      } catch (error) {
        console.error('Detection error:', error);
      }
    }, 500);
  };

  const drawDetections = (detections) => {
    const canvas = canvasRef.current;
    const video = videoRef.current;
    
    if (!canvas || !video) return;
    
    const ctx = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    detections.forEach(detection => {
      const [x1, y1, x2, y2] = detection.bbox;
      const width = x2 - x1;
      const height = y2 - y1;
      
      const isWeapon = detection.class_name.toLowerCase().includes('knife') ||
                       detection.class_name.toLowerCase().includes('gun') ||
                       detection.class_name.toLowerCase().includes('pistol') ||
                       detection.class_name.toLowerCase().includes('weapon');
      
      const isPhone = detection.class_name.toLowerCase().includes('phone');
      const isPerson = detection.class_name.toLowerCase().includes('person');
      const hasSuspiciousAttributes = detection.attributes && detection.attributes.length > 0;
      
      let color = '#007AFF';
      if (isWeapon) color = '#FF3B30';
      else if (isPhone) color = '#FF9500';
      else if (isPerson && hasSuspiciousAttributes) color = '#FFD700'; // Gold for suspicious persons
      
      ctx.strokeStyle = color;
      ctx.lineWidth = 3;
      ctx.strokeRect(x1, y1, width, height);
      
      ctx.fillStyle = color;
      ctx.globalAlpha = 0.2;
      ctx.fillRect(x1, y1, width, height);
      ctx.globalAlpha = 1;
      
      // Build label with attributes
      let label = `${detection.class_name} ${Math.round(detection.confidence * 100)}%`;
      if (detection.attributes && detection.attributes.length > 0) {
        const attrText = detection.attributes.map(attr => {
          if (attr === 'FACE_COVERED') return 'Face Covered';
          if (attr === 'SUNGLASSES') return 'Sunglasses';
          if (attr === 'PARTIAL_COVER') return 'Partial Cover';
          return attr;
        }).join(', ');
        label += ` [${attrText}]`;
      }
      
      ctx.font = 'bold 14px JetBrains Mono';
      const textWidth = ctx.measureText(label).width;
      
      ctx.fillStyle = color;
      ctx.fillRect(x1, y1 - 25, textWidth + 10, 25);
      
      ctx.fillStyle = '#FFFFFF';
      ctx.fillText(label, x1 + 5, y1 - 7);
    });
  };

  useEffect(() => {
    return () => {
      stopCamera();
    };
  }, []);

  return (
    <div className="relative h-full border border-white/10 bg-[#0f0f11] rounded-sm overflow-hidden" data-testid="video-feed-container">
      <div className="reticle-corner top-left" />
      <div className="reticle-corner top-right" />
      <div className="reticle-corner bottom-left" />
      <div className="reticle-corner bottom-right" />
      
      {hasWeapon && (
        <div 
          className="absolute top-4 left-4 right-4 bg-red-500/20 border-2 border-red-500 p-4 rounded-sm flex items-center gap-3 z-10 alert-pulse"
          data-testid="weapon-alert"
        >
          <AlertTriangle className="w-6 h-6 text-red-500" />
          <span className="text-red-500 font-bold uppercase tracking-wide" style={{ fontFamily: 'Barlow Condensed, sans-serif' }}>
            WEAPON DETECTED
          </span>
        </div>
      )}
      
      <div className="relative w-full h-full flex items-center justify-center">
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className="max-w-full max-h-full object-contain"
          data-testid="video-element"
        />
        <canvas
          ref={canvasRef}
          className="absolute top-0 left-0 w-full h-full pointer-events-none"
          style={{ objectFit: 'contain' }}
        />
        
        {!isActive && !error && (
          <div className="absolute inset-0 flex items-center justify-center bg-black/50">
            <div className="text-center">
              <Camera className="w-16 h-16 text-white/50 mx-auto mb-4" />
              <p className="text-white/70 font-mono">Camera standby</p>
            </div>
          </div>
        )}
        
        {error && (
          <div className="absolute inset-0 flex items-center justify-center bg-black/50">
            <div className="text-center p-6">
              <CameraOff className="w-16 h-16 text-red-500 mx-auto mb-4" />
              <p className="text-red-400 font-mono">{error}</p>
            </div>
          </div>
        )}
      </div>
      
      <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-4">
        {!isActive ? (
          <button
            onClick={startCamera}
            className="h-12 px-8 bg-green-600 hover:bg-green-700 text-white font-mono text-sm uppercase tracking-wider rounded-sm border border-green-500/50 transition-all active:scale-95 flex items-center gap-2"
            data-testid="start-camera-btn"
          >
            <Camera className="w-5 h-5" />
            START DETECTION
          </button>
        ) : (
          <button
            onClick={stopCamera}
            className="h-12 px-8 bg-red-600 hover:bg-red-700 text-white font-mono text-sm uppercase tracking-wider rounded-sm border border-red-500/50 transition-all active:scale-95 flex items-center gap-2"
            data-testid="stop-camera-btn"
          >
            <CameraOff className="w-5 h-5" />
            STOP DETECTION
          </button>
        )}
      </div>
    </div>
  );
}