# from flask import Flask, render_template, redirect, url_for, session, request
# import os
# import pandas as pd
# import re

# app = Flask(__name__)
# app.secret_key = "clave_secreta_para_sesiones"  # En producción, usar una clave segura

# # Configuración de directorios
# DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
# os.makedirs(DATA_DIR, exist_ok=True)  # Crea la carpeta si no existe

# class ExcelController:
#     """Controlador para manejar la visualización y procesamiento de archivos Excel"""
    
#     @staticmethod
#     def get_excel_data():
#         """Obtiene los datos de todos los archivos Excel disponibles"""
#         tablas = []
        
#         # Verificar si la carpeta existe
#         if not os.path.exists(DATA_DIR):
#             return tablas
            
#         # Obtener archivos Excel en la carpeta
#         archivos_excel = [f for f in os.listdir(DATA_DIR) 
#                           if f.endswith('.xlsx') or f.endswith('.xls')]
        
#         for archivo in archivos_excel:
#             nombre = os.path.splitext(archivo)[0]  # Nombre sin extensión
#             ruta_completa = os.path.join(DATA_DIR, archivo)
            
#             try:
#                 # Leer el archivo Excel
#                 df = pd.read_excel(ruta_completa)
                
#                 # Convertir a HTML para visualización
#                 tabla_html = df.to_html(
#                     classes="table table-striped", 
#                     index=False,
#                     border=0
#                 )
                
#                 tablas.append((nombre, tabla_html))
#             except Exception as e:
#                 app.logger.error(f"Error al procesar {archivo}: {str(e)}")
                
#         return tablas

# # Ruta principal que muestra los archivos Excel
# @app.route('/')
# def index():
#     """Vista principal que muestra todos los archivos Excel disponibles"""
#     # Usar el controlador para obtener los datos de Excel
#     tablas = ExcelController.get_excel_data()
#     return render_template('index.html', tablas=tablas)

# # Las demás rutas y funciones permanecen igual...
# @app.route('/flujo/<nombre_flujo>', methods=["GET", "POST"])
# def flujo(nombre_flujo):
#     return render_template('flujo.html', flujo=nombre_flujo)

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, session, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_sesiones'  # Debe ser un valor seguro en producción

# Asegurar que exista la carpeta data
os.makedirs('app/data', exist_ok=True)

# Registrar el componente excel_viewer
from app.components.excel_viewer.routes import excel_viewer_bp
app.register_blueprint(excel_viewer_bp)

@app.route('/')
def index():
    """Página principal que utiliza el componente excel_viewer"""
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)