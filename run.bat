@echo off
echo ============================================
echo  Iniciando Visualizador de Excel...
echo ============================================

REM Verificar si el entorno virtual existe, si no, crearlo
if not exist .venv (
    echo El entorno virtual no existe. Creando e instalando dependencias...
    python -m venv .venv
    call .venv\Scripts\activate
    pip install -r requirements.txt
) else (
    call .venv\Scripts\activate
)

echo.
echo ============================================
echo  Iniciando la aplicacion...
echo ============================================
echo.
echo Para detener la aplicacion, presiona Ctrl+C
echo Abriendo navegador en http://127.0.0.1:5000
echo.

REM Iniciar la aplicación
start http://127.0.0.1:5000
python app/main.py
