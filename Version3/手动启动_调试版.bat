@echo off
chcp 65001 >nul

echo.
echo ========================================
echo   MirrorPost AI - 手动启动（调试版）
echo ========================================
echo.

REM 检查当前目录
echo 当前目录: %cd%
echo.

REM 检查Python
echo [1/4] 检查Python环境...
python --version
if errorlevel 1 (
    echo.
    echo [错误] 未找到Python！
    echo 请确保已安装Python 3.8+并添加到PATH
    echo.
    pause
    exit /b 1
)
echo [OK] Python已安装
echo.

REM 检查.env
echo [2/4] 检查配置文件...
if not exist ".env" (
    echo.
    echo [错误] 未找到.env文件！
    echo.
    echo 请在当前目录创建.env文件，内容为：
    echo GOOGLE_API_KEY=你的实际API_Key
    echo.
    echo 按任意键打开记事本创建.env文件...
    pause >nul
    notepad .env
    echo.
    echo 保存后请重新运行此脚本
    pause
    exit /b 1
)
echo [OK] .env文件存在
echo.

REM 显示.env内容（隐藏Key）
echo .env文件内容：
type .env | findstr /v "GOOGLE_API_KEY" >nul
if errorlevel 1 (
    echo   GOOGLE_API_KEY=已配置
) else (
    echo   [警告] .env文件可能为空
    type .env
)
echo.

REM 启动后端
echo [3/4] 启动后端服务器...
echo 正在新窗口启动后端（保持窗口打开）...
start "MirrorPost Backend Server" cmd /k "cd /d %cd% && echo 启动后端... && python server.py"
echo.

REM 等待后端启动
echo 等待5秒让后端完全启动...
timeout /t 5 /nobreak
echo.

REM 启动前端
echo [4/4] 启动前端服务器...
echo 正在新窗口启动前端（保持窗口打开）...
start "MirrorPost Frontend Server" cmd /k "cd /d %cd% && echo 启动前端... && python -m http.server 8080"
echo.

REM 等待前端启动
echo 等待3秒让前端完全启动...
timeout /t 3 /nobreak
echo.

echo ========================================
echo   启动完成！
echo ========================================
echo.
echo 如果看到两个新窗口（Backend和Frontend），说明启动成功！
echo.
echo 访问地址:
echo   后端API: http://localhost:8000
echo   前端界面: http://localhost:8080/Landing page.html
echo.
echo 正在打开浏览器...
start http://localhost:8080/Landing%%20page.html
echo.
echo 提示:
echo   • 如果后端窗口显示错误，检查.env中的API Key
echo   • 如果前端窗口显示错误，检查端口8080是否被占用
echo   • 关闭后端/前端窗口即可停止服务器
echo.
echo.
pause
