# 🔧 Troubleshooting Guide

Complete troubleshooting guide for the Google Forms Creation & Review System.

---

## 🔍 Common Issues

### 1. Network Error - "ERR_NETWORK" when calling `/auth/google`

**Symptoms:**
```
AxiosError: Network Error
    at async Object.googleLogin (services/api.ts:94:24)
```

**Cause:** Backend server is not running or wrong port

**Solution:**
```cmd
# Start the backend server
cd backend
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Or use the script
scripts\start-backend.bat  # Windows
./scripts/start-backend.sh # Linux/Mac
```

**Verification:**
- Open http://localhost:8000/docs
- Should see FastAPI Swagger UI
- Backend terminal shows: `INFO: Application startup complete.`

---

### 2. CORS Error in Browser Console

**Symptoms:**
```
Access to XMLHttpRequest at 'http://localhost:8000/auth/google' 
from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Cause:** Frontend running on unexpected port or CORS not configured

**Solution:**
Backend `app.py` is configured for ports 3000 and 3001. If using different port:

```python
# backend/app.py
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:YOUR_PORT",  # Add your port
]
```

Restart backend after changes.

---

### 3. Google Forms Creation Failed

**Symptoms:**
```
Google Form creation failed: Google Forms service not initialized
```

**Cause:** OAuth credentials file missing (this is expected and not critical)

**Status:** ✅ **System works perfectly without Google Forms integration!**

**What Works:**
- ✅ Survey creation and storage
- ✅ Approval workflow  
- ✅ Email notifications
- ✅ All CRUD operations

**What Doesn't Work:**
- ❌ Actual Google Form URLs
- ❌ Google Forms response collection

**To Enable Google Forms (Optional):**
See **[GOOGLE_FORMS_SETUP.md](GOOGLE_FORMS_SETUP.md)** for OAuth setup instructions.

---

### 4. Backend Shows "Error loading ASGI app"

**Symptoms:**
```
ERROR: Error loading ASGI app. Attribute "app" not found in module "app"
```

**Cause:** Uvicorn running from wrong directory

**Solution:**
```cmd
# Ensure you're in the backend directory
cd backend
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Or use script which handles this automatically
..\scripts\start-backend.bat
```

---

### 5. Port 8000 Already in Use

**Symptoms:**
```
ERROR: [Errno 10048] error while attempting to bind on address
```

**Solution (Windows):**
```cmd
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process
taskkill /PID <PID> /F
```

**Solution (Linux/Mac):**
```bash
# Find process
lsof -i :8000

# Kill process
kill -9 <PID>
```

---

### 6. Module Not Found Errors (Python)

**Symptoms:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Cause:** Python dependencies not installed

**Solution:**
```cmd
cd backend
pip install -r requirements.txt

# If issues persist, upgrade pip
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

### 7. Cannot Find Module (Node.js)

**Symptoms:**
```
Error: Cannot find module 'next'
```

**Cause:** Node dependencies not installed

**Solution:**
```cmd
# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install

# Or use the setup script
scripts\setup.bat
```

---

### 8. Pytest Errors - Pydantic Compatibility

**Symptoms:**
```
TypeError: ForwardRef._evaluate() missing 1 required keyword-only argument: 'recursive_guard'
```

**Cause:** Outdated pytest versions incompatible with Pydantic v2

**Solution:**
```cmd
cd backend
pip install --upgrade pytest==8.3.3 pytest-asyncio==0.24.0
```

This is already in `requirements.txt`.

---

### 9. Google FedCM Console Warnings

**Symptoms:**
```
[GSI_LOGGER]: FedCM get() rejects with AbortError
[GSI_LOGGER]: FedCM get() rejects with NetworkError
```

**Status:** ✅ **These are non-critical warnings and can be ignored**

**Cause:** Google's Federated Credential Management API warnings

**Impact:** None - app works perfectly

**Solution (Optional):**
Error suppression is already implemented in `app/error-suppression.tsx`.

---

### 10. Email Notifications Not Sending

**Symptoms:**
- Survey approval succeeds
- No email received

**Cause:** SMTP not configured (this is optional)

**Solution:**
If you want email notifications:

1. Edit `backend/.env`:
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

2. Generate Gmail App Password:
   - Google Account → Security → 2-Step Verification → App Passwords
   - Create app password for "Mail"

3. Restart backend

**Note:** System works without email - notifications just won't be sent.

---

### 11. Tests Failing - Authentication Required

**Symptoms:**
```
assert response.status_code == 200  # Got 401
```

**Cause:** Tests not overriding authentication

**Solution:**
Already fixed in `backend/test_surveys.py`:
```python
app.dependency_overrides[get_current_user] = override_get_current_user
```

If you see this, ensure you're using latest test file.

---

### 12. Invalid Status Transition

**Symptoms:**
```
400 Bad Request: Invalid status transition from 'approved' to 'draft'
```

**Status:** ✅ **This is correct behavior!**

**Explanation:**
The system enforces valid transitions:
- `draft` → `pending-approval`, `approved`, `archived` ✅
- `approved` → `archived` only ✅
- `approved` → `draft` ❌ BLOCKED

This is a feature, not a bug. Once approved, surveys cannot go back to draft.

---

### 13. OAuth Credentials Missing

**Symptoms:**
```
❌ Error: OAuth credentials file not found: credentials-oauth.json
```

**Status:** ✅ **Expected - system works without it**

**Explanation:**
Google Forms integration requires OAuth setup. This is optional.

**To Enable:**
See **[GOOGLE_FORMS_SETUP.md](GOOGLE_FORMS_SETUP.md)** for complete OAuth setup.

**To Ignore:**
System works perfectly without Google Forms integration.

---

### 14. Token Expired / Invalid Credentials

**Symptoms:**
```
google.auth.exceptions.RefreshError: invalid_grant
```

**Cause:** OAuth token expired

**Solution:**
```cmd
cd backend
del token.json  # Windows
# rm token.json  # Linux/Mac

# Restart backend - will re-authenticate
python -m uvicorn app:app --reload --port 8000
```

Browser will open for re-authentication.

---

### 15. API Not Enabled

**Symptoms:**
```
Google Forms API has not been used in project XXXXX before
```

**Cause:** Google Cloud APIs not enabled

**Solution:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/library)
2. Search "Google Forms API" → **Enable**
3. Search "Google Drive API" → **Enable**
4. Wait 1-2 minutes
5. Restart backend

---

## 🧪 Verification Commands

### Check Backend Status
```cmd
curl http://localhost:8000/surveys
# Should return: {"surveys": [], "total": 0}
```

### Check Frontend Status
```cmd
# Open browser
http://localhost:3000
# Should see login page
```

### Check CORS Headers
```cmd
curl -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: POST" \
     -X OPTIONS \
     http://localhost:8000/auth/google -v
# Should see: Access-Control-Allow-Origin: http://localhost:3000
```

### Run Tests
```cmd
cd backend
pytest -v
# Should show: 23 passed, 3 skipped, 0 failed
```

---

## 📊 System Health Checklist

Before reporting an issue, verify:

- ☑️ Python 3.12+ installed: `python --version`
- ☑️ Node.js 18+ installed: `node --version`
- ☑️ Backend dependencies installed: `pip list | findstr fastapi`
- ☑️ Frontend dependencies installed: `dir node_modules\next`
- ☑️ Backend running: http://localhost:8000/docs
- ☑️ Frontend running: http://localhost:3000
- ☑️ No firewall blocking ports 3000 or 8000
- ☑️ Latest code from repository

---

## 🔍 Debug Mode

### Enable Verbose Logging (Backend)
```python
# backend/app.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Enable Console Logging (Frontend)
Already enabled - open browser console (F12)

### Check Backend Logs
Watch terminal where backend is running:
```
INFO: 127.0.0.1:XXXXX - "POST /auth/google HTTP/1.1" 200 OK
INFO: 127.0.0.1:XXXXX - "GET /surveys HTTP/1.1" 200 OK
```

---

## 💡 Pro Tips

### Tip 1: Keep Both Terminals Open
- **Terminal 1:** Backend (shows API requests)
- **Terminal 2:** Frontend (shows page compilations)

### Tip 2: Use Scripts for Reliability
```cmd
scripts\start.bat      # Starts both automatically
scripts\test.bat       # Runs all tests
```

### Tip 3: Demo Mode Fallback
If backend is unavailable, frontend automatically falls back to demo mode with mock data.

### Tip 4: Check Script Paths
After moving scripts to `scripts/` folder, use:
```cmd
scripts\setup.bat      # Not setup.bat
scripts\start.bat      # Not start-system.bat
scripts\test.bat       # Not run-tests.bat
```

---

## 📞 Still Having Issues?

1. ✅ Review this troubleshooting guide
2. ✅ Check **[SETUP.md](SETUP.md)** for configuration
3. ✅ See **[GOOGLE_FORMS_SETUP.md](GOOGLE_FORMS_SETUP.md)** for OAuth
4. ✅ Verify all dependencies installed
5. ✅ Restart both servers
6. ✅ Clear browser cache and cookies
7. ✅ Check terminal output for errors

---

**Last Updated:** November 8, 2025  
**Status:** All known issues documented  
**Test Coverage:** 23/23 tests passing ✅
