@echo off
echo ========================================
echo Generador de Audiolibros
echo ========================================
echo.
cd /d "%~dp0"

REM Verificar si hay PDF en carpeta input
if exist "input\*.pdf" (
    echo PDF encontrado en carpeta input/
    echo.
    py audiobook_pipeline.py
) else (
    echo No se encontro PDF en la carpeta input/
    echo.
    echo Coloca un archivo PDF en la carpeta input/ y vuelve a ejecutar este script
    echo O especifica la ruta del PDF como argumento:
    echo    run_audiobook.bat "ruta\al\archivo.pdf"
    echo.
    if not "%~1"=="" (
        echo Procesando: %~1
        py audiobook_pipeline.py "%~1"
    )
)
echo.
pause



