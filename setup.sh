#!/bin/bash
# ====================================
# Google Forms System - Complete Setup
# ====================================

echo ""
echo "========================================"
echo "  Google Forms Creation Review System"
echo "  Complete Setup Script"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "[ERROR] Node.js is not installed"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

echo "[1/3] Setting up Backend..."
echo "========================================"
cd backend

echo "Installing Python dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install Python dependencies"
    exit 1
fi

echo ""
echo "Backend setup complete!"
echo ""

cd ..

echo "[2/3] Setting up Frontend..."
echo "========================================"

echo "Installing Node.js dependencies..."
npm install
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install Node.js dependencies"
    exit 1
fi

echo ""
echo "Frontend setup complete!"
echo ""

echo "[3/3] Verifying Configuration..."
echo "========================================"

# Check if credentials files exist
if [ ! -f "backend/.env" ]; then
    echo "[WARNING] backend/.env not found"
    echo "Please create .env file with Google OAuth credentials"
fi

if [ ! -f "backend/credentials-oauth.json" ]; then
    echo "[WARNING] backend/credentials-oauth.json not found"
    echo "Please download OAuth 2.0 credentials from Google Cloud Console"
fi

echo ""
echo "========================================"
echo "  Setup Complete! ✅"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. Configure Google OAuth credentials (.env and credentials-oauth.json)"
echo "  2. Run: ./start-system.sh"
echo ""
echo "For manual start:"
echo "  Backend:  cd backend && python3 app.py"
echo "  Frontend: npm run dev"
echo ""
