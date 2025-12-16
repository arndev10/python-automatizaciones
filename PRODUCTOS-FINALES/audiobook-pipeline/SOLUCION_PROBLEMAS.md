# Solucion de Problemas - Servidor Local

## El localhost no se abre

### Solucion 1: Ejecutar script de prueba simple

Ejecuta el script de prueba que es mas simple:

```bash
python test_server.py
```

Este script es mas basico y deberia funcionar siempre.

### Solucion 2: Verificar que el puerto no este ocupado

Si el puerto 8000 esta ocupado, el script intentara usar otro puerto (8001, 8002, etc.).

**Verificar puerto ocupado en Windows:**
```powershell
netstat -ano | findstr :8000
```

**Cerrar proceso que usa el puerto:**
```powershell
taskkill /PID <numero_pid> /F
```

### Solucion 3: Abrir manualmente en el navegador

Si el navegador no se abre automaticamente:

1. El script mostrara la URL, por ejemplo: `http://localhost:8000/`
2. Abre tu navegador (Chrome, Firefox, Edge)
3. Pega la URL en la barra de direcciones
4. Presiona Enter

### Solucion 4: Usar IP local en lugar de localhost

Si `localhost` no funciona, intenta con:

- `http://127.0.0.1:8000/`
- `http://0.0.0.0:8000/`

### Solucion 5: Verificar firewall de Windows

El firewall de Windows puede estar bloqueando el servidor:

1. Abre "Firewall de Windows Defender"
2. Busca "Permitir una aplicacion a traves del firewall"
3. Agrega Python o permite conexiones entrantes en el puerto 8000

### Solucion 6: Ejecutar como administrador

A veces se necesitan permisos de administrador:

1. Cierra la terminal actual
2. Abre PowerShell como administrador (clic derecho > Ejecutar como administrador)
3. Navega a la carpeta del proyecto
4. Ejecuta: `python run_local.py`

### Solucion 7: Verificar que Python este instalado

Verifica que Python este instalado y en el PATH:

```powershell
python --version
```

Si no funciona, prueba:

```powershell
py --version
```

### Solucion 8: Usar script batch en Windows

Usa el archivo `start_server.bat`:

1. Haz doble clic en `start_server.bat`
2. Esto deberia iniciar el servidor automaticamente

## El navegador se abre pero muestra error

### Error 404 - No se encuentra la pagina

- Verifica que estas en la URL correcta: `http://localhost:8000/index.html`
- Asegurate de que el archivo `index.html` se haya creado en la carpeta del proyecto

### Error de conexion rechazada

- El servidor no esta corriendo
- Verifica que no haya errores en la terminal
- Intenta reiniciar el servidor

### Los archivos MP3 no aparecen

- Verifica que hayas ejecutado el pipeline primero: `python audiobook_pipeline.py`
- Verifica que los archivos esten en la carpeta `output/`
- Espera unos segundos (el navegador actualiza cada 5 segundos)

## Comandos utiles

### Verificar que el servidor esta corriendo

Abre otra terminal y ejecuta:

```powershell
curl http://localhost:8000
```

O abre el navegador y ve a: `http://localhost:8000`

### Detener el servidor

Presiona `Ctrl+C` en la terminal donde esta corriendo el servidor

### Ver logs del servidor

El servidor muestra informacion en la terminal. Si no ves nada, puede que haya un error.

## Contacto

Si ninguno de estos metodos funciona, verifica:
1. Que Python este correctamente instalado
2. Que no haya otros programas usando el puerto 8000
3. Que el firewall no este bloqueando la conexion
4. Los mensajes de error en la terminal

