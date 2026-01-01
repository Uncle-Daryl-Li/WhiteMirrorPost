@echo off
color 0E

echo ========================================
echo   MirrorPost AI - Diagnostic Tool
echo ========================================
echo.

echo [Check 1] Current Directory
echo Path: %cd%
echo.

echo [Check 2] Python Environment
python --version
if errorlevel 1 (
    echo [ERROR] Python not found!
    goto :end
)
echo [OK] Python is installed
echo.

echo [Check 3] .env File
if exist ".env" (
    echo [OK] .env file exists
    echo Content:
    type .env
) else (
    echo [ERROR] .env file NOT found!
    echo.
    echo Please create .env file with:
    echo GOOGLE_API_KEY=your_actual_key
    goto :end
)
echo.

echo [Check 4] Core Files
if exist "backend.py" (echo [OK] backend.py) else (echo [ERROR] backend.py missing)
if exist "server.py" (echo [OK] server.py) else (echo [ERROR] server.py missing)
if exist "SaaS.html" (echo [OK] SaaS.html) else (echo [ERROR] SaaS.html missing)
if exist "Landing page.html" (echo [OK] Landing page.html) else (echo [ERROR] Landing page.html missing)
echo.

echo [Check 5] Python Dependencies
python -c "import fastapi; print('[OK] fastapi installed')" 2>nul || echo [ERROR] fastapi NOT installed
python -c "import uvicorn; print('[OK] uvicorn installed')" 2>nul || echo [ERROR] uvicorn NOT installed
python -c "from google import genai; print('[OK] google-genai installed')" 2>nul || echo [ERROR] google-genai NOT installed
python -c "from PIL import Image; print('[OK] Pillow installed')" 2>nul || echo [ERROR] Pillow NOT installed
echo.

echo [Check 6] Port Status
netstat -ano | findstr ":8000" >nul 2>&1
if errorlevel 1 (
    echo [OK] Port 8000 is free
) else (
    echo [WARNING] Port 8000 is occupied:
    netstat -ano | findstr ":8000"
)
echo.
netstat -ano | findstr ":8080" >nul 2>&1
if errorlevel 1 (
    echo [OK] Port 8080 is free
) else (
    echo [WARNING] Port 8080 is occupied:
    netstat -ano | findstr ":8080"
)
echo.

echo ========================================
echo   Diagnostic Complete!
echo ========================================
echo.

:end
echo.
echo Press any key to continue...
pause >nul
