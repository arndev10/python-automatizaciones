import pandas as pd
import openpyxl
import os

# 📂 Rutas de archivos (MODIFICA SI ES NECESARIO)
ruta_modelo = "D:/MSI/DT CLUSTERS/G02/PHYTON CREACION/MODELO.xlsx"  # 📄 Archivo base
ruta_datos = "D:/MSI/DT CLUSTERS/G02/PHYTON CREACION/DATOSG08.xlsx"  # 📄 Datos
ruta_salida = "D:/MSI/DT CLUSTERS/G02/PHYTON CREACION/RESULTADO/"  # 📂 Carpeta de salida

# 🟢 1. Cargar la tabla de datos
df_datos = pd.read_excel(ruta_datos, sheet_name="Datos")  # 📋 Asegúrate que la hoja se llame "Datos"

# 🟢 2. Iterar sobre cada fila de la tabla Datos
for index, fila in df_datos.iterrows():
    # 📄 Cargar el archivo Modelo
    wb = openpyxl.load_workbook(ruta_modelo)
    hoja = wb["ESAR"]  # 📄 Hoja donde se reemplazarán los datos

    # 📝 Extraer valores de la tabla Datos
    po_number = str(fila["PO Number"])  # 📌 Asegurar que sea texto
    po_line = fila["PO Line"]
    site_name = fila["Site Name"]
    item_description = fila["Item Description"]
    qty = fila["QTY"]
    po_number2 = fila["PO Number2"]

    # 🔄 Reemplazar valores en la hoja ESAR
    hoja["L11"] = po_number
    hoja["C26"] = po_line
    hoja["D26"] = site_name
    hoja["F26"] = item_description
    hoja["J26"] = qty
    hoja["G33"] = po_number2

    # 🏷 Guardar archivo con el formato ESAR__<PO_NUMBER>.xlsx
    nombre_archivo = f"ESAR__{po_number}.xlsx"
    ruta_final = os.path.join(ruta_salida, nombre_archivo)
    wb.save(ruta_final)
    wb.close()

    print(f"✅ Archivo creado: {ruta_final}")  # Confirmación en consola

print("🎉 Proceso finalizado.")
