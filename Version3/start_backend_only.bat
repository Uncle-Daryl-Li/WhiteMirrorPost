@echo off
color 0C

echo ========================================
echo   Starting Backend Server ONLY
echo ========================================
echo.

echo Current directory: %cd%
echo.

echo Checking Python...
python --version
echo.

echo Starting backend server...
echo.
echo If you see "Uvicorn running on http://0.0.0.0:8000"
echo then the backend is working!
echo.
echo Keep this window OPEN!
echo Press Ctrl+C to stop the server.
echo.
echo ========================================
echo.

python server.py

echo.
echo Backend server stopped.
pause
