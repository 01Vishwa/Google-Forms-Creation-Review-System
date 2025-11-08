@echo off
cd /d "%~dp0"
echo Starting FastAPI Backend Server...
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
