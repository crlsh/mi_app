from flask import Flask, render_template, session, redirect, url_for
import os
import logging

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_sesiones'  # Debe ser un valor seguro en producción

# Asegurar que exista la carpeta data
os.makedirs('app/data', exist_ok=True)

# Configurar logging
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app_debug.log')
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Importar el componente excel_viewer
from components.excel_viewer.routes import excel_viewer_bp
from components.excel_viewer.excel_viewer import get_excel_files

# Registrar el blueprint
app.register_blueprint(excel_viewer_bp)

@app.route('/')
def index():
    """Página principal que utiliza el componente excel_viewer"""
    # Obtener archivos Excel directamente
    excel_files = get_excel_files()
    print(f"Archivos Excel en index: {len(excel_files)}")
    return render_template('index.html', excel_files=excel_files)

if __name__ == '__main__':
    logger.info("Iniciando la aplicación...")
    logger.info(f"Directorio de trabajo actual: {os.getcwd()}")
    app.run(debug=True)
