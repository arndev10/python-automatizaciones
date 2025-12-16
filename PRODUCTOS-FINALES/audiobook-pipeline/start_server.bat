@echo off
echo Iniciando servidor de audiolibros...
cd /d "%~dp0"
echo.
echo Intentando con 'py' (launcher de Python)...
py run_local.py
if errorlevel 1 (
    echo.
    echo 'py' no funciono, intentando con ruta completa de Python...
    "C:\Users\Ar\AppData\Local\Programs\Python\Python313\python.exe" run_local.py
    if errorlevel 1 (
        echo.
        echo Error: No se pudo ejecutar Python.
        echo Verifica que Python este instalado correctamente.
        pause
        exit /b 1
    )
)
pause

