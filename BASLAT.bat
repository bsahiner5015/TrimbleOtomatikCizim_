@echo off
chcp 65001 >nul
title TrimbleOtomatikCizim
cd /d "%~dp0"
python main.py
if errorlevel 1 (
    echo.
    echo Hata olustu. Ilk kez calistiriyorsaniz KUR_VE_CALISTIR.bat kullanin.
    pause
)
