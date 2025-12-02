import pandas as pd
import openpyxl
import os
import re
import warnings

# 🔇 Ignorar advertencias de openpyxl sobre DrawingML
warnings.simplefilter("ignore", UserWarning)

# 📂 Rutas
ruta_modelo = "D:/MSI/DT CLUSTERS/G02/PHYTON CREACION/MODELO.xlsx"
ruta_inputos = "D:/MSI/DT CLUSTERS/G02/PHYTON CREACION/INPUTS"
ruta_salida = "D:/MSI/DT CLUSTERS/G02/PHYTON CREACION/RESULTADO/"

# 📋 Buscar archivos en la carpeta INPUTS
archivos_datos = [f for f in os.listdir(ruta_inputos) if f.endswith(".xlsx")]
print(f"📋 Se encontraron {len(archivos_datos)} archivos para procesar.")

# 🔄 Iterar sobre cada archivo en INPUTS
for archivo in archivos_datos:
    ruta_datos = os.path.join(ruta_inputos, archivo)
    df_datos = pd.read_excel(ruta_datos, sheet_name="Datos")  

    # 🏷 Crear carpeta de salida
    nombre_carpeta = os.path.splitext(archivo)[0]  
    ruta_carpeta_salida = os.path.join(ruta_salida, nombre_carpeta)

    if not os.path.exists(ruta_carpeta_salida):
        os.makedirs(ruta_carpeta_salida)
        print(f"✅ Carpeta creada: {ruta_carpeta_salida}")
    else:
        print(f"✅ La carpeta ya existe: {ruta_carpeta_salida}")

    # 🟢 Iterar sobre cada fila de la tabla Datos
    for _, fila in df_datos.iterrows():
        wb = openpyxl.load_workbook(ruta_modelo)
        hoja = wb["ESAR"]

        # 📝 Extraer valores
        po_number = str(fila["PO Number"])
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

        # 🧹 Limpiar nombres
        site_name_limpio = re.sub(r'[\\/*?:"<>|]', "", site_name).replace(" ", "_")

        # 🔄 Reemplazar datos en ESAR
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

        # 💾 Guardar archivo ESAR
        nombre_archivo = f"ESAR__{po_number}__{po_line}__{site_name_limpio}.xlsx"
        ruta_final = os.path.join(ruta_carpeta_salida, nombre_archivo)
        wb.save(ruta_final)
        wb.close()

        print(f"✅ Archivo creado: {ruta_final}")

print("🎉 Proceso finalizado.")
