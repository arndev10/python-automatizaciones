"""Modulo para generar audio desde texto usando edge-tts."""
import asyncio
import edge_tts
from pathlib import Path
from pydub import AudioSegment
import tempfile
import os


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


async def text_to_speech(text: str, output_path: str, voice_name: str = None, rate: str = "+15%") -> str:
    """
    Convierte texto a audio usando edge-tts.
    
    Args:
        text: Texto a convertir
        output_path: Ruta donde guardar el MP3
        voice_name: Nombre de la voz (si None, busca automáticamente)
        rate: Velocidad de lectura (default: +15% para 1.15x)
    
    Returns:
        Ruta del archivo de audio generado
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
    
    try:
        communicate = edge_tts.Communicate(text, voice_name, rate=rate)
        await communicate.save(temp_path)
        
        # Convertir de webm a MP3 y comprimir con pydub
        audio = AudioSegment.from_file(temp_path, format="webm")
        
        # Exportar con compresión (96 kbps)
        audio.export(output_path, format="mp3", bitrate="96k")
        
        return output_path
    finally:
        # Limpiar archivo temporal
        if os.path.exists(temp_path):
            os.unlink(temp_path)


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


async def generate_chapter_audio(chapter_title: str, chapter_content: str, output_dir: Path, chapter_num: int) -> str:
    """
    Genera audio para un capitulo.
    
    Returns:
        Ruta del archivo MP3 generado
    """
    # Sanitizar titulo para nombre de archivo
    safe_title = sanitize_filename(chapter_title)
    
    # Formatear numero de capitulo con ceros a la izquierda
    chapter_prefix = f"{chapter_num:02d} - {safe_title}"
    
    output_path = output_dir / f"{chapter_prefix}.mp3"
    
    # Generar audio
    await text_to_speech(chapter_content, str(output_path))
    
    return str(output_path)

