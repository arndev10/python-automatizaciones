"""Script simple para probar si el servidor funciona."""
import http.server
import socketserver
import webbrowser
from pathlib import Path
import os

PORT = 8000

def find_available_port(start_port=8000, max_attempts=10):
    """Encuentra un puerto disponible."""
    import socket
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    return None

def main():
    """Inicia un servidor web simple."""
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Buscar puerto disponible
    port = find_available_port(PORT)
    if port is None:
        print("❌ No se pudo encontrar un puerto disponible")
        input("Presiona Enter para salir...")
        return
    
    if port != PORT:
        print(f"⚠️  Puerto {PORT} ocupado, usando puerto {port}")
    
    # Crear HTML simple
    html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Servidor de Audiolibros</title>
    <style>
        body { font-family: Arial; padding: 20px; background: #f5f5f5; }
        h1 { color: #333; }
        .info { background: white; padding: 20px; border-radius: 8px; margin: 20px 0; }
        a { color: #0066cc; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>🚀 Servidor de Audiolibros Activo</h1>
    <div class="info">
        <h2>✅ El servidor esta funcionando correctamente</h2>
        <p><strong>Archivos MP3:</strong> <a href="/output/">Ver carpeta output</a></p>
        <p><strong>Instrucciones:</strong></p>
        <ol>
            <li>Coloca un PDF en la carpeta <code>input/</code></li>
            <li>Ejecuta: <code>python audiobook_pipeline.py</code></li>
            <li>Los MP3 apareceran en <a href="/output/">output/</a></li>
        </ol>
    </div>
</body>
</html>"""
    
    index_path = Path("index.html")
    index_path.write_text(html_content, encoding='utf-8')
    
    url = f"http://localhost:{port}/"
    
    print(f"\n{'='*60}")
    print(f"🚀 SERVIDOR INICIADO")
    print(f"{'='*60}")
    print(f"URL: {url}")
    print(f"Directorio: {Path.cwd()}")
    print(f"{'='*60}\n")
    
    # Intentar abrir navegador
    try:
        import time
        time.sleep(1)
        webbrowser.open(url)
        print("✅ Navegador abierto")
    except:
        print(f"⚠️  Abre manualmente: {url}")
    
    print("\n⏹️  Presiona Ctrl+C para detener\n")
    
    # Iniciar servidor
    try:
        with socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido")
        if index_path.exists():
            index_path.unlink()

if __name__ == "__main__":
    main()



