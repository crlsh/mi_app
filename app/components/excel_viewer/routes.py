from flask import Blueprint, render_template, jsonify, current_app
import logging
from .excel_viewer import get_excel_files

# Configurar logger para este módulo
logger = logging.getLogger(__name__)

# Crear el blueprint para el componente
excel_viewer_bp = Blueprint('excel_viewer', __name__, 
                          template_folder='templates',
                          url_prefix='/excel-viewer')

@excel_viewer_bp.route('/')
def show_excel_viewer():
    """Renderiza el componente excel_viewer"""
    try:
        logger.info("Solicitando el componente excel_viewer")
        excel_files = get_excel_files()
        logger.info(f"Se encontraron {len(excel_files)} archivos Excel para mostrar")
        return render_template('excel_viewer.html', excel_files=excel_files)
    except Exception as e:
        logger.error(f"Error al renderizar el componente excel_viewer: {e}")
        # Renderizar con mensaje de error
        return render_template('excel_viewer.html', excel_files=[], error=str(e))

@excel_viewer_bp.route('/data')
def get_excel_data():
    """API para obtener datos de Excel en formato JSON"""
    try:
        logger.info("Solicitando datos de Excel en formato JSON")
        excel_files = get_excel_files()
        # No podemos devolver el HTML directamente en JSON, así que devolvemos solo los nombres
        excel_names = [nombre for nombre, _ in excel_files]
        logger.info(f"Devolviendo nombres de {len(excel_names)} archivos Excel")
        return jsonify({
            "status": "success",
            "files": excel_names,
            "count": len(excel_names)
        })
    except Exception as e:
        logger.error(f"Error al obtener datos de Excel para API: {e}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "files": [],
            "count": 0
        }), 500
