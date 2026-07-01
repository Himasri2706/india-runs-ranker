@echo off
title India RUNS AI Ranker - Setup & Launch
color 0B

echo ==================================================
echo   🚀 India RUNS Hackathon - AI Ranker Launchpad
echo ==================================================
echo.

echo [1/3] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH. Please install Python 3.9+ and try again.
    pause
    exit /b
)
echo Python is installed.
echo.

echo [2/3] Installing required dependencies...
pip install -r requirements.txt
echo.

echo [3/3] Preparing AI Models (Offline Cache)...
python download_model.py
echo.

echo ==================================================
echo   ✅ All systems go! Starting the Dashboard...
echo ==================================================
echo.
streamlit run app.py

pause
