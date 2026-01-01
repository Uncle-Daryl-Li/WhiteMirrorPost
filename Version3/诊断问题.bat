@echo off
chcp 65001 >nul
color 0E

echo ========================================
echo   MirrorPost AI - 问题诊断工具
echo ========================================
echo.

echo [检查1] 当前目录
echo 当前路径: %cd%
echo.

echo [检查2] Python环境
python --version
if errorlevel 1 (
    echo [错误] Python未安装或未添加到PATH
    goto :end
)
echo [OK] Python已安装
echo.

echo [检查3] .env文件
if exist ".env" (
    echo [OK] .env文件存在
    type .env
) else (
    echo [错误] .env文件不存在！
    echo.
    echo 请创建.env文件并添加：
    echo GOOGLE_API_KEY=你的实际Key
    goto :end
)
echo.

echo [检查4] 核心文件
if exist "backend.py" (echo [OK] backend.py 存在) else (echo [错误] backend.py 缺失)
if exist "server.py" (echo [OK] server.py 存在) else (echo [错误] server.py 缺失)
if exist "SaaS.html" (echo [OK] SaaS.html 存在) else (echo [错误] SaaS.html 缺失)
if exist "Landing page.html" (echo [OK] Landing page.html 存在) else (echo [错误] Landing page.html 缺失)
if exist "start_backend.bat" (echo [OK] start_backend.bat 存在) else (echo [错误] start_backend.bat 缺失)
if exist "start_frontend.bat" (echo [OK] start_frontend.bat 存在) else (echo [错误] start_frontend.bat 缺失)
echo.

echo [检查5] Python依赖
echo 检查关键依赖...
python -c "import fastapi; print('[OK] fastapi 已安装')" 2>nul || echo [错误] fastapi 未安装
python -c "import uvicorn; print('[OK] uvicorn 已安装')" 2>nul || echo [错误] uvicorn 未安装
python -c "from google import genai; print('[OK] google-genai 已安装')" 2>nul || echo [错误] google-genai 未安装
python -c "from PIL import Image; print('[OK] Pillow 已安装')" 2>nul || echo [错误] Pillow 未安装
echo.

echo [检查6] 端口占用
echo 检查8000端口...
netstat -ano | findstr ":8000" >nul 2>&1
if errorlevel 1 (
    echo [OK] 端口8000空闲
) else (
    echo [警告] 端口8000已被占用
    netstat -ano | findstr ":8000"
)
echo.
echo 检查8080端口...
netstat -ano | findstr ":8080" >nul 2>&1
if errorlevel 1 (
    echo [OK] 端口8080空闲
) else (
    echo [警告] 端口8080已被占用
    netstat -ano | findstr ":8080"
)
echo.

echo ========================================
echo   诊断完成！
echo ========================================
echo.
echo 如果所有检查都通过，请尝试：
echo   1. 手动启动后端：双击 start_backend.bat
echo   2. 手动启动前端：双击 start_frontend.bat
echo   3. 访问 http://localhost:8080/Landing page.html
echo.

:end
echo.
pause
