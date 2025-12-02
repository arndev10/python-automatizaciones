from pydub import AudioSegment
import os

# Ruta de entrada y salida
input_folder = r"D:\OGG A MP3 O WAV\OGG"
output_folder = r"D:\OGG A MP3 O WAV\MP3"

# Crear carpeta de salida si no existe
os.makedirs(output_folder, exist_ok=True)

# Recorremos todos los archivos .ogg
for filename in os.listdir(input_folder):
    if filename.lower().endswith(".ogg"):
        ogg_path = os.path.join(input_folder, filename)
        mp3_filename = os.path.splitext(filename)[0] + ".mp3"
        mp3_path = os.path.join(output_folder, mp3_filename)

        # Cargar y convertir
        audio = AudioSegment.from_file(ogg_path, format="ogg")
        audio.export(mp3_path, format="mp3")
        print(f"Convertido: {filename} → {mp3_filename}")

print("Conversión completa.")
