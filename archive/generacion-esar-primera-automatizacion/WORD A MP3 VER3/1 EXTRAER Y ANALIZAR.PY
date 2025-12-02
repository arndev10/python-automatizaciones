from docx import Document

# Ruta del archivo Word
archivo_word = r"D:\LIBROS\Cómo ganar amigos e influir sobre las personas ( PDFDrive )\Cómo ganar amigos e influir sobre las personas ( PDFDrive ).docx"

# Cargar el documento
doc = Document(archivo_word)

# Extraer y mostrar los primeros 2000 caracteres para ver la estructura
texto_completo = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
print(texto_completo[:9000])  # Muestra solo los primeros 2000 caracteres para analizar
