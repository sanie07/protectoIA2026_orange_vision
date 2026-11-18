# Datos

Las imágenes **no están en el repositorio** (pesan varios GB y la licencia de Mendeley es no comercial).
Los notebooks las descargan solos en Colab. Aquí se guarda lo necesario para reproducir exactamente la
misma división train / val / test.

| Archivo | Dataset | Contenido |
|---|---|---|
| `division_v4_N1500.csv` | Mendeley *Oranges in the field* | 1502 fotos usadas en v4: `archivo`, `id` de árbol, `entorno` y `split` (train 1050 · val 152 · test 300). Las fotos del mismo árbol quedan en el mismo split. |
| `division_v4_1_deepfruits.csv` | Roboflow *deepFruits orange* v2 | 66 fotos: `archivo` y `split` oficial (train 52 · val 7 · test 7). |

## Fuentes

- **Mendeley — Oranges in the field.** Lucas et al., Mendeley Data. https://doi.org/10.17632/93f32zgkxz.1 — licencia CC BY-NC 3.0.
  5025 fotos de naranjos con cajas en formato YOLO, clase única `orange`. Entornos: AC, AS, AR, EC, ES, IN, MC, MS, NI.
- **deepFruits orange.** Roboflow Universe, `inkyu-sa-e0c78/deepfruits-orange`, versión 2 — licencia CC BY 4.0.
  https://universe.roboflow.com/inkyu-sa-e0c78/deepfruits-orange
  Fotos de DeepFruits (Sa et al., 2016, *Sensors* 16(8):1222) publicadas con deepNIR (Sa et al., 2022, *Sensors* 22(13):4721).
  Para descargarlo, `OrangeAI_v4.1.0.ipynb` pide una API key de Roboflow (secreto de Colab `ROBOFLOW_API_KEY`).
