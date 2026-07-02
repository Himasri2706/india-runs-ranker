@echo off
title India RUNS AI Ranker - Enterprise Full Stack
color 0B

echo ==================================================
echo   🚀 India RUNS Hackathon - Enterprise AI Engine
echo ==================================================
echo.

echo [1/3] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    pause
    exit /b
)

echo [2/3] Installing Backend Dependencies...
pip install -r requirements.txt

echo [3/3] Preparing AI Models (Offline Cache)...
python download_model.py

echo.
echo ==================================================
echo   ✅ Starting FastAPI Backend on Port 8000
echo ==================================================
start cmd /k "title FastAPI Backend && uvicorn api:app --host 127.0.0.1 --port 8000"

echo.
echo ==================================================
echo   ✅ Starting React Frontend on Port 5173
echo ==================================================
cd frontend
start cmd /k "title React Frontend && npm install && npm run dev -- --force"

echo.
echo ==================================================
echo   All systems go! Close this window to exit.
echo ==================================================
pause
