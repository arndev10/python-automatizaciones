import pandas as pd
import openpyxl
import os
import re  # Para limpiar caracteres no permitidos en nombres de archivos

# 📂 Rutas de archivos (MODIFICA SI ES NECESARIO)
ruta_modelo = "D:/MSI/DT CLUSTERS/G02/PHYTON CREACION/MODELO.xlsx"  # 📄 Archivo base
ruta_datos = "D:/MSI/DT CLUSTERS/G02/PHYTON CREACION/ASIA01_POST.xlsx"  # 📄 Datos
ruta_salida = "D:/MSI/DT CLUSTERS/G02/PHYTON CREACION/RESULTADO/"  # 📂 Carpeta de salida

# 🟢 1. Cargar la tabla de datos
df_datos = pd.read_excel(ruta_datos, sheet_name="Datos")  # 📋 Asegúrate que la hoja se llame "Datos"

# 🟢 2. Crear carpeta de salida con el nombre de la ruta de datos
nombre_carpeta = os.path.basename(ruta_datos).replace(".xlsx", "")  # Extrae "DATOSG03" de la ruta
ruta_carpeta_salida = os.path.join(ruta_salida, nombre_carpeta)  # Carpeta destino para los archivos

# Crear la carpeta si no existe
if not os.path.exists(ruta_carpeta_salida):
    os.makedirs(ruta_carpeta_salida)
    print(f"✅ Carpeta creada: {ruta_carpeta_salida}")
else:
    print(f"✅ La carpeta ya existe: {ruta_carpeta_salida}")

# 🟢 3. Iterar sobre cada fila de la tabla Datos
for index, fila in df_datos.iterrows():
    # 📄 Cargar el archivo Modelo
    wb = openpyxl.load_workbook(ruta_modelo)
    hoja = wb["ESAR"]  # 📄 Hoja donde se reemplazarán los datos

    # 📝 Extraer valores de la tabla Datos
    po_number = str(fila["PO Number"])  # 📌 Asegurar que sea texto
    po_line = str(fila["PO Line"])
    site_name = str(fila["Site Name"])
    item_description = fila["Item Description"]
    qty = fila["QTY"]
    po_number2 = fila["PO Number2"]
    project_code = fila["Project code"]
    project_name = fila["Project Name"]
    start_date = fila["Start Date"]
    finishing_date = fila["Finishing Date"]
    Amount_of_Attachment = fila["Amount of Attachment"]




    # 🧹 Limpiar el Site Name para que no tenga caracteres problemáticos
    site_name_limpio = re.sub(r'[\\/*?:"<>|]', "", site_name).replace(" ", "_")

    # 🔄 Reemplazar valores en la hoja ESAR
    hoja["L11"] = po_number
    hoja["C26"] = po_line
    hoja["D26"] = site_name
    hoja["F26"] = item_description
    hoja["J26"] = qty
    hoja["G33"] = po_number2
    hoja["E7"] = project_code
    hoja["E8"] = project_name
    hoja["F21"] = start_date
    hoja["L21"] = finishing_date
    hoja["H50"] = Amount_of_Attachment

    # 🏷 Guardar archivo con el formato ESAR__<PO_NUMBER>__<PO_LINE>__<SITE_NAME>.xlsx
    nombre_archivo = f"ESAR__{po_number}__{po_line}__{site_name_limpio}.xlsx"
    ruta_final = os.path.join(ruta_carpeta_salida, nombre_archivo)  # Ruta completa de destino
    wb.save(ruta_final)
    wb.close()

    print(f"✅ Archivo creado: {ruta_final}")  # Confirmación en consola

print("🎉 Proceso finalizado.")
