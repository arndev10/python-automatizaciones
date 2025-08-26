import os
import pyttsx3
from docx import Document

# 📌 Ruta de la carpeta con los archivos Word (MODIFICA SEGÚN TU UBICACIÓN)
carpeta_libros = r"D:\LIBROS\Cómo ganar amigos e influir sobre las personas ( PDFDrive )\TEST 1"

# Configurar pyttsx3 (motor de voz sin conexión)
engine = pyttsx3.init()
engine.setProperty("rate", 180)  # Velocidad de lectura
engine.setProperty("volume", 1.0)  # Volumen máximo

def convertir_docx_a_mp3(ruta_docx):
    nombre_archivo = os.path.splitext(os.path.basename(ruta_docx))[0]  # Nombre del archivo sin extensión
    ruta_mp3 = os.path.join(os.path.dirname(ruta_docx), f"{nombre_archivo}.mp3")  # Crear ruta MP3

    # Leer el contenido del documento Word
    doc = Document(ruta_docx)
    texto = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

    if texto:
        print(f"🎙️ Convirtiendo: {nombre_archivo} → {ruta_mp3}")
        engine.save_to_file(texto, ruta_mp3)
        engine.runAndWait()
        print(f"✅ Archivo convertido: {ruta_mp3}")
    else:
        print(f"⚠️ El archivo {ruta_docx} está vacío.")

# 📌 Convertir todos los archivos .docx en la carpeta a MP3
for archivo in os.listdir(carpeta_libros):
    if archivo.endswith(".docx"):  
        ruta_docx = os.path.join(carpeta_libros, archivo)
        convertir_docx_a_mp3(ruta_docx)

print("\n✅ Todos los archivos han sido convertidos a MP3.")
