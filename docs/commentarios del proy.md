engo varios códigos por separado que representan diferentes flujos para la selección de materiales en la intervención de un pozo petrolero: FLUJO A, FLUJO B, FLUJO C, FLUJO D, FLUJO E, FLUJO F, FLUJO G y FLUJO H. Cada uno de ellos inicia con una pregunta que, si el usuario responde “NO”, salta inmediatamente al siguiente flujo; y si el usuario responde “SÍ”, entonces ejecuta su lógica, imprime una lista de materiales y luego avanza al siguiente flujo.

Los flujos se llaman y se encadenan de la siguiente forma:

FLUJO A (Ajuste de medida)
Si el usuario responde SÍ , se ejecuta el flujo, se imprimen los materiales, y al terminar salta a FLUJO H.
Si el usuario responde NO , salta a FLUJO B.
FLUJO B (Tubo de saca)
Si el usuario responde SÍ , se ejecuta el flujo, se imprimen los materiales, y al terminar salta a FLUJO C.
Si el usuario responde NO , salta a FLUJO C.
FLUJO C (tubería de Baja)
Si el usuario responde SÍ , se ejecuta el flujo, se imprimen los materiales, y al terminar salta a FLUJO D.
Si el usuario responde NO , salta a FLUJO D.
FLUJO D (Profundiza)
Si el usuario responde SÍ , se ejecuta el flujo, se imprimen los materiales, y al terminar salta a FLUJO E.
Si el usuario responde NO , salta a FLUJO E.
FLUJO E (Baja varillas)
Si el usuario responde SÍ , se ejecuta el flujo, se imprimen los materiales, y al terminar salta a FLUJO G.
Luego de terminar FLUJO G , debe continuar a FLUJO H .
Si el usuario responde NO , salta a FLUJO F , y al terminar FLUJO F , avanza a FLUJO H.
FLUJO F (Abandona pozo)
Luego de terminar (sea cual sea la respuesta, si aplica), avanza a FLUJO H .
FLUJO G (Instalación BM)
Cuando termine este flujo, avanza a FLUJO H.
FLUJO H (Material de agregación)
No es condicional: se supone que, al llegar aquí, se ejecuta y finaliza.
El resultado deseado es un único script de Python que combina estos ocho flujos en el orden descrito y respeta las condiciones de salto (SÍ/NO). Cada flujo debe:

Preguntar al usuario si desea ejecutar ese flujo (excepto FLUJO H, que siempre se ejecuta al llegar).
Si responde SÍ: ejecute la lógica interna de ese flujo (por ejemplo, las preguntas o procesos que incluían), e imprima la lista de materiales correspondientes.
Terminar ese flujo y, en lugar de salirse del programa, encadenar inmediatamente con el siguiente flujo indicado.
Si responde NO: saltarse la ejecución de ese flujo (no imprime materiales) y avanzar al siguiente flujo, salvo en el caso de FLUJO A y FLUJO E, que ya tienen desvíos particulares a otros flujos.


/IMPLEMNTACION BASICA COMO MOCKUP, A MODO DE EJEMPLO, NO ES EL CODIGO REAL

import os

import pandas as pd

import ipywidgets as widgets

from IPython.display import display, clear_output

 

# Variable global para almacenar los DataFrames finales de cada flujo

materiales_finales = []

 

# Función para renombrar las columnas y dejar solo las 5 requeridas

def renombrar_columnas(df):

    df_renombrado = df.rename(

        columns={

            "1. Cód.SAP": "Cód.SAP",

            "2. MATERIAL": "MATERIAL",

            "3. Descripción": "Descripción",

            "5.CONDICIÓN": "CONDICIÓN"

        }

    )

    # Asegurarse de que queden las siguientes columnas

    columnas = ["Cód.SAP", "MATERIAL", "Descripción", "4.CANTIDAD", "CONDICIÓN"]

    columnas_presentes = [col for col in columnas if col in df_renombrado.columns]

    return df_renombrado[columnas_presentes]

 

# ===============================

# FLUJO A: Ajuste de medida

# ===============================

def flujo_A():

    clear_output()

    print("FLUJO A: Ajuste de medida")

    varilla_widget = widgets.RadioButtons(

        options=["seleccionar", "SI", "NO"],

        description="¿Ajuste de medida?",

        value="seleccionar"

    )

   

    def load_excel_and_create_filters():

        clear_output()

        # print("Cargando archivo Excel...")  # Desactivado

        try:

            file_path = r"C:\Users\ry16123\OneDrive - YPF\Escritorio\power BI\GUADAL- POWER BI\Inteligencia Artificial\materiales\ajuste de medida.xlsx"

            df = pd.read_excel(file_path)

            df.columns = df.columns.str.strip()

            df["DIÁMETRO"] = df["DIÁMETRO"].astype(str).str.strip()

            # print("Excel cargado correctamente.\n")  # Desactivado

        except Exception as e:

            print("Error al cargar el archivo Excel:", e)

            return

 

        all_diams = sorted([x for x in df["DIÁMETRO"].dropna().unique() if x.upper() != "TODOS"])

        diam_widget = widgets.SelectMultiple(

            options=all_diams,

            value=(),

            description="DIÁMETRO",

            layout=widgets.Layout(width="50%")

        )

        accordion = widgets.Accordion(children=[])

        accordion_widgets = {}

       

        def crear_select_multiple_tipo(diam_value):

            subset = df[df["DIÁMETRO"] == diam_value]

            unique_tipos = sorted([x for x in subset["TIPO"].dropna().unique() if x.upper() != "TODOS"])

            if not unique_tipos:

                print(f"[Info] Para DIÁMETRO '{diam_value}', no hay TIPO disponibles. Se usará 'TODOS'.")

                return widgets.SelectMultiple(options=[], value=(), description=f"TIPO ({diam_value})", layout=widgets.Layout(width="90%"))

            else:

                return widgets.SelectMultiple(options=unique_tipos, value=(), description=f"TIPO ({diam_value})", layout=widgets.Layout(width="90%"))

       

        def crear_dropdown_unico(diam_value, columna, desc):

            subset = df[df["DIÁMETRO"] == diam_value]

            unique_vals = sorted([x for x in subset[columna].dropna().unique() if str(x).upper() != "TODOS"])

            if not unique_vals:

                print(f"[Info] Para DIÁMETRO '{diam_value}', no hay valores para {columna}. Se usará 'TODOS'.")

                return widgets.Dropdown(options=["Seleccionar"], value="Seleccionar", description=desc, layout=widgets.Layout(width="70%"))

            else:

                return widgets.Dropdown(options=["Seleccionar"] + unique_vals, value="Seleccionar", description=desc, layout=widgets.Layout(width="70%"))

       

        def update_accordion(*args):

            selected_diams = diam_widget.value

            accordion.children = []

            accordion_widgets.clear()

            if not selected_diams:

                return

            children_list = []

            for diam_value in selected_diams:

                w_tipo = crear_select_multiple_tipo(diam_value)

                w_acero = crear_dropdown_unico(diam_value, "GRADO DE ACERO", "GRADO ACERO")

                w_acero_cup = crear_dropdown_unico(diam_value, "GRADO DE ACERO CUPLA", "ACERO CUPLA")

                w_tipo_cup = crear_dropdown_unico(diam_value, "TIPO DE CUPLA", "TIPO CUPLA")

                box = widgets.VBox([w_tipo, w_acero, w_acero_cup, w_tipo_cup])

                children_list.append(box)

                accordion_widgets[diam_value] = {"tipo": w_tipo, "acero": w_acero, "acero_cup": w_acero_cup, "tipo_cup": w_tipo_cup}

            accordion.children = children_list

            for i, diam_value in enumerate(selected_diams):

                accordion.set_title(i, f"DIÁMETRO: {diam_value}")

       

        diam_widget.observe(update_accordion, names="value")

        update_accordion()

       

        output_filters = widgets.Output()

        apply_filters_button = widgets.Button(description="Aplicar Filtros", button_style="info")

       

        def on_apply_filters(b):

            with output_filters:

                clear_output()

                selected_diams = diam_widget.value

                if not selected_diams:

                    selected_diams = ["TODOS"]

                all_filters = {}

                for diam_value in selected_diams:

                    if diam_value == "TODOS":

                        tipo_list = ["TODOS"]

                        acero_list = ["TODOS"]

                        acero_cup_list = ["TODOS"]

                        tipo_cup_list = ["TODOS"]

                    else:

                        w = accordion_widgets[diam_value]

                        tipo_sel = list(w["tipo"].value)

                        if not tipo_sel:

                            tipo_sel = ["TODOS"]

                        else:

                            tipo_sel.append("TODOS")

                        ac = w["acero"].value

                        acero_list = ["TODOS"] if ac == "Seleccionar" else [ac, "TODOS"]

                        ac_cup = w["acero_cup"].value

                        acero_cup_list = ["TODOS"] if ac_cup == "Seleccionar" else [ac_cup, "TODOS"]

                        t_cup = w["tipo_cup"].value

                        tipo_cup_list = ["TODOS"] if t_cup == "Seleccionar" else [t_cup, "TODOS"]

                        all_filters[diam_value] = {"tipo_list": tipo_sel, "acero_list": acero_list, "acero_cup_list": acero_cup_list, "tipo_cup_list": tipo_cup_list}

                # print("=== Filtros recopilados ===")  # Desactivado

                # for diam_value, fdict in all_filters.items():

                #     print(f"DIÁMETRO: {diam_value}")

                #     print("   TIPO:", fdict["tipo_list"])

                #     print("   GRADO ACERO:", fdict["acero_list"])

                #     print("   ACERO CUPLA:", fdict["acero_cup_list"])

                #     print("   TIPO CUPLA:", fdict["tipo_cup_list"])

                final_condition = pd.Series([False] * len(df))

                for diam_value, fdict in all_filters.items():

                    temp_cond_diam = pd.Series([False] * len(df))

                    for tipo_val in fdict["tipo_list"]:

                        cond = (df["DIÁMETRO"].isin([diam_value, "TODOS"]) &

                                df["TIPO"].isin([tipo_val, "TODOS"]) &

                                df["GRADO DE ACERO"].isin(fdict["acero_list"]) &

                                df["GRADO DE ACERO CUPLA"].isin(fdict["acero_cup_list"]) &

                                df["TIPO DE CUPLA"].isin(fdict["tipo_cup_list"]))

                        temp_cond_diam = temp_cond_diam | cond

                    final_condition = final_condition | temp_cond_diam

                final_df = df[final_condition]

                # En lugar de mostrar inmediatamente, se almacena el DataFrame renombrado

                final_df_renombrado = renombrar_columnas(final_df)

                materiales_finales.append(("FLUJO A", final_df_renombrado))

                # print("Materiales del FLUJO A guardados.")  # Desactivado

               

                # Botón para continuar a FLUJO H (ya que en FLUJO A si se responde SI se salta directamente a H)

                continue_button = widgets.Button(description="Continuar a FLUJO H", button_style="success")

                def on_continue(b):

                    flujo_H()

                continue_button.on_click(on_continue)

                display(continue_button)

       

        apply_filters_button.on_click(on_apply_filters)

        display(widgets.VBox([diam_widget, accordion, apply_filters_button, output_filters]))

   

    def on_varilla_change(change):

        if change['name'] == 'value':

            if change['new'] == "SI":

                load_excel_and_create_filters()

            elif change['new'] == "NO":

                clear_output()

                # print("Se seleccionó NO en FLUJO A. Saltando a FLUJO B...")  # Desactivado

                flujo_B()

    varilla_widget.observe(on_varilla_change, names="value")

    display(varilla_widget)

 

# ===============================

# FLUJO B: Tubo de saca

# ===============================

def flujo_B():

    clear_output()

    print("FLUJO B: Tubo de saca")

    folder_path = r"C:\Users\ry16123\OneDrive - YPF\Escritorio\power BI\GUADAL- POWER BI\Inteligencia Artificial\materiales"

    filename_saca = "saca tubing.xlsx"

    file_path_saca = os.path.join(folder_path, filename_saca)

    global df_saca_tubing

    df_saca_tubing = None

 

    def load_saca_tubing_excel():

        global df_saca_tubing

        if not os.path.exists(file_path_saca):

            print(f"El archivo {file_path_saca} no se encontró.")

            return

        df_tmp = pd.read_excel(file_path_saca)

        df_tmp.columns = df_tmp.columns.str.strip()

        for c in df_tmp.columns:

            if df_tmp[c].dtype == object:

                df_tmp[c] = df_tmp[c].astype(str).str.strip()

        df_saca_tubing = df_tmp.copy()

        diametro_multi_picker.options = sorted(

            [d for d in df_saca_tubing['DIÁMETRO'].unique() if d.upper() != 'TODOS']

        )

 

    diametro_multi_picker = widgets.SelectMultiple(

        options=[],

        description='DIÁMETRO:',

        style={'description_width': 'initial'}

    )

    confirm_diameter_button = widgets.Button(

        description='Confirmar diámetros',

        button_style='info'

    )

    quantities_container = widgets.VBox()

    final_output = widgets.Output()

    show_table_button = widgets.Button(

        description='Mostrar tabla final',

        button_style='success'

    )

 

    def on_show_table_button_clicked(b):

        with final_output:

            clear_output()

            if df_saca_tubing is None:

                print("No hay datos cargados de saca tubing.")

                return

            selected_diameters = list(diametro_multi_picker.value)

            df_filtered = df_saca_tubing[

                (df_saca_tubing['DIÁMETRO'].isin(selected_diameters)) |

                (df_saca_tubing['DIÁMETRO'].str.upper() == 'TODOS')

            ].copy()

            for child in quantities_container.children:

                dia = child.description

                cantidad = child.value

                mask = (df_filtered['DIÁMETRO'] == dia)

                df_filtered.loc[mask, '4.CANTIDAD'] = cantidad

            df_filtered_renombrado = renombrar_columnas(df_filtered)

            materiales_finales.append(("FLUJO B", df_filtered_renombrado))

            print("Materiales del FLUJO B guardados.")

 

        # Cierra la interfaz de FLUJO B

        multi_select_container.close()

 

        # Muestra el botón para continuar al FLUJO C

        continue_button = widgets.Button(

            description="Continuar a FLUJO C",

            button_style="success"

        )

        def on_continue(b):

            clear_output()

            flujo_C()

        continue_button.on_click(on_continue)

        display(continue_button)

 

    show_table_button.on_click(on_show_table_button_clicked)

 

    def on_confirm_diameter_button_clicked(b):

        with final_output:

            clear_output()

        quantities_container.children = []

        for dia in diametro_multi_picker.value:

            qty_widget = widgets.IntText(

                value=0,

                description=dia,

                style={'description_width': 'initial'}

            )

            quantities_container.children += (qty_widget,)

 

    confirm_diameter_button.on_click(on_confirm_diameter_button_clicked)

 

    multi_select_container = widgets.VBox([

        diametro_multi_picker,

        confirm_diameter_button,

        quantities_container,

        show_table_button,

        final_output

    ])

 

    bajara_tubing_picker = widgets.Dropdown(

        options=["Seleccione opción", "SI", "NO"],

        value="Seleccione opción",

        description="¿saca Tubing?:"

    )

 

    def on_bajara_tubing_change(change):

        clear_output()

        if change['new'] == "SI":

            load_saca_tubing_excel()

            display(multi_select_container)

        elif change['new'] == "NO":

            print("No se saca tubing.")

            flujo_C()

 

    bajara_tubing_picker.observe(on_bajara_tubing_change, names='value')

 

    print("¿Saca Tubing?")

    display(bajara_tubing_picker)

 

# ===============================

# FLUJO C: Tubería de Baja

# ===============================

def flujo_C():

    clear_output()

    print("FLUJO C: Tubería de Baja")

    file_path_baja = r"C:\Users\ry16123\OneDrive - YPF\Escritorio\power BI\GUADAL- POWER BI\Inteligencia Artificial\materiales\baja tubing.xlsx"

    global df_baja_tubing

    df_baja_tubing = None

    output = widgets.Output()

    baja_tubing_widget = widgets.ToggleButtons(

        options=['SI', 'NO'],

        description='¿Baja Tubing?',

        disabled=False,

        value=None

    )

    display(baja_tubing_widget, output)

   

    def load_excel():

        with output:

            print("\n--- Carga del Excel ---")

            if not os.path.exists(file_path_baja):

                print(f"El archivo no se encontró en la ruta:\n{file_path_baja}")

                return False

            try:

                df = pd.read_excel(file_path_baja)

                df.columns = df.columns.str.strip()

                for col in df.columns:

                    if df[col].dtype == object:

                        df[col] = df[col].astype(str).str.strip()

                if 'TIPO' in df.columns:

                    df['TIPO'] = df['TIPO'].replace('nan', '').fillna('')

                if 'DIÁMETRO CSG' in df.columns:

                    df['DIÁMETRO CSG'] = df['DIÁMETRO CSG'].replace('nan', '').fillna('')

                global df_baja_tubing

                df_baja_tubing = df.copy()

                print("Archivo cargado y limpiado con éxito.")

                return True

            except Exception as e:

                print("Error al cargar el Excel:", e)

                return False

   

    def show_diametro_selection():

        with output:

            print("\n--- Selección de DIÁMETRO ---")

            df = df_baja_tubing

            unique_diametros = sorted([x for x in df['DIÁMETRO'].unique() if x != "TODOS"])

            diametro_widget = widgets.SelectMultiple(

                options=unique_diametros,

                value=(),

                description="DIÁMETRO",

                layout=widgets.Layout(width='50%')

            )

            display(diametro_widget)

            button_diametro = widgets.Button(description="Siguiente - Selección DIÁMETRO")

            display(button_diametro)

           

            def on_diametro_button_clicked(_):

                selected = list(diametro_widget.value)

                selected_diametros = ["TODOS"] if not selected else selected

                show_tipo_accordion(selected_diametros)

            button_diametro.on_click(on_diametro_button_clicked)

   

    def show_tipo_accordion(selected_diametros):

        with output:

            print("\n--- Selección de TIPO para cada DIÁMETRO ---")

            df = df_baja_tubing

            tipo_widgets = {}

            children = []

            titles = []

            for d in selected_diametros:

                df_temp = df if d=="TODOS" else df[df['DIÁMETRO'] == d]

                unique_tipos = sorted([x for x in df_temp['TIPO'].unique() if x != "TODOS"])

                widget_t = widgets.SelectMultiple(

                    options=unique_tipos,

                    value=(),

                    description=f"TIPO ({d})",

                    layout=widgets.Layout(width='50%')

                )

                tipo_widgets[d] = widget_t

                children.append(widget_t)

                titles.append(f"DIÁMETRO: {d}")

            accordion = widgets.Accordion(children=children)

            for idx, title in enumerate(titles):

                accordion.set_title(idx, title)

            display(accordion)

            button_tipo = widgets.Button(description="Siguiente - Selección TIPO")

            display(button_tipo)

           

            def on_tipo_button_clicked(_):

                selected_tipos_dict = {}

                for d, widget_t in tipo_widgets.items():

                    st = list(widget_t.value)

                    if not st:

                        st = ["TODOS"]

                    selected_tipos_dict[d] = st

                show_diametro_csg_selection(selected_diametros, selected_tipos_dict)

            button_tipo.on_click(on_tipo_button_clicked)

   

    def show_diametro_csg_selection(selected_diametros, selected_tipos_dict):

        with output:

            print("\n--- Selección de DIÁMETRO CSG ---")

            df = df_baja_tubing

            union_tipos = set()

            for tlist in selected_tipos_dict.values():

                if tlist == ["TODOS"]:

                    union_tipos.add("TODOS")

                else:

                    union_tipos.update(tlist)

                    union_tipos.add("TODOS")

            diam_filter = ["TODOS"] if selected_diametros == ["TODOS"] else selected_diametros + ["TODOS"]

            df_filtered = df[df['DIÁMETRO'].isin(diam_filter) & df['TIPO'].isin(union_tipos)]

            unique_csg = sorted([x for x in df_filtered['DIÁMETRO CSG'].unique() if x != "TODOS"])

            if not unique_csg:

                print("Nota: Solo 'TODOS' disponible para DIÁMETRO CSG. Se procede automáticamente.")

                show_quantity_inputs(selected_diametros, selected_tipos_dict, ["TODOS"])

            else:

                csg_widget = widgets.Dropdown(

                    options=unique_csg,

                    value=unique_csg[0],

                    description="DIÁMETRO CSG",

                    layout=widgets.Layout(width='50%')

                )

                display(csg_widget)

                button_csg = widgets.Button(description="Siguiente - Selección DIÁMETRO CSG")

                display(button_csg)

               

                def on_csg_button_clicked(_):

                    selected_csg = csg_widget.value

                    selected_csg_filter = [selected_csg, "TODOS"] if selected_csg != "TODOS" else ["TODOS"]

                    show_quantity_inputs(selected_diametros, selected_tipos_dict, selected_csg_filter)

                button_csg.on_click(on_csg_button_clicked)

   

    def show_quantity_inputs(selected_diametros, selected_tipos_dict, selected_csg_filter):

        with output:

            print("\n--- Ingreso de Cantidades ---")

            df = df_baja_tubing

            quantity_widgets = {}

            qty_items = []

            for d in selected_diametros:

                for t in selected_tipos_dict[d]:

                    key = (d, t)

                    w = widgets.IntText(

                        value=0,

                        description=f"{d} - {t}:",

                        layout=widgets.Layout(width='400px')

                    )

                    quantity_widgets[key] = w

                    qty_items.append(w)

            quantity_box = widgets.VBox(qty_items)

            display(quantity_box)

            update_qty_button = widgets.Button(description="Aplicar Cantidades", button_style="success")

            display(update_qty_button)

           

            def on_update_qty(b2):

                for (d, t), qty_widget in quantity_widgets.items():

                    qty_value = qty_widget.value

                    if d == "TODOS":

                        continue

                    condition = (df["DIÁMETRO"].isin([d, "TODOS"]) & df["TIPO"].isin([t, "TODOS"]))

                    df.loc[condition & df["4.CANTIDAD"].isna(), "4.CANTIDAD"] = qty_value

                final_condition = pd.Series([False]*len(df))

                for diam_value, fdict in selected_tipos_dict.items():

                    temp_cond_diam = pd.Series([False]*len(df))

                    for tipo_val in fdict:

                        cond = (df["DIÁMETRO"].isin([diam_value, "TODOS"]) & df["TIPO"].isin([tipo_val, "TODOS"]))

                        temp_cond_diam = temp_cond_diam | cond

                    final_condition = final_condition | temp_cond_diam

                final_df = df[final_condition]

                final_df_renombrado = renombrar_columnas(final_df)

                materiales_finales.append(("FLUJO C", final_df_renombrado))

                # print("Materiales del FLUJO C guardados.")  # Desactivado

                continue_button = widgets.Button(description="Continuar a FLUJO D", button_style="success")

                def on_continue(b):

                    flujo_D()

                continue_button.on_click(on_continue)

                display(continue_button)

            update_qty_button.on_click(on_update_qty)

   

    def on_baja_tubing_change(change):

        if change['name'] == 'value' and change['new'] is not None:

            if change['new'] == 'SI':

                if load_excel():

                    show_diametro_selection()

            else:

                with output:

                    print("No se procede con Baja Tubing.")

                flujo_D()

    baja_tubing_widget.observe(on_baja_tubing_change, names='value')

   

# ===============================

# FLUJO D: Profundiza

# ===============================

def flujo_D():

    clear_output()

    print("FLUJO D: Profundiza")

    output = widgets.Output()

    file_path_prof = r"C:\Users\ry16123\OneDrive - YPF\Escritorio\power BI\GUADAL- POWER BI\Inteligencia Artificial\materiales\profundiza.xlsx"

    global df_prof

    df_prof = None

    def load_excel():

        with output:

            print("\n--- Carga del Excel ---")

            if not os.path.exists(file_path_prof):

                print(f"El archivo no se encontró en la ruta:\n{file_path_prof}")

                return False

            try:

                df = pd.read_excel(file_path_prof)

                df.columns = df.columns.str.strip()

                for col in df.columns:

                    if df[col].dtype == object:

                        df[col] = df[col].astype(str).str.strip()

                if 'TIPO' in df.columns:

                    df['TIPO'] = df['TIPO'].replace('nan', '').fillna('')

                if 'DIÁMETRO CSG' in df.columns:

                    df['DIÁMETRO CSG'] = df['DIÁMETRO CSG'].replace('nan', '').fillna('')

                global df_prof

                df_prof = df.copy()

                print("Archivo cargado y limpiado con éxito.")

                return True

            except Exception as e:

                print("Error al cargar el Excel:", e)

                return False

    profundiza_widget = widgets.Dropdown(

        options=["seleccionar", "SI", "NO"],

        description="Profundizar:",

        value="seleccionar"

    )

    def on_change(change):

        if change['type'] == 'change' and change['name'] == 'value':

            clear_output()

            display(output)

            if change['new'] == "SI":

                if load_excel():

                    if "DIÁMETRO" in df_prof.columns:

                        col_diametro = "DIÁMETRO"

                    elif "DIÁMETRO CSG" in df_prof.columns:

                        col_diametro = "DIÁMETRO CSG"

                    else:

                        with output:

                            print("La columna de DIÁMETRO no se encontró en el Excel.")

                        return

                    diametro_select = widgets.SelectMultiple(

                        options=df_prof[col_diametro].unique().tolist(),

                        description="DIÁMETRO",

                        rows=10

                    )

                    display(diametro_select)

                    confirm_button = widgets.Button(description="Confirmar selección")

                    output_area = widgets.Output()

                    def on_confirm(b):

                        with output_area:

                            clear_output()

                            selected_diametros = list(diametro_select.value)

                            if not selected_diametros:

                                print("No se seleccionaron diámetros.")

                                return

                            print("Ingrese la cantidad para cada DIÁMETRO seleccionado:")

                            numeric_widgets = {}

                            for d in selected_diametros:

                                numeric_widgets[d] = widgets.BoundedFloatText(

                                    value=0,

                                    min=0,

                                    max=1000000,

                                    step=1,

                                    description=f"{d}:"

                                )

                                display(numeric_widgets[d])

                            apply_button = widgets.Button(description="Aplicar cantidades")

                            def on_apply(b):

                                filtered_df = df_prof[df_prof[col_diametro].isin(selected_diametros)].copy()

                                for d in selected_diametros:

                                    cantidad = numeric_widgets[d].value

                                    filtered_df.loc[filtered_df[col_diametro] == d, "4.CANTIDAD"] = cantidad

                                final_df_renombrado = renombrar_columnas(filtered_df)

                                materiales_finales.append(("FLUJO D", final_df_renombrado))

                                # print("Materiales del FLUJO D guardados.")  # Desactivado

                                continue_button = widgets.Button(description="Continuar a FLUJO E", button_style="success")

                                def on_continue(b):

                                    flujo_E()

                                continue_button.on_click(on_continue)

                                display(continue_button)

                            apply_button.on_click(on_apply)

                            display(apply_button)

                    confirm_button.on_click(on_confirm)

                    display(confirm_button, output_area)

            else:

                with output:

                    print("No se profundizará en la información.")

                flujo_E()

    profundiza_widget.observe(on_change)

    display(profundiza_widget)

    display(output)

 

# ===============================

# FLUJO E: Baja varillas

# ===============================

def flujo_E():

    clear_output()

    print("FLUJO E: Baja varillas")

    varilla_widget = widgets.RadioButtons(

        options=["seleccionar", "SI", "NO"],

        description="¿Baja Varilla?",

        value="seleccionar"

    )

    def load_excel_and_create_filters():

        clear_output()

        # print("Cargando archivo Excel...")  # Desactivado

        try:

            file_path = r"C:\Users\ry16123\OneDrive - YPF\Escritorio\power BI\GUADAL- POWER BI\Inteligencia Artificial\materiales\baja varillas.xlsx"

            df = pd.read_excel(file_path)

            df.columns = df.columns.str.strip()

            df["DIÁMETRO"] = df["DIÁMETRO"].astype(str).str.strip()

            # print("Excel cargado correctamente.\n")  # Desactivado

        except Exception as e:

            print("Error al cargar el archivo Excel:", e)

            return

 

        all_diams = sorted([x for x in df["DIÁMETRO"].dropna().unique() if x.upper() != "TODOS"])

        diam_widget = widgets.SelectMultiple(

            options=all_diams,

            value=(),

            description="DIÁMETRO",

            layout=widgets.Layout(width="50%")

        )

        accordion = widgets.Accordion(children=[])

        accordion_widgets = {}

        def crear_select_multiple_tipo(diam_value):

            subset = df[df["DIÁMETRO"] == diam_value]

            unique_tipos = sorted([x for x in subset["TIPO"].dropna().unique() if x.upper() != "TODOS"])

            if not unique_tipos:

                print(f"[Info] Para DIÁMETRO '{diam_value}', no hay TIPO disponibles. Se usará 'TODOS'.")

                return widgets.SelectMultiple(options=[], value=(), description=f"TIPO ({diam_value})", layout=widgets.Layout(width="90%"))

            else:

                return widgets.SelectMultiple(options=unique_tipos, value=(), description=f"TIPO ({diam_value})", layout=widgets.Layout(width="90%"))

        def crear_dropdown_unico(diam_value, columna, desc):

            subset = df[df["DIÁMETRO"] == diam_value]

            unique_vals = sorted([x for x in subset[columna].dropna().unique() if str(x).upper() != "TODOS"])

            if not unique_vals:

                print(f"[Info] Para DIÁMETRO '{diam_value}', no hay valores para {columna}. Se usará 'TODOS'.")

                return widgets.Dropdown(options=["Seleccionar"], value="Seleccionar", description=desc, layout=widgets.Layout(width="70%"))

            else:

                return widgets.Dropdown(options=["Seleccionar"] + unique_vals, value="Seleccionar", description=desc, layout=widgets.Layout(width="70%"))

        def update_accordion(*args):

            selected_diams = diam_widget.value

            accordion.children = []

            accordion_widgets.clear()

            if not selected_diams:

                return

            children_list = []

            for diam_value in selected_diams:

                w_tipo = crear_select_multiple_tipo(diam_value)

                w_acero = crear_dropdown_unico(diam_value, "GRADO DE ACERO", "GRADO ACERO")

                w_acero_cup = crear_dropdown_unico(diam_value, "GRADO DE ACERO CUPLA", "ACERO CUPLA")

                w_tipo_cup = crear_dropdown_unico(diam_value, "TIPO DE CUPLA", "TIPO CUPLA")

                box = widgets.VBox([w_tipo, w_acero, w_acero_cup, w_tipo_cup])

                children_list.append(box)

                accordion_widgets[diam_value] = {"tipo": w_tipo, "acero": w_acero, "acero_cup": w_acero_cup, "tipo_cup": w_tipo_cup}

            accordion.children = children_list

            for i, diam_value in enumerate(selected_diams):

                accordion.set_title(i, f"DIÁMETRO: {diam_value}")

        diam_widget.observe(update_accordion, names="value")

        update_accordion()

        output_filters = widgets.Output()

        apply_filters_button = widgets.Button(description="Aplicar Filtros", button_style="info")

        def on_apply_filters(b):

            with output_filters:

                clear_output()

                selected_diams = diam_widget.value

                if not selected_diams:

                    selected_diams = ["TODOS"]

                all_filters = {}

                for diam_value in selected_diams:

                    if diam_value == "TODOS":

                        tipo_list = ["TODOS"]

                        acero_list = ["TODOS"]

                        acero_cup_list = ["TODOS"]

                        tipo_cup_list = ["TODOS"]

                    else:

                        w = accordion_widgets[diam_value]

                        tipo_sel = list(w["tipo"].value)

                        if not tipo_sel:

                            tipo_sel = ["TODOS"]

                        else:

                            tipo_sel.append("TODOS")

                        ac = w["acero"].value

                        acero_list = ["TODOS"] if ac == "Seleccionar" else [ac, "TODOS"]

                        ac_cup = w["acero_cup"].value

                        acero_cup_list = ["TODOS"] if ac_cup == "Seleccionar" else [ac_cup, "TODOS"]

                        t_cup = w["tipo_cup"].value

                        tipo_cup_list = ["TODOS"] if t_cup == "Seleccionar" else [t_cup, "TODOS"]

                        all_filters[diam_value] = {"tipo_list": tipo_sel, "acero_list": acero_list, "acero_cup_list": acero_cup_list, "tipo_cup_list": tipo_cup_list}

                # print("=== Filtros recopilados ===")  # Desactivado

                # for diam_value, fdict in all_filters.items():

                #     print(f"DIÁMETRO: {diam_value}")

                #     print("   TIPO:", fdict["tipo_list"])

                #     print("   GRADO ACERO:", fdict["acero_list"])

                #     print("   ACERO CUPLA:", fdict["acero_cup_list"])

                #     print("   TIPO CUPLA:", fdict["tipo_cup_list"])

                final_condition = pd.Series([False]*len(df))

                for diam_value, fdict in all_filters.items():

                    temp_cond_diam = pd.Series([False]*len(df))

                    for tipo_val in fdict["tipo_list"]:

                        cond = (df["DIÁMETRO"].isin([diam_value, "TODOS"]) &

                                df["TIPO"].isin([tipo_val, "TODOS"]) &

                                df["GRADO DE ACERO"].isin(fdict["acero_list"]) &

                                df["GRADO DE ACERO CUPLA"].isin(fdict["acero_cup_list"]) &

                                df["TIPO DE CUPLA"].isin(fdict["tipo_cup_list"]))

                        temp_cond_diam = temp_cond_diam | cond

                    final_condition = final_condition | temp_cond_diam

                final_df = df[final_condition]

                final_df_renombrado = renombrar_columnas(final_df)

                materiales_finales.append(("FLUJO E", final_df_renombrado))

                # print("Materiales del FLUJO E guardados.")  # Desactivado

                continue_button = widgets.Button(description="Continuar a FLUJO G", button_style="success")

                def on_continue(b):

                    flujo_G()

                continue_button.on_click(on_continue)

                display(continue_button)

        apply_filters_button.on_click(on_apply_filters)

        display(widgets.VBox([diam_widget, accordion, apply_filters_button, output_filters]))

   

    def on_varilla_change(change):

        if change['name'] == 'value':

            if change['new'] == "SI":

                load_excel_and_create_filters()

            elif change['new'] == "NO":

                clear_output()

                # print("Se seleccionó NO en FLUJO E. Saltando a FLUJO F...")  # Desactivado

                flujo_F()

    varilla_widget.observe(on_varilla_change, names="value")

    display(varilla_widget)

 

# ===============================

# FLUJO F: Abandona pozo

# ===============================

def flujo_F():

    clear_output()

    print("FLUJO F: Abandona pozo")

    file_path = r"C:\Users\ry16123\OneDrive - YPF\Escritorio\power BI\GUADAL- POWER BI\Inteligencia Artificial\materiales\abandono-recupero.xlsx"

    global df_abandono

    df_abandono = None

    output = widgets.Output()

    question_widget = widgets.Dropdown(

        options=["NO", "SI"],

        value="NO",

        description="¿Abandono/recupero?:"

    )

    def filter_by_todos(df, column, selected_values):

        if "TODOS" in selected_values:

            return df

        else:

            allowed_values = list(selected_values) + ["TODOS"]

            return df[df[column].isin(allowed_values)]

    def on_question_change(change):

        if change['type'] == 'change' and change['name'] == 'value':

            clear_output()

            display(question_widget, output)

            if change['new'] == "SI":

                with output:

                    # print("Cargando el Excel...")  # (Este print no está en la lista a desactivar, se mantiene)

                    if not os.path.exists(file_path):

                        print(f"No se encontró el archivo:\n{file_path}")

                        return

                    global df_abandono

                    try:

                        df_abandono = pd.read_excel(file_path)

                    except Exception as e:

                        print("Error al cargar el Excel:", e)

                        return

                    print("Archivo cargado exitosamente.")

                df_abandono.columns = df_abandono.columns.str.strip()

                for col in df_abandono.columns:

                    if df_abandono[col].dtype == object:

                        df_abandono[col] = df_abandono[col].astype(str).str.strip()

                if "DIÁMETRO" not in df_abandono.columns:

                    with output:

                        print("La columna 'DIÁMETRO' no existe en el Excel.")

                    return

                unique_diametros = df_abandono["DIÁMETRO"].dropna().unique().tolist()

                if "TODOS" not in unique_diametros:

                    unique_diametros.insert(0, "TODOS")

                else:

                    unique_diametros.remove("TODOS")

                    unique_diametros.insert(0, "TODOS")

                if "DIÁMETRO CSG" not in df_abandono.columns:

                    with output:

                        print("La columna 'DIÁMETRO CSG' no existe en el Excel.")

                    return

                unique_diametros_csg = df_abandono["DIÁMETRO CSG"].dropna().unique().tolist()

                if "TODOS" not in unique_diametros_csg:

                    unique_diametros_csg.insert(0, "TODOS")

                else:

                    unique_diametros_csg.remove("TODOS")

                    unique_diametros_csg.insert(0, "TODOS")

                diametro_multi = widgets.SelectMultiple(

                    options=unique_diametros,

                    value=["TODOS"],

                    description="DIÁMETRO:",

                    rows=6

                )

                diametro_csg_single = widgets.Dropdown(

                    options=unique_diametros_csg,

                    value="TODOS",

                    description="DIÁM CSG:"

                )

                confirm_button = widgets.Button(

                    description="Confirmar Filtros",

                    button_style="info"

                )

                next_output = widgets.Output()

                def on_confirm_filters(b):

                    with next_output:

                        clear_output()

                        selected_diametros = list(diametro_multi.value)

                        selected_diametro_csg = diametro_csg_single.value

                        filtered_df = df_abandono.copy()

                        filtered_df = filter_by_todos(filtered_df, "DIÁMETRO", selected_diametros)

                        filtered_df = filter_by_todos(filtered_df, "DIÁMETRO CSG", [selected_diametro_csg])

                        print("Filtrado Aplicado. A continuación, ingrese cantidades (solo para celdas vacías).")

                        numeric_widgets = {}

                        diametros_especificos = [d for d in selected_diametros if d != "TODOS"]

                        if diametros_especificos:

                            print("Ingrese la cantidad para cada DIÁMETRO seleccionado:")

                            for d in diametros_especificos:

                                numeric_widgets[d] = widgets.BoundedFloatText(

                                    value=0,

                                    min=0,

                                    max=1e9,

                                    step=1,

                                    description=f"{d}:"

                                )

                                display(numeric_widgets[d])

                        else:

                            print("No se seleccionaron diámetros específicos. No se solicitarán cantidades.")

                        apply_button = widgets.Button(

                            description="Aplicar Cantidades",

                            button_style="success"

                        )

                        final_output = widgets.Output()

                        def on_apply_quantities(btn):

                            with final_output:

                                clear_output()

                                if "4.CANTIDAD" not in df_abandono.columns:

                                    print("La columna '4.CANTIDAD' no existe en el Excel.")

                                    return

                                df_abandono["4.CANTIDAD"] = pd.to_numeric(df_abandono["4.CANTIDAD"], errors="coerce")

                                for d in diametros_especificos:

                                    qty = numeric_widgets[d].value

                                    mask_diam = (df_abandono["DIÁMETRO"] == d)

                                    mask_nan = df_abandono["4.CANTIDAD"].isna()

                                    df_abandono.loc[mask_diam & mask_nan, "4.CANTIDAD"] = qty

                                filtered_final = df_abandono.copy()

                                filtered_final = filter_by_todos(filtered_final, "DIÁMETRO", selected_diametros)

                                filtered_final = filter_by_todos(filtered_final, "DIÁMETRO CSG", [selected_diametro_csg])

                                print("Listado Final Filtrado:")

                                filtered_final_renombrado = renombrar_columnas(filtered_final)

                                materiales_finales.append(("FLUJO F", filtered_final_renombrado))

                                # print("Materiales del FLUJO F guardados.")  # Desactivado

                                continue_button = widgets.Button(description="Continuar a FLUJO H", button_style="success")

                                def on_continue(b):

                                    flujo_H()

                                continue_button.on_click(on_continue)

                                display(continue_button)

                        apply_button.on_click(on_apply_quantities)

                        display(apply_button, final_output)

                confirm_button.on_click(on_confirm_filters)

                display(diametro_multi, diametro_csg_single, confirm_button, next_output)

            else:

                with output:

                    # print("No se realizará la acción. Saltando a FLUJO H...")  # Desactivado

                    pass

                flujo_H()

    question_widget.observe(on_question_change, names='value')

    display(question_widget, output)

 

 

# ===============================

# FLUJO G: Instalación BM

# ===============================

def flujo_G():

    clear_output()

    print("FLUJO G: Instalación BM")

    file_path = r"C:\Users\ry16123\OneDrive - YPF\Escritorio\power BI\GUADAL- POWER BI\Inteligencia Artificial\materiales\WO.xlsx"

    pregunta_widget = widgets.RadioButtons(

        options=["seleccionar", "SI", "NO"],

        description="¿WO a BM?",

        value="seleccionar"

    )

    def mostrar_materiales(change):

        clear_output()

        display(pregunta_widget)

        if change['new'] == "SI":

            try:

                df = pd.read_excel(file_path)

                print("Lista de materiales:")

                df_renombrado = renombrar_columnas(df)

                materiales_finales.append(("FLUJO G", df_renombrado))

                # print("Materiales del FLUJO G guardados.")  # Desactivado

            except Exception as e:

                print("Error al cargar Excel:", e)

            continue_button = widgets.Button(description="Continuar a FLUJO H", button_style="success")

            def on_continue(b):

                flujo_H()

            continue_button.on_click(on_continue)

            display(continue_button)

        elif change['new'] == "NO":

            print("No se mostrarán los materiales.")

            flujo_H()

    pregunta_widget.observe(mostrar_materiales, names='value')

    display(pregunta_widget)

 

def flujo_H():

    clear_output()

    print("=== FLUJO H: Material de agregación ===")

    try:

        file_path_H = r"C:\Users\ry16123\OneDrive - YPF\Escritorio\power BI\GUADAL- POWER BI\Inteligencia Artificial\materiales\GENERAL(1).xlsx"

        df_H = pd.read_excel(file_path_H)

        df_H.columns = df_H.columns.str.strip()

        if "4.CANTIDAD" not in df_H.columns:

            df_H["4.CANTIDAD"] = 0

    except Exception as e:

        print("Error al cargar el Excel:", e)

        df_H = pd.DataFrame()

   

    pregunta_widget_H = widgets.RadioButtons(

        options=["Seleccionar", "SI", "NO"],

        description="¿Agregar más material?",

        value="Seleccionar"

    )

    output_container_H = widgets.Output()

 

    apply_selection_button_H = widgets.Button(description="Aplicar selección", button_style="info")

    apply_qty_button_H = widgets.Button(description="Asignar cantidades", button_style="success")

   

    final_list_button = widgets.Button(description="Mostrar Listado Final de Materiales", button_style="warning")

    final_button_container = widgets.VBox([final_list_button])

   

    def on_show_final_list(b):

        clear_output()

        print("Listado final de materiales de todos los flujos ejecutados:")

        for flow, df in materiales_finales:

            print(f"\n---- {flow} ----")

            display(df)

    final_list_button.on_click(on_show_final_list)

   

    if not df_H.empty and "2. MATERIAL" in df_H.columns:

        materiales = df_H["2. MATERIAL"].astype(str).unique().tolist()

    else:

        materiales = []

    materiales_widget_H = widgets.SelectMultiple(

        options=materiales,

        description="Materiales",

        layout=widgets.Layout(width='50%', height='150px')

    )

    qty_widgets_H = {}

   

    def on_apply_selection_H(b):

        with output_container_H:

            clear_output()

            seleccionados = list(materiales_widget_H.value)

            if not seleccionados:

                print("No se seleccionó ningún material.")

                return

            print("Materiales seleccionados:")

            for mat in seleccionados:

                print("-", mat)

            qty_widgets_H.clear()

            input_boxes = []

            for mat in seleccionados:

                qty_box = widgets.BoundedFloatText(

                    value=0,

                    min=0,

                    step=1,

                    description=f"Cant: {mat}",

                    layout=widgets.Layout(width='50%')

                )

                qty_widgets_H[mat] = qty_box

                input_boxes.append(qty_box)

            display(widgets.VBox(input_boxes))

            display(apply_qty_button_H)

   

    def on_apply_qty_H(b):

        with output_container_H:

            clear_output()

            if df_H.empty:

                print("El DataFrame está vacío o no se cargó correctamente.")

                return

            selected_materials = list(qty_widgets_H.keys())

            for mat, widget_box in qty_widgets_H.items():

                cant = widget_box.value

                df_H.loc[df_H["2. MATERIAL"].astype(str) == mat, "4.CANTIDAD"] = cant

            assigned_df = df_H[

                df_H["2. MATERIAL"].astype(str).isin(selected_materials) &

                (df_H["4.CANTIDAD"] > 0)

            ]

            if not assigned_df.empty:

                assigned_df_renombrado = renombrar_columnas(assigned_df)

                materiales_finales.append(("FLUJO H", assigned_df_renombrado))

                # print("Materiales del FLUJO H guardados.")  # Desactivado

            else:

                print("No se asignaron cantidades (o todas fueron 0).")

           

            display(final_button_container)

   

    def on_pregunta_change_H(change):

        with output_container_H:

            clear_output()

            if change['new'] == "SI":

                if df_H.empty:

                    print("El DataFrame no se cargó o está vacío.")

                    return

                print("Lista completa de materiales del Excel:\n")

                display(df_H)

                print("\nSeleccione los materiales que desea agregar:")

                display(materiales_widget_H)

                display(apply_selection_button_H)

            elif change['new'] == "NO":

                print("No se agregarán más materiales.")

                display(final_button_container)

   

    pregunta_widget_H.observe(on_pregunta_change_H, names='value')

    apply_selection_button_H.on_click(on_apply_selection_H)

    apply_qty_button_H.on_click(on_apply_qty_H)

   

    display(pregunta_widget_H)

    display(output_container_H)

   

    # print("FLUJO H finalizado. Fin del proceso.")  # Desactivado

 

 

# ===============================

# Función principal: inicia en FLUJO A

# ===============================

def main():

    flujo_A()

 

# Inicia el proceso

main()