import fitz  # PyMuPDF
import re

# 📌 Ruta del archivo PDF (MODIFICA SEGÚN TU ARCHIVO)
archivo_pdf = r"D:\LIBROS\Cómo ganar amigos e influir sobre las personas ( PDFDrive )\Cómo ganar amigos e influir sobre las personas ( PDFDrive ).pdf"

# Cargar el PDF
pdf_document = fitz.open(archivo_pdf)

# Expresión regular para detectar títulos con palabras clave
regex_titulo = re.compile(
    r"^(PREFACIO|PARTE\s*\d+|CAP[IÍ]TULO\s*\d+|SECCI[ÓO]N\s*\d+|EP[IÍ]LOGO|INTRODUCCI[ÓO]N|CONCLUSI[ÓO]N|RESUMEN|APÉNDICE|OCHO OBJETIVOS|NUEVE SUGERENCIAS|CÓMO FUE ESCRITO|UN BREVE CAMINO HACIA LA DISTINCIÓN)",
    re.IGNORECASE
)

# 📌 Parámetros de detección de títulos
TAMANO_MINIMO_TITULO = 14  # Ajusta según el tamaño de letra del PDF
MARGEN_SUPERIOR = 200  # Detectar si el texto está en la parte superior de la página
LONGITUD_MINIMA_TITULO = 10  # Evitar detectar palabras sueltas
LONGITUD_MAXIMA_TITULO = 60  # Evitar detectar párrafos largos como títulos

# 📌 Lista para almacenar los títulos detectados
titulos_encontrados = []

# 📌 Analizar cada página del PDF
for pagina_num in range(len(pdf_document)):  
    pagina = pdf_document[pagina_num]
    bloques_texto = pagina.get_text("dict")["blocks"]  # Extraer bloques de texto con formato

    for bloque in bloques_texto:
        if "lines" in bloque:  # Verifica si hay líneas de texto en el bloque
            for linea in bloque["lines"]:
                for span in linea["spans"]:
                    texto = span["text"].strip()
                    tamano = span["size"]  # Tamaño de letra
                    fuente = span["font"]  # Tipo de fuente
                    y_pos = bloque["bbox"][1]  # Posición vertical en la página

                    # 📌 Condiciones para detectar títulos reales
                    es_mayusculas = texto.isupper()  # Verificar si todo está en mayúsculas
                    es_negrita = "bold" in fuente.lower()  # Verificar si es negrita
                    es_cercano_al_inicio = y_pos < MARGEN_SUPERIOR  # Verificar si está en la parte superior
                    es_titulo_claro = regex_titulo.match(texto)  # Verificar si es un título conocido
                    es_suficientemente_largo = LONGITUD_MINIMA_TITULO <= len(texto) <= LONGITUD_MAXIMA_TITULO  # Evitar detectar frases largas

                    # 📌 Aplicar reglas combinadas para minimizar falsos positivos
                    if (
                        (tamano > TAMANO_MINIMO_TITULO and es_negrita and es_suficientemente_largo) or
                        (es_titulo_claro) or
                        (es_mayusculas and es_negrita and es_suficientemente_largo and es_cercano_al_inicio)
                    ):
                        titulos_encontrados.append(texto)

# 📌 Mostrar los títulos detectados
print("\n📌 **Títulos detectados:**\n")
for titulo in titulos_encontrados:
    print(titulo)
