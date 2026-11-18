"""
Servidor local de Orange Vision AI.

- Sirve la página (index.html + _layouts/default.html) en http://localhost:8000
- Abre la cámara, corre un modelo entrenado en v4 (YOLO11n o YOLO11m sobre
  Mendeley, carpeta models/v4/) y transmite el video con las detecciones
  dibujadas en /video_feed.
- Solo detección: cajas + confianza. No estima posición ni tamaño.

Uso:  python serve.py        (variables opcionales: CAMARA=1, UMBRAL=0.4)
"""
import json
import os
import re
import threading
import time
import webbrowser

import cv2
from flask import Flask, Response, jsonify, request, send_file, send_from_directory
from ultralytics import YOLO

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=DIRECTORY, static_url_path='/')

# ---------------------------------------------------------------------------
# Modelo
# ---------------------------------------------------------------------------
MODELOS_DIR = os.path.join(DIRECTORY, 'models', 'v4')
IMGSZ = 640
CAMARA = int(os.environ.get('CAMARA', 0))

# Umbral de confianza inicial de la demo. El umbral de máximo F1 en validación
# (≈0.28–0.35, en modelos.json) está pensado para fotos de campo de Mendeley; con
# la cámara en vivo deja pasar dedos y piel como "naranjas". 0.50 los descarta
# y conserva casi todos los frutos reales. Se puede mover con el deslizador.
UMBRAL_DEMO = float(os.environ.get('UMBRAL', 0.50))

# Modelos entrenados en v4 (Mendeley, N1500, fine-tuning). Métricas de test
# (promedio de 3 semillas) de resultados/v4_N1500/resumen_test.csv y
# tamano_y_velocidad.csv.
MODELOS = {
    'YOLO11n': {'archivo': 'orange_yolo11n.pt',
                'metricas': {'map50': 79.3, 'precision': 83.5, 'recall': 69.9, 'ms_gpu': 10}},
    'YOLO11m': {'archivo': 'orange_yolo11m.pt',
                'metricas': {'map50': 81.8, 'precision': 84.4, 'recall': 73.7, 'ms_gpu': 28}},
}
# YOLO11n por defecto: en CPU corre ~5× más rápido que YOLO11m (≈35 vs ≈170 ms
# por cuadro), así las cajas siguen a la naranja en vez de quedar atrasadas.
MODELO_INICIAL = 'YOLO11n'

try:
    with open(os.path.join(MODELOS_DIR, 'modelos.json'), encoding='utf-8') as f:
        IMGSZ = int(json.load(f).get('imgsz', IMGSZ))
except Exception as e:
    print(f"Aviso: no se pudo leer modelos.json ({e}); se usa imgsz={IMGSZ}")

# Se cargan ambos al inicio para que el cambio desde la página sea instantáneo
modelos = {}
for nombre, m in MODELOS.items():
    ruta = os.path.join(MODELOS_DIR, m['archivo'])
    try:
        modelos[nombre] = YOLO(ruta)
        print(f"Modelo cargado: {nombre} ({ruta})")
    except Exception as e:
        print(f"Error al cargar {nombre}: {e}")
if MODELO_INICIAL not in modelos and modelos:
    MODELO_INICIAL = next(iter(modelos))

# ---------------------------------------------------------------------------
# Estado compartido entre hilos
# ---------------------------------------------------------------------------
lock = threading.Lock()
config = {'modelo': MODELO_INICIAL, 'conf': UMBRAL_DEMO, 'cajas': True, 'etiquetas': True}
ultimo_frame = None          # último cuadro de la cámara (BGR)
detecciones = []             # [(x1, y1, x2, y2, conf), ...] del último cuadro analizado
estado = {'naranjas': 0, 'confianza': 0.0, 'fps': 0.0, 'ms': 0.0, 'camara': False}

COLOR = (0, 140, 255)  # naranja en BGR


def hilo_camara():
    """Lee la cámara continuamente y guarda el último cuadro."""
    global ultimo_frame
    cap = cv2.VideoCapture(CAMARA, cv2.CAP_DSHOW) if os.name == 'nt' else cv2.VideoCapture(CAMARA)
    if not cap.isOpened():
        cap = cv2.VideoCapture(CAMARA)
    while True:
        ok, frame = cap.read()
        if not ok:
            estado['camara'] = False
            time.sleep(0.5)
            continue
        estado['camara'] = True
        with lock:
            ultimo_frame = frame


def hilo_modelo():
    """Corre el modelo sobre el cuadro más reciente, tan rápido como puede."""
    global detecciones
    while True:
        with lock:
            frame = None if ultimo_frame is None else ultimo_frame.copy()
            conf = config['conf']
            nombre = config['modelo']
        modelo = modelos.get(nombre)
        if frame is None or modelo is None:
            time.sleep(0.1)
            continue
        t0 = time.perf_counter()
        r = modelo(frame, conf=conf, imgsz=IMGSZ, verbose=False)[0]
        dt = time.perf_counter() - t0
        cajas = [(*map(int, b.xyxy[0].tolist()), float(b.conf[0])) for b in r.boxes]
        with lock:
            if config['modelo'] != nombre:  # se cambió de modelo mientras inferíamos
                continue
            detecciones = cajas
        estado['naranjas'] = len(cajas)
        estado['confianza'] = round(100 * sum(c[4] for c in cajas) / len(cajas), 1) if cajas else 0.0
        estado['ms'] = round(dt * 1000)
        estado['fps'] = round(1 / dt, 1) if dt > 0 else 0.0


def dibujar(frame, cajas):
    """Dibuja cajas y etiquetas 'naranja 87%' según los interruptores de la página."""
    for x1, y1, x2, y2, conf in cajas:
        if config['cajas']:
            cv2.rectangle(frame, (x1, y1), (x2, y2), COLOR, 2)
        if config['etiquetas']:
            texto = f"naranja {conf * 100:.0f}%"
            (tw, th), _ = cv2.getTextSize(texto, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            y_top = max(0, y1 - th - 8)
            x_izq = max(0, min(x1, frame.shape[1] - tw - 8))  # que la etiqueta no se salga del cuadro
            cv2.rectangle(frame, (x_izq, y_top), (x_izq + tw + 8, y_top + th + 8), COLOR, -1)
            cv2.putText(frame, texto, (x_izq + 4, y_top + th + 3),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    return frame


def gen_frames():
    """Video MJPEG: cuadro actual de la cámara + últimas detecciones."""
    while True:
        with lock:
            frame = None if ultimo_frame is None else ultimo_frame.copy()
            cajas = list(detecciones)
        if frame is None:
            time.sleep(0.1)
            continue
        ok, buffer = cv2.imencode('.jpg', dibujar(frame, cajas), [cv2.IMWRITE_JPEG_QUALITY, 80])
        if ok:
            yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n'
        time.sleep(1 / 30)


# ---------------------------------------------------------------------------
# Página (vista previa local del sitio Jekyll)
# ---------------------------------------------------------------------------
def build_site():
    layout_path = os.path.join(DIRECTORY, '_layouts', 'default.html')
    index_path = os.path.join(DIRECTORY, 'index.html')
    output_path = os.path.join(DIRECTORY, '_preview.html')

    if not os.path.exists(layout_path) or not os.path.exists(index_path):
        return False

    with open(layout_path, 'r', encoding='utf-8') as f:
        layout_content = f.read()

    with open(index_path, 'r', encoding='utf-8') as f:
        page_content = f.read()

    title = "Orange Vision AI - Detección de Naranjas | UNA"
    description = "Prototipo de Inteligencia Artificial para la detección de naranjas reales."

    frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', page_content, re.DOTALL)
    body = page_content
    if frontmatter_match:
        fm_text = frontmatter_match.group(1)
        body = frontmatter_match.group(2)

        t_match = re.search(r'title:\s*["\']?(.*?)["\']?$', fm_text, re.MULTILINE)
        if t_match: title = t_match.group(1)

        d_match = re.search(r'description:\s*["\']?(.*?)["\']?$', fm_text, re.MULTILINE)
        if d_match: description = d_match.group(1)

    merged = layout_content.replace('{{ content }}', body)
    merged = re.sub(r'\{\{\s*page\.title\s*\|\s*default:\s*site\.title\s*\}\}', title, merged)
    merged = re.sub(r'\{\{\s*page\.description\s*\|\s*default:\s*site\.description\s*\}\}', description, merged)
    merged = re.sub(r'\{\{\s*[\'"]/(.*?)[\'"]\s*\|\s*relative_url\s*\}\}', lambda m: m.group(1) if m.group(1) else '#', merged)
    merged = re.sub(r'\{\{\s*[\'"]/(.*?)[\'"]\s*\}\}', lambda m: m.group(1) if m.group(1) else '#', merged)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(merged)
    return True


@app.route('/')
def index():
    build_site()
    return send_file(os.path.join(DIRECTORY, '_preview.html'))


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/api/estado')
def api_estado():
    m = MODELOS[config['modelo']]
    return jsonify({**estado, **config,
                    'modelo_ok': config['modelo'] in modelos,
                    'modelos': list(modelos),
                    'metricas': m['metricas']})


@app.route('/api/config', methods=['POST'])
def api_config():
    global detecciones
    datos = request.get_json(silent=True) or {}
    with lock:
        if datos.get('modelo') in modelos and datos['modelo'] != config['modelo']:
            config['modelo'] = datos['modelo']  # el umbral elegido se mantiene
            detecciones = []
            estado.update(naranjas=0, confianza=0.0, fps=0.0, ms=0.0)
        if 'conf' in datos:
            config['conf'] = min(0.95, max(0.05, float(datos['conf'])))
        for clave in ('cajas', 'etiquetas'):
            if clave in datos:
                config[clave] = bool(datos[clave])
    return jsonify(config)


@app.route('/<path:path>')
def serve_assets(path):
    return send_from_directory(DIRECTORY, path)


if __name__ == '__main__':
    threading.Thread(target=hilo_camara, daemon=True).start()
    threading.Thread(target=hilo_modelo, daemon=True).start()

    url = f"http://localhost:{PORT}"
    print("\n=======================================================")
    print(" Servidor de IA iniciado:")
    print(f" -> {url}")
    print(f" Modelos (v4): {', '.join(modelos)}  |  inicial: {MODELO_INICIAL} (umbral {UMBRAL_DEMO})")
    print("=======================================================\n")
    try:
        webbrowser.open(url)
    except Exception:
        pass
    app.run(host='0.0.0.0', port=PORT, threaded=True)
