# Visualizador de Excel

Esta aplicación simple permite visualizar archivos Excel como tablas HTML en un navegador web.

## Requisitos

- Python 3.6 o superior
- pip (gestor de paquetes de Python)


# Configuración y ejecución en VS Code (Windows)
Requisitos previos

Python 3.6 o superior
pip (gestor de paquetes de Python)

Pasos para ejecutar la aplicación
1. Clonar el repositorio

```
git clone [URL_DEL_REPOSITORIO]
cd mi_app
```
2. Crear y activar un entorno virtual

 Crear entorno virtual
```
python -m venv venv
```

# Activar el entorno virtual

```
venv\Scripts\activate
```

4. Preparar los archivos Excel

Coloca tus archivos Excel (.xlsx o .xls) en la carpeta app/data/
Si la carpeta no existe, se creará automáticamente al iniciar la aplicación


#### 5. Iniciar la aplicación
```
python app/main.py
```

#### 6. Acceder a la aplicación

en el navegador
```
 http://127.0.0.1:5000
```
Se veran todos los archivos Excel cargados y podrás iniciar los flujos de trabajo

7. Desactivar el entorno virtual cuando termines
Copydeactivate
Solución de problemas comunes

Error "No module named...": Verifica que el entorno virtual esté activado y que todas las dependencias estén instaladas
Archivos Excel no visibles: Asegúrate de que estén en la carpeta correcta (app/data/) y tengan la extensión correcta (.xlsx o .xls)

3. Abre tu navegador y ve a `http://localhost:5000`

## Notas

- La aplicación mostrará todos los archivos Excel (.xlsx o .xls) encontrados en la carpeta `data`
- Cada archivo se convertirá en una tabla HTML
- Puedes recargar la página para actualizar los datos si agregas nuevos archivos Excel mientras la aplicación está corriendo