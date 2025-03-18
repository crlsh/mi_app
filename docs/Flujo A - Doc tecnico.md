📌 Especificación Técnica para Desarrollo – FLUJO A (Ajuste de Medida)
1️⃣ Descripción General
FLUJO A permite al usuario seleccionar materiales basados en criterios específicos de ajuste de medida. Si el usuario acepta el ajuste, el flujo filtra los materiales y salta directamente a FLUJO H. Si el usuario rechaza, salta a FLUJO B sin procesar datos.

2️⃣ Datos de Entrada
La información proviene de una tabla estructurada (ajuste_de_medida.xlsx), con las siguientes columnas clave:

Columna	Tipo	Descripción
DIÁMETRO	string	Diámetro del material
TIPO	string	Tipo de material
GRADO DE ACERO	string	Grado de acero
GRADO DE ACERO CUPLA	string	Grado de acero de la cupla
TIPO DE CUPLA	string	Tipo de cupla
4.CANTIDAD	float	Cantidad del material (opcional)
3️⃣ Flujo de Ejecución
Pregunta al usuario:

Si responde "NO" → Salta directamente a FLUJO B.
Si responde "SÍ" → Carga la tabla y aplica filtros.
Carga y Filtrado de Datos:

Carga la tabla ajuste_de_medida.xlsx y limpia valores.
El usuario selecciona valores en los siguientes filtros:
DIÁMETRO
TIPO
GRADO DE ACERO
GRADO DE ACERO CUPLA
TIPO DE CUPLA
Si el usuario no selecciona un valor, se usa "TODOS" como fallback.
Construcción de final_condition (máscara booleana de filtrado):

Inicializa final_condition con False para excluir todos los registros.
Para cada DIÁMETRO seleccionado, evalúa si los materiales cumplen con los criterios del usuario.
Incluye "TODOS" en cada filtro para garantizar que los valores no seleccionados no eliminen registros útiles.
Se combinan las condiciones (| lógico) para crear el filtro final.
Aplicación del Filtro:

python
Copy
Edit
final_df = df[final_condition]
Solo quedan los materiales que cumplen con los criterios del usuario.
Almacena los materiales filtrados en materiales_finales:

python
Copy
Edit
materiales_finales.append(("FLUJO A", final_df_renombrado))
Salto a FLUJO H (el flujo no sigue la secuencia normal):

Si el usuario ejecuta FLUJO A, no sigue a FLUJO B, sino directamente a FLUJO H.
4️⃣ Consideraciones Técnicas
✔ No modifica la estructura de la tabla, solo aplica filtros.
✔ Debe permitir múltiples selecciones en cada filtro.
✔ Evita pérdida de datos con "TODOS" en cada condición.
✔ Encapsular final_condition como lógica reutilizable para otros flujos.
✔ Optimizar el acceso a archivos si se requiere ejecución frecuente.

📌 Resumen Final
FLUJO A solo se ejecuta si el usuario dice "SÍ".
Carga una tabla de materiales y filtra datos según selección del usuario.
Almacena los materiales seleccionados y salta directamente a FLUJO H.
Si el usuario dice "NO", salta a FLUJO B sin procesar nada.
final_condition es el mecanismo que define qué materiales quedan en la selección final.
🚀 Resultado esperado: Un módulo optimizado que procesa materiales en base a filtros dinámicos y garantiza la continuidad del flujo sin interrumpir la secuencia de ejecución.