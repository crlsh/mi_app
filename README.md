# Visualizador de Excel

Esta aplicación simple permite visualizar archivos Excel como tablas HTML en un navegador web.

## Requisitos

- Python 3.6 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. Clona o descarga este repositorio
2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Uso

1. Coloca tus archivos Excel (.xlsx o .xls) en la carpeta `data` 
   (se creará automáticamente si no existe)
2. Ejecuta la aplicación:

```bash
python app.py
```

3. Abre tu navegador y ve a `http://localhost:5000`

## Notas

- La aplicación mostrará todos los archivos Excel (.xlsx o .xls) encontrados en la carpeta `data`
- Cada archivo se convertirá en una tabla HTML
- Puedes recargar la página para actualizar los datos si agregas nuevos archivos Excel mientras la aplicación está corriendo