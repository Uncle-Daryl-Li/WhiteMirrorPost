@echo off
echo Checking backend server status...
echo.

echo [Test 1] Checking if port 8000 is listening...
netstat -ano | findstr ":8000"
if errorlevel 1 (
    echo [ERROR] Port 8000 is NOT listening!
    echo Backend server is NOT running.
    echo.
    echo Please start backend first:
    echo   1. Open new CMD window
    echo   2. cd D:\WhiteMirror\Post\Version3
    echo   3. python server.py
) else (
    echo [OK] Port 8000 is active
)
echo.

echo [Test 2] Testing backend API...
curl -s http://localhost:8000/ 2>nul
if errorlevel 1 (
    echo [ERROR] Cannot connect to backend API
) else (
    echo [OK] Backend API is responding
)
echo.

echo [Test 3] Testing generate endpoint...
curl -s -X POST http://localhost:8000/api/generate -H "Content-Type: application/json" -d "{\"prompt\":\"test\",\"count\":1}" 2>nul
echo.
echo.

pause
