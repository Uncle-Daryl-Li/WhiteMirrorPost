@echo off
color 0A

echo.
echo ========================================
echo   MirrorPost AI - Quick Start
echo ========================================
echo.

echo [1/3] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    pause
    exit /b 1
)
echo [OK] Python is installed
echo.

echo [2/3] Checking .env file...
if not exist ".env" (
    echo [ERROR] .env file not found!
    echo Please create .env file with: GOOGLE_API_KEY=your_key
    pause
    exit /b 1
)
echo [OK] .env file exists
echo.

echo [3/3] Starting servers...
echo.

echo Starting Backend Server...
start "MirrorPost Backend" cmd /k "python server.py"
timeout /t 3 /nobreak >nul
echo [OK] Backend starting...
echo.

echo Starting Frontend Server...
start "MirrorPost Frontend" cmd /k "python -m http.server 8080"
timeout /t 3 /nobreak >nul
echo [OK] Frontend starting...
echo.

echo ========================================
echo   Servers Started!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:8080/Landing%%20page.html
echo.
echo Opening browser...
timeout /t 2 /nobreak >nul
start http://localhost:8080/Landing%%20page.html
echo.
echo [Done] MirrorPost AI is running!
echo.
echo To stop: Close the Backend and Frontend windows
echo.
pause
