import pandas as pd
import os

def ejecutar(respuesta):
    """
    Ejecuta el Flujo A (Ajuste de medida)
    
    Args:
        respuesta (str): "SI" o "NO" según la respuesta del usuario
        
    Returns:
        DataFrame: DataFrame con los materiales seleccionados o vacío
    """
    # Si la respuesta es NO, retornar DataFrame vacío
    if respuesta == "NO":
        return pd.DataFrame()
        
    # Si la respuesta es SI, procesar el archivo Excel
    try:
        # Ruta del archivo Excel
        file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                               "data", "ajuste_de_medida.xlsx")
        
        # Verificar si el archivo existe
        if not os.path.exists(file_path):
            print(f"El archivo {file_path} no existe")
            return pd.DataFrame()
            
        # Cargar el archivo Excel
        df = pd.read_excel(file_path)
        
        # Limpiar los datos
        df.columns = df.columns.str.strip()
        
        # Aquí iría la lógica específica del Flujo A
        # Por ahora, simplemente retornamos todo el DataFrame
        
        # Renombrar columnas según requerimiento
        df_renombrado = df.rename(
            columns={
                "1. Cód.SAP": "Cód.SAP",
                "2. MATERIAL": "MATERIAL",
                "3. Descripción": "Descripción",
                "5.CONDICIÓN": "CONDICIÓN"
            }
        )
        
        # Asegurarse de que queden las columnas requeridas
        columnas = ["Cód.SAP", "MATERIAL", "Descripción", "4.CANTIDAD", "CONDICIÓN"]
        columnas_presentes = [col for col in columnas if col in df_renombrado.columns]
        
        return df_renombrado[columnas_presentes]
        
    except Exception as e:
        print(f"Error en Flujo A: {e}")
        return pd.DataFrame()