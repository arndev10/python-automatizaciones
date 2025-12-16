"""Modulo para generar audio desde texto usando edge-tts."""
import asyncio
import edge_tts
from pathlib import Path
from pydub import AudioSegment
import tempfile
import os
import time


async def get_spanish_female_voice() -> str:
    """Obtiene una voz femenina en español."""
    voices = await edge_tts.list_voices()
    
    # Buscar voces femeninas en espanol
    # edge-tts devuelve diccionarios con claves como 'Locale', 'Gender', 'Name', 'ShortName'
    spanish_female_voices = []
    for voice in voices:
        locale = str(voice.get('Locale', '')).lower()
        gender = str(voice.get('Gender', '')).lower()
        if 'es' in locale and gender == 'female':
            spanish_female_voices.append(voice)
    
    if not spanish_female_voices:
        # Fallback: cualquier voz en español
        spanish_voices = []
        for voice in voices:
            locale = str(voice.get('Locale', '')).lower()
            if 'es' in locale:
                spanish_voices.append(voice)
        
        if spanish_voices:
            return spanish_voices[0].get('Name', spanish_voices[0].get('ShortName', ''))
        raise Exception("No se encontro voz en espanol")
    
    # Preferir voces Microsoft (generalmente mejor calidad)
    preferred = []
    for voice in spanish_female_voices:
        short_name = str(voice.get('ShortName', '')).lower()
        name = str(voice.get('Name', '')).lower()
        if 'microsoft' in short_name or 'microsoft' in name:
            preferred.append(voice)
    
    if preferred:
        return preferred[0].get('Name', preferred[0].get('ShortName', ''))
    
    return spanish_female_voices[0].get('Name', spanish_female_voices[0].get('ShortName', ''))


async def text_to_speech(text: str, output_path: str, voice_name: str = None, rate: str = "+15%", max_retries: int = 3, delay: float = 2.0) -> str:
    """
    Convierte texto a audio usando edge-tts con reintentos.
    
    Args:
        text: Texto a convertir
        output_path: Ruta donde guardar el MP3
        voice_name: Nombre de la voz (si None, busca automáticamente)
        rate: Velocidad de lectura (default: +15% para 1.15x)
        max_retries: Numero maximo de reintentos en caso de error
        delay: Tiempo de espera entre reintentos (segundos)
    
    Returns:
        Ruta del archivo de audio generado
    
    Raises:
        Exception: Si falla despues de todos los reintentos
    """
    if voice_name is None:
        voice_name = await get_spanish_female_voice()
    
    # Crear directorio si no existe
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generar audio temporal en formato webm (edge-tts usa webm por defecto)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.webm')
    temp_path = temp_file.name
    temp_file.close()
    
    last_error = None
    
    for attempt in range(max_retries):
        try:
            # Esperar un poco entre intentos para evitar rate limiting
            if attempt > 0:
                await asyncio.sleep(delay * attempt)  # Esperar mas tiempo en cada reintento
            
            communicate = edge_tts.Communicate(text, voice_name, rate=rate)
            await communicate.save(temp_path)
            
            # Convertir de webm a MP3 y comprimir con pydub
            audio = AudioSegment.from_file(temp_path, format="webm")
            
            # Exportar con compresión (96 kbps)
            audio.export(output_path, format="mp3", bitrate="96k")
            
            return output_path
        except Exception as e:
            last_error = e
            error_msg = str(e)
            # Si es error 403, esperar mas tiempo antes del siguiente intento
            if "403" in error_msg or "Invalid response status" in error_msg:
                if attempt < max_retries - 1:
                    wait_time = delay * (attempt + 2)  # Esperar mas tiempo
                    await asyncio.sleep(wait_time)
            continue
        finally:
            # Limpiar archivo temporal
            if os.path.exists(temp_path):
                try:
                    os.unlink(temp_path)
                except:
                    pass
    
    # Si llegamos aqui, todos los intentos fallaron
    raise Exception(f"Error al generar audio despues de {max_retries} intentos: {last_error}")


def sanitize_filename(filename: str) -> str:
    """Sanitiza nombre de archivo para evitar caracteres invalidos."""
    # Remover caracteres invalidos
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '')
    
    # Limitar longitud
    if len(filename) > 200:
        filename = filename[:200]
    
    return filename.strip()


async def generate_chapter_audio(chapter_title: str, chapter_content: str, output_dir: Path, chapter_num: int, delay_between_chapters: float = 1.0) -> str:
    """
    Genera audio para un capitulo.
    
    Args:
        chapter_title: Titulo del capitulo
        chapter_content: Contenido del capitulo
        output_dir: Directorio de salida
        chapter_num: Numero de capitulo
        delay_between_chapters: Tiempo de espera entre capitulos (segundos)
    
    Returns:
        Ruta del archivo MP3 generado
    """
    # Esperar un poco entre capitulos para evitar rate limiting
    if chapter_num > 1:
        await asyncio.sleep(delay_between_chapters)
    
    # Sanitizar titulo para nombre de archivo
    safe_title = sanitize_filename(chapter_title)
    
    # Formatear numero de capitulo con ceros a la izquierda
    chapter_prefix = f"{chapter_num:02d} - {safe_title}"
    
    output_path = output_dir / f"{chapter_prefix}.mp3"
    
    # Generar audio con reintentos
    await text_to_speech(chapter_content, str(output_path), max_retries=3, delay=2.0)
    
    return str(output_path)

