import fitz  # PyMuPDF

# 📌 Ruta del archivo PDF
archivo_pdf = r"D:\LIBROS\Cómo ganar amigos e influir sobre las personas ( PDFDrive )\Cómo ganar amigos e influir sobre las personas ( PDFDrive ).pdf"

# Cargar el PDF
pdf_document = fitz.open(archivo_pdf)

# Extraer texto de las primeras 10 páginas
for pagina_num in range(10):
    pagina = pdf_document[pagina_num]
    texto = pagina.get_text("text")  # Extrae el texto en orden
    print(f"\n📌 **Página {pagina_num + 1}:**\n")
    print(texto[:1000])  # Muestra los primeros 1000 caracteres por página

