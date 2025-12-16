"""Script para ejecutar el pipeline localmente con servidor web simple."""
import http.server
import socketserver
import webbrowser
import os
from pathlib import Path
import subprocess
import sys

PORT = 8000
OUTPUT_DIR = Path("output")


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Handler personalizado para servir archivos MP3."""
    
    def end_headers(self):
        # Agregar headers CORS para permitir acceso desde cualquier origen
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()
    
    def do_GET(self):
        # Si es la raiz, servir el HTML
        if self.path == '/' or self.path == '/index.html':
            self.path = '/index.html'
        return super().do_GET()


def create_index_html():
    """Crea un archivo HTML simple para probar los audiolibros."""
    html_content = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reproductor de Audiolibros</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
        }
        .audio-list {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .audio-item {
            margin: 20px 0;
            padding: 15px;
            background: #f9f9f9;
            border-radius: 5px;
        }
        .audio-item h3 {
            margin-top: 0;
            color: #555;
        }
        audio {
            width: 100%;
            margin-top: 10px;
        }
        .no-files {
            text-align: center;
            color: #999;
            padding: 40px;
        }
    </style>
</head>
<body>
    <h1>Reproductor de Audiolibros</h1>
    <div class="audio-list">
        <div id="audio-container">
            <div class="no-files">Cargando archivos...</div>
        </div>
    </div>
    
    <script>
        async function loadAudioFiles() {
            const container = document.getElementById('audio-container');
            
            try {
                const response = await fetch('/output/');
                const text = await response.text();
                
                // Parsear HTML para encontrar enlaces a MP3
                const parser = new DOMParser();
                const doc = parser.parseFromString(text, 'text/html');
                const links = doc.querySelectorAll('a[href$=".mp3"]');
                
                if (links.length === 0) {
                    container.innerHTML = '<div class="no-files">No hay archivos MP3 en la carpeta output. Ejecuta el pipeline primero.</div>';
                    return;
                }
                
                let html = '';
                links.forEach(link => {
                    const filename = link.textContent.trim();
                    const url = link.getAttribute('href');
                    html += `
                        <div class="audio-item">
                            <h3>${filename}</h3>
                            <audio controls>
                                <source src="${url}" type="audio/mpeg">
                                Tu navegador no soporta audio HTML5.
                            </audio>
                        </div>
                    `;
                });
                
                container.innerHTML = html;
            } catch (error) {
                container.innerHTML = '<div class="no-files">Error al cargar archivos. Asegurate de que el servidor este corriendo.</div>';
            }
        }
        
        // Cargar archivos al iniciar
        loadAudioFiles();
        
        // Recargar cada 5 segundos para detectar nuevos archivos
        setInterval(loadAudioFiles, 5000);
    </script>
</body>
</html>"""
    
    index_path = Path("index.html")
    index_path.write_text(html_content, encoding='utf-8')
    return index_path


def main():
    """Inicia el servidor web local."""
    # Crear carpeta output si no existe
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Crear archivo HTML
    index_path = create_index_html()
    print(f"✅ Archivo HTML creado: {index_path.absolute()}")
    
    # Cambiar al directorio del script
    os.chdir(Path(__file__).parent)
    
    # Iniciar servidor
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        url = f"http://localhost:{PORT}/index.html"
        print(f"\n🚀 Servidor iniciado en: {url}")
        print(f"📁 Sirviendo archivos desde: {Path.cwd()}")
        print(f"📂 Archivos MP3 en: {OUTPUT_DIR.absolute()}")
        print("\n💡 Instrucciones:")
        print("   1. Coloca un PDF en la carpeta 'input/'")
        print("   2. Ejecuta: python audiobook_pipeline.py")
        print("   3. Los MP3 apareceran automaticamente en el navegador")
        print("\n⏹️  Presiona Ctrl+C para detener el servidor\n")
        
        # Abrir navegador automaticamente
        try:
            webbrowser.open(url)
        except:
            print(f"⚠️  No se pudo abrir el navegador automaticamente.")
            print(f"   Abre manualmente: {url}")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛑 Servidor detenido")
            if index_path.exists():
                index_path.unlink()
                print("✅ Archivo temporal eliminado")


if __name__ == "__main__":
    main()

