import os
from gtts import gTTS
from docx import Document

# Ruta de la carpeta donde están los archivos Word
carpeta_libros = r"D:\LIBROS\Cómo ganar amigos e influir sobre las personas ( PDFDrive )"

# Función para convertir un documento Word en MP3
def convertir_docx_a_mp3(ruta_docx):
    # Extraer el nombre del archivo sin extensión
    nombre_archivo = os.path.splitext(os.path.basename(ruta_docx))[0]
    ruta_mp3 = os.path.join(os.path.dirname(ruta_docx), f"{nombre_archivo}.mp3")

    # Leer el contenido del archivo Word
    doc = Document(ruta_docx)
    texto = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])  # Evita líneas vacías
    
    if texto:
        tts = gTTS(text=texto, lang="es")
        tts.save(ruta_mp3)
        print(f"✅ Archivo convertido: {ruta_mp3}")
    else:
        print(f"⚠️ El archivo {ruta_docx} no tiene texto legible.")

# Buscar todos los archivos .docx en la carpeta y convertirlos
for archivo in os.listdir(carpeta_libros):
    if archivo.endswith(".docx"):  
        ruta_docx = os.path.join(carpeta_libros, archivo)
        convertir_docx_a_mp3(ruta_docx)

print("\n✅ Todos los archivos han sido convertidos a MP3 en la misma carpeta.")
