@echo off
chcp 65001 >nul

echo 测试后端启动...
echo.
echo 当前目录: %cd%
echo.

echo 检查Python...
python --version
echo.

echo 尝试启动后端服务器...
echo 如果成功，你会看到 "Uvicorn running on..." 的消息
echo 按 Ctrl+C 可停止
echo.
echo ========================================
echo.

python server.py

echo.
echo ========================================
echo 后端已停止
pause
