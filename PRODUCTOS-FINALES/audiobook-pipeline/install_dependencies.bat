@echo off
echo ========================================
echo Instalando dependencias del proyecto
echo ========================================
echo.
cd /d "%~dp0"

echo Instalando paquetes de Python...
py -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Error al instalar dependencias
    pause
    exit /b 1
)

echo.
echo Instalando recursos de NLTK...
py -m nltk.downloader punkt stopwords

if errorlevel 1 (
    echo.
    echo Advertencia: No se pudieron instalar todos los recursos de NLTK
    echo El proyecto puede funcionar pero con funcionalidad limitada
)

echo.
echo ========================================
echo Instalacion completada
echo ========================================
echo.
echo Ahora puedes ejecutar:
echo   py audiobook_pipeline.py
echo.
pause

