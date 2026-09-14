@echo off
title NEXTGEN DEFENDX - UNIFIED ATTACK PREDICTION & REMEDIATION
color 0A

echo ============================================================
echo [!] INITIALIZING NEXTGEN DEFENDX UNIFIED SOC...
echo ============================================================
echo.

:: 1. Start System 1 (Core Detector)
echo [1/3] Launching Core Detector (.exe)...
:: Using 'run_core.exe' as per your folder screenshot
if exist "run_core.exe" (
    start run_core.exe
) else (
    echo [!] ERROR: run_core.exe not found in this folder!
)

:: 2. Start System 3 (AI Service)
echo [2/3] Launching AI Prediction Engine (System 3)...
:: We navigate into the ai folder, activate the venv, and run the service
start cmd /k "cd ai && venv\Scripts\activate && uvicorn ai_service:app --port 8001"

:: 3. Wait and Launch Dashboard
echo [3/3] Synchronizing systems...
timeout /t 6 /nobreak > nul

echo.
echo [!] Launching Unified Dashboard UI...
if exist "dashboard.html" (
    start dashboard.html
) else (
    echo [!] ERROR: dashboard.html not found!
)

echo.
echo ============================================================
echo [SUCCESS] ALL SYSTEMS ONLINE.
echo.
echo 🛡️ DETECTION (SYSTEM 1): PORT 8000
echo 🧠 AI BRAIN (SYSTEM 3):   PORT 8001
echo 🖥️ DASHBOARD:            ACTIVE
echo ============================================================
echo.
echo Keep this window open during your demo.
pause