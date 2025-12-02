import os
import re
from docx import Document

# Ruta del archivo original
archivo_original = r"D:\LIBROS\Cómo ganar amigos e influir sobre las personas ( PDFDrive )\Cómo ganar amigos e influir sobre las personas ( PDFDrive ).docx"

# Cargar el documento
doc = Document(archivo_original)

# Ruta de la carpeta donde se guardarán los archivos
carpeta_destino = os.path.dirname(archivo_original)  # Usa la misma carpeta donde está el archivo original

# Variables de control
secciones = {}
current_section = "Prefacio"
secciones[current_section] = []

# Expresión regular para detectar títulos (funciona con diferentes formatos)
regex_titulo = re.compile(r"^(prefacio|parte\s*\d*|cap[ií]tulo\s*\d+|secci[oó]n\s*\d*|ep[ií]logo|introducci[oó]n)", re.IGNORECASE)

# Buscar títulos de capítulos y dividir el contenido
for para in doc.paragraphs:
    texto = para.text.strip()
    if regex_titulo.match(texto):  # Detectar títulos con la expresión regular
        current_section = texto.replace(":", "").replace(".", "").replace("/", "_")  # Limpiar caracteres extraños
        secciones[current_section] = []
    secciones[current_section].append(texto)

# Guardar cada sección en un archivo separado
for idx, (titulo, contenido) in enumerate(secciones.items()):
    # Determinar si es Prefacio, Parte, Capítulo o Sección
    titulo_limpio = titulo.lower()
    if "prefacio" in titulo_limpio:
        nombre_archivo = f"Prefacio_Cómo ganar amigos e influir sobre las personas ( PDFDrive ).docx"
    elif "parte" in titulo_limpio:
        nombre_archivo = f"Parte_{idx}_Cómo ganar amigos e influir sobre las personas ( PDFDrive ).docx"
    elif "capítulo" in titulo_limpio:
        numero = re.search(r"\d+", titulo)  # Extraer el número del capítulo
        nombre_archivo = f"Capitulo_{numero.group()}_Cómo ganar amigos e influir sobre las personas ( PDFDrive ).docx" if numero else f"Capitulo_{idx}_Cómo ganar amigos e influir sobre las personas ( PDFDrive ).docx"
    else:
        nombre_archivo = f"Seccion_{idx}_Cómo ganar amigos e influir sobre las personas ( PDFDrive ).docx"

    ruta_guardado = os.path.join(carpeta_destino, nombre_archivo)

    # Crear un nuevo documento y guardar el contenido
    nuevo_doc = Document()
    nuevo_doc.add_paragraph(titulo)  # Agregar el título al documento
    nuevo_doc.add_paragraph("\n".join(contenido))  # Agregar el contenido de la sección
    nuevo_doc.save(ruta_guardado)

    print(f"✅ Archivo creado: {ruta_guardado}")

print("\n✅ Todas las secciones han sido guardadas correctamente.")
