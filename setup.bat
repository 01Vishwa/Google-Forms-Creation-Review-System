@echo off
REM ====================================
REM Google Forms System - Complete Setup
REM ====================================

echo.
echo ========================================
echo   Google Forms Creation Review System
echo   Complete Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo [1/3] Setting up Backend...
echo ========================================
cd backend

echo Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install Python dependencies
    pause
    exit /b 1
)

echo.
echo Backend setup complete!
echo.

cd ..

echo [2/3] Setting up Frontend...
echo ========================================

echo Installing Node.js dependencies...
call npm install
if errorlevel 1 (
    echo [ERROR] Failed to install Node.js dependencies
    pause
    exit /b 1
)

echo.
echo Frontend setup complete!
echo.

echo [3/3] Verifying Configuration...
echo ========================================

REM Check if credentials files exist
if not exist "backend\.env" (
    echo [WARNING] backend\.env not found
    echo Please create .env file with Google OAuth credentials
)

if not exist "backend\credentials-oauth.json" (
    echo [WARNING] backend\credentials-oauth.json not found
    echo Please download OAuth 2.0 credentials from Google Cloud Console
)

echo.
echo ========================================
echo   Setup Complete! ✅
echo ========================================
echo.
echo Next steps:
echo   1. Configure Google OAuth credentials (.env and credentials-oauth.json)
echo   2. Run: start-system.bat
echo.
echo For manual start:
echo   Backend:  cd backend ^&^& python app.py
echo   Frontend: npm run dev
echo.
pause
