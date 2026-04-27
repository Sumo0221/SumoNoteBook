@echo off
REM Drawer Cleanup Scheduled Task - Windows
REM 每天 02:00 自動執行清理
REM 
REM 使用方式:
REM   cleanup_drawer.bat          - 預覽模式
REM   cleanup_drawer.bat --force   - 執行實際清理

set SCRIPT_DIR=%~dp0
python "%SCRIPT_DIR%cleanup_drawer.py" %*

if errorlevel 1 (
    echo 清理腳本執行失敗
    pause
    exit /b 1
)

echo 清理完成
exit /b 0