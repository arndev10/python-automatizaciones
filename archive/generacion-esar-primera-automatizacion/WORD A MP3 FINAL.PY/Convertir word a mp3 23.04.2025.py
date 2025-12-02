import os
import pyttsx3
from docx import Document

# Rutas de las carpetas
input_folder = r"D:\LIBROS\El poder del ahora\Resultado resumen"
output_folder = r"D:\LIBROS\El poder del ahora\MP3 resumen"

# Inicializar pyttsx3 (motor de texto a voz)
engine = pyttsx3.init()

# Configuración de la voz (puedes cambiarla si lo deseas)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # 0 para voz masculina, 1 para voz femenina
engine.setProperty('rate', 150)  # Velocidad de la voz

# Función para convertir el texto en MP3
def convert_text_to_mp3(text, filename):
    mp3_file = os.path.join(output_folder, filename)
    engine.save_to_file(text, mp3_file)
    print(f"Archivo MP3 guardado en: {mp3_file}")

# Recorrer todos los archivos de Word en la carpeta de entrada
for filename in os.listdir(input_folder):
    if filename.endswith(".docx"):
        doc_path = os.path.join(input_folder, filename)
        
        # Leer el archivo de Word
        doc = Document(doc_path)
        text = ""
        
        # Extraer el texto del documento
        for para in doc.paragraphs:
            text += para.text + "\n"
        
        # Crear un nombre para el archivo MP3
        mp3_filename = filename.replace(".docx", ".mp3")
        
        # Convertir el texto a MP3
        convert_text_to_mp3(text, mp3_filename)

# Finalizar la conversión
engine.runAndWait()
