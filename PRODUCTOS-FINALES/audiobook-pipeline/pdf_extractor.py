"""Modulo para extraer y limpiar texto de PDFs."""
import re
from pathlib import Path
from typing import List, Tuple
import pdfplumber


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extrae texto completo de un PDF."""
    text_parts = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    
    return '\n'.join(text_parts)


def clean_text(text: str) -> str:
    """Limpia el texto de artefactos y normaliza formato."""
    # NOTA: No usamos unidecode aqui para mantener las tildes en el audio
    # Solo normalizamos espacios y formato
    
    # Eliminar multiples espacios
    text = re.sub(r' +', ' ', text)
    
    # Eliminar multiples saltos de linea (maximo 2 consecutivos)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Arreglar palabras cortadas por saltos de linea
    text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)
    
    # Limpiar espacios alrededor de saltos de linea
    text = re.sub(r' +\n', '\n', text)
    text = re.sub(r'\n +', '\n', text)
    
    # Eliminar caracteres de control excepto saltos de linea y tabs
    text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]', '', text)
    
    return text.strip()


def extract_and_clean_pdf(pdf_path: str) -> str:
    """Extrae y limpia texto de un PDF en un solo paso."""
    raw_text = extract_text_from_pdf(pdf_path)
    cleaned_text = clean_text(raw_text)
    return cleaned_text

