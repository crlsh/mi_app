@echo off
:: Script para activar entorno y ejecutar aplicación en Windows
ECHO Iniciando Visualizador de Excel...

:: Directorio de la aplicación
SET APP_DIR=app

:: Verificar si el entorno virtual existe
IF NOT EXIST .venv (
    ECHO Configurando entorno por primera vez...
    python -m venv .venv
    CALL .venv\Scripts\activate.bat
    pip install -r requirements.txt
    ECHO Entorno configurado correctamente.
) ELSE (
    ECHO Activando entorno existente...
    CALL .venv\Scripts\activate.bat
)

:: Asegurar que existe la carpeta data
IF NOT EXIST %APP_DIR%\data MKDIR %APP_DIR%\data

ECHO.
ECHO Entorno activado!
ECHO Ejecutando aplicación...
ECHO Navegue a http://127.0.0.1:5000 en su navegador
ECHO (Presione Ctrl+C para detener la aplicación)
ECHO.

:: Ejecutar la aplicación
python %APP_DIR%\main.py
