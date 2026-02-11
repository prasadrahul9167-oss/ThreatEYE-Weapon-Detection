# 🚀 Quick Setup Guide - SENTIENT EYE

This is a simplified guide to get the weapon detection system running in minutes.

---

## ✅ Prerequisites Check

Before starting, ensure you have:
- [ ] Python 3.11 or higher
- [ ] Node.js 18+ and Yarn
- [ ] MongoDB running on localhost:27017
- [ ] A working webcam
- [ ] Internet connection (for model download)

---

## 📦 Installation Steps

### Step 1: Install Backend Dependencies (2-3 minutes)
```bash
cd /app/backend
pip install -r requirements.txt
```

**What gets installed:**
- YOLOv8 (AI model framework)
- FastAPI (web server)
- OpenCV (image processing)
- PyTorch (deep learning)
- MongoDB driver

### Step 2: Install Frontend Dependencies (1-2 minutes)
```bash
cd /app/frontend
yarn install
```

**What gets installed:**
- React and React Router
- Tailwind CSS
- Axios (API client)
- Lucide Icons

### Step 3: Configure Environment Variables

**Backend** - Check `/app/backend/.env`:
```env
MONGO_URL="mongodb://localhost:27017"
DB_NAME="test_database"
CORS_ORIGINS="*"
```

**Frontend** - Check `/app/frontend/.env`:
```env
REACT_APP_BACKEND_URL=https://easy-weapon-scan.preview.emergentagent.com
WDS_SOCKET_PORT=443
ENABLE_HEALTH_CHECK=false
```

> ⚠️ **Note**: URLs are pre-configured for cloud deployment. For local development, change to `http://localhost:8001`

### Step 4: Start Services
```bash
sudo supervisorctl restart backend frontend
```

Wait 10-15 seconds for services to start.

### Step 5: Verify Services Are Running
```bash
# Check status
sudo supervisorctl status

# Expected output:
# backend    RUNNING   pid 1234
# frontend   RUNNING   pid 5678
```

### Step 6: Test Backend API
```bash
curl https://easy-weapon-scan.preview.emergentagent.com/api/
```

**Expected response:**
```json
{"message":"Weapon Detection System API","status":"active"}
```

### Step 7: Open in Browser
Navigate to:
```
https://easy-weapon-scan.preview.emergentagent.com
```

---

## 🎮 How to Use

### 1️⃣ Start Detection
1. Click the green **"START DETECTION"** button
2. Allow camera permissions when prompted
3. Wait for video feed to appear

### 2️⃣ Test Detection
- Hold a phone in front of the camera
- Hold keys, pens, or other objects
- Watch bounding boxes appear in real-time

### 3️⃣ Monitor Results
- **Top Right**: FPS counter and system status
- **Right Panel (Top)**: Detection log with timestamps
- **Right Panel (Bottom)**: Statistics (total detections, weapons, phones, uptime)

### 4️⃣ Stop Detection
- Click the red **"STOP DETECTION"** button

---

## 🔍 Verification Checklist

After setup, verify each component:

### Backend ✅
```bash
# Test health endpoint
curl https://easy-weapon-scan.preview.emergentagent.com/api/

# Test stats endpoint
curl https://easy-weapon-scan.preview.emergentagent.com/api/stats
```

### Frontend ✅
- [ ] Page loads without errors
- [ ] Header shows "SENTIENT EYE"
- [ ] Video feed area visible with corner brackets
- [ ] START DETECTION button appears
- [ ] Detection Log panel shows "No detections yet"
- [ ] System Stats panel displays 4 metrics

### Camera ✅
- [ ] Browser requests camera permission
- [ ] Video feed shows webcam
- [ ] Detection starts when button clicked

### Detection ✅
- [ ] Bounding boxes appear on objects
- [ ] Labels show class name and confidence %
- [ ] Detection log updates in real-time
- [ ] Stats panel increments counts

---

## 🛠️ Common Issues & Quick Fixes

### ❌ Issue: Backend not starting
**Check logs:**
```bash
tail -n 50 /var/log/supervisor/backend.err.log
```

**Solution:**
```bash
# Reinstall dependencies
cd /app/backend
pip install -r requirements.txt
sudo supervisorctl restart backend
```

### ❌ Issue: Frontend not loading
**Check logs:**
```bash
tail -n 50 /var/log/supervisor/frontend.err.log
```

**Solution:**
```bash
# Reinstall and rebuild
cd /app/frontend
yarn install
sudo supervisorctl restart frontend
```

### ❌ Issue: Camera not working
**Symptoms**: Permission denied or black screen

**Solutions**:
1. Ensure you're using HTTPS (camera requires secure context)
2. Check browser permissions (Settings → Privacy → Camera)
3. Try different browser (Chrome recommended)
4. Refresh page and try again

### ❌ Issue: No detections appearing
**Symptoms**: Camera works but no bounding boxes

**Check backend is responding:**
```bash
curl https://easy-weapon-scan.preview.emergentagent.com/api/stats
```

**Check browser console (F12)** for errors

**Solution:**
```bash
# Restart backend
sudo supervisorctl restart backend

# Wait 10 seconds
sleep 10

# Test again
curl https://easy-weapon-scan.preview.emergentagent.com/api/
```

### ❌ Issue: MongoDB errors
**Symptoms**: Errors mentioning "MongoDB" or "connection refused"

**Check MongoDB:**
```bash
# Test MongoDB connection
mongo --eval "db.runCommand({ping:1})"
```

**Start MongoDB:**
```bash
sudo systemctl start mongod
# or
sudo service mongodb start
```

---

## 📊 Performance Tips

### For Better FPS (Speed)
Edit `/app/frontend/src/components/VideoFeed.jsx`:
```javascript
// Change from 500ms to 1000ms
detectionIntervalRef.current = setInterval(async () => {
  // ...
}, 1000);  // Slower but less CPU usage
```

### For Better Accuracy
Edit `/app/backend/server.py`:
```python
# Lower confidence threshold (more detections)
results = model(img_array, conf=0.2, verbose=False)  # Changed from 0.3
```

### For Lower CPU Usage
1. Increase detection interval (500ms → 1000ms)
2. Reduce camera resolution
3. Use larger confidence threshold (0.3 → 0.5)

---

## 📁 Project Files Overview

```
/app/
├── backend/
│   ├── server.py          # Main FastAPI server
│   ├── requirements.txt   # Python packages
│   └── .env              # Backend config
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── App.js       # Main app
│   │   └── index.css    # Styles
│   ├── package.json     # Node packages
│   └── .env            # Frontend config
├── README.md           # User guide
├── PROJECT.md          # Complete documentation
└── SETUP_GUIDE.md      # This file
```

---

## 🎯 Next Steps

After successful setup:

1. **Test with real objects**: Try phones, keys, pens, etc.
2. **Review detection logs**: Check accuracy and confidence scores
3. **Monitor statistics**: Watch total detections count increase
4. **Experiment with settings**: Adjust confidence threshold, FPS, etc.
5. **Read full documentation**: See PROJECT.md for advanced features

---

## 📞 Need Help?

### Quick Diagnostics
```bash
# Check all services
sudo supervisorctl status

# Test backend
curl https://easy-weapon-scan.preview.emergentagent.com/api/stats

# View recent backend errors
tail -n 20 /var/log/supervisor/backend.err.log

# View recent frontend errors
tail -n 20 /var/log/supervisor/frontend.err.log

# Check MongoDB
mongo --eval "db.detections.count()"
```

### Restart Everything
```bash
# Nuclear option - restart all services
sudo supervisorctl restart backend frontend
sleep 15  # Wait for services to start
```

### Check System Resources
```bash
# CPU and memory usage
top

# Disk space
df -h

# Port usage
netstat -tulpn | grep -E ':(3000|8001|27017)'
```

---

## ✨ Success!

If you can see the dashboard, start detection, and see bounding boxes on objects, you're all set! 🎉

**Live URL**: https://easy-weapon-scan.preview.emergentagent.com

---

## 🔗 Related Files

- **README.md** - User guide with features and API docs
- **PROJECT.md** - Complete technical documentation
- **design_guidelines.json** - UI/UX specifications

---

*Setup completed in under 5 minutes!*
