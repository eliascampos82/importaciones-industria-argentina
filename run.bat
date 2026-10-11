@echo off
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    set PYTHON=.venv\Scripts\python.exe
) else (
    set PYTHON=python
)

echo Usando: %PYTHON%
echo.
echo Instalando dependencias (la primera vez tarda un par de minutos)...
"%PYTHON%" -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR instalando dependencias. Revisa el mensaje de arriba.
    pause
    exit /b 1
)

echo.
echo Abriendo el dashboard...
"%PYTHON%" -m streamlit run dashboard/Inicio.py

echo.
echo El dashboard se cerro.
pause
