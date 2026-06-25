@echo off
chcp 65001 >nul
title TrimbleOtomatikCizim — Kurulum ve Başlatma

echo ============================================================
echo   TrimbleOtomatikCizim  V29  —  Kurulum
echo ============================================================
echo.

REM Python kontrolü
python --version >nul 2>&1
if errorlevel 1 (
    echo [HATA] Python bulunamadı!
    echo.
    echo Lütfen Python 3.11 veya üstünü yükleyin:
    echo   https://www.python.org/downloads/
    echo.
    echo Kurulumda "Add Python to PATH" seçeneğini işaretleyin!
    echo.
    pause
    exit /b 1
)

echo [OK] Python bulundu:
python --version
echo.

REM pip güncelle
echo [1/2] pip güncelleniyor...
python -m pip install --upgrade pip --quiet
echo.

REM Bağımlılıkları kur
echo [2/2] Bağımlılıklar kuruluyor (ilk kurulum birkaç dakika sürebilir)...
echo       laspy, numpy, opencv, ezdxf, PyQt6 ...
echo.
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo [HATA] Bağımlılık kurulumu başarısız!
    echo Lütfen internet bağlantınızı kontrol edin.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   Kurulum tamamlandı! Uygulama başlatılıyor...
echo ============================================================
echo.

python main.py
