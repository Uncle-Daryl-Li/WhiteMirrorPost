@echo off
chcp 65001 >nul
echo ========================================
echo   MirrorPost AI - Frontend Server
echo ========================================
echo.
echo Starting HTTP server...
echo URL: http://localhost:8080/Landing page.html
echo.
echo Press Ctrl+C to stop
echo.
python -m http.server 8080
