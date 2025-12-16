"""Modulo para adaptar texto a formato narrativo para audiolibro."""
import re
from typing import List
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words


def remove_visual_references(text: str) -> str:
    """Elimina referencias visuales comunes."""
    patterns_replacements = [
        (r'como se (muestra|ve|observa|puede ver|ilustra) (arriba|abajo|en la (figura|imagen|tabla|gráfico))', ''),
        (r'como (muestra|muestran|indica|indican) (la|el|las|los) (figura|imagen|tabla|gráfico)', ''),
        (r'ver (la|el|las|los) (figura|imagen|tabla|gráfico)', ''),
        (r'\(ver (figura|imagen|tabla|gráfico)', '('),
        (r'en la (página|pág\.?) \d+', ''),
        (r'\(véase (página|pág\.?) \d+\)', ''),
    ]
    
    for pattern, replacement in patterns_replacements:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return text


def convert_lists_to_prose(text: str) -> str:
    """Convierte listas numeradas o con viñetas a prosa narrativa."""
    lines = text.split('\n')
    result_lines = []
    in_list = False
    list_items = []
    
    for line in lines:
        stripped = line.strip()
        
        # Detectar inicio de lista (números, viñetas, guiones)
        is_list_item = (
            re.match(r'^[\d]+[\.\)]\s+', stripped) or
            re.match(r'^[-•*]\s+', stripped) or
            re.match(r'^[a-z][\.\)]\s+', stripped)
        )
        
        if is_list_item:
            if not in_list:
                in_list = True
            # Extraer texto del ítem
            item_text = re.sub(r'^[\d]+[\.\)]\s+', '', stripped)
            item_text = re.sub(r'^[-•*]\s+', '', item_text)
            item_text = re.sub(r'^[a-z][\.\)]\s+', '', item_text)
            list_items.append(item_text.strip())
        else:
            if in_list and list_items:
                # Convertir lista acumulada a prosa
                if len(list_items) == 1:
                    result_lines.append(list_items[0] + '.')
                elif len(list_items) == 2:
                    result_lines.append(f"{list_items[0]} y {list_items[1]}.")
                else:
                    items_text = ', '.join(list_items[:-1])
                    result_lines.append(f"{items_text}, y {list_items[-1]}.")
                list_items = []
                in_list = False
            
            if stripped:  # Solo agregar líneas no vacías
                result_lines.append(line)
    
    # Procesar última lista si termina el texto
    if in_list and list_items:
        if len(list_items) == 1:
            result_lines.append(list_items[0] + '.')
        elif len(list_items) == 2:
            result_lines.append(f"{list_items[0]} y {list_items[1]}.")
        else:
            items_text = ', '.join(list_items[:-1])
            result_lines.append(f"{items_text}, y {list_items[-1]}.")
    
    return '\n'.join(result_lines)


def improve_sentence_flow(text: str) -> str:
    """Mejora el flujo de oraciones para audio."""
    # NOTA: Mantenemos las tildes en el texto para el audio
    # Eliminar abreviaciones problematicas
    text = re.sub(r'\bDr\.', 'Doctor', text)
    text = re.sub(r'\bSr\.', 'Señor', text)
    text = re.sub(r'\bSra\.', 'Señora', text)
    text = re.sub(r'\betc\.', 'etcétera', text)
    
    # Asegurar espacios después de puntuación
    text = re.sub(r'([.!?])([A-Z])', r'\1 \2', text)
    
    # Eliminar espacios multiples
    text = re.sub(r' +', ' ', text)
    
    return text


def moderate_summarize(text: str, reduction_percent: float = 0.15) -> str:
    """
    Resumen moderado usando LSA (Latent Semantic Analysis).
    
    reduction_percent: porcentaje de reduccion (0.15 = 15% menos texto)
    """
    if not text.strip():
        return text
    
    # Calcular numero de oraciones objetivo
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if len(sentences) < 3:
        return text  # Texto muy corto, no resumir
    
    target_sentences = max(3, int(len(sentences) * (1 - reduction_percent)))
    
    try:
        # Usar sumy para resumen extractivo
        parser = PlaintextParser.from_string(text, Tokenizer('spanish'))
        stemmer = Stemmer('spanish')
        summarizer = LsaSummarizer(stemmer)
        summarizer.stop_words = get_stop_words('spanish')
        
        summary_sentences = summarizer(parser.document, target_sentences)
        summarized_text = ' '.join(str(sentence) for sentence in summary_sentences)
        
        return summarized_text
    except Exception:
        # Si falla el resumen, devolver texto original
        return text


def adapt_for_audiobook(text: str, apply_summary: bool = True) -> str:
    """
    Adapta texto completo para audiolibro.
    
    Aplica:
    - Eliminacion de referencias visuales
    - Conversion de listas a prosa
    - Mejora de flujo de oraciones
    - Resumen moderado (opcional)
    """
    # Paso 1: Eliminar referencias visuales
    text = remove_visual_references(text)
    
    # Paso 2: Convertir listas a prosa
    text = convert_lists_to_prose(text)
    
    # Paso 3: Mejorar flujo
    text = improve_sentence_flow(text)
    
    # Paso 4: Resumen moderado (15% de reducción)
    if apply_summary:
        text = moderate_summarize(text, reduction_percent=0.15)
    
    # Limpieza final
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip()
    
    return text

