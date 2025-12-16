"""Modulo para detectar y segmentar capitulos."""
import re
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Chapter:
    """Representa un capitulo detectado."""
    title: str
    content: str
    start_index: int
    end_index: int


def detect_chapter_patterns(text: str) -> List[Tuple[int, str]]:
    """Detecta patrones comunes de titulos de capitulo."""
    # NOTA: Los patrones regex mantienen tildes para detectar correctamente
    patterns = [
        # "CAPITULO 1" o "CAPITULO 1" (acepta con y sin tilde) - Prioridad alta
        r'(?i)^(?:cap[íi]tulo|cap\.?)\s*(\d+[a-z]?)[\.\s:]+(.+?)$',
        # "Capitulo 1: Titulo" (acepta con y sin tilde) - Prioridad alta
        r'(?i)^cap[íi]tulo\s+(\d+[a-z]?)[\.\s:]+(.+?)$',
        # "PARTE I" o "PARTE 1" - Prioridad alta
        r'(?i)^(?:parte|part)\s+([IVX\d]+)[\.\s:]+(.+?)$',
        # "I. Titulo" (numeros romanos) - Solo si tiene suficiente contenido
        r'^([IVX]+)[\.\)]\s+(.+?)$',
    ]
    
    lines = text.split('\n')
    chapter_markers = []
    
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        # Filtrar lineas muy cortas o muy largas
        if len(line_stripped) < 10 or len(line_stripped) > 200:
            continue
        
        # Verificar que la linea siguiente tenga contenido sustancial
        # para evitar detectar elementos de lista como capitulos
        if i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            if len(next_line) < 50:  # Si la siguiente linea es muy corta, probablemente es una lista
                continue
        
        for pattern in patterns:
            match = re.match(pattern, line_stripped)
            if match:
                # Verificar que tenga texto significativo (no solo numeros)
                if any(c.isalpha() for c in line_stripped) and len(line_stripped) > 10:
                    chapter_markers.append((i, line_stripped))
                    break
    
    return chapter_markers


def extract_chapters(text: str) -> List[Chapter]:
    """Extrae capitulos del texto."""
    chapter_markers = detect_chapter_patterns(text)
    
    if not chapter_markers:
        return []
    
    chapters = []
    lines = text.split('\n')
    
    for i, (marker_idx, title) in enumerate(chapter_markers):
        start_idx = marker_idx
        
        # Determinar fin del capitulo (inicio del siguiente o fin del texto)
        if i + 1 < len(chapter_markers):
            end_idx = chapter_markers[i + 1][0]
        else:
            end_idx = len(lines)
        
        # Extraer contenido del capitulo
        chapter_lines = lines[start_idx:end_idx]
        # Remover el titulo del contenido si esta duplicado
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


def split_long_chapter(chapter: Chapter, max_words: int = 10380) -> List[Chapter]:
    """Divide un capitulo largo en partes mas pequenas."""
    words = chapter.content.split()
    
    if len(words) <= max_words:
        return [chapter]
    
    parts = []
    current_part = []
    current_word_count = 0
    part_num = 1
    
    # Dividir por parrafos cuando sea posible
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


def combine_small_chapters(chapters: List[Chapter], min_words: int) -> List[Chapter]:
    """Combina capitulos pequeños hasta alcanzar el minimo de palabras."""
    if not chapters:
        return []
    
    combined = []
    current_chapter = None
    current_words = 0
    
    for chapter in chapters:
        chapter_words = len(chapter.content.split())
        
        if current_chapter is None:
            # Iniciar nuevo capitulo combinado
            current_chapter = chapter
            current_words = chapter_words
        elif current_words + chapter_words < min_words:
            # Combinar con el capitulo actual
            # Usar el titulo del primero y combinar contenido
            combined_title = current_chapter.title
            if chapter.title != current_chapter.title:
                combined_title = f"{current_chapter.title} y {chapter.title}"
            
            combined_content = current_chapter.content + "\n\n" + chapter.content
            current_chapter = Chapter(
                title=combined_title,
                content=combined_content,
                start_index=current_chapter.start_index,
                end_index=chapter.end_index
            )
            current_words += chapter_words
        else:
            # El capitulo actual ya tiene suficientes palabras, guardarlo
            combined.append(current_chapter)
            # Iniciar nuevo capitulo
            current_chapter = chapter
            current_words = chapter_words
    
    # Agregar el ultimo capitulo
    if current_chapter:
        combined.append(current_chapter)
    
    return combined


def segment_text(text: str, min_audio_minutes: int = 20, max_audio_minutes: int = 60) -> List[Chapter]:
    """
    Segmenta el texto en capitulos de duracion apropiada.
    
    Asume ~150 palabras por minuto de audio a velocidad normal.
    Con velocidad 1.15x, son ~173 palabras por minuto.
    """
    words_per_minute = 173  # Con velocidad 1.15x
    min_words = min_audio_minutes * words_per_minute  # ~3460 palabras
    max_words = max_audio_minutes * words_per_minute  # ~10380 palabras
    
    # Intentar detectar capitulos existentes
    detected_chapters = extract_chapters(text)
    
    if detected_chapters:
        # Filtrar capitulos muy pequeños (menos de 100 palabras) que probablemente son listas
        filtered_chapters = []
        for chapter in detected_chapters:
            word_count = len(chapter.content.split())
            if word_count >= 100:  # Solo incluir capitulos con al menos 100 palabras
                filtered_chapters.append(chapter)
        
        if not filtered_chapters:
            # Si todos los capitulos son muy pequeños, usar segmentacion automatica
            return create_automatic_segmentation(text, min_words, max_words)
        
        # IMPORTANTE: Si solo hay 1 capítulo y es muy grande, forzar segmentacion automatica
        # Esto asegura que siempre se divida en capitulos de tamaño adecuado
        if len(filtered_chapters) == 1:
            single_chapter = filtered_chapters[0]
            single_chapter_words = len(single_chapter.content.split())
            # Si el unico capitulo es mas grande que el maximo, usar segmentacion automatica
            if single_chapter_words > max_words * 1.5:  # Si es mas de 1.5x el maximo
                print(f"   ⚠️  Capítulo único muy grande ({single_chapter_words} palabras), dividiendo automáticamente...")
                return create_automatic_segmentation(text, min_words, max_words)
        
        # Combinar capitulos pequeños hasta alcanzar el minimo
        combined_chapters = combine_small_chapters(filtered_chapters, min_words)
        
        # Dividir capitulos muy largos (SIEMPRE dividir si excede el maximo)
        final_chapters = []
        for chapter in combined_chapters:
            chapter_words = len(chapter.content.split())
            if chapter_words > max_words:
                # Forzar division si excede el maximo
                parts = split_long_chapter(chapter, max_words)
                final_chapters.extend(parts)
            elif chapter_words < min_words and len(combined_chapters) == 1:
                # Si solo hay 1 capítulo y es pequeño, usar segmentacion automatica para mejor distribucion
                return create_automatic_segmentation(text, min_words, max_words)
            else:
                final_chapters.append(chapter)
        
        return final_chapters
    
    # Si no hay capitulos detectados, crear segmentacion automatica
    return create_automatic_segmentation(text, min_words, max_words)


def create_automatic_segmentation(text: str, min_words: int, max_words: int) -> List[Chapter]:
    """Crea segmentacion automatica cuando no hay capitulos detectados."""
    words = text.split()
    chapters = []
    chapter_num = 1
    
    current_chunk = []
    current_word_count = 0
    
    # Dividir por parrafos
    paragraphs = text.split('\n\n')
    
    for para in paragraphs:
        para_words = para.split()
        para_word_count = len(para_words)
        
        # Si agregar este parrafo excede el maximo, crear nuevo capitulo
        if current_word_count + para_word_count > max_words and current_chunk:
            # Asegurar minimo de palabras
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
                # Si no alcanza el minimo, agregarlo de todas formas
                current_chunk.append(para)
                current_word_count += para_word_count
        else:
            current_chunk.append(para)
            current_word_count += para_word_count
    
    # Agregar ultimo capitulo
    if current_chunk:
        chapter_content = '\n\n'.join(current_chunk)
        chapters.append(Chapter(
            title=f"Capítulo {chapter_num}",
            content=chapter_content,
            start_index=0,
            end_index=0
        ))
    
    return chapters

