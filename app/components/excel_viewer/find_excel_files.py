import os
import sys

def find_excel_directory():
    """
    Busca la carpeta 'data' que contiene archivos Excel en varias ubicaciones posibles.
    
    Returns:
        str: Ruta absoluta a la carpeta de datos
    """
    # Lista de posibles ubicaciones relativas
    possible_locations = [
        # Directamente en el directorio actual
        'data',
        # Un nivel arriba
        os.path.join('..', 'data'),
        # Dos niveles arriba
        os.path.join('..', '..', 'data'),
        # Desde la raíz del proyecto
        os.path.join('app', 'data'),
        # Desde la raíz del proyecto, un nivel arriba
        os.path.join('..', 'app', 'data'),
    ]
    
    # Comprobar cada ubicación posible
    for location in possible_locations:
        path = os.path.abspath(location)
        if os.path.exists(path) and os.path.isdir(path):
            excel_files = [f for f in os.listdir(path) if f.endswith(('.xlsx', '.xls'))]
            if excel_files:
                return path
    
    # Si no se encuentra en ninguna ubicación relativa, buscar en todo el proyecto
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    for root, dirs, files in os.walk(base_dir):
        if 'data' in dirs:
            data_dir = os.path.join(root, 'data')
            excel_files = [f for f in os.listdir(data_dir) if f.endswith(('.xlsx', '.xls'))]
            if excel_files:
                return data_dir
    
    # Si aún no se encuentra, devolvemos una ruta predeterminada
    return os.path.abspath('app/data')

if __name__ == "__main__":
    # Mostrar la ruta encontrada si se ejecuta directamente
    print(find_excel_directory())
