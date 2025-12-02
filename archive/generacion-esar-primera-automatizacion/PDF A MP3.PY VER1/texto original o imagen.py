import fitz  # PyMuPDF

# 📌 Ruta del archivo PDF
archivo_pdf = r"D:\LIBROS\Cómo ganar amigos e influir sobre las personas ( PDFDrive )\Cómo ganar amigos e influir sobre las personas ( PDFDrive ).pdf"

# Cargar el PDF
pdf_document = fitz.open(archivo_pdf)

# Extraer el texto de las primeras 5 páginas
for pagina_num in range(5):
    pagina = pdf_document[pagina_num]
    texto = pagina.get_text("text")  # Extrae texto sin formato
    print(f"\n📌 **Texto de la Página {pagina_num + 1}:**\n")
    print(texto[:1000])  # Mostrar los primeros 1000 caracteres por página
