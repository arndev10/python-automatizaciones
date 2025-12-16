# Comandos Rapidos - Windows

## Problema: "python" no se encuentra

En Windows, a veces `python` no funciona pero `py` si. Usa estos comandos:

## Servidor Web

### Opcion 1: Script Batch (Mas Facil)
Haz doble clic en:
- `start_server_py.bat` ⭐ (Recomendado)
- `test_server_py.bat` (Servidor simple de prueba)

### Opcion 2: Desde Terminal
```powershell
cd "D:\VCODE\TEST 1\PRODUCTOS-FINALES\audiobook-pipeline"
py run_local.py
```

O con ruta completa:
```powershell
"C:\Users\Ar\AppData\Local\Programs\Python\Python313\python.exe" run_local.py
```

## Generar Audiolibro

### Con PDF en carpeta input/
```powershell
cd "D:\VCODE\TEST 1\PRODUCTOS-FINALES\audiobook-pipeline"
py audiobook_pipeline.py
```

### Con ruta especifica
```powershell
py audiobook_pipeline.py "ruta\al\archivo.pdf"
```

## Resumen de Comandos

| Accion | Comando |
|--------|---------|
| Iniciar servidor | `py run_local.py` |
| Servidor de prueba | `py test_server.py` |
| Generar audiolibro | `py audiobook_pipeline.py` |
| Ver version Python | `py --version` |

## Nota Importante

- **Usa `py` en lugar de `python`** en Windows PowerShell
- Si `py` no funciona, usa la ruta completa de Python
- Los scripts `.bat` funcionan haciendo doble clic

