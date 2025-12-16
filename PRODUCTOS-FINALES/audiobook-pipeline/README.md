# Pipeline de Generacion de Audiolibros

Transforma PDFs en audiolibros profesionales segmentados por capitulos usando Python y tecnologias de sintesis de voz.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Descripcion

Este proyecto automatiza la conversion de documentos PDF a audiolibros de alta calidad, incluyendo:
- Extraccion inteligente de texto
- Deteccion automatica de capitulos
- Adaptacion narrativa del contenido
- Generacion de audio con voces naturales
- Optimizacion y compresion de archivos de audio

## Caracteristicas

- Extraccion automatica de texto desde PDFs
- Deteccion inteligente de capitulos (con fallback automatico)
- Segmentacion automatica (capitulos largos se dividen en partes)
- Resumen moderado para optimizar contenido (15% de reduccion)
- Conversion a audio con voces naturales (edge-tts)
- Compresion de audio optimizada (96 kbps)
- Velocidad de lectura ajustable (1.15x)
- Eliminacion automatica de referencias visuales
- Conversion de listas a prosa narrativa
- Mantiene tildes y acentos en el audio generado

## Instalacion

### Requisitos Previos

1. **Python 3.11 o superior**
   - Descarga desde: https://www.python.org/downloads/

2. **FFmpeg** (requerido para pydub)
   - **Windows**: 
     - Opcion 1: `winget install ffmpeg`
     - Opcion 2: Descarga desde https://ffmpeg.org/download.html
     - Asegurate de agregar FFmpeg al PATH
   - **Linux**: `sudo apt install ffmpeg` (Ubuntu/Debian)
   - **macOS**: `brew install ffmpeg`

### Instalacion del Proyecto

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

### Estructura de Carpetas

El proyecto usa dos carpetas principales:
- **`input/`**: Coloca aqui los archivos PDF que quieres convertir
- **`output/`**: Aqui se guardan los archivos MP3 generados

### Uso Basico (con carpeta input)

1. Coloca tu archivo PDF en la carpeta `input/`
2. Ejecuta el script sin especificar ruta:
```bash
python audiobook_pipeline.py
```

Los archivos MP3 se guardaran automaticamente en la carpeta `output/`.

### Uso con Ruta Especifica

```bash
python audiobook_pipeline.py ruta/al/archivo.pdf
```

### Especificar Carpeta de Salida

```bash
python audiobook_pipeline.py ruta/al/archivo.pdf --output mi_carpeta
```

### Ejemplo Completo

```bash
python audiobook_pipeline.py "C:\Libros\Mi Libro.pdf" --output "C:\Audiolibros\Mi Libro"
```

## Configuracion

### Parametros Actuales

- **Duracion por MP3**: 20 minutos - 1 hora
- **Velocidad**: 1.15x (ligeramente rapida)
- **Voz**: Femenina en espanol (seleccion automatica)
- **Bitrate**: 96 kbps (balance calidad/tamano)
- **Reduccion de contenido**: 15% (resumen moderado)

### Personalizacion

Para cambiar estos valores, edita los archivos correspondientes:
- `chapter_detector.py`: Duracion de capitulos
- `audio_generator.py`: Velocidad, bitrate, voz
- `narrative_adapter.py`: Porcentaje de resumen

## Estructura de Salida

```
output/
├── 01 - Introduccion.mp3
├── 02 - Capitulo 1 - Parte 1.mp3
├── 02 - Capitulo 1 - Parte 2.mp3
├── 03 - Capitulo 2.mp3
└── ...
```

Los archivos se nombran con:
- Numero de capitulo (con ceros a la izquierda)
- Titulo del capitulo
- Si un capitulo es muy largo, se agrega "Parte X"

## Proceso del Pipeline

1. **Extraccion**: Lee el PDF y extrae todo el texto
2. **Limpieza**: Elimina artefactos, normaliza formato (mantiene tildes)
3. **Deteccion de Capitulos**: Busca titulos de capitulos o crea segmentacion automatica
4. **Segmentacion**: Divide capitulos largos en partes de 20-60 min
5. **Adaptacion Narrativa**: 
   - Elimina referencias visuales
   - Convierte listas a prosa
   - Aplica resumen moderado (15%)
6. **Generacion de Audio**: Convierte cada capitulo a MP3 (con tildes preservadas)
7. **Compresion**: Optimiza tamano de archivos

## Solucion de Problemas

### Error: "No se encontro voz en espanol"
- Verifica tu conexion a internet (edge-tts necesita conexion)
- El problema puede ser temporal, intenta de nuevo

### Error: "FFmpeg no encontrado"
- Asegurate de tener FFmpeg instalado y en el PATH
- Reinicia la terminal despues de instalar FFmpeg

### Error: "No se pudo extraer texto del PDF"
- El PDF puede estar escaneado (solo imagenes)
- Necesitarias OCR primero (no incluido en este pipeline)

### Los capitulos no se detectan correctamente
- El pipeline tiene fallback automatico
- Si los capitulos no estan claramente marcados, creara segmentacion automatica
- Puedes ajustar los patrones en `chapter_detector.py`

## Notas Importantes

- **Conexion a Internet**: edge-tts requiere conexion para generar audio
- **Tiempo de Procesamiento**: Depende del tamano del PDF (1-2 min por capitulo)
- **Calidad de Voz**: edge-tts usa voces de Microsoft Edge (alta calidad)
- **Tamano de Archivos**: ~1-2 MB por cada 10 minutos de audio (a 96 kbps)
- **Tildes y Acentos**: Se mantienen en el audio generado para pronunciacion correcta

## Estructura del Proyecto

```
.
├── audiobook_pipeline.py    # Script principal del pipeline
├── pdf_extractor.py         # Extraccion y limpieza de texto PDF
├── chapter_detector.py      # Deteccion y segmentacion de capitulos
├── narrative_adapter.py    # Adaptacion narrativa del texto
├── audio_generator.py      # Generacion de audio con edge-tts
├── requirements.txt        # Dependencias del proyecto
├── input/                  # Carpeta para archivos PDF de entrada
├── output/                 # Carpeta para archivos MP3 generados
└── README.md              # Este archivo
```

## Tecnologias Utilizadas

- **pdfplumber**: Extraccion de texto de PDFs
- **edge-tts**: Sintesis de voz de Microsoft Edge
- **pydub**: Procesamiento y compresion de audio
- **sumy**: Resumen automatico de texto
- **nltk**: Procesamiento de lenguaje natural
- **click**: Interfaz de linea de comandos

## Licencia

Este proyecto es parte de la coleccion de automatizaciones Python de [arndev10](https://github.com/arndev10/python-automatizaciones).

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request si tienes sugerencias o mejoras.

## Contacto

Para mas informacion sobre este proyecto y otros, visita: [python-automatizaciones](https://github.com/arndev10/python-automatizaciones)

## Proximas Mejoras

- Integracion con APIs de LLM para mejor adaptacion narrativa
- Soporte para multiples idiomas
- Interfaz grafica (GUI)
- Procesamiento por lotes (multiples PDFs)
- Previsualizacion de audio antes de generar todo
