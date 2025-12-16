# Guia Rapida para Windows

## Problema Comun: "python" no se encuentra

En Windows PowerShell, el comando `python` a veces no funciona porque apunta al alias de Microsoft Store.

**Solucion: Usa `py` en lugar de `python`**

## Comandos Rapidos

### Iniciar Servidor Web

**Opcion 1: Script Batch (Mas Facil)**
- Haz doble clic en: `start_server_py.bat` o `test_server_py.bat`

**Opcion 2: Desde Terminal**
```powershell
cd "D:\VCODE\TEST 1\PRODUCTOS-FINALES\audiobook-pipeline"
py test_server.py
```

### Generar Audiolibro

**Opcion 1: Script Batch**
- Haz doble clic en: `run_audiobook.bat`
- Coloca tu PDF en la carpeta `input/` antes de ejecutar

**Opcion 2: Desde Terminal**

Con PDF en carpeta input/:
```powershell
py audiobook_pipeline.py
```

Con ruta especifica:
```powershell
py audiobook_pipeline.py "ruta\al\archivo.pdf"
```

## Tabla de Comandos

| Accion | Comando Correcto | Comando Incorrecto |
|--------|------------------|-------------------|
| Iniciar servidor | `py test_server.py` | `python test_server.py` ❌ |
| Generar audiolibro | `py audiobook_pipeline.py` | `python audiobook_pipeline.py` ❌ |
| Ver version | `py --version` | `python --version` ❌ |

## Instalacion de Dependencias

**Primera vez que usas el proyecto:**

1. **Opcion A: Script Batch (Mas Facil)**
   - Haz doble clic en: `install_dependencies.bat`

2. **Opcion B: Desde Terminal**
```powershell
cd "D:\VCODE\TEST 1\PRODUCTOS-FINALES\audiobook-pipeline"
py -m pip install -r requirements.txt
py -m nltk.downloader punkt stopwords
```

## Por Que Usar `py`?

- `py` es el Python Launcher de Windows que funciona correctamente
- `python` puede apuntar al alias de Microsoft Store que no funciona
- `py` detecta automaticamente todas las versiones de Python instaladas

## Scripts Batch Disponibles

1. **start_server_py.bat** - Inicia el servidor web completo
2. **test_server_py.bat** - Servidor de prueba simple
3. **run_audiobook.bat** - Genera audiolibro desde PDF en input/

## Notas Importantes

- Siempre usa `py` en PowerShell de Windows
- Los scripts `.bat` funcionan haciendo doble clic
- El servidor se abre automaticamente en `http://localhost:8000/`

