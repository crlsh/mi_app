#!/bin/bash
echo "============================================"
echo " Iniciando Visualizador de Excel..."
echo "============================================"

# Verificar si el entorno virtual existe, si no, crearlo
if [ ! -d ".venv" ]; then
    echo "El entorno virtual no existe. Creando e instalando dependencias..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
else
    source .venv/bin/activate
fi

echo ""
echo "============================================"
echo " Iniciando la aplicacion..."
echo "============================================"
echo ""
echo "Para detener la aplicacion, presiona Ctrl+C"
echo "Abriendo navegador en http://127.0.0.1:5000"
echo ""

# Abrir navegador (intenta varios comandos según el sistema)
(python -m webbrowser "http://127.0.0.1:5000" || 
 xdg-open "http://127.0.0.1:5000" || 
 open "http://127.0.0.1:5000") &

# Iniciar la aplicación
python app/main.py
