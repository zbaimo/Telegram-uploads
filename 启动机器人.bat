@echo off
chcp 65001 >nul
echo.
echo ========================================
echo    Telegram 文件上传机器人
echo ========================================
echo.
echo 正在停止所有Python进程...
taskkill /f /im python.exe >nul 2>&1
echo.
echo 等待进程完全停止...
timeout /t 3 /nobreak >nul
echo.
echo 启动超简单稳定版机器人...
echo.
python start_simple_robust.py
echo.
echo 机器人已停止
pause
