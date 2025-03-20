🔹 1. Introducción
Este documento detalla la arquitectura propuesta para la implementación de un sistema de flujos modulares en una aplicación basada en Python y Flask. El objetivo es permitir la ejecución de múltiples flujos de trabajo (Flujo A, B, C, etc.), en los cuales cada flujo es un módulo independiente que recibe entradas del usuario, filtra datos de archivos Excel, y proporciona salidas que pueden afectar a los siguientes flujos.

🔹 2. Análisis Inicial del Problema
El código original consistía en una serie de filtros aplicados secuencialmente sobre distintos archivos de datos. Cada flujo:

Preguntaba al usuario si debía ejecutarse.
Aplicaba filtros a un conjunto de datos en función de la respuesta.
Mostraba los materiales resultantes.
Determinaba el siguiente flujo a ejecutar.
📌 Conclusión: La lógica de cada flujo era principalmente un filtro condicional sobre un conjunto de datos basado en respuestas del usuario.

Problemas detectados en la implementación inicial
❌ Código monolítico y difícil de extender.
❌ Falta de modularidad: cada flujo estaba acoplado a la lógica general.
❌ No había un manejo centralizado del estado y flujo de datos.

🔹 3. Patrón de Diseño Elegido
Se adoptó una arquitectura basada en plugins combinada con un manejo centralizado del flujo utilizando Flask Sessions. Esto permite:

📌 Modularidad: Cada flujo es un plugin independiente que puede añadirse sin modificar la estructura general.
📌 Flexibilidad: El orden de ejecución se define externamente y no dentro de cada módulo.
📌 Escalabilidad: Es fácil agregar nuevos flujos sin afectar el sistema.
📌 Manejo de Estado: Se utiliza Flask Sessions para almacenar respuestas y materiales seleccionados.
🔹 Patrón de diseño:
Plugin-Based Architecture + State Management
Cada flujo actúa como un plugin independiente y el sistema maneja las transiciones y datos entre ellos.

🔹 4. Arquitectura Resultante
📂 Estructura del Proyecto

/app
  ├── main.py               # Punto de entrada de la aplicación
  ├── flujo_loader.py       # Carga y gestiona los flujos dinámicamente
  ├── plugins/              # Módulos independientes de cada flujo
  │   ├── __init__.py
  │   ├── flujo_a.py        # Flujo A
  │   ├── flujo_b.py        # Flujo B
  │   ├── flujo_c.py        # Flujo C
  │   ├── flujo_d.py        # Flujo D
  │   ├── flujo_e.py        # Flujo E
  │   ├── flujo_f.py        # Flujo F
  │   ├── flujo_g.py        # Flujo G
  │   ├── flujo_h.py        # Flujo H (siempre se ejecuta)
  ├── templates/            # HTML para la interfaz de usuario
  │   ├── base.html
  │   ├── index.html
  │   ├── flujo.html        # Página genérica para cada flujo
  │   ├── resultados.html   # Página de resultados finales
  ├── static/               # Archivos CSS y JS
  ├── data/                 # Archivos Excel
  ├── requirements.txt
  └── README.md
🔹 5. Manejo del Flujo de Ejecución
En lugar de definir el orden de los flujos dentro de cada módulo, se utiliza un diccionario de transición que maneja la lógica centralmente.

📌 Configuración de flujos en flujo_loader.py


SECUENCIA_FLUJOS = {
    "A": {"SI": "H", "NO": "B"},
    "B": {"SI": "C", "NO": "C"},
    "C": {"SI": "D", "NO": "D"},
    "D": {"SI": "E", "NO": "E"},
    "E": {"SI": "G", "NO": "F"},
    "F": {"SI": "H", "NO": "H"},
    "G": {"SI": "H", "NO": "H"},
    "H": None  # Último flujo
}
📌 Cómo funciona:

Cada flujo tiene una entrada (respuesta del usuario).
Se determina el siguiente flujo basado en la respuesta (SI o NO).
Los datos de cada flujo se almacenan en session para ser utilizados en flujos posteriores.
🔹 6. Ejemplo de Flujo Individual
Cada flujo es un módulo independiente en la carpeta plugins/.

📌 Ejemplo de plugins/flujo_a.py

python

from flask import render_template, request

nombre = "A"

def ejecutar():
    if request.method == "POST":
        respuesta = request.form.get("respuesta")
        materiales_seleccionados = ["Material X", "Material Y"] if respuesta == "SI" else []
        return respuesta, materiales_seleccionados

    return render_template("flujo.html", flujo=nombre)
📌 Explicación:

Cada flujo recibe una entrada (POST del usuario).
Si el usuario responde "SI", filtra materiales y los guarda.
Si el usuario responde "NO", se salta el procesamiento.
El sistema decide cuál es el siguiente flujo.
🔹 7. Manejo del Estado Global
Se utiliza Flask Sessions para mantener los datos entre flujos.

📌 Ejemplo de cómo se almacenan los datos en session

python

@app.route("/flujo/<nombre_flujo>", methods=["GET", "POST"])
def flujo(nombre_flujo):
    if nombre_flujo in flujos:
        respuesta, materiales, siguiente_flujo = ejecutar_flujo(nombre_flujo, session)

        # Guardar en sesión
        session[nombre_flujo] = {"respuesta": respuesta, "materiales": materiales}

        # Continuar al siguiente flujo o finalizar
        return redirect(url_for("flujo", nombre_flujo=siguiente_flujo)) if siguiente_flujo else redirect(url_for("resultados"))

    return redirect(url_for("index"))
📌 Beneficios del uso de session ✔ Permite almacenar datos persistentes sin base de datos.
✔ Mantiene la continuidad entre flujos.
✔ Hace que cada flujo sea independiente sin necesidad de modificar otros flujos.

🔹 8. Beneficios de la Arquitectura
Característica	Beneficio
Plugins Modulares	Se pueden agregar nuevos flujos sin modificar main.py.
Configuración Centralizada	El orden de ejecución se define en flujo_loader.py.
Manejo de Estado con session	Cada flujo puede acceder a respuestas y materiales previos.
Separación de Responsabilidades	main.py maneja la app, flujo_loader.py los flujos, y los plugins contienen la lógica específica.
Escalabilidad	Fácil de expandir sin modificar el código existente.
🔹 9. Conclusión
Se pasó de una estructura monolítica a una arquitectura basada en plugins donde:

Cada flujo es un módulo autónomo con entrada y salida.
El flujo de ejecución es gestionado dinámicamente.
Se utiliza session para almacenar respuestas y datos.
Los desarrolladores pueden agregar nuevos flujos sin modificar la estructura base.
Este modelo permite escalabilidad, modularidad y facilidad de mantenimiento, alineándose con buenas prácticas de arquitectura de software.