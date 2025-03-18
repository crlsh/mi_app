from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)

# Directorio donde se almacenan los archivos Excel
DATA_DIR = os.path.join(os.getcwd(), "data")
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
    print(f"Directorio data creado en: {DATA_DIR}")

def cargar_excels():
    """Carga todos los archivos Excel en el directorio data"""
    tablas = []
    
    # Información de diagnóstico
    print(f"Buscando archivos Excel en: {DATA_DIR}")
    print(f"¿La ruta existe? {os.path.exists(DATA_DIR)}")
    
    # Verificar si hay archivos en el directorio
    if not os.path.exists(DATA_DIR):
        print("El directorio data no existe")
        return tablas
    
    # Listar todos los archivos en el directorio
    try:
        todos_archivos = os.listdir(DATA_DIR)
        print(f"Archivos en el directorio: {todos_archivos}")
        
        # Filtrar solo archivos Excel
        archivos = [f for f in todos_archivos if f.lower().endswith(('.xlsx', '.xls'))]
        print(f"Archivos Excel encontrados: {archivos}")
        
        if not archivos:
            print("No se encontraron archivos Excel")
            return tablas
            
    except Exception as e:
        print(f"Error al listar archivos: {e}")
        return tablas
    
    # Procesar cada archivo Excel
    for nombre_archivo in archivos:
        try:
            # Ruta completa del archivo
            ruta_archivo = os.path.join(DATA_DIR, nombre_archivo)
            print(f"Procesando archivo: {ruta_archivo}")
            
            # Cargar el archivo Excel
            df = pd.read_excel(ruta_archivo)
            
            # Limpiar datos (opcional)
            df.columns = df.columns.str.strip()
            
            # Agregar a la lista de tablas
            tablas.append((nombre_archivo, df))
            print(f"Archivo {nombre_archivo} cargado correctamente. Filas: {len(df)}, Columnas: {len(df.columns)}")
            
        except Exception as e:
            print(f"Error al cargar {nombre_archivo}: {e}")
    
    return tablas

@app.route("/")
def index():
    # Cargar todos los archivos Excel
    tablas = cargar_excels()
    
    # Convertir DataFrames a HTML
    tablas_html = []
    for nombre, df in tablas:
        html = df.to_html(classes='table table-striped', index=False)
        tablas_html.append((nombre, html))
    
    # Imprimir información para diagnóstico
    print(f"Total de tablas encontradas: {len(tablas_html)}")
    
    return render_template("index.html", tablas=tablas_html)

if __name__ == "__main__":
    # Imprimir información sobre el entorno
    print(f"Directorio de trabajo actual: {os.getcwd()}")
    print(f"Directorio de datos: {DATA_DIR}")
    
    # Iniciar la aplicación Flask
    app.run(debug=True)