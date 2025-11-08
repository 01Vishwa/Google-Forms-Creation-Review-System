#!/bin/bash
# ====================================
# Google Forms System - Start All Services
# ====================================

echo ""
echo "========================================"
echo "  Starting Google Forms System"
echo "========================================"
echo ""

# Check if backend dependencies are installed
if [ ! -d "backend/__pycache__" ]; then
    echo "[WARNING] Backend may not be set up. Run ./setup.sh first."
    echo "Continuing anyway..."
    echo ""
fi

# Check if frontend dependencies are installed
if [ ! -d "node_modules" ]; then
    echo "[WARNING] Frontend may not be set up. Run ./setup.sh first."
    echo "Continuing anyway..."
    echo ""
fi

echo "[1/2] Starting Backend Server..."
echo "========================================"

# Start backend in background
cd backend
python3 app.py &
BACKEND_PID=$!
cd ..

echo "Backend started (PID: $BACKEND_PID)"
echo "Waiting for backend to initialize..."
sleep 5

echo ""
echo "[2/2] Starting Frontend Server..."
echo "========================================"

# Start frontend in background
npm run dev &
FRONTEND_PID=$!

echo "Frontend started (PID: $FRONTEND_PID)"
echo "Waiting for frontend to initialize..."
sleep 3

echo ""
echo "========================================"
echo "  System Started Successfully! ✅"
echo "========================================"
echo ""
echo "Access the application:"
echo "  Frontend:  http://localhost:3000"
echo "  Backend:   http://localhost:8000"
echo "  API Docs:  http://localhost:8000/docs"
echo "  OpenAPI:   http://localhost:8000/openapi.json"
echo ""
echo "Process IDs:"
echo "  Backend:  $BACKEND_PID"
echo "  Frontend: $FRONTEND_PID"
echo ""
echo "To stop the system:"
echo "  kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "Press Ctrl+C to stop all services..."

# Wait for user interrupt
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
