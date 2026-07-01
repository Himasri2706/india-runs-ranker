@echo off
title India RUNS AI Ranker - Full Stack
color 0B

echo ==================================================
echo   🚀 India RUNS Hackathon - Full Stack Launchpad
echo ==================================================
echo.

echo [1/3] Preparing AI Models (Offline Cache)...
python download_model.py
echo.

echo [2/3] Starting FastAPI AI Engine Backend...
start cmd /k "python api.py"

echo [3/3] Starting React Web Interface Frontend...
cd frontend
start cmd /k "npm run dev"

echo.
echo ==================================================
echo   ✅ Backend API and Frontend App started!
echo   Wait a few seconds, then open your browser to:
echo   http://localhost:5173
echo ==================================================
pause
