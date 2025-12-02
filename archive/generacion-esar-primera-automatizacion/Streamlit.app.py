import streamlit as st
import pandas as pd
import openpyxl
import os

# Función para crear la guía ESAR
def crear_guia_esar(row, modelo_path, salida_path):
    # Cargar el archivo modelo
    wb = openpyxl.load_workbook(modelo_path)
    hoja = wb["ESAR"]  # La hoja donde se reemplazarán los datos

    # Extraer valores de la fila de datos
    po_number = str(row["PO Number"])  # Asegurarse de que sea texto
    po_line = row["PO Line"]
    site_name = row["Site Name"]
    item_description = row["Item Description"]
    qty = row["QTY"]
    po_number2 = row["PO Number2"]

    # Reemplazar valores en el modelo
    hoja["L11"] = po_number
    hoja["C26"] = po_line
    hoja["D26"] = site_name
    hoja["F26"] = item_description
    hoja["J26"] = qty
    hoja["G33"] = po_number2

    # Guardar el archivo generado
    nombre_archivo = f"ESAR__{po_number}.xlsx"
    ruta_final = os.path.join(salida_path, nombre_archivo)
    wb.save(ruta_final)
    wb.close()

    return ruta_final  # Retornamos la ruta del archivo generado

# Función para leer y procesar el archivo subido
def procesar_archivo(uploaded_file, carpeta_destino):
    # Leer el archivo Excel con pandas
    df_datos = pd.read_excel(uploaded_file, sheet_name="Datos")  # Cambiar "Datos" si es necesario

    # Definir la ruta del modelo
    ruta_modelo = "D:/MSI/DT CLUSTERS/G02/PHYTON CREACION/MODELO.xlsx"

    # Lista para almacenar las rutas de las guías generadas
    archivos_generados = []

    # Iterar sobre cada fila del dataframe
    for index, fila in df_datos.iterrows():
        archivo_azar = crear_guia_esar(fila, ruta_modelo, carpeta_destino)
        archivos_generados.append(archivo_azar)

    return archivos_generados

# Título de la aplicación
st.title('Generador de Guías ESAR')

# Subir archivo de datos
uploaded_file = st.file_uploader("Sube el archivo con los datos", type=["xlsx"])

# Input para seleccionar la carpeta donde guardar las guías
carpeta_destino = st.text_input("Ingresa la ruta de la carpeta para guardar las guías generadas:", "D:/MSI/DT CLUSTERS/G02/PHYTON CREACION/RESULTADO/")

# Cuando el archivo es subido
if uploaded_file is not None:
    if os.path.isdir(carpeta_destino):  # Verificar que la carpeta existe
        # Procesar el archivo y generar las guías ESAR
        archivos_generados = procesar_archivo(uploaded_file, carpeta_destino)

        # Mostrar mensaje de éxito
        st.success(f"Se han generado {len(archivos_generados)} guías ESAR con éxito.")

        # Ofrecer los archivos generados para su descarga
        for archivo in archivos_generados:
            with open(archivo, "rb") as f:
                st.download_button(
                    label=f"Descargar {os.path.basename(archivo)}",
                    data=f,
                    file_name=os.path.basename(archivo),
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    else:
        st.error("La carpeta especificada no existe. Por favor, ingresa una ruta válida.")

