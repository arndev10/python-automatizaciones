import fitz  # PyMuPDF

# 📌 Ruta del archivo PDF
archivo_pdf = r"D:\LIBROS\Cómo ganar amigos e influir sobre las personas ( PDFDrive )\Cómo ganar amigos e influir sobre las personas ( PDFDrive ).pdf"

# Cargar el PDF
pdf_document = fitz.open(archivo_pdf)

# Extraer la estructura de la primera página
pagina = pdf_document[0]
estructura = pagina.get_text("dict")

# Mostrar la estructura del texto extraído
import json
print(json.dumps(estructura, indent=4, ensure_ascii=False))
