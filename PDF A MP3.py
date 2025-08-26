from gtts import gTTS

# Texto del prefacio
texto = """
Cuando Dale Carnegie escribió «Cómo ganar amigos e influir sobre las personas»,
su principal objetivo era proporcionar un texto de suplemento a su curso sobre Oratoria y Relaciones Humanas.
Nunca soñó que se transformaría en el mayor de los best-sellers, y que la gente lo leería, lo citaría y viviría según sus reglas mucho después de su propia muerte.
"""

# Convertir a audio
tts = gTTS(text=texto, lang="es")

# Guardar el archivo en la ubicación deseada
ruta_guardado = r"D:\LIBROS\Cómo ganar amigos e influir sobre las personas ( PDFDrive )\prefacio.mp3"
tts.save(ruta_guardado)

print(f"¡Conversión completa! El archivo se ha guardado en: {ruta_guardado}")
