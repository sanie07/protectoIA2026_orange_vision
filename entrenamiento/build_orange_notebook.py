import json
from pathlib import Path

notebook_path = Path("orange_vision_1cam.ipynb")

with open(notebook_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

def code_cell(source_lines):
    raw_lines = source_lines.strip().split("\n")
    lines = [l + "\n" for l in raw_lines[:-1]] + ([raw_lines[-1]] if raw_lines else [])
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": lines
    }

def markdown_cell(source_lines):
    raw_lines = source_lines.strip().split("\n")
    lines = [l + "\n" for l in raw_lines[:-1]] + ([raw_lines[-1]] if raw_lines else [])
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": lines
    }

cells = []

# Header / Markdown
cells.append(markdown_cell("""# **Orange Vision: Detección de Naranjas con YOLOv11**
### Flujo integral: Inferencia Pura, Transfer Learning, Fine-Tuning y Detección en Tiempo Real (Webcam)
Este cuaderno implementa el ciclo completo de visión artificial para la detección de naranjas:
1. **Inferencia Pura**: Utilización del modelo base YOLOv11 preentrenado en el dataset COCO (filtrando la clase `orange`).
2. **Dataset "Oranges in the field" (Mendeley Data)**: Descarga y estructuración automática de imágenes de campo con etiquetas YOLO (https://data.mendeley.com/datasets/93f32zgkxz/1).
3. **Transfer Learning**: Congelamiento de las primeras 10 capas (*backbone*) y reentrenamiento de la cabeza detectora con el dataset de naranjas.
4. **Fine-Tuning**: Descongelamiento completo de la red y entrenamiento fino con baja tasa de aprendizaje (*Learning Rate* adaptativo con AdamW).
5. **Comparación y Métricas**: Evaluación sobre el conjunto de test con mAP50, mAP50-95 y Recall comparando el modelo base vs transfer learning vs fine-tuning.
6. **Detección con Foto**: Inferencia sobre imágenes estáticas comparando modelos.
7. **Detección en Tiempo Real con Webcam**: Procesamiento continuo de video con OpenCV, conteo de naranjas y medición de FPS."""))

# Cell 0: Librerías
cells.append(code_cell("""# 1. Librerías Básicas
%pip install -q ultralytics torchmetrics pycocotools opencv-python

import os
import shutil
import time
import json
import random
import urllib.request
import joblib
import numpy as np
import pandas as pd
import torch
import cv2
from pathlib import Path

from ultralytics import YOLO, settings
from ultralytics.data.utils import check_det_dataset

# Métricas de detección
from torchmetrics.detection import MeanAveragePrecision"""))

# Cell 1: Clases objetivo
cells.append(code_cell("""# 2. Configurar clases de interés para Inferencia Pura
# El modelo YOLO preentrenado en COCO incluye la clase 'orange' (ID 49 en COCO).
class_names = ['orange']
print('Clases objetivo iniciales para detección:', class_names)"""))

# Cell 2: Inferencia Pura modelo base
cells.append(code_cell("""# 3. Inferencia pura: YOLO preentrenado en COCO, sin entrenar con nuestros datos
modelo_base = YOLO('yolo11n.pt')

print('Total de clases que conoce YOLO COCO:', len(modelo_base.names))
for nombre in class_names:
    print(f'  {nombre}:', 'sí' if nombre in modelo_base.names.values() else 'NO')"""))

# Cell 3: Función de detección en imagen
cells.append(code_cell("""# 4. Función para realizar predicciones filtrando por 'orange' (naranja)
def detectar_naranjas(modelo, ruta_imagen, conf_min=0.25):
    \"\"\"
    Realiza inferencia sobre una imagen y muestra las detecciones de naranjas.
    \"\"\"
    ruta_p = Path(ruta_imagen)
    if not ruta_p.exists():
        print(f"Error: La imagen '{ruta_imagen}' no existe.")
        return None

    # Inferencia con YOLO
    resultados = modelo.predict(ruta_imagen, conf=conf_min, verbose=False)[0]

    nombre_modelo = getattr(modelo, 'model_name', 'YOLO')
    print(f"\\nResultados para {ruta_p.name} ({nombre_modelo}):")
    encontrado = False
    conteo = 0

    for caja in resultados.boxes:
        nombre_clase = resultados.names[int(caja.cls)]
        # Si el modelo tiene la clase 'orange', o si tiene solo 1 clase entrenada (dataset propio)
        if nombre_clase == 'orange' or len(resultados.names) == 1:
            encontrado = True
            conteo += 1
            conf = round(float(caja.conf), 3)
            coords = [round(x, 1) for x in caja.xyxy[0].tolist()]
            print(f"  [Naranja #{conteo}] Confianza: {conf} | Coordenadas: {coords}")

    if not encontrado:
        print("  No se detectaron naranjas en la imagen con la confianza mínima requerida.")
    else:
        print(f"  Total de naranjas detectadas: {conteo}")

    resultados.show()
    return resultados"""))

# Cell 4: Detección en foto de prueba
cells.append(code_cell("""# 5. Detección con una foto usando el modelo base
ruta_prueba = 'orange_sample.jpg'

# Si no existe una foto local, generamos una imagen sintética de prueba
if not Path(ruta_prueba).exists():
    img_temp = np.zeros((480, 640, 3), dtype=np.uint8)
    img_temp[:] = (34, 110, 34)  # Fondo verdoso simulando follaje
    cv2.circle(img_temp, (240, 240), 75, (0, 140, 255), -1)  # Naranja 1
    cv2.circle(img_temp, (420, 210), 65, (0, 165, 255), -1)  # Naranja 2
    cv2.circle(img_temp, (330, 330), 80, (0, 150, 255), -1)  # Naranja 3
    cv2.imwrite(ruta_prueba, img_temp)
    print(f"Se ha creado una imagen de prueba temporal en: {ruta_prueba}")

detectar_naranjas(modelo_base, ruta_prueba, conf_min=0.25)"""))

# Cell 5: Dataset Mendeley "Oranges in the field"
cells.append(code_cell("""# 6. Cargar datos: Dataset "Oranges in the field" (Mendeley Data)
# Referencia: https://data.mendeley.com/datasets/93f32zgkxz/1
# 5025 imágenes de 640x640 tomadas en campos de Sicilia con etiquetas YOLO (clase xc yc w h).

API_NARANJAS = 'https://data.mendeley.com/public-api/datasets/93f32zgkxz'
CABECERA = {'User-Agent': 'Mozilla/5.0'}
CARPETA_DATASET = Path('dataset_naranjas')
USAR_CARPETA_LOCAL = False  # Cambiar a True si ya tienes el dataset descargado en local

class_names = ['orange']

def descargar_dataset_mendeley(n_imagenes=120, carpeta_destino='dataset_naranjas', 
                               split_train=0.7, split_val=0.2, semilla=42, prefijo=''):
    \"\"\"
    Descarga imágenes y etiquetas YOLO desde Mendeley Data y organiza las carpetas en
    formato estándar de YOLO (images/train, images/val, images/test, labels/...).
    \"\"\"
    destino = Path(carpeta_destino)
    yaml_path = destino / 'data.yaml'

    # Verificar si ya fue descargado previamente
    imgs_descargadas = list(destino.glob('images/**/*.jpg'))
    if len(imgs_descargadas) >= int(n_imagenes * 0.8) and yaml_path.exists():
        print(f"Dataset ya encontrado en '{destino}' con {len(imgs_descargadas)} imágenes.")
        return yaml_path

    print(f"Consultando API de Mendeley Data ({API_NARANJAS})...")
    req = urllib.request.Request(API_NARANJAS, headers=CABECERA)
    with urllib.request.urlopen(req, timeout=45) as r:
        datos = json.loads(r.read().decode('utf-8'))

    archivos = datos['files']
    imagenes = sorted([a for a in archivos if a['filename'].endswith('.jpg') and a['filename'].startswith(prefijo)],
                      key=lambda x: x['filename'])
    etiquetas = {a['filename'][:-4]: a for a in archivos if a['filename'].endswith('.txt')}

    random.Random(semilla).shuffle(imagenes)
    seleccion = imagenes[:n_imagenes]

    n_train = int(len(seleccion) * split_train)
    n_val = int(len(seleccion) * split_val)

    splits = {
        'train': seleccion[:n_train],
        'val': seleccion[n_train:n_train + n_val],
        'test': seleccion[n_train + n_val:]
    }

    print(f"Descargando {len(seleccion)} imágenes de naranjas (Train: {len(splits['train'])}, Val: {len(splits['val'])}, Test: {len(splits['test'])})...")

    for split_name, lista_imgs in splits.items():
        dir_img = destino / 'images' / split_name
        dir_lbl = destino / 'labels' / split_name
        dir_img.mkdir(parents=True, exist_ok=True)
        dir_lbl.mkdir(parents=True, exist_ok=True)

        for item in lista_imgs:
            base = item['filename'][:-4]
            ruta_img = dir_img / item['filename']
            ruta_lbl = dir_lbl / f"{base}.txt"

            # Descargar imagen JPG
            if not ruta_img.exists() or ruta_img.stat().st_size == 0:
                try:
                    req_img = urllib.request.Request(item['content_details']['download_url'], headers=CABECERA)
                    with urllib.request.urlopen(req_img, timeout=45) as r_img:
                        with open(ruta_img, 'wb') as f_img:
                            f_img.write(r_img.read())
                except Exception as e:
                    print(f"Error descargando {item['filename']}: {e}")

            # Descargar etiqueta TXT (formato YOLO)
            if base in etiquetas and (not ruta_lbl.exists() or ruta_lbl.stat().st_size == 0):
                try:
                    req_lbl = urllib.request.Request(etiquetas[base]['content_details']['download_url'], headers=CABECERA)
                    with urllib.request.urlopen(req_lbl, timeout=45) as r_lbl:
                        with open(ruta_lbl, 'wb') as f_lbl:
                            f_lbl.write(r_lbl.read())
                except Exception as e:
                    print(f"Error descargando etiqueta {base}.txt: {e}")

    # Generar data.yaml para Ultralytics YOLO
    with open(yaml_path, 'w', encoding='utf-8') as f:
        f.write(f"path: {destino.resolve().as_posix()}\\n")
        f.write("train: images/train\\n")
        f.write("val: images/val\\n")
        f.write("test: images/test\\n")
        f.write("names:\\n")
        f.write("  0: orange\\n")

    print(f"data.yaml generado en: {yaml_path}")
    return yaml_path

# Preparar y cargar el dataset
if USAR_CARPETA_LOCAL and CARPETA_DATASET.exists():
    yaml_path = CARPETA_DATASET / 'data.yaml'
    DATA = str(yaml_path)
else:
    # Puedes ajustar n_imagenes (ej. 100 para prueba rápida o más para entrenamiento intensivo)
    yaml_path = descargar_dataset_mendeley(n_imagenes=120, carpeta_destino='dataset_naranjas', semilla=42)
    DATA = str(yaml_path)

info = check_det_dataset(DATA)
TEST = info.get('test', info.get('val'))
print('Dataset listo:', DATA)
print('Clases:', class_names)
print('Imágenes de test:', len(list(Path(TEST).glob('*.jpg'))) if Path(TEST).exists() else 'N/A')"""))

# Cell 6: Configuración de Tensorboard
cells.append(code_cell("""# 7. Configurar TensorBoard para monitoreo del entrenamiento
%load_ext tensorboard

settings.update({'tensorboard': True})

# Limpiar ejecuciones previas de transfer y fine-tuning si se desea reiniciar
shutil.rmtree('runs/detect/transfer_orange', ignore_errors=True)
shutil.rmtree('runs/detect/finetune_orange', ignore_errors=True)"""))

# Cell 7: Transfer Learning
cells.append(code_cell("""# 8. Transfer Learning: Modelo preentrenado con las primeras 10 capas congeladas
# Solo se entrenan las capas finales (head), adaptándolas al dataset de naranjas de Mendeley.
modelo_transfer = YOLO('yolo11n.pt')

modelo_transfer.train(
    data=DATA,
    epochs=10,
    freeze=10,
    patience=5,
    imgsz=640,
    name='transfer_orange'
)"""))

# Cell 8: Fine-Tuning
cells.append(code_cell("""# 9. Fine-Tuning: Partir del modelo de transfer, descongelar todas las capas y reentrenar con LR bajo
# Se reentrena la red completa con un optimizador adaptativo y learning rate pequeño (lr0=1e-4)
# para refinar las características de bajo y alto nivel sin olvidar lo aprendido.
modelo_ft = YOLO(modelo_transfer.trainer.best)

modelo_ft.train(
    data=DATA,
    epochs=10,
    optimizer='AdamW',
    lr0=1e-4,
    warmup_epochs=0,
    freeze=0,
    patience=5,
    imgsz=640,
    name='finetune_orange'
)"""))

# Cell 9: Visualización de Tensorboard
cells.append(code_cell("""# 10. Visualizar y contrastar las curvas de pérdida y métricas en TensorBoard
%tensorboard --logdir runs"""))

# Cell 10: Evaluación y Comparación Cuantitativa
cells.append(code_cell("""# 11. Evaluar y comparar los tres modelos sobre el set de test de Mendeley
# Comparamos Inferencia pura (COCO), Transfer Learning y Fine-Tuning sobre las mismas fotos de campo.

def evaluar(modelo):
    mapa = {i: class_names.index(n) for i, n in modelo.names.items() if n in class_names}
    metrica = MeanAveragePrecision(class_metrics=True)

    if not TEST or not Path(TEST).exists():
        return {'mAP50': 0.0, 'mAP50-95': 0.0, 'Recall': 0.0}

    for r in modelo.predict(TEST, conf=0.001, max_det=100, stream=True, verbose=False):
        cls = r.boxes.cls.int().tolist()
        ok = [k for k, c in enumerate(cls) if c in mapa]
        pred = {
            'boxes': r.boxes.xyxy[ok].cpu(),
            'scores': r.boxes.conf[ok].cpu(),
            'labels': torch.tensor([mapa[cls[k]] for k in ok], dtype=torch.long)
        }

        h, w = r.orig_shape
        # Reemplazar path a formato label
        txt_path = Path(r.path.replace('/images/', '/labels/').replace('\\\\images\\\\', '\\\\labels\\\\')).with_suffix('.txt')
        e = np.loadtxt(txt_path, ndmin=2) if txt_path.exists() and txt_path.read_text().strip() else np.zeros((0, 5))
        xyxy = np.c_[e[:, 1] - e[:, 3] / 2, e[:, 2] - e[:, 4] / 2,
                     e[:, 1] + e[:, 3] / 2, e[:, 2] + e[:, 4] / 2] * [w, h, w, h]
        real = {
            'boxes': torch.tensor(xyxy, dtype=torch.float32),
            'labels': torch.tensor(e[:, 0], dtype=torch.long)
        }

        metrica.update([pred], [real])

    m = metrica.compute()
    fila = {
        'mAP50': float(m['map_50']),
        'mAP50-95': float(m['map']),
        'Recall': float(m['mar_100'])
    }
    classes_t = m['classes']
    map_pc_t = m['map_per_class']
    if getattr(classes_t, 'ndim', 0) > 0:
        for c, v in zip(classes_t.tolist(), map_pc_t.tolist()):
            if c < len(class_names):
                fila[f'mAP {class_names[c]}'] = max(float(v), 0.0)
    return fila

# Seleccionar los mejores checkpoints obtenidos
try:
    mejor_transfer = YOLO(modelo_transfer.trainer.best)
except Exception:
    mejor_transfer = modelo_base

try:
    modelo_final = YOLO(modelo_ft.trainer.best)
except Exception:
    modelo_final = mejor_transfer

tabla_comparacion = pd.DataFrame({
    'Inferencia pura (COCO)': evaluar(modelo_base),
    'Transfer Learning (Mendeley)': evaluar(mejor_transfer),
    'Fine-Tuning (Mendeley)': evaluar(modelo_final),
}).T.round(3)

print("=== TABLA DE COMPARACIÓN DE DESEMPEÑO ===")
tabla_comparacion"""))

# Cell 11: Comparación con foto
cells.append(code_cell("""# 12. Comparar visualmente la detección en una foto de prueba
# Comparación directa entre Inferencia Pura y el Modelo Final ajustado
foto_evaluacion = ruta_prueba

modelos_comparar = [
    ('Modelo Base (Inferencia Pura COCO)', modelo_base),
    ('Modelo Final (Fine-Tuning Mendeley)', modelo_final)
]

for nombre, mod in modelos_comparar:
    print(f"\\n==================== {nombre} ====================")
    detectar_naranjas(mod, foto_evaluacion, conf_min=0.25)"""))

# Cell 12: Guardar modelo final
cells.append(code_cell("""# 13. Guardar el modelo final y sus metadatos
archivo_modelo = 'orange_detector_best.pt'
modelo_final.save(archivo_modelo)

# Guardar clases y configuraciones adicionales
joblib.dump({
    'class_names': class_names,
    'source_base': 'yolo11n.pt',
    'dataset': 'Mendeley Data - Oranges in the field'
}, 'orange_detector_extras.joblib')

print(f"Modelo final guardado en: {archivo_modelo}")
print("Metadatos guardados en: orange_detector_extras.joblib")"""))

# Cell 13: Detección en tiempo real con Webcam (OpenCV local)
cells.append(code_cell("""# 14. Detección en tiempo real usando Webcam (OpenCV)
# Permite detectar naranjas en vivo mediante la cámara conectada a tu computadora.
# Presiona la tecla 'q' o 'ESC' en la ventana de video para salir.

def detectar_en_webcam(modelo, cam_id=0, conf_min=0.3):
    \"\"\"
    Inicia la captura de video en vivo desde la webcam, detecta naranjas en tiempo real,
    dibuja las cajas delimitadoras, el conteo actual y los FPS.
    \"\"\"
    cap = cv2.VideoCapture(cam_id)
    if not cap.isOpened():
        print(f"Error: No se pudo acceder a la webcam con ID {cam_id}.")
        print("Si tienes varias cámaras, intenta cambiando cam_id (ej. 1 o 2).")
        return

    print(f"Cámara #{cam_id} iniciada con éxito.")
    print("Controles: Presiona 'q' o 'ESC' en la ventana de video para salir.")

    prev_time = time.time()

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("No se pudo leer el fotograma de la cámara.")
                break

            # Inferencia con YOLO sobre el fotograma actual
            resultados = modelo.predict(frame, conf=conf_min, verbose=False)[0]

            conteo_naranjas = 0

            # Procesar las cajas detectadas
            for caja in resultados.boxes:
                cls_id = int(caja.cls[0])
                nombre_clase = resultados.names[cls_id]

                # Filtrar naranjas (o clase única del modelo entrenado)
                if nombre_clase == 'orange' or len(resultados.names) == 1:
                    conteo_naranjas += 1
                    confianza = float(caja.conf[0])
                    x1, y1, x2, y2 = map(int, caja.xyxy[0])

                    # Dibujar caja delimitadora naranja
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 165, 255), 2)
                    
                    # Etiqueta con porcentaje de confianza
                    texto = f"Naranja: {confianza * 100:.1f}%"
                    (tw, th), _ = cv2.getTextSize(texto, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                    cv2.rectangle(frame, (x1, max(0, y1 - 25)), (x1 + tw, max(0, y1)), (0, 165, 255), -1)
                    cv2.putText(frame, texto, (x1, max(18, y1 - 6)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            # Cálculo de fotogramas por segundo (FPS)
            curr_time = time.time()
            fps = 1.0 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0.0
            prev_time = curr_time

            # Barra informativa superior
            cv2.rectangle(frame, (0, 0), (320, 75), (0, 0, 0), -1)
            cv2.putText(frame, f"FPS: {fps:.1f}", (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
            cv2.putText(frame, f"Naranjas: {conteo_naranjas}", (15, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 165, 255), 2)

            # Mostrar ventana con el fotograma anotado
            cv2.imshow("Orange Vision - Deteccion en Tiempo Real", frame)

            # Salir con la tecla 'q' o 'ESC' (código 27)
            tecla = cv2.waitKey(1) & 0xFF
            if tecla == ord('q') or tecla == 27:
                print("Detección detenida por el usuario.")
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Recursos de la cámara liberados correctamente.")

# Ejecutar detección con webcam:
# Puedes usar 'modelo_final' o 'modelo_base'
modelo_a_usar = modelo_final if 'modelo_final' in locals() else modelo_base
# Para iniciar la cámara en tu máquina local, descomenta y ejecuta la siguiente línea:
# detectar_en_webcam(modelo_a_usar, cam_id=0, conf_min=0.25)
print("Función detectar_en_webcam cargada. Descomenta la línea anterior para iniciar tu cámara.")"""))

# Cell 14: Webcam alternativa para Colab
cells.append(code_cell("""# 15. [Opcional] Captura de foto con Webcam en Google Colab
# Google Colab se ejecuta en la nube y no tiene acceso directo a ventanas de cv2.imshow().
# Si ejecutas este notebook en Google Colab, esta celda captura una foto usando JavaScript
# directamente desde tu navegador web y realiza la detección de naranjas sobre ella.

from IPython.display import display, Javascript
try:
    from google.colab.output import eval_js
    import base64

    def capturar_foto_colab(filename='colab_webcam_photo.jpg', quality=0.8):
        js = Javascript('''
            async function takePhoto(quality) {
                const div = document.createElement('div');
                const capture = document.createElement('button');
                capture.textContent = 'Tomar Foto para Detección';
                capture.className = 'btn';
                div.appendChild(capture);

                const video = document.createElement('video');
                video.style.display = 'block';
                const stream = await navigator.mediaDevices.getUserMedia({video: true});

                document.body.appendChild(div);
                div.appendChild(video);
                video.srcObject = stream;
                await video.play();

                // Esperar clic en el botón
                await new Promise((resolve) => capture.onclick = resolve);

                const canvas = document.createElement('canvas');
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                canvas.getContext('2d').drawImage(video, 0, 0);
                stream.getVideoTracks()[0].stop();
                div.remove();
                return canvas.toDataURL('image/jpeg', quality);
            }
        ''')
        display(js)
        data = eval_js('takePhoto({})'.format(quality))
        binary = base64.b64decode(data.split(',')[1])
        with open(filename, 'wb') as f:
            f.write(binary)
        print(f"Foto capturada con éxito en: {filename}")
        return filename

    # Ejemplo de uso en Colab:
    # foto_colab = capturar_foto_colab()
    # if foto_colab:
    #     detectar_naranjas(modelo_a_usar, foto_colab, conf_min=0.25)
except ImportError:
    print("Entorno local detectado. Para webcam en local, usa la celda anterior 'detectar_en_webcam'.")"""))

nb["cells"] = cells

with open(notebook_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"Notebook updated successfully with Mendeley Data integration. Total cells: {len(nb['cells'])}")
