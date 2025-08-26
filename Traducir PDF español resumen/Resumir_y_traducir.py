import os
import fitz      # pip install PyMuPDF
import openai    # pip install openai==0.27.0

# ——— Configuración ———
PDF_PATH   = r"D:\LIBROS\Cracking the coding for interview\Libro\Cracking the coding for interview.pdf"
OUT_DIR    = r"D:\LIBROS\Cracking the coding for interview\Español"
openai.api_key = "TU_OPENAI_API_KEY"
CHUNK_SIZE = 3000  # aprox caracteres por fragmento

os.makedirs(OUT_DIR, exist_ok=True)

# ——— Helpers ———
def extraer_texto(doc, start, end):
    txt = ""
    for p in range(start-1, end):
        txt += doc.load_page(p).get_text()
    return txt

def filtrar_codigo(texto):
    líneas = []
    for l in texto.splitlines():
        if any(tok in l for tok in ("{", ";", " def ", " class ", "->")):
            continue
        líneas.append(l)
    return "\n".join(líneas)

def chunk_text(text, max_chars=CHUNK_SIZE):
    buf = ""
    for line in text.splitlines(keepends=True):
        if len(buf) + len(line) > max_chars:
            yield buf
            buf = ""
        buf += line
    if buf:
        yield buf

def traducir_fragmento(fragmento):
    prompt = (
        "Traduce al español este fragmento manteniendo términos técnicos "
        "y omitiendo cualquier bloque de código:\n\n" + fragmento
    )
    resp = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role":"user","content":prompt}],
        temperature=0
    )
    return resp.choices[0].message.content.strip()

# ——— Pipeline principal ———
doc = fitz.open(PDF_PATH)
toc = doc.get_toc(simple=True)  # [(nivel, título, pág), ...]

# Construye lista de capítulos: (título, inicio, fin)
chapters = []
for i, (_, title, page) in enumerate(toc):
    start = page
    end   = toc[i+1][2] - 1 if i+1 < len(toc) else doc.page_count
    chapters.append((title.strip(), start, end))

# Procesa cada capítulo
for idx, (title, start, end) in enumerate(chapters, 1):
    print(f"\n► Procesando {idx}/{len(chapters)}: “{title}” (pág {start}-{end})")
    raw  = extraer_texto(doc, start, end)
    narr = filtrar_codigo(raw)
    trad = ""

    for j, chunk in enumerate(chunk_text(narr), 1):
        print(f"   – traduciendo parte {j}…", end="")
        trad += traducir_fragmento(chunk) + "\n\n"
        print(" OK")

    safe_title = "".join(c for c in title if c.isalnum() or c.isspace()).strip()
    out_path   = os.path.join(OUT_DIR, f"{idx:02d} - {safe_title}.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n" + trad)

    print(f"   → Guardado: {out_path}")

print("\n✅ Traducción completa en tu carpeta “Español”.")
