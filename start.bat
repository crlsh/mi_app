@echo off
echo ============================================
echo  Activando entorno virtual, espere...
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
echo  Entorno virtual activado correctamente!
echo ============================================
echo.
echo Para ejecutar la aplicacion, escribe:
echo python app/main.py
echo.
echo Para acceder a la aplicacion: http://127.0.0.1:5000
echo.
cmd /k
