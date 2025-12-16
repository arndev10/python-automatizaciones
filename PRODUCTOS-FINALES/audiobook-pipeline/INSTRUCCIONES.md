# Instrucciones de Uso Local

## Opcion 1: Servidor Web Local (Recomendado)

Este metodo te permite probar los audiolibros en tu navegador con un reproductor simple.

### Pasos:

**OPCION A: Usar script batch (Mas facil en Windows)**

Haz doble clic en uno de estos archivos:
- `start_server_py.bat` (recomendado - usa 'py')
- `start_server_direct.bat` (usa ruta completa de Python)
- `test_server_py.bat` (servidor de prueba simple)

**OPCION B: Desde terminal**

1. **Inicia el servidor web:**
```powershell
# Usa 'py' en lugar de 'python' (funciona mejor en Windows)
py run_local.py

# O si 'py' no funciona, usa la ruta completa:
"C:\Users\Ar\AppData\Local\Programs\Python\Python313\python.exe" run_local.py
```

2. **El navegador se abrira automaticamente** en `http://localhost:8000`

3. **Coloca un PDF en la carpeta `input/`**

4. **En otra terminal, ejecuta el pipeline:**
```bash
python audiobook_pipeline.py
```

5. **Los archivos MP3 apareceran automaticamente** en el navegador cuando se generen

### Ventajas:
- Interfaz visual para escuchar los audiolibros
- Actualizacion automatica cuando se generan nuevos archivos
- Facil de usar

---

## Opcion 2: Uso Directo desde Terminal

### Pasos:

1. **Coloca tu PDF en la carpeta `input/`:**
```bash
# Windows PowerShell
Copy-Item "ruta\a\tu\archivo.pdf" input\

# Linux/Mac
cp ruta/a/tu/archivo.pdf input/
```

2. **Ejecuta el pipeline:**
```powershell
# Usa 'py' en lugar de 'python'
py audiobook_pipeline.py

# O ruta completa:
"C:\Users\Ar\AppData\Local\Programs\Python\Python313\python.exe" audiobook_pipeline.py
```

3. **Los archivos MP3 estaran en la carpeta `output/`**

4. **Reproduce los archivos** con tu reproductor favorito:
   - Windows: Reproductor de Windows Media
   - Mac: iTunes/Music
   - Linux: VLC, Audacious, etc.

---

## Opcion 3: Con Ruta Especifica

Si prefieres especificar la ruta del PDF directamente:

```powershell
# Usa 'py' en lugar de 'python'
py audiobook_pipeline.py "ruta/completa/al/archivo.pdf"
```

---

## Recomendaciones para Probar

1. **Empieza con un PDF pequeno** (menos de 50 paginas) para probar rapidamente
2. **Asegurate de tener conexion a internet** (edge-tts la necesita)
3. **Verifica que FFmpeg este instalado** antes de ejecutar
4. **Revisa la carpeta `output/`** para ver los archivos generados

## Solucion de Problemas

### El servidor no inicia
- Verifica que el puerto 8000 no este en uso
- Cambia el puerto en `run_local.py` si es necesario

### Los archivos no aparecen en el navegador
- Espera unos segundos (el navegador actualiza cada 5 segundos)
- Recarga la pagina manualmente (F5)
- Verifica que los archivos esten en `output/`

### Error al generar audio
- Verifica tu conexion a internet
- Asegurate de tener FFmpeg instalado
- Revisa los mensajes de error en la terminal

