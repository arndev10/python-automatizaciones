import os
import pyttsx3
import subprocess
from docx import Document

# 📌 Ruta de la carpeta con los archivos Word
carpeta_libros = r"D:\LIBROS\Cómo ganar amigos e influir sobre las personas ( PDFDrive )\TEST 1"

# Configurar pyttsx3
engine = pyttsx3.init()
engine.setProperty("rate", 180)  # Velocidad de lectura
engine.setProperty("volume", 1.0)  # Volumen máximo

def convertir_docx_a_mp3(ruta_docx):
    nombre_archivo = os.path.splitext(os.path.basename(ruta_docx))[0]
    ruta_mp3 = os.path.join(os.path.dirname(ruta_docx), f"{nombre_archivo}.mp3")
    ruta_mp3_comprimido = os.path.join(os.path.dirname(ruta_docx), f"{nombre_archivo}_comprimido.mp3")

    # Leer el contenido del documento Word
    doc = Document(ruta_docx)
    texto = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

    if texto:
        print(f"🎙️ Convirtiendo: {nombre_archivo} → {ruta_mp3}")
        engine.save_to_file(texto, ruta_mp3)
        engine.runAndWait()

        # 📌 Comprimir el MP3 con FFmpeg
        print(f"🎛️ Comprimiendo: {ruta_mp3} → {ruta_mp3_comprimido}")
        comando_ffmpeg = f'ffmpeg -i "{ruta_mp3}" -b:a 64k "{ruta_mp3_comprimido}" -y'
        resultado = subprocess.run(comando_ffmpeg, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # 📌 Verificar si FFmpeg generó el archivo correctamente
        if os.path.exists(ruta_mp3_comprimido):
            os.remove(ruta_mp3)  # Borrar el archivo original
            os.rename(ruta_mp3_comprimido, ruta_mp3)  # Renombrar el comprimido
            print(f"✅ Archivo final: {ruta_mp3} (comprimido)")
        else:
            print(f"⚠️ Error: FFmpeg no generó el archivo comprimido para {nombre_archivo}. Detalles:")
            print(resultado.stderr.decode())

    else:
        print(f"⚠️ El archivo {ruta_docx} está vacío.")

# 📌 Convertir todos los archivos .docx en la carpeta a MP3
for archivo in os.listdir(carpeta_libros):
    if archivo.endswith(".docx"):  
        ruta_docx = os.path.join(carpeta_libros, archivo)
        convertir_docx_a_mp3(ruta_docx)

print("\n✅ Todos los archivos han sido convertidos y comprimidos a MP3.")
