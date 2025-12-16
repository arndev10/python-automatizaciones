"""Script principal del pipeline de generación de audiolibros."""
import asyncio
import click
from pathlib import Path
from tqdm import tqdm

from pdf_extractor import extract_and_clean_pdf
from chapter_detector import segment_text
from narrative_adapter import adapt_for_audiobook
from audio_generator import generate_chapter_audio


async def process_audiobook(pdf_path: str, output_dir: str = "output"):
    """Procesa un PDF completo y genera audiolibro."""
    pdf_path_obj = Path(pdf_path)
    output_path_obj = Path(output_dir)
    output_path_obj.mkdir(parents=True, exist_ok=True)
    
    if not pdf_path_obj.exists():
        raise FileNotFoundError(f"El archivo PDF no existe: {pdf_path}")
    
    print(f"📖 Extrayendo texto de: {pdf_path_obj.name}")
    text = extract_and_clean_pdf(str(pdf_path_obj))
    
    if not text.strip():
        raise ValueError("No se pudo extraer texto del PDF. Verifica que el PDF contenga texto.")
    
    print(f"✅ Texto extraído: {len(text)} caracteres")
    
    print("\n📚 Detectando y segmentando capítulos...")
    chapters = segment_text(text, min_audio_minutes=20, max_audio_minutes=60)
    
    if not chapters:
        raise ValueError("No se pudieron detectar o crear capítulos.")
    
    print(f"✅ {len(chapters)} capítulo(s) detectado(s)")
    for i, chapter in enumerate(chapters, 1):
        word_count = len(chapter.content.split())
        estimated_minutes = word_count / 173  # palabras por minuto a 1.15x
        print(f"   {i}. {chapter.title} (~{estimated_minutes:.1f} min, {word_count} palabras)")
    
    print("\n✍️  Adaptando texto para audiolibro...")
    adapted_chapters = []
    for chapter in tqdm(chapters, desc="Adaptando capítulos"):
        adapted_content = adapt_for_audiobook(chapter.content, apply_summary=True)
        adapted_chapters.append((chapter.title, adapted_content))
    
    print("\n🎙️  Generando archivos de audio...")
    generated_files = []
    
    for i, (title, content) in enumerate(tqdm(adapted_chapters, desc="Generando audio"), 1):
        try:
            output_file = await generate_chapter_audio(
                title, content, output_path_obj, i
            )
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
@click.argument('pdf_path', type=click.Path(exists=True))
@click.option('--output', '-o', default='output', help='Carpeta de salida para los MP3')
def main(pdf_path: str, output: str):
    """Genera audiolibro desde un PDF."""
    try:
        asyncio.run(process_audiobook(pdf_path, output))
    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso cancelado por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise


if __name__ == "__main__":
    main()

