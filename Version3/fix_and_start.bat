@echo off
color 0A

echo.
echo ========================================
echo   MirrorPost AI - Auto Fix and Start
echo ========================================
echo.

echo [Step 1] Checking if backend is already running...
netstat -ano | findstr ":8000" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Port 8000 is free. Good!
    goto :start_backend
) else (
    echo [WARNING] Port 8000 is occupied!
    echo.
    echo Killing process on port 8000...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000"') do (
        taskkill /PID %%a /F >nul 2>&1
    )
    timeout /t 2 /nobreak >nul
    echo [OK] Port cleared.
)
echo.

:start_backend
echo [Step 2] Starting Backend Server...
start "MirrorPost Backend" cmd /k "cd /d %~dp0 && color 0C && echo Backend Server Starting... && echo. && python server.py"
echo [INFO] Backend window opened.
timeout /t 5 /nobreak >nul
echo.

echo [Step 3] Testing backend connection...
python -c "import requests; r = requests.get('http://localhost:8000/', timeout=3); print('[OK] Backend is responding!')" 2>nul
if errorlevel 1 (
    echo [WARNING] Backend might still be starting...
    echo Please wait 5 more seconds.
    timeout /t 5 /nobreak >nul
)
echo.

echo [Step 4] Starting Frontend Server...
start "MirrorPost Frontend" cmd /k "cd /d %~dp0 && color 0B && echo Frontend Server Starting... && echo. && python -m http.server 8080"
echo [INFO] Frontend window opened.
timeout /t 3 /nobreak >nul
echo.

echo ========================================
echo   All Done!
echo ========================================
echo.
echo You should now see TWO windows:
echo   1. MirrorPost Backend (red)
echo   2. MirrorPost Frontend (cyan)
echo.
echo Opening browser...
timeout /t 2 /nobreak >nul
start http://localhost:8080/Landing%%20page.html
echo.
echo [SUCCESS] Servers are running!
echo.
echo If you still get "Failed to fetch":
echo   1. Check the Backend window for errors
echo   2. Wait 10 seconds and try again
echo   3. Make sure both windows stay OPEN
echo.
pause
