@echo off
color 0A

echo.
echo ========================================
echo   MirrorPost AI - Start (Port 8001)
echo ========================================
echo.
echo NOTE: Using port 8001 for backend
echo       (Port 8000 is occupied)
echo.

echo [1/2] Starting Backend Server (Port 8001)...
start "MirrorPost Backend - Port 8001" cmd /k "python server_port_8001.py"
timeout /t 3 /nobreak >nul
echo [OK] Backend starting on port 8001...
echo.

echo [2/2] Starting Frontend Server (Port 8080)...
start "MirrorPost Frontend" cmd /k "python -m http.server 8080"
timeout /t 3 /nobreak >nul
echo [OK] Frontend starting on port 8080...
echo.

echo ========================================
echo   Servers Started!
echo ========================================
echo.
echo Backend:  http://localhost:8001
echo Frontend: http://localhost:8080
echo.
echo IMPORTANT: You need to update SaaS.html
echo            to use port 8001 instead of 8000
echo.
echo Opening browser...
timeout /t 2 /nobreak >nul
start http://localhost:8080/Landing%%20page.html
echo.
echo [Done] Servers are running!
echo.
pause
