@echo off
chcp 65001 >nul
echo.
echo ========================================
echo    Telegram 文件上传机器人
echo           超稳定版
echo ========================================
echo.
echo 正在停止所有Python进程...
taskkill /f /im python.exe >nul 2>&1
echo.
echo 等待进程完全停止...
timeout /t 5 /nobreak >nul
echo.
echo 启动超稳定版机器人...
echo 此版本专门优化了网络稳定性
echo.
python start_ultra_stable.py
echo.
echo 机器人已停止
pause
