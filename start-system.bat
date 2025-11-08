@echo off
REM ====================================
REM Google Forms System - Start All Services
REM ====================================

echo.
echo ========================================
echo   Starting Google Forms System
echo ========================================
echo.

REM Check if backend dependencies are installed
if not exist "backend\__pycache__" (
    echo [WARNING] Backend may not be set up. Run setup.bat first.
    echo Continuing anyway...
    echo.
)

REM Check if frontend dependencies are installed
if not exist "node_modules" (
    echo [WARNING] Frontend may not be set up. Run setup.bat first.
    echo Continuing anyway...
    echo.
)

echo [1/2] Starting Backend Server...
echo ========================================
start "Backend - Google Forms API" cmd /k "cd /d %~dp0backend && python app.py"

REM Wait for backend to start
echo Waiting for backend to initialize...
timeout /t 5 /nobreak >nul

echo.
echo [2/2] Starting Frontend Server...
echo ========================================
start "Frontend - Next.js" cmd /k "cd /d %~dp0 && npm run dev"

REM Wait for frontend to start
echo Waiting for frontend to initialize...
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo   System Started Successfully! ✅
echo ========================================
echo.
echo Access the application:
echo   Frontend:  http://localhost:3000
echo   Backend:   http://localhost:8000
echo   API Docs:  http://localhost:8000/docs
echo   OpenAPI:   http://localhost:8000/openapi.json
echo.
echo To stop the system:
echo   Close both terminal windows
echo.
echo Press any key to open the application in browser...
pause >nul

REM Open browser
start http://localhost:3000

echo.
echo Application opened in browser!
echo Keep the terminal windows open to keep the system running.
echo.
