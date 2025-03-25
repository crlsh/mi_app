import os
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def get_excel_files():
    """
    Obtiene la lista de archivos Excel en la carpeta data y los convierte en HTML
    
    Returns:
        list: Lista de tuplas (nombre_archivo, tabla_html)
    """
    # Definir ruta de la carpeta data
    data_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data')
    
    # Imprimir información adicional en la consola para depuración
    print(f"Directorio de trabajo actual: {os.getcwd()}")
    print(f"Buscando archivos Excel en: {data_folder}")
    print(f"¿La carpeta existe? {os.path.exists(data_folder)}")
    
    excel_files = []
    
    # Verificar si la carpeta existe
    if not os.path.exists(data_folder):
        print(f"ERROR: La carpeta de datos no existe: {data_folder}")
        return excel_files
    
    # Listar archivos en el directorio
    try:
        archivos = os.listdir(data_folder)
        print(f"Archivos encontrados en la carpeta: {archivos}")
        
        # Filtrar solo archivos Excel
        archivos_excel = [f for f in archivos if f.lower().endswith(('.xlsx', '.xls'))]
        print(f"Archivos Excel encontrados: {archivos_excel}")
        
        # Procesar cada archivo Excel
        for filename in archivos_excel:
            file_path = os.path.join(data_folder, filename)
            print(f"Procesando archivo: {file_path}")
            
            try:
                # Leer el archivo Excel
                df = pd.read_excel(file_path)
                print(f"Archivo {filename} leído correctamente. Filas: {len(df)}")
                
                # Convertir a HTML
                table_html = df.to_html(classes='table table-striped', index=False)
                
                # Añadir a la lista
                excel_files.append((filename, table_html))
                print(f"Archivo {filename} agregado a la lista de resultados")
            except Exception as e:
                print(f"ERROR al procesar {filename}: {str(e)}")
        
    except Exception as e:
        print(f"ERROR general: {str(e)}")
    
    print(f"Total de archivos Excel procesados: {len(excel_files)}")
    for nombre, _ in excel_files:
        print(f"  - {nombre}")
    
    return excel_files
