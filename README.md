# 📚 Pipeline de Generación de Audiolibros

Transforma PDFs en audiolibros profesionales segmentados por capítulos usando Python y tecnologías de síntesis de voz.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 Descripción

Este proyecto automatiza la conversión de documentos PDF a audiolibros de alta calidad, incluyendo:
- Extracción inteligente de texto
- Detección automática de capítulos
- Adaptación narrativa del contenido
- Generación de audio con voces naturales
- Optimización y compresión de archivos de audio

## Características

- ✅ Extracción automática de texto desde PDFs
- ✅ Detección inteligente de capítulos (con fallback automático)
- ✅ Segmentación automática (capítulos largos se dividen en partes)
- ✅ Resumen moderado para optimizar contenido (15% de reducción)
- ✅ Conversión a audio con voces naturales (edge-tts)
- ✅ Compresión de audio optimizada (96 kbps)
- ✅ Velocidad de lectura ajustable (1.15x)
- ✅ Eliminación automática de referencias visuales
- ✅ Conversión de listas a prosa narrativa

## Instalación

### Requisitos Previos

1. **Python 3.11 o superior**
   - Descarga desde: https://www.python.org/downloads/

2. **FFmpeg** (requerido para pydub)
   - **Windows**: 
     - Opción 1: `winget install ffmpeg`
     - Opción 2: Descarga desde https://ffmpeg.org/download.html
     - Asegúrate de agregar FFmpeg al PATH
   - **Linux**: `sudo apt install ffmpeg` (Ubuntu/Debian)
   - **macOS**: `brew install ffmpeg`

### Instalación del Proyecto

1. Clona o descarga este proyecto
2. Abre una terminal en la carpeta del proyecto
3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Descarga los recursos de NLTK:
```bash
python -m nltk.downloader punkt stopwords
```

## Uso

### Uso Básico

```bash
python audiobook_pipeline.py ruta/al/archivo.pdf
```

Los archivos MP3 se guardarán en la carpeta `output/` por defecto.

### Especificar Carpeta de Salida

```bash
python audiobook_pipeline.py ruta/al/archivo.pdf --output mi_carpeta
```

### Ejemplo Completo

```bash
python audiobook_pipeline.py "C:\Libros\Mi Libro.pdf" --output "C:\Audiolibros\Mi Libro"
```

## Configuración

### Parámetros Actuales

- **Duración por MP3**: 20 minutos - 1 hora
- **Velocidad**: 1.15x (ligeramente rápida)
- **Voz**: Femenina en español (selección automática)
- **Bitrate**: 96 kbps (balance calidad/tamaño)
- **Reducción de contenido**: 15% (resumen moderado)

### Personalización

Para cambiar estos valores, edita los archivos correspondientes:
- `chapter_detector.py`: Duración de capítulos
- `audio_generator.py`: Velocidad, bitrate, voz
- `narrative_adapter.py`: Porcentaje de resumen

## Estructura de Salida

```
output/
├── 01 - Introducción.mp3
├── 02 - Capítulo 1 - Parte 1.mp3
├── 02 - Capítulo 1 - Parte 2.mp3
├── 03 - Capítulo 2.mp3
└── ...
```

Los archivos se nombran con:
- Número de capítulo (con ceros a la izquierda)
- Título del capítulo
- Si un capítulo es muy largo, se agrega "Parte X"

## Proceso del Pipeline

1. **Extracción**: Lee el PDF y extrae todo el texto
2. **Limpieza**: Elimina artefactos, normaliza formato
3. **Detección de Capítulos**: Busca títulos de capítulos o crea segmentación automática
4. **Segmentación**: Divide capítulos largos en partes de 20-60 min
5. **Adaptación Narrativa**: 
   - Elimina referencias visuales
   - Convierte listas a prosa
   - Aplica resumen moderado (15%)
6. **Generación de Audio**: Convierte cada capítulo a MP3
7. **Compresión**: Optimiza tamaño de archivos

## Solución de Problemas

### Error: "No se encontró voz en español"
- Verifica tu conexión a internet (edge-tts necesita conexión)
- El problema puede ser temporal, intenta de nuevo

### Error: "FFmpeg no encontrado"
- Asegúrate de tener FFmpeg instalado y en el PATH
- Reinicia la terminal después de instalar FFmpeg

### Error: "No se pudo extraer texto del PDF"
- El PDF puede estar escaneado (solo imágenes)
- Necesitarías OCR primero (no incluido en este pipeline)

### Los capítulos no se detectan correctamente
- El pipeline tiene fallback automático
- Si los capítulos no están claramente marcados, creará segmentación automática
- Puedes ajustar los patrones en `chapter_detector.py`

## Notas Importantes

- **Conexión a Internet**: edge-tts requiere conexión para generar audio
- **Tiempo de Procesamiento**: Depende del tamaño del PDF (1-2 min por capítulo)
- **Calidad de Voz**: edge-tts usa voces de Microsoft Edge (alta calidad)
- **Tamaño de Archivos**: ~1-2 MB por cada 10 minutos de audio (a 96 kbps)

## 📁 Estructura del Proyecto

```
.
├── audiobook_pipeline.py    # Script principal del pipeline
├── pdf_extractor.py         # Extracción y limpieza de texto PDF
├── chapter_detector.py      # Detección y segmentación de capítulos
├── narrative_adapter.py    # Adaptación narrativa del texto
├── audio_generator.py      # Generación de audio con edge-tts
├── requirements.txt        # Dependencias del proyecto
└── README.md              # Este archivo
```

## 🔧 Tecnologías Utilizadas

- **pdfplumber**: Extracción de texto de PDFs
- **edge-tts**: Síntesis de voz de Microsoft Edge
- **pydub**: Procesamiento y compresión de audio
- **sumy**: Resumen automático de texto
- **nltk**: Procesamiento de lenguaje natural
- **click**: Interfaz de línea de comandos

## 📝 Licencia

Este proyecto es parte de la colección de automatizaciones Python de [arndev10](https://github.com/arndev10/python-automatizaciones).

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request si tienes sugerencias o mejoras.

## 📧 Contacto

Para más información sobre este proyecto y otros, visita: [python-automatizaciones](https://github.com/arndev10/python-automatizaciones)

## 🚀 Próximas Mejoras

- Integración con APIs de LLM para mejor adaptación narrativa
- Soporte para múltiples idiomas
- Interfaz gráfica (GUI)
- Procesamiento por lotes (múltiples PDFs)
- Previsualización de audio antes de generar todo

