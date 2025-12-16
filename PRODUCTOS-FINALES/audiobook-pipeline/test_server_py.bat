@echo off
echo Iniciando servidor de prueba...
cd /d "%~dp0"
py test_server.py
pause

