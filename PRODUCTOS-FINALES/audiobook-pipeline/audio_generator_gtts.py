"""Modulo alternativo para generar audio usando gTTS (Google Text-to-Speech)."""
from pathlib import Path
from pydub import AudioSegment
import tempfile
import os
from gtts import gTTS
import time


def split_text_into_chunks(text: str, max_chars: int = 4500) -> list:
    """
    Divide el texto en chunks para evitar el limite de caracteres de gTTS.
    
    Args:
        text: Texto a dividir
        max_chars: Maximo de caracteres por chunk (gTTS tiene limite de ~5000)
    
    Returns:
        Lista de chunks de texto
    """
    if len(text) <= max_chars:
        return [text]
    
    chunks = []
    current_chunk = ""
    
    # Dividir por oraciones cuando sea posible
    sentences = text.split('. ')
    
    for sentence in sentences:
        # Si agregar esta oracion excede el limite
        if len(current_chunk) + len(sentence) + 2 > max_chars and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            if current_chunk:
                current_chunk += ". " + sentence
            else:
                current_chunk = sentence
    
    # Agregar ultimo chunk
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks


def text_to_speech_gtts(text: str, output_path: str, lang: str = 'es', slow: bool = False, max_retries: int = 3) -> str:
    """
    Convierte texto a audio usando gTTS (Google Text-to-Speech).
    
    Args:
        text: Texto a convertir
        output_path: Ruta donde guardar el MP3
        lang: Idioma (default: 'es' para espanol)
        slow: Si True, habla mas lento (default: False)
        max_retries: Numero maximo de reintentos
    
    Returns:
        Ruta del archivo de audio generado
    
    Raises:
        Exception: Si falla despues de todos los reintentos
    """
    # Crear directorio si no existe
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Dividir texto en chunks si es muy largo
    text_chunks = split_text_into_chunks(text, max_chars=4500)
    
    temp_files = []
    last_error = None
    
    try:
        # Generar audio para cada chunk
        audio_segments = []
        total_chunks = len([c for c in text_chunks if c.strip()])
        
        for i, chunk in enumerate(text_chunks):
            if not chunk.strip():
                continue
            
            # Mostrar progreso si hay muchos chunks
            if total_chunks > 5:
                print(f"      Procesando chunk {i+1}/{total_chunks}...", end='\r')
            
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_path = temp_file.name
            temp_file.close()
            temp_files.append(temp_path)
            
            # Intentar generar audio para este chunk
            for attempt in range(max_retries):
                try:
                    # Esperar un poco entre intentos
                    if attempt > 0:
                        time.sleep(2 * attempt)
                    
                    tts = gTTS(text=chunk, lang=lang, slow=slow)
                    tts.save(temp_path)
                    
                    # Cargar el audio generado
                    audio = AudioSegment.from_mp3(temp_path)
                    audio_segments.append(audio)
                    break
                    
                except Exception as e:
                    last_error = e
                    if attempt == max_retries - 1:
                        raise Exception(f"Error al generar audio para chunk {i+1}: {e}")
                    continue
            
            # Pequena pausa entre chunks para evitar rate limiting
            if i < len(text_chunks) - 1:
                time.sleep(0.5)
        
        if total_chunks > 5:
            print()  # Nueva linea despues del progreso
        
        # Combinar todos los segmentos de audio
        if audio_segments:
            combined_audio = audio_segments[0]
            for segment in audio_segments[1:]:
                combined_audio += segment
            
            # Aplicar velocidad 1.15x (equivalente a +15% de edge-tts)
            combined_audio = combined_audio.speedup(playback_speed=1.15)
            
            # Exportar con compresion (96 kbps)
            combined_audio.export(output_path, format="mp3", bitrate="96k")
            
            return output_path
        else:
            raise Exception("No se pudo generar ningun segmento de audio")
            
    finally:
        # Limpiar archivos temporales
        for temp_path in temp_files:
            if os.path.exists(temp_path):
                try:
                    os.unlink(temp_path)
                except:
                    pass


def generate_chapter_audio_gtts(chapter_title: str, chapter_content: str, output_dir: Path, chapter_num: int, delay_between_chapters: float = 0.5) -> str:
    """
    Genera audio para un capitulo usando gTTS.
    
    Args:
        chapter_title: Titulo del capitulo
        chapter_content: Contenido del capitulo
        output_dir: Directorio de salida
        chapter_num: Numero de capitulo
        delay_between_chapters: Tiempo de espera entre capitulos (segundos)
    
    Returns:
        Ruta del archivo MP3 generado
    """
    # Esperar un poco entre capitulos
    if chapter_num > 1:
        time.sleep(delay_between_chapters)
    
    # Sanitizar titulo para nombre de archivo
    from audio_generator import sanitize_filename
    safe_title = sanitize_filename(chapter_title)
    
    # Formatear numero de capitulo con ceros a la izquierda
    chapter_prefix = f"{chapter_num:02d} - {safe_title}"
    
    output_path = output_dir / f"{chapter_prefix}.mp3"
    
    # Generar audio
    text_to_speech_gtts(chapter_content, str(output_path), lang='es', slow=False, max_retries=3)
    
    return str(output_path)

