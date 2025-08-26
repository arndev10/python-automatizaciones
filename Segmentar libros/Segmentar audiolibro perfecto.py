import os
import math
import shutil
import subprocess

# --- Configuración ---
audio_input = r"D:\LIBROS\habitos automicos\Completo\Habitos atomicos de james clearr.mp3"
output_dir  = r"D:\LIBROS\habitos automicos\Segmentado"
total_parts = 8

# --- Verificar FFmpeg y FFprobe en PATH ---
ffmpeg = shutil.which("ffmpeg")
ffprobe = shutil.which("ffprobe")
if not ffmpeg or not ffprobe:
    raise EnvironmentError("Asegúrate de tener ffmpeg y ffprobe en tu PATH")
print(f"ffmpeg: {ffmpeg}\nffprobe: {ffprobe}")

# Crear carpeta de salida si no existe
os.makedirs(output_dir, exist_ok=True)

# --- Obtener duración total con ffprobe ---
cmd = [ffprobe, '-v', 'error', '-show_entries', 'format=duration',
       '-of', 'default=nw=1:nk=1', audio_input]
result = subprocess.run(cmd, capture_output=True, text=True, check=True)
duration_s = float(result.stdout.strip())
part_duration = duration_s / total_parts

print(f"Duración total: {duration_s/60:.2f} minutos")
print(f"Cada parte: {part_duration/60:.2f} minutos (~{part_duration:.0f} s)")

# --- Segmentación con llamadas a ffmpeg ---
for i in range(total_parts):
    start = part_duration * i
    # Para la última parte, cubrimos hasta el final
    length = part_duration if i < total_parts - 1 else (duration_s - start)

    outfile = os.path.join(
        output_dir,
        f"habitos atomicos parte {i+1}.mp3"
    )
    cmd = [
        ffmpeg,
        '-ss', str(start),
        '-t', str(length),
        '-i', audio_input,
        '-c', 'copy',
        outfile
    ]
    print(f"Exportando parte {i+1} (inicio {start:.0f}s, duración {length:.0f}s)")
    subprocess.run(cmd, check=True)

print("Segmentación completada.")