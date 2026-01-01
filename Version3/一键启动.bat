@echo off
chcp 65001 >nul
color 0A

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                                                               ║
echo ║          MirrorPost AI - 一键启动程序                         ║
echo ║                                                               ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo [1/3] 检查环境配置...
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python已安装

REM 检查.env文件
if not exist ".env" (
    echo [警告] 未找到.env文件
    echo.
    echo 请创建.env文件并添加以下内容:
    echo GOOGLE_API_KEY=你的实际API_Key
    echo.
    echo 获取API Key: https://aistudio.google.com/app/apikey
    echo.
    pause
    exit /b 1
)
echo [OK] .env配置文件存在

echo.
echo [2/3] 启动后端服务器...
echo.

REM 启动后端（新窗口）
start "MirrorPost Backend" cmd /k "title MirrorPost AI - Backend && start_backend.bat"

REM 等待后端启动
timeout /t 3 /nobreak >nul

echo [OK] 后端服务器启动中...
echo.
echo [3/3] 启动前端服务器...
echo.

REM 等待2秒确保后端完全启动
timeout /t 2 /nobreak >nul

REM 启动前端（新窗口）
start "MirrorPost Frontend" cmd /k "title MirrorPost AI - Frontend && start_frontend.bat"

REM 等待前端启动
timeout /t 2 /nobreak >nul

echo [OK] 前端服务器启动中...
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo   ✓ 后端服务器: http://localhost:8000
echo   ✓ 前端服务器: http://localhost:8080
echo.
echo   正在自动打开浏览器...
echo.
echo ═══════════════════════════════════════════════════════════════
echo.

REM 等待3秒确保前端完全启动
timeout /t 3 /nobreak >nul

REM 自动打开浏览器
start http://localhost:8080/Landing%%20page.html

echo.
echo [完成] MirrorPost AI 已成功启动！
echo.
echo 提示:
echo  • 关闭此窗口不会停止服务器
echo  • 要停止服务器，请关闭后端和前端窗口
echo  • 或按 Ctrl+C 停止对应的服务
echo.
echo.
pause
