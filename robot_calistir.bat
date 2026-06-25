@echo off
chcp 65001 >nul
title TrimbleOtomatikCizim — Robot Modu
cd /d "%~dp0"

echo ============================================================
echo   TrimbleOtomatikCizim  —  Otomatik Robot Modu
echo ============================================================
echo.
echo giris\ klasoründeki tüm LAZ/LAS dosyaları işlenecek.
echo Çıktılar: cikti\  |  Tamamlananlar: islenmis\
echo.
echo Başlamak için herhangi bir tuşa basın...
pause >nul

python main.py --robot --config robot_config.json

echo.
echo İşlem tamamlandı.
pause
