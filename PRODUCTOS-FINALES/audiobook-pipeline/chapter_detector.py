"""Módulo para detectar y segmentar capítulos."""
import re
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Chapter:
    """Representa un capítulo detectado."""
    title: str
    content: str
    start_index: int
    end_index: int


def detect_chapter_patterns(text: str) -> List[Tuple[int, str]]:
    """Detecta patrones comunes de títulos de capítulo."""
    patterns = [
        # "CAPÍTULO 1" o "CAPITULO 1"
        r'(?i)^(?:cap[íi]tulo|cap\.?)\s*(\d+[a-z]?)[\.\s:]+(.+?)$',
        # "Capítulo 1: Título"
        r'(?i)^cap[íi]tulo\s+(\d+[a-z]?)[\.\s:]+(.+?)$',
        # "1. Título" (al inicio de línea, con número seguido de punto)
        r'^(\d+[a-z]?)[\.\)]\s+(.+?)$',
        # "I. Título" (números romanos)
        r'^([IVX]+)[\.\)]\s+(.+?)$',
        # "PARTE I" o "PARTE 1"
        r'(?i)^(?:parte|part)\s+([IVX\d]+)[\.\s:]+(.+?)$',
    ]
    
    lines = text.split('\n')
    chapter_markers = []
    
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        if len(line_stripped) < 3 or len(line_stripped) > 200:
            continue
            
        for pattern in patterns:
            match = re.match(pattern, line_stripped)
            if match:
                # Verificar que no sea solo un número suelto
                if len(line_stripped) > 10 or any(c.isalpha() for c in line_stripped):
                    chapter_markers.append((i, line_stripped))
                    break
    
    return chapter_markers


def extract_chapters(text: str) -> List[Chapter]:
    """Extrae capítulos del texto."""
    chapter_markers = detect_chapter_patterns(text)
    
    if not chapter_markers:
        return []
    
    chapters = []
    lines = text.split('\n')
    
    for i, (marker_idx, title) in enumerate(chapter_markers):
        start_idx = marker_idx
        
        # Determinar fin del capítulo (inicio del siguiente o fin del texto)
        if i + 1 < len(chapter_markers):
            end_idx = chapter_markers[i + 1][0]
        else:
            end_idx = len(lines)
        
        # Extraer contenido del capítulo
        chapter_lines = lines[start_idx:end_idx]
        # Remover el título del contenido si está duplicado
        content = '\n'.join(chapter_lines[1:]) if len(chapter_lines) > 1 else '\n'.join(chapter_lines)
        content = content.strip()
        
        if content:  # Solo agregar si tiene contenido
            chapters.append(Chapter(
                title=title,
                content=content,
                start_index=start_idx,
                end_index=end_idx
            ))
    
    return chapters


def split_long_chapter(chapter: Chapter, max_words: int = 3500) -> List[Chapter]:
    """Divide un capítulo largo en partes más pequeñas."""
    words = chapter.content.split()
    
    if len(words) <= max_words:
        return [chapter]
    
    parts = []
    current_part = []
    current_word_count = 0
    part_num = 1
    
    # Dividir por párrafos cuando sea posible
    paragraphs = chapter.content.split('\n\n')
    
    for para in paragraphs:
        para_words = para.split()
        para_word_count = len(para_words)
        
        if current_word_count + para_word_count > max_words and current_part:
            # Crear parte actual
            part_content = '\n\n'.join(current_part)
            parts.append(Chapter(
                title=f"{chapter.title} - Parte {part_num}",
                content=part_content,
                start_index=chapter.start_index,
                end_index=chapter.end_index
            ))
            current_part = [para]
            current_word_count = para_word_count
            part_num += 1
        else:
            current_part.append(para)
            current_word_count += para_word_count
    
    # Agregar última parte
    if current_part:
        part_content = '\n\n'.join(current_part)
        parts.append(Chapter(
            title=f"{chapter.title} - Parte {part_num}",
            content=part_content,
            start_index=chapter.start_index,
            end_index=chapter.end_index
        ))
    
    return parts


def segment_text(text: str, min_audio_minutes: int = 20, max_audio_minutes: int = 60) -> List[Chapter]:
    """
    Segmenta el texto en capítulos de duración apropiada.
    
    Asume ~150 palabras por minuto de audio a velocidad normal.
    Con velocidad 1.15x, son ~173 palabras por minuto.
    """
    words_per_minute = 173  # Con velocidad 1.15x
    min_words = min_audio_minutes * words_per_minute  # ~3460 palabras
    max_words = max_audio_minutes * words_per_minute  # ~10380 palabras
    
    # Intentar detectar capítulos existentes
    detected_chapters = extract_chapters(text)
    
    if detected_chapters:
        final_chapters = []
        for chapter in detected_chapters:
            # Si el capítulo es muy largo, dividirlo
            if len(chapter.content.split()) > max_words:
                parts = split_long_chapter(chapter, max_words)
                final_chapters.extend(parts)
            else:
                final_chapters.append(chapter)
        return final_chapters
    
    # Si no hay capítulos detectados, crear segmentación automática
    return create_automatic_segmentation(text, min_words, max_words)


def create_automatic_segmentation(text: str, min_words: int, max_words: int) -> List[Chapter]:
    """Crea segmentación automática cuando no hay capítulos detectados."""
    words = text.split()
    chapters = []
    chapter_num = 1
    
    current_chunk = []
    current_word_count = 0
    
    # Dividir por párrafos
    paragraphs = text.split('\n\n')
    
    for para in paragraphs:
        para_words = para.split()
        para_word_count = len(para_words)
        
        # Si agregar este párrafo excede el máximo, crear nuevo capítulo
        if current_word_count + para_word_count > max_words and current_chunk:
            # Asegurar mínimo de palabras
            if current_word_count >= min_words:
                chapter_content = '\n\n'.join(current_chunk)
                chapters.append(Chapter(
                    title=f"Capítulo {chapter_num}",
                    content=chapter_content,
                    start_index=0,
                    end_index=0
                ))
                chapter_num += 1
                current_chunk = [para]
                current_word_count = para_word_count
            else:
                # Si no alcanza el mínimo, agregarlo de todas formas
                current_chunk.append(para)
                current_word_count += para_word_count
        else:
            current_chunk.append(para)
            current_word_count += para_word_count
    
    # Agregar último capítulo
    if current_chunk:
        chapter_content = '\n\n'.join(current_chunk)
        chapters.append(Chapter(
            title=f"Capítulo {chapter_num}",
            content=chapter_content,
            start_index=0,
            end_index=0
        ))
    
    return chapters

