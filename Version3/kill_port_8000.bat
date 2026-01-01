@echo off
echo Killing process on port 8000...
echo.
echo Finding process...
netstat -ano | findstr ":8000"
echo.
echo Killing process ID 18936...
taskkill /PID 18936 /F
echo.
echo Done! Port 8000 should now be free.
echo.
echo You can now run: start.bat
echo.
pause
