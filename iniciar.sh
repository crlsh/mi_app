#!/bin/bash
# Script para activar entorno y ejecutar aplicación en Linux/Mac

# Colores para mensajes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Directorio de la aplicación
APP_DIR="app"

echo -e "${YELLOW}Iniciando Visualizador de Excel...${NC}"

# Verificar si el entorno virtual existe
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Configurando entorno por primera vez...${NC}"
    python3 -m venv .venv || python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    echo -e "${GREEN}Entorno configurado correctamente.${NC}"
else
    echo -e "${YELLOW}Activando entorno existente...${NC}"
    source .venv/bin/activate
fi

# Asegurar que existe la carpeta data
mkdir -p ${APP_DIR}/data

echo -e "${GREEN}Entorno activado!${NC}"
echo -e "${YELLOW}Ejecutando aplicación...${NC}"
echo -e "${GREEN}Navegue a http://127.0.0.1:5000 en su navegador${NC}"
echo -e "${YELLOW}(Presione Ctrl+C para detener la aplicación)${NC}"

# Ejecutar la aplicación
python ${APP_DIR}/main.py
