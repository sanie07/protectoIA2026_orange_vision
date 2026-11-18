/**
 * Orange Vision AI - Demostración en vivo
 * Universidad Nacional de Asunción 2026
 *
 * El video con las detecciones lo genera serve.py (/video_feed).
 * Este script solo envía el umbral y los interruptores al servidor
 * y muestra las estadísticas del último cuadro analizado.
 */

document.addEventListener('DOMContentLoaded', () => {
  const feed = document.getElementById('ia-camera-feed');
  if (!feed) return;

  const confidenceSlider = document.getElementById('confidenceSlider');
  const confidenceValue = document.getElementById('confidenceValue');
  const toggleBoxes = document.getElementById('toggleBoxes');
  const toggleLabels = document.getElementById('toggleLabels');
  const countTotalEl = document.getElementById('countTotal');
  const avgConfEl = document.getElementById('avgConf');
  const inferMsEl = document.getElementById('inferMs');
  const modelBtns = document.querySelectorAll('.model-btn');
  const fpsCounterEl = document.getElementById('fpsCounter');
  const msgEl = document.getElementById('viewportMsg');

  let sliderInicializado = false;
  let modeloActual = null;

  function mostrarMensaje(texto) {
    if (!msgEl) return;
    msgEl.textContent = texto || '';
    msgEl.style.display = texto ? 'flex' : 'none';
  }

  function enviarConfig(datos) {
    return fetch('/api/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(datos)
    }).then(r => r.json()).catch(() => null);
  }

  function mostrarUmbral(conf) {
    confidenceSlider.value = conf;
    confidenceValue.textContent = `${Math.round(conf * 100)}%`;
  }

  // Marca el modelo activo y actualiza la sección de métricas
  function mostrarModelo(e) {
    modelBtns.forEach(b => {
      b.classList.toggle('active', b.dataset.modelo === e.modelo);
      b.disabled = !e.modelos.includes(b.dataset.modelo);
    });
    if (e.modelo === modeloActual) return;
    modeloActual = e.modelo;
    const m = e.metricas;
    const set = (id, txt) => { const el = document.getElementById(id); if (el) el.textContent = txt; };
    set('metricsModel', e.modelo);
    set('metricMap50', `${m.map50}%`);
    set('metricPrecision', `${m.precision}%`);
    set('metricRecall', `${m.recall}%`);
    set('metricMs', `${m.ms_gpu} ms`);
  }

  async function actualizarEstado() {
    try {
      const r = await fetch('/api/estado');
      const e = await r.json();

      if (!sliderInicializado && confidenceSlider) {
        mostrarUmbral(e.conf);
        toggleBoxes.checked = e.cajas;
        toggleLabels.checked = e.etiquetas;
        sliderInicializado = true;
      }

      countTotalEl.textContent = e.naranjas;
      avgConfEl.textContent = e.naranjas ? `${e.confianza}%` : '-';
      inferMsEl.textContent = e.ms ? `${e.ms} ms` : '-';
      mostrarModelo(e);
      fpsCounterEl.textContent = `${e.fps} FPS (IA)`;

      if (!e.modelo_ok) mostrarMensaje('No se pudo cargar el modelo (ver consola del servidor).');
      else if (!e.camara) mostrarMensaje('Esperando la cámara...');
      else mostrarMensaje('');
    } catch (err) {
      mostrarMensaje('Sin conexión con el servidor. Ejecute: python serve.py');
    }
  }

  if (confidenceSlider) {
    confidenceSlider.addEventListener('input', (ev) => {
      confidenceValue.textContent = `${Math.round(ev.target.value * 100)}%`;
    });
    confidenceSlider.addEventListener('change', (ev) => {
      enviarConfig({ conf: parseFloat(ev.target.value) });
    });
  }
  if (toggleBoxes) toggleBoxes.addEventListener('change', (ev) => enviarConfig({ cajas: ev.target.checked }));
  if (toggleLabels) toggleLabels.addEventListener('change', (ev) => enviarConfig({ etiquetas: ev.target.checked }));

  modelBtns.forEach(btn => {
    btn.addEventListener('click', async () => {
      if (btn.classList.contains('active')) return;
      modelBtns.forEach(b => b.disabled = true);
      const cfg = await enviarConfig({ modelo: btn.dataset.modelo });
      if (cfg) mostrarUmbral(cfg.conf);  // el servidor mantiene el umbral elegido
      await actualizarEstado();
    });
  });

  actualizarEstado();
  setInterval(actualizarEstado, 700);
});
