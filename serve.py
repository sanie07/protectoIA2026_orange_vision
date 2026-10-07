import http.server
import socketserver
import os
import re
import webbrowser
import sys

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

def build_site():
    """Generates the combined HTML file from Jekyll layout and page content for local preview."""
    layout_path = os.path.join(DIRECTORY, '_layouts', 'default.html')
    index_path = os.path.join(DIRECTORY, 'index.html')
    output_path = os.path.join(DIRECTORY, '_preview.html')

    if not os.path.exists(layout_path) or not os.path.exists(index_path):
        print("Error: Missing _layouts/default.html or index.html")
        return False

    with open(layout_path, 'r', encoding='utf-8') as f:
        layout_content = f.read()

    with open(index_path, 'r', encoding='utf-8') as f:
        page_content = f.read()

    # Extract frontmatter
    title = "Orange Vision AI - Detección de Naranjas | UNA"
    description = "Prototipo de Inteligencia Artificial para la detección e identificación de naranjas reales en arbustos sintéticos de prueba."
    
    frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', page_content, re.DOTALL)
    body = page_content
    if frontmatter_match:
        fm_text = frontmatter_match.group(1)
        body = frontmatter_match.group(2)
        
        t_match = re.search(r'title:\s*["\']?(.*?)["\']?$', fm_text, re.MULTILINE)
        if t_match:
            title = t_match.group(1)
            
        d_match = re.search(r'description:\s*["\']?(.*?)["\']?$', fm_text, re.MULTILINE)
        if d_match:
            description = d_match.group(1)

    # Replace liquid tags
    merged = layout_content.replace('{{ content }}', body)
    merged = re.sub(r'\{\{\s*page\.title\s*\|\s*default:\s*site\.title\s*\}\}', title, merged)
    merged = re.sub(r'\{\{\s*page\.description\s*\|\s*default:\s*site\.description\s*\}\}', description, merged)
    merged = re.sub(r'\{\{\s*[\'"]/(.*?)[\'"]\s*\|\s*relative_url\s*\}\}', lambda m: m.group(1) if m.group(1) else '#', merged)
    merged = re.sub(r'\{\{\s*[\'"]/(.*?)[\'"]\s*\}\}', lambda m: m.group(1) if m.group(1) else '#', merged)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(merged)

    print(" Preview generated: _preview.html")
    return True

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.path = '/_preview.html'
        return super().do_GET()

def run_server():
    build_site()
    os.chdir(DIRECTORY)
    
    # Allow address reuse
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        url = f"http://localhost:{PORT}"
        print(f"\n=======================================================")
        print(f" Servidor local de vista previa iniciado exitosamente:")
        print(f" -> {url}")
        print(f" Presiona Ctrl+C en esta terminal para detener el servidor.")
        print(f"=======================================================\n")
        try:
            webbrowser.open(url)
        except Exception:
            pass
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido.")
            sys.exit(0)

if __name__ == '__main__':
    run_server()
