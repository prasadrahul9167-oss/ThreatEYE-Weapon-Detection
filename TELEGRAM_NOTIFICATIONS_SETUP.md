# 🚨 Telegram Weapon Detection Alerts - ACTIVE

## ✅ Setup Complete!

Your ThreatEYE system is now configured to send instant Telegram notifications when weapons are detected.

---

## 📱 Configuration

### Telegram Bot Details
- **Bot Token**: `8379847326:AAGs2cWMq5nNKf9ifnIttb2s933CxOSC6iw`
- **Chat ID**: `93372553`
- **Alert Phone Number**: `9167937612`

### Alert Settings
- **Cooldown**: 10 seconds between alerts (prevents spam)
- **Notification Type**: Telegram instant message
- **Alert Format**: Markdown with emojis

---

## 📬 How It Works

### When Weapon is Detected:
1. ✅ YOLOv8 detects weapon (gun, knife, scissors, blade)
2. ✅ System sends instant Telegram message to your phone
3. ✅ Message includes:
   - Weapon type
   - Confidence percentage
   - Timestamp
   - Alert phone number

### Alert Message Format:
```
🚨 WEAPON DETECTED ALERT 🚨

⚠️ Type: knife
📊 Confidence: 85.5%
📱 Alert Number: 9167937612
⏰ Time: 2026-02-11 17:58:30
🎯 System: ThreatEYE Detection System

⚡ Immediate attention required!
```

---

## 🧪 Testing

### Test the Notification System:
```bash
curl -X POST https://easy-weapon-scan.preview.emergentagent.com/api/test-telegram
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Test notification sent to Telegram"
}
```

**Check Your Telegram:**
You should receive a test message immediately!

---

## 🔧 Configuration Files

### Backend Environment (.env)
Location: `/app/backend/.env`

```env
TELEGRAM_BOT_TOKEN="8379847326:AAGs2cWMq5nNKf9ifnIttb2s933CxOSC6iw"
TELEGRAM_CHAT_ID="93372553"
ALERT_PHONE_NUMBER="9167937612"
```

### Code Implementation
Location: `/app/backend/server.py`

**Features:**
- Async Telegram notifications (non-blocking)
- 10-second cooldown to prevent spam
- Automatic retry on failure
- Detailed logging
- Error handling

---

## 🎯 What Triggers Alerts

Alerts are sent when these weapons are detected:
- 🔫 Guns, pistols, rifles
- 🔪 Knives, blades
- ✂️ Scissors (sharp objects)
- ⚔️ Other weapons detected by YOLOv8

**Detection Thresholds:**
- General weapons: 25% confidence
- Knives: 20% confidence (more sensitive)

---

## 🚦 Alert Flow

```
[Webcam Feed]
     ↓
[YOLOv8 Detection]
     ↓
[Weapon Found?] → No → Continue monitoring
     ↓ Yes
[Check Cooldown]
     ↓
[Send Telegram Alert] ⚡
     ↓
[You receive notification on phone] 📱
```

---

## 📊 Monitoring

### Check Backend Logs:
```bash
tail -f /var/log/supervisor/backend.err.log | grep -i telegram
```

### Recent Detections:
```bash
curl https://easy-weapon-scan.preview.emergentagent.com/api/recent-detections
```

### System Stats:
```bash
curl https://easy-weapon-scan.preview.emergentagent.com/api/stats
```

---

## 🔒 Security Notes

### Bot Token Security:
- ✅ Stored in .env file (not in code)
- ✅ Not exposed in API responses
- ✅ Only accessible by backend server

### Best Practices:
- Don't share your bot token publicly
- Regenerate token if compromised (via @BotFather)
- Keep .env file secure
- Monitor notification logs

### To Regenerate Token:
1. Message @BotFather in Telegram
2. Send `/mybots`
3. Select your bot
4. Choose "API Token" → "Revoke current token"
5. Update `.env` file with new token
6. Restart backend: `sudo supervisorctl restart backend`

---

## 🐛 Troubleshooting

### Problem: Not Receiving Notifications

**Check 1: Bot Token Valid?**
```bash
curl https://api.telegram.org/bot8379847326:AAGs2cWMq5nNKf9ifnIttb2s933CxOSC6iw/getMe
```
Should return bot info.

**Check 2: Chat ID Correct?**
```bash
curl https://api.telegram.org/bot8379847326:AAGs2cWMq5nNKf9ifnIttb2s933CxOSC6iw/getUpdates
```
Verify your chat ID appears.

**Check 3: Started Bot?**
- Open your bot in Telegram
- Send `/start`
- Try test notification again

**Check 4: Backend Logs**
```bash
tail -n 50 /var/log/supervisor/backend.err.log
```

### Problem: Too Many Notifications

**Adjust Cooldown:**
Edit `/app/backend/server.py`:
```python
ALERT_COOLDOWN = 30  # Change from 10 to 30 seconds
```

Restart: `sudo supervisorctl restart backend`

### Problem: Test Works but Real Detections Don't

**Check Detection Logs:**
```bash
curl -s https://easy-weapon-scan.preview.emergentagent.com/api/recent-detections | python3 -m json.tool
```

Verify `has_weapon: true` in recent detections.

---

## 🔄 Modifying Settings

### Change Alert Phone Number:
Edit `/app/backend/.env`:
```env
ALERT_PHONE_NUMBER="NEW_NUMBER_HERE"
```

Restart: `sudo supervisorctl restart backend`

### Change Cooldown Period:
Edit `/app/backend/server.py`:
```python
ALERT_COOLDOWN = 20  # seconds
```

### Change Message Format:
Edit `/app/backend/server.py` - find `send_telegram_alert` function and modify the `message` variable.

---

## 📈 Statistics

### Messages Sent:
Check backend logs for count:
```bash
grep "Telegram alert sent successfully" /var/log/supervisor/backend.err.log | wc -l
```

### Failed Alerts:
```bash
grep "Telegram alert failed" /var/log/supervisor/backend.err.log
```

---

## 🎓 Advanced Usage

### Multiple Recipients:
You can send to multiple chat IDs by modifying the function to loop through a list.

### Custom Alerts for Different Weapons:
Modify `send_telegram_alert()` to send different messages based on weapon type.

### Include Screenshot:
Future enhancement: Send photo of detection along with alert.

---

## ✅ Current Status

- ✅ **Telegram Bot**: Active
- ✅ **Notifications**: Enabled
- ✅ **Weapon Detection**: Running
- ✅ **Alert System**: Live
- ✅ **Test Passed**: Success

**System URL**: https://easy-weapon-scan.preview.emergentagent.com

---

## 📞 Next Steps

1. ✅ Test notification received - DONE
2. ✅ Monitor your Telegram for weapon alerts
3. ✅ Test with actual weapon detection (hold a knife/scissors in front of camera)
4. ✅ Verify you receive real-time alert

---

## 🎉 Success!

Your ThreatEYE weapon detection system is now fully operational with instant Telegram alerts!

Every weapon detection will trigger an immediate notification to your phone at Chat ID: **93372553**

**Stay safe and monitor your space! 🛡️**

---

*Last Updated: February 11, 2026*
*ThreatEYE v1.2.0 - Now with Telegram Alerts*
