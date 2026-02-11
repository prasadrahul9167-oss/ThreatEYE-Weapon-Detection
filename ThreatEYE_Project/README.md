# 🎯 ThreatEYE - Weapon Detection System

![ThreatEYE](https://img.shields.io/badge/AI-YOLOv8-blue)
![Version](https://img.shields.io/badge/version-1.1.0-green)
![License](https://img.shields.io/badge/license-MIT-orange)

A real-time weapon detection system powered by YOLOv8 that identifies guns, knives, and mobile phones through webcam feed with a modern tactical dashboard interface.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+ and Yarn
- MongoDB (running on localhost:27017)
- Webcam

### Installation

```bash
# 1. Install backend dependencies
cd backend
pip install -r requirements.txt

# 2. Install frontend dependencies
cd ../frontend
yarn install

# 3. Configure environment variables
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
# Edit .env files with your settings

# 4. Start backend
cd backend
uvicorn server:app --host 0.0.0.0 --port 8001

# 5. Start frontend (in new terminal)
cd frontend
yarn start
```

### Access Application
Open browser: `http://localhost:3000`

## 📋 Features

- ✅ Real-time webcam detection
- ✅ YOLOv8n model (lightweight, CPU optimized)
- ✅ Detects guns, knives, mobile phones
- ✅ Live bounding box overlay
- ✅ Detection history logging
- ✅ System statistics dashboard
- ✅ Modern tactical UI with dark theme
- ✅ Alert system for weapon detection

## 📁 Project Structure

```
ThreatEYE_Project/
├── backend/
│   ├── server.py              # FastAPI server
│   ├── requirements.txt       # Python dependencies
│   └── .env.example          # Environment template
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── App.js           # Main app
│   │   └── index.css        # Styles
│   ├── package.json         # Node dependencies
│   └── .env.example        # Environment template
├── docs/
│   ├── README.md           # User guide
│   ├── PROJECT.md          # Technical docs
│   ├── SETUP_GUIDE.md      # Setup instructions
│   ├── CHANGELOG.md        # Version history
│   └── design_guidelines.json
├── tests/                  # Test files
├── scripts/                # Utility scripts
└── LICENSE                 # License file
```

## 🛠️ Technology Stack

**Backend:**
- Python 3.11+
- FastAPI
- YOLOv8 (Ultralytics)
- PyTorch
- OpenCV
- MongoDB (Motor)

**Frontend:**
- React 19
- Tailwind CSS
- Axios
- Lucide React Icons

## 📖 Documentation

Detailed documentation is available in the `docs/` folder:

- **[README.md](docs/README.md)** - Complete user guide
- **[PROJECT.md](docs/PROJECT.md)** - Technical documentation
- **[SETUP_GUIDE.md](docs/SETUP_GUIDE.md)** - Quick setup guide
- **[CHANGELOG.md](docs/CHANGELOG.md)** - Version history

## 🔧 API Endpoints

### GET `/api/`
Health check endpoint

### POST `/api/detect`
Process image and return detections
```json
{
  "image": "base64_encoded_image"
}
```

### GET `/api/stats`
Get system statistics

### GET `/api/recent-detections?limit=10`
Get detection history

## 🎨 UI Features

- **Dark Tactical Theme**: Professional security interface
- **Reticle Corners**: Military-style brackets on video feed
- **Color-Coded Detections**:
  - 🔴 Red: Weapons (guns, knives)
  - 🟠 Orange: Mobile phones
  - 🔵 Blue: Other objects
- **Real-time FPS Counter**: Performance monitoring
- **Glassmorphism Effects**: Modern blur effects

## 🧪 Testing

```bash
# Run backend tests
cd tests
python test_backend.py

# Manual testing
# 1. Start the application
# 2. Click "START DETECTION"
# 3. Hold objects in front of camera
# 4. Verify bounding boxes appear
```

## 📊 Performance

- **FPS**: 2-3 frames per second
- **Latency**: ~500ms per detection
- **Model Size**: 6.2 MB (YOLOv8n)
- **CPU Usage**: 30-40% during detection
- **GPU**: Not required

## 🐛 Troubleshooting

### Camera not working
- Check browser permissions
- Ensure HTTPS (camera requires secure context)
- Try different browser

### No detections appearing
- Check backend logs
- Verify YOLOv8 model downloaded
- Test API endpoint: `curl http://localhost:8001/api/`

### Low FPS
- Increase detection interval in VideoFeed.jsx
- Reduce camera resolution
- Check CPU usage

## 🚀 Future Enhancements

- [ ] Email/SMS alerts on weapon detection
- [ ] Video file upload for batch processing
- [ ] Multi-camera support
- [ ] Custom weapon dataset training
- [ ] Export detection reports (PDF/CSV)
- [ ] User authentication
- [ ] WebSocket real-time notifications
- [ ] Detection heatmap visualization

## 📝 License

MIT License - see LICENSE file for details

## 🙏 Credits

- **YOLOv8**: Ultralytics
- **Icons**: Lucide React
- **Framework**: React + FastAPI
- **Built with**: Emergent AI Platform

## 📞 Support

For issues or questions:
1. Check documentation in `docs/` folder
2. Review troubleshooting section
3. Check logs for errors

---

**Version**: 1.1.0  
**Last Updated**: February 11, 2026

⭐ If you find this project useful, please consider giving it a star!