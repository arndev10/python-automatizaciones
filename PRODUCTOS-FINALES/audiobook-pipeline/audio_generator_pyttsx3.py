"""Modulo para generar audio usando pyttsx3 (offline, rapido)."""
from pathlib import Path
from pydub import AudioSegment
import tempfile
import os
import pyttsx3
import time


def generate_chapter_audio_pyttsx3(chapter_title: str, chapter_content: str, output_dir: Path, chapter_num: int, delay_between_chapters: float = 0.1) -> str:
    """
    Genera audio para un capitulo usando pyttsx3 (offline, rapido).
    
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
    
    # Crear archivo temporal WAV
    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    temp_wav_path = temp_wav.name
    temp_wav.close()
    
    try:
        # Inicializar motor TTS
        engine = pyttsx3.init()
        
        # Configurar propiedades de voz (espanol si esta disponible)
        voices = engine.getProperty('voices')
        
        # Buscar voz en espanol
        spanish_voice = None
        for voice in voices:
            if 'spanish' in voice.name.lower() or 'espanol' in voice.name.lower() or 'es' in voice.id.lower():
                spanish_voice = voice.id
                break
        
        if spanish_voice:
            engine.setProperty('voice', spanish_voice)
        
        # Configurar velocidad (valores tipicos: 50-200, default ~200)
        # Reducir velocidad para mejor comprension
        engine.setProperty('rate', 170)  # Similar a velocidad normal
        
        # Configurar volumen (0.0 a 1.0)
        engine.setProperty('volume', 1.0)
        
        # Generar audio directamente a archivo WAV
        print(f"      Generando audio con pyttsx3...", end='\r')
        engine.save_to_file(chapter_content, temp_wav_path)
        engine.runAndWait()
        
        # Convertir WAV a MP3 y aplicar compresion
        audio = AudioSegment.from_wav(temp_wav_path)
        
        # Aplicar velocidad 1.15x (equivalente a edge-tts)
        audio = audio.speedup(playback_speed=1.15)
        
        # Exportar con compresion (96 kbps)
        audio.export(str(output_path), format="mp3", bitrate="96k")
        
        print(f"      Audio generado exitosamente                    ")
        
        return str(output_path)
        
    finally:
        # Limpiar archivo temporal
        if os.path.exists(temp_wav_path):
            try:
                os.unlink(temp_wav_path)
            except:
                pass

