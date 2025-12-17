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
    # SOLO detectar patrones muy específicos para evitar falsos positivos
    patterns = [
        # "CAPITULO 1" o "CAPITULO 1" (acepta con y sin tilde) - Prioridad alta
        r'(?i)^(?:cap[íi]tulo|cap\.?)\s*(\d+[a-z]?)[\.\s:]+(.+?)$',
        # "Capitulo 1: Titulo" (acepta con y sin tilde) - Prioridad alta
        r'(?i)^cap[íi]tulo\s+(\d+[a-z]?)[\.\s:]+(.+?)$',
        # "PARTE I" o "PARTE 1" - Prioridad alta
        r'(?i)^(?:parte|part)\s+([IVX\d]+)[\.\s:]+(.+?)$',
    ]
    
    lines = text.split('\n')
    chapter_markers = []
    
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        # Filtrar lineas muy cortas o muy largas
        if len(line_stripped) < 15 or len(line_stripped) > 200:
            continue
        
        # Verificar que la linea siguiente tenga contenido sustancial
        # para evitar detectar elementos de lista como capitulos
        if i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            if len(next_line) < 100:  # Aumentado a 100 para ser más estricto
                continue
        
        for pattern in patterns:
            match = re.match(pattern, line_stripped)
            if match:
                # Verificar que tenga texto significativo (no solo numeros)
                if any(c.isalpha() for c in line_stripped) and len(line_stripped) > 15:
                    chapter_markers.append((i, line_stripped))
                    break
    
    # Si detecta muy pocos capítulos (menos de 3), probablemente son falsos positivos
    # En ese caso, retornar lista vacía para forzar segmentación automática
    if len(chapter_markers) < 3:
        return []
    
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


def segment_text_by_minutes(text: str, pdf_title: str, minutes_per_chapter: int = 45) -> List[Chapter]:
    """
    Segmenta el texto dividiendo por minutos fijos (enfoque MVP simple).
    
    Calcula el total de minutos y divide en partes de tamaño fijo.
    Nombres: primeras 5 palabras del PDF + "Parte X"
    
    Args:
        text: Texto completo a segmentar
        pdf_title: Nombre del archivo PDF (sin extension)
        minutes_per_chapter: Minutos por parte (default: 45)
    
    Returns:
        Lista de capitulos de aproximadamente minutes_per_chapter minutos cada uno
    """
    words_per_minute = 173  # Con velocidad 1.15x
    words_per_part = minutes_per_chapter * words_per_minute  # ~7785 palabras por parte de 45 min
    
    # Calcular total de palabras y minutos
    total_words = len(text.split())
    total_minutes = total_words / words_per_minute
    num_parts = max(1, int(total_minutes / minutes_per_chapter))
    
    # Obtener primeras 5 palabras del titulo del PDF
    title_words = pdf_title.split()[:5]
    base_title = ' '.join(title_words)
    
    print(f"   📊 Total: {total_words} palabras (~{total_minutes:.1f} minutos)")
    print(f"   📚 Dividiendo en {num_parts} parte(s) de ~{minutes_per_chapter} minutos cada una")
    
    # Dividir texto directamente por palabras (enfoque simple y confiable)
    words_list = text.split()
    total_words = len(words_list)
    words_per_part = total_words // num_parts
    
    chapters = []
    
    # Dividir por palabras y reconstruir texto
    for i in range(num_parts):
        start_word_idx = i * words_per_part
        
        if i == num_parts - 1:
            # Ultima parte: tomar todo lo que queda
            end_word_idx = total_words
        else:
            end_word_idx = (i + 1) * words_per_part
        
        # Obtener palabras de esta parte
        part_words = words_list[start_word_idx:end_word_idx]
        
        if not part_words:
            continue
        
        # Reconstruir texto: unir palabras con espacios
        # Esto mantiene el contenido exacto y el tamaño correcto
        part_text = ' '.join(part_words)
        
        chapters.append(Chapter(
            title=f"{base_title} - Parte {i + 1}",
            content=part_text,
            start_index=0,
            end_index=0
        ))
    
    return chapters


def segment_text(text: str, pdf_title: str = "", min_audio_minutes: int = 20, max_audio_minutes: int = 60) -> List[Chapter]:
    """
    Segmenta el texto en partes usando divisor simple por minutos (MVP).
    
    Enfoque simple: calcula minutos totales y divide en partes de 45 minutos.
    Nombres: primeras 5 palabras del PDF + "Parte X"
    """
    # Limpiar nombre del PDF (quitar extension y caracteres especiales)
    if not pdf_title:
        pdf_title = "Documento"
    else:
        # Quitar extension .pdf
        pdf_title = pdf_title.replace('.pdf', '').replace('.PDF', '')
        # Limpiar caracteres especiales para nombre
        import re
        pdf_title = re.sub(r'[<>:"/\\|?*]', '', pdf_title)
    
    # Usar divisor simple de 45 minutos por parte
    return segment_text_by_minutes(text, pdf_title, minutes_per_chapter=45)


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

