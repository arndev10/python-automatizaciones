import os
import openpyxl

# 📂 Rutas
ruta_inputos = "D:/MSI/DT CLUSTERS/G02/PHYTON CREACION/INPUTS"
ruta_salida = "D:/MSI/DT CLUSTERS/G02/PHYTON CREACION/CELDA M1"

# 🛠 Crear carpeta de salida si no existe
if not os.path.exists(ruta_salida):
    os.makedirs(ruta_salida)

# 📋 Archivos Excel
archivos_excel = [f for f in os.listdir(ruta_inputos) if f.endswith(".xlsx")]
print(f"🔍 Se encontraron {len(archivos_excel)} archivos para modificar.")

# 🔁 Recorrer archivos
for archivo in archivos_excel:
    ruta_archivo = os.path.join(ruta_inputos, archivo)
    wb = openpyxl.load_workbook(ruta_archivo)

    # ✅ Verificar si existe la hoja "Datos"
    if "Datos" in wb.sheetnames:
        hoja = wb["Datos"]
        hoja["M1"] = "Finishing Date"  # 📝 Cambiar texto
        print(f"✅ Modificado M1 en archivo: {archivo}")
    else:
        print(f"⚠️ Hoja 'Datos' no encontrada en: {archivo}")
        wb.close()
        continue

    # 💾 Guardar en nueva ruta
    ruta_guardado = os.path.join(ruta_salida, archivo)
    wb.save(ruta_guardado)
    wb.close()

print("🎉 Proceso finalizado.")
