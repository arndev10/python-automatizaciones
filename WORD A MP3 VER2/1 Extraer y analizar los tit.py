from docx import Document

# Ruta del archivo Word
archivo_word = r"D:\LIBROS\Cómo ganar amigos e influir sobre las personas ( PDFDrive )\Libro_Limpio.docx"

# Cargar el documento
doc = Document(archivo_word)

# Extraer texto
texto_completo = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

# Mostrar los primeros 1000 caracteres
print(texto_completo[:1000])
