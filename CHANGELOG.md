# Changelog - ThreatEYE Weapon Detection System

## [1.1.0] - 2026-02-11

### Changed
- **Rebranding**: Application title changed from "SENTIENT EYE" to "ThreatEYE"
  - Updated frontend Dashboard component
  - Updated README.md documentation
  - Updated PROJECT.md complete documentation
  - Updated SETUP_GUIDE.md quick start guide
  - Updated design_guidelines.json

### Files Modified
- `/app/frontend/src/components/Dashboard.jsx` - Main title display
- `/app/README.md` - User documentation
- `/app/PROJECT.md` - Technical documentation
- `/app/SETUP_GUIDE.md` - Setup instructions
- `/app/design_guidelines.json` - Design specifications

---

## [1.0.0] - 2026-02-11

### Added
- **Real-time Weapon Detection System** using YOLOv8n
- **FastAPI Backend** with detection endpoints
- **React Frontend** with modern tactical dashboard UI
- **MongoDB Integration** for detection history
- **Webcam Integration** for live video feed
- **Bounding Box Overlay** with color-coded detections
- **Alert System** for weapon detection
- **Statistics Panel** showing real-time metrics
- **Detection Log** with timestamp tracking

### Features
- Detects: guns, knives, mobile phones, and other objects
- Real-time FPS monitoring
- System uptime tracking
- Dark tactical theme with glassmorphism effects
- Reticle-style corner brackets on video feed
- Responsive grid layout

### Technology Stack
- **Backend**: Python 3.11, FastAPI, YOLOv8, PyTorch, OpenCV, MongoDB
- **Frontend**: React 19, Tailwind CSS, Lucide Icons, Axios
- **AI Model**: YOLOv8n (lightweight, optimized for low GPU)

### Performance
- FPS: 2-3 frames per second
- Detection interval: 500ms
- Model size: 6.2 MB
- CPU optimized (no GPU required)

### Documentation
- README.md - User guide with API documentation
- PROJECT.md - Complete technical documentation
- SETUP_GUIDE.md - Quick setup instructions
- CHANGELOG.md - This file

---

## Future Roadmap

### Planned Features
- [ ] Email/SMS alerts on weapon detection
- [ ] Video file upload for batch processing
- [ ] Multi-camera support
- [ ] Custom training for weapon datasets
- [ ] Export detection reports (PDF/CSV)
- [ ] User authentication
- [ ] Real-time notifications via WebSocket
- [ ] Detection heatmap visualization
- [ ] RTSP camera stream integration
- [ ] Cloud storage for detection images

---

**Live Application**: https://easy-weapon-scan.preview.emergentagent.com

**Last Updated**: February 11, 2026
