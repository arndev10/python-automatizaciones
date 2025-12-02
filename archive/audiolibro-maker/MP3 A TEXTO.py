import whisper
import os
import torch
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No detectada")

# Cargar el modelo de Whisper
model = whisper.load_model("base")  # Puedes usar "small", "medium", etc.

# Directorios
input_folder = r"D:\OGG A MP3 O WAV\MP3"
output_folder = r"D:\OGG A MP3 O WAV\TEXTO"
os.makedirs(output_folder, exist_ok=True)

# Procesar cada archivo .mp3
for filename in os.listdir(input_folder):
    if filename.lower().endswith(".mp3"):
        mp3_path = os.path.join(input_folder, filename)
        result = model.transcribe(mp3_path)

        # Guardar en archivo .txt
        txt_filename = os.path.splitext(filename)[0] + ".txt"
        txt_path = os.path.join(output_folder, txt_filename)
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(result["text"])

        print(f"Transcripción guardada: {txt_filename}")

print("✅ Transcripción completada para todos los archivos.")
