# Visualizador de Excel

Esta aplicación simple permite visualizar archivos Excel como tablas HTML en un navegador web.

## Requisitos

- Python 3.6 o superior
- pip (gestor de paquetes de Python)

## Instrucciones SUPER SIMPLES

### Primera vez y todos los días

#### Opción 1: Ejecución con un solo clic
- **Windows**: Haz doble clic en `run.bat`
- **Mac/Linux**: 
  1. Abre una terminal en la carpeta del proyecto
  2. Ejecuta `chmod +x run.sh` (solo la primera vez)
  3. Ejecuta `./run.sh`

La aplicación se iniciará automáticamente y abrirá tu navegador.

#### Opción 2: Inicio manual
Si prefieres iniciar manualmente:

1. **Windows**: Ejecuta `start.bat`
   **Mac/Linux**: Ejecuta `./start.sh` (después de `chmod +x start.sh` la primera vez)

2. Cuando veas el mensaje de confirmación, ejecuta:
   ```
   python app/main.py
   ```

3. Accede a http://127.0.0.1:5000 en tu navegador

### Para colocar archivos Excel

1. Coloca tus archivos Excel (.xlsx o .xls) en la carpeta `app/data/`
2. Haz clic en el botón "Recargar Datos" en la aplicación para ver los cambios

### Para detener la aplicación

Presiona `Ctrl+C` en la ventana de la terminal donde se ejecuta la aplicación.

## ¿Qué hace esta aplicación?

- Muestra archivos Excel de la carpeta `app/data/` como tablas HTML en tu navegador
- Facilita la visualización de datos tabulares sin necesidad de abrir Excel
- Permite compartir fácilmente información en formato tabular

## Solución de problemas comunes

- **Error "No module named..."**: Los scripts de inicio deberían resolver esto automáticamente
- **Archivos Excel no visibles**: Asegúrate de que estén en la carpeta correcta (app/data/) y tengan la extensión correcta (.xlsx o .xls)
- **Problemas persistentes**: Elimina la carpeta `.venv` y ejecuta nuevamente el script de inicio

## Notas técnicas (para desarrolladores)

Los scripts automatizan:
1. La creación del entorno virtual (.venv) si no existe
2. La instalación de dependencias necesarias
3. La activación del entorno virtual
4. La ejecución de la aplicación (solo los scripts `run.bat` y `run.sh`)

Esto elimina la necesidad de recordar comandos complejos o entender cómo funcionan los entornos virtuales.
