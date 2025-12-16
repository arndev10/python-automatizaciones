"""Script principal del pipeline de generacion de audiolibros."""
import asyncio
import click
from pathlib import Path
from tqdm import tqdm

from pdf_extractor import extract_and_clean_pdf
from chapter_detector import segment_text
from narrative_adapter import adapt_for_audiobook
from audio_generator import generate_chapter_audio
from audio_generator_gtts import generate_chapter_audio_gtts


async def process_audiobook(pdf_path: str, output_dir: str = "output", tts_engine: str = "gtts"):
    """Procesa un PDF completo y genera audiolibro."""
    # Usar carpeta output por defecto si no se especifica
    pdf_path_obj = Path(pdf_path)
    output_path_obj = Path(output_dir)
    output_path_obj.mkdir(parents=True, exist_ok=True)
    
    if not pdf_path_obj.exists():
        raise FileNotFoundError(f"El archivo PDF no existe: {pdf_path}")
    
    print(f"📖 Extrayendo texto de: {pdf_path_obj.name}")
    text = extract_and_clean_pdf(str(pdf_path_obj))
    
    if not text.strip():
        raise ValueError("No se pudo extraer texto del PDF. Verifica que el PDF contenga texto.")
    
    print(f"✅ Texto extraido: {len(text)} caracteres")
    
    print("\n📚 Detectando y segmentando capitulos...")
    chapters = segment_text(text, min_audio_minutes=20, max_audio_minutes=60)
    
    if not chapters:
        raise ValueError("No se pudieron detectar o crear capitulos.")
    
    print(f"✅ {len(chapters)} capitulo(s) detectado(s)")
    for i, chapter in enumerate(chapters, 1):
        word_count = len(chapter.content.split())
        estimated_minutes = word_count / 173  # palabras por minuto a 1.15x
        print(f"   {i}. {chapter.title} (~{estimated_minutes:.1f} min, {word_count} palabras)")
    
    print("\n✍️  Adaptando texto para audiolibro...")
    adapted_chapters = []
    for chapter in tqdm(chapters, desc="Adaptando capitulos"):
        adapted_content = adapt_for_audiobook(chapter.content, apply_summary=True)
        adapted_chapters.append((chapter.title, adapted_content))
    
    print("\n🎙️  Generando archivos de audio...")
    print(f"   Usando motor: {tts_engine.upper()}")
    generated_files = []
    
    # Seleccionar funcion de generacion de audio
    if tts_engine.lower() == 'gtts':
        generate_func = generate_chapter_audio_gtts
        is_async = False
    else:
        generate_func = generate_chapter_audio
        is_async = True
    
    for i, (title, content) in enumerate(tqdm(adapted_chapters, desc="Generando audio"), 1):
        try:
            if is_async:
                output_file = await generate_func(title, content, output_path_obj, i)
            else:
                output_file = generate_func(title, content, output_path_obj, i)
            generated_files.append(output_file)
            print(f"   ✅ {Path(output_file).name}")
        except Exception as e:
            print(f"   ❌ Error en {title}: {e}")
            continue
    
    print(f"\n🎉 ¡Proceso completado!")
    print(f"📁 Archivos generados en: {output_path_obj.absolute()}")
    print(f"📊 Total de archivos: {len(generated_files)}")
    
    return generated_files


@click.command()
@click.argument('pdf_path', type=click.Path(exists=True), required=False)
@click.option('--output', '-o', default='output', help='Carpeta de salida para los MP3')
@click.option('--tts', default='gtts', type=click.Choice(['gtts', 'edge'], case_sensitive=False), 
              help='Motor de texto a voz: gtts (Google, recomendado) o edge (Microsoft)')
def main(pdf_path: str, output: str, tts: str):
    """Genera audiolibro desde un PDF."""
    # Si no se especifica PDF, buscar en carpeta input
    if pdf_path is None:
        input_dir = Path('input')
        if not input_dir.exists():
            input_dir.mkdir(exist_ok=True)
        
        pdf_files = list(input_dir.glob('*.pdf'))
        if not pdf_files:
            print("❌ No se encontro ningun PDF en la carpeta 'input'")
            print("   Coloca un archivo PDF en la carpeta 'input' o especifica la ruta:")
            import sys
            if sys.platform == 'win32':
                print("   py audiobook_pipeline.py ruta\\al\\archivo.pdf")
            else:
                print("   python audiobook_pipeline.py ruta/al/archivo.pdf")
            return
        
        if len(pdf_files) > 1:
            print("⚠️  Se encontraron multiples PDFs en 'input'. Usando el primero.")
        
        pdf_path = str(pdf_files[0])
        print(f"📄 Usando PDF: {pdf_files[0].name}")
    
    # Usar carpeta output por defecto
    if output == 'output':
        output_dir = Path('output')
        output_dir.mkdir(exist_ok=True)
        output = str(output_dir)
    
    try:
        asyncio.run(process_audiobook(pdf_path, output, tts))
    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso cancelado por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise


if __name__ == "__main__":
    main()

