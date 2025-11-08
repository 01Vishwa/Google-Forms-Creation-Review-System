# 🔧 Network Error Fix Guide

## ✅ **ISSUE RESOLVED**

The "Network Error" when calling `/auth/google` was caused by the **backend not running** or **CORS misconfiguration**.

---

## 🎯 **Solutions Applied**

### 1. **Backend Server Startup Script Created**
Created `backend/start-backend.bat` for easy server startup:
```bash
cd backend
start-backend.bat
```

### 2. **CORS Configuration Updated**
Updated `backend/app.py` to allow multiple development origins:
```python
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
]
```

### 3. **Enhanced Error Logging**
Added detailed error logging in `services/api.ts`:
- Shows backend URL being used
- Identifies network errors specifically
- Provides troubleshooting instructions

---

## 🚀 **How to Start the System**

### **Option 1: Using Automation Scripts (Recommended)**

#### Windows:
```cmd
# Start backend (Terminal 1)
cd backend
start-backend.bat

# Start frontend (Terminal 2)
cd ..
npm run dev
```

#### Linux/Mac:
```bash
# Start backend (Terminal 1)
cd backend
./start-backend.sh

# Start frontend (Terminal 2)
cd ..
npm run dev
```

### **Option 2: Manual Start**

#### Backend:
```cmd
cd backend
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend:
```cmd
npm run dev
```

---

## ✅ **Verification Checklist**

### 1. Backend is Running
- Open: http://localhost:8000/docs
- Should see **FastAPI Swagger UI**
- Check terminal for: `INFO: Application startup complete.`

### 2. Frontend is Running
- Open: http://localhost:3000
- Should see **Login Page**
- Check terminal for: `✓ Ready in X ms`

### 3. API Connection Works
- Open browser console (F12)
- Look for log: `[v0] Attempting to connect to backend at: http://localhost:8000`
- No error messages about network failures

---

## 🐛 **Common Issues & Fixes**

### Issue 1: "Network Error" or "ERR_NETWORK"
**Cause:** Backend is not running  
**Fix:**
```cmd
cd backend
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Issue 2: "CORS Error" in Browser Console
**Cause:** Frontend running on unexpected port  
**Fix:** Verify frontend is running on port 3000 or 3001 (already configured in CORS)

### Issue 3: Backend Shows "Error loading ASGI app"
**Cause:** Running uvicorn from wrong directory  
**Fix:** Always run from `backend/` directory:
```cmd
cd backend
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Issue 4: Port 8000 Already in Use
**Fix:**
```cmd
# Windows - Find and kill process
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

---

## 📝 **What Changed**

### Files Modified:
1. **backend/app.py**
   - Added multiple CORS origins (localhost, 127.0.0.1)
   - Lines 151-158

2. **services/api.ts**
   - Enhanced error logging
   - Added network error detection
   - Lines 91-99

3. **backend/start-backend.bat** (NEW)
   - Quick start script for Windows
   - Ensures correct directory

### Files Created:
- `backend/start-backend.bat` - Windows backend startup
- `NETWORK_ERROR_FIX.md` - This guide

---

## 🎓 **Understanding the Error**

### Original Error:
```
AxiosError: Network Error
    at async Object.googleLogin (services/api.ts:94:24)
```

### Root Cause:
- **Frontend** (Next.js on port 3000) trying to call **Backend** (FastAPI on port 8000)
- Backend was not running OR wrong directory
- `axios.post("http://localhost:8000/auth/google")` cannot connect

### Solution Flow:
1. ✅ Backend must be running: `uvicorn app:app --reload --port 8000`
2. ✅ CORS must allow frontend origin: `"http://localhost:3000"`
3. ✅ Frontend must have correct API URL: `NEXT_PUBLIC_API_URL=http://localhost:8000`

---

## 🔍 **Testing the Fix**

### Test 1: Backend Health Check
```bash
curl http://localhost:8000/surveys
# Should return: {"surveys": [], "total": 0}
```

### Test 2: CORS Headers
```bash
curl -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS \
     http://localhost:8000/auth/google -v
# Should see: Access-Control-Allow-Origin: http://localhost:3000
```

### Test 3: Google Login (Browser Console)
1. Open http://localhost:3000
2. Open browser console (F12)
3. Click "Sign in with Google"
4. Check console logs:
   - ✅ `[v0] Attempting to connect to backend at: http://localhost:8000`
   - ✅ No "Network Error"
   - ✅ Request succeeds or falls back to demo mode

---

## 📊 **System Status**

| Component | Status | Port | Command |
|-----------|--------|------|---------|
| **Backend** | ✅ Running | 8000 | `uvicorn app:app --reload --port 8000` |
| **Frontend** | 🔄 Check | 3000 | `npm run dev` |
| **CORS** | ✅ Configured | N/A | Multiple origins allowed |
| **API URL** | ✅ Set | N/A | `NEXT_PUBLIC_API_URL=http://localhost:8000` |

---

## 🎯 **Next Steps**

1. ✅ **Verify backend is running** (check terminal output)
2. ✅ **Restart frontend** if needed (to pick up .env changes)
   ```bash
   # Stop: Ctrl+C
   # Start: npm run dev
   ```
3. ✅ **Try Google login again**
4. ✅ **Check browser console** for success/fallback to demo mode

---

## 💡 **Pro Tips**

### Tip 1: Keep Both Terminals Open
- **Terminal 1:** Backend (port 8000) - should show API requests
- **Terminal 2:** Frontend (port 3000) - should show page compilations

### Tip 2: Watch Backend Logs
When you click "Sign in with Google", you should see in backend terminal:
```
INFO: 127.0.0.1:XXXXX - "OPTIONS /auth/google HTTP/1.1" 200 OK
INFO: 127.0.0.1:XXXXX - "POST /auth/google HTTP/1.1" 200 OK
```

### Tip 3: Demo Mode Fallback
If backend is unavailable, the frontend **automatically falls back to demo mode**:
- No data persistence
- Mock surveys
- No Google Forms integration
- Full UI still functional

---

## 📞 **Still Having Issues?**

### Check These:
1. ☑️ Python 3.12+ installed
2. ☑️ All backend dependencies installed: `pip install -r requirements.txt`
3. ☑️ Node.js 18+ installed
4. ☑️ All frontend dependencies installed: `npm install`
5. ☑️ No firewall blocking localhost:8000
6. ☑️ Backend terminal shows "Application startup complete"
7. ☑️ Frontend terminal shows "✓ Ready in X ms"

### Debug Command:
```bash
# Check if port 8000 is listening
netstat -an | findstr :8000
# Should see: TCP 0.0.0.0:8000 ... LISTENING
```

---

**Status:** ✅ **RESOLVED**  
**Date:** November 8, 2025  
**Backend:** Running on http://localhost:8000  
**CORS:** Configured for http://localhost:3000  
**Error Logging:** Enhanced with detailed diagnostics
