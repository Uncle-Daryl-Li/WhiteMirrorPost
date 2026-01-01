@echo off
chcp 65001 >nul
echo ========================================
echo   MirrorPost AI - Backend Server
echo ========================================
echo.
echo Starting FastAPI server...
echo API: http://localhost:8000
echo Docs: http://localhost:8000/docs
echo.
python server.py
