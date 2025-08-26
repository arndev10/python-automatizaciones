import fitz  # PyMuPDF

# 📌 Ruta del archivo PDF
archivo_pdf = r"D:\LIBROS\Cómo ganar amigos e influir sobre las personas ( PDFDrive )\Cómo ganar amigos e influir sobre las personas ( PDFDrive ).pdf"

# Cargar el PDF
pdf_document = fitz.open(archivo_pdf)

# Detectar títulos según su tamaño de letra y negrita
titulos_encontrados = []

for pagina_num in range(len(pdf_document)):  # Recorre todas las páginas del PDF
    pagina = pdf_document[pagina_num]
    bloques_texto = pagina.get_text("dict")["blocks"]  # Extrae bloques de texto con formato
    
    for bloque in bloques_texto:
        for linea in bloque["lines"]:
            for span in linea["spans"]:
                texto = span["text"].strip()
                tamano = span["size"]  # Tamaño de letra
                negrita = "bold" in span["font"]  # Detecta si es negrita
                
                # Detectar si es un título basándonos en el tamaño de la fuente
                if tamano > 12 and negrita:  # Ajusta este valor si es necesario
                    titulos_encontrados.append(texto)

# Mostrar los títulos detectados
print("\n📌 **Títulos detectados:**\n")
for titulo in titulos_encontrados:
    print(titulo)
