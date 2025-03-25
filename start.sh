#!/bin/bash
echo "============================================"
echo " Activando entorno virtual, espere..."
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
echo " Entorno virtual activado correctamente!"
echo "============================================"
echo ""
echo "Para ejecutar la aplicacion, escribe:"
echo "python app/main.py"
echo ""
echo "Para acceder a la aplicacion: http://127.0.0.1:5000"
echo ""
exec $SHELL
