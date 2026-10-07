/**
 * Orange Vision AI - Interactive Detection Simulator
 * Universidad Nacional de Asunción 2026
 */

document.addEventListener('DOMContentLoaded', () => {
  const canvas = document.getElementById('detectionCanvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  
  // Controls
  const confidenceSlider = document.getElementById('confidenceSlider');
  const confidenceValue = document.getElementById('confidenceValue');
  const toggleBoxes = document.getElementById('toggleBoxes');
  const toggleMasks = document.getElementById('toggleMasks');
  const toggleLabels = document.getElementById('toggleLabels');
  
  // Counters
  const countTotalEl = document.getElementById('countTotal');
  const countRipeEl = document.getElementById('countRipe');
  const countUnripeEl = document.getElementById('countUnripe');
  const fpsCounterEl = document.getElementById('fpsCounter');

  // Simulated Orange Objects on Synthetic Tree
  const oranges = [
    { id: 1, x: 220, y: 140, r: 38, ripe: true, confidence: 0.98, label: 'Naranja Madura' },
    { id: 2, x: 480, y: 180, r: 42, ripe: true, confidence: 0.96, label: 'Naranja Madura' },
    { id: 3, x: 340, y: 260, r: 45, ripe: true, confidence: 0.99, label: 'Naranja Madura' },
    { id: 4, x: 620, y: 230, r: 35, ripe: false, confidence: 0.89, label: 'Naranja Verde' },
    { id: 5, x: 160, y: 290, r: 36, ripe: true, confidence: 0.94, label: 'Naranja Madura' },
    { id: 6, x: 740, y: 160, r: 40, ripe: true, confidence: 0.97, label: 'Naranja Madura' },
    { id: 7, x: 530, y: 310, r: 34, ripe: false, confidence: 0.83, label: 'Naranja Verde' },
    { id: 8, x: 290, y: 110, r: 30, ripe: true, confidence: 0.91, label: 'Naranja Madura' },
    { id: 9, x: 680, y: 320, r: 37, ripe: true, confidence: 0.95, label: 'Naranja Madura' },
    { id: 10, x: 420, y: 120, r: 32, ripe: false, confidence: 0.76, label: 'Naranja Verde' }
  ];

  let currentConfidence = parseFloat(confidenceSlider ? confidenceSlider.value : 0.70);
  let showBoxes = toggleBoxes ? toggleBoxes.checked : true;
  let showMasks = toggleMasks ? toggleMasks.checked : true;
  let showLabels = toggleLabels ? toggleLabels.checked : true;

  // Resize canvas to parent container resolution
  function resizeCanvas() {
    const rect = canvas.parentElement.getBoundingClientRect();
    canvas.width = rect.width || 800;
    canvas.height = rect.height || 450;
    drawFrame();
  }

  window.addEventListener('resize', resizeCanvas);

  // Drawing Background (Synthetic Tree & Real Oranges)
  function drawTreeBackground() {
    const w = canvas.width;
    const h = canvas.height;

    // Dark foliage backdrop
    const grad = ctx.createLinearGradient(0, 0, 0, h);
    grad.addColorStop(0, '#0a1912');
    grad.addColorStop(1, '#050c08');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, w, h);

    // Draw synthetic tree branches
    ctx.strokeStyle = '#2d2015';
    ctx.lineWidth = 14;
    ctx.lineCap = 'round';
    
    ctx.beginPath();
    ctx.moveTo(w * 0.5, h);
    ctx.quadraticCurveTo(w * 0.48, h * 0.5, w * 0.3, h * 0.2);
    ctx.moveTo(w * 0.48, h * 0.6);
    ctx.quadraticCurveTo(w * 0.65, h * 0.4, w * 0.8, h * 0.25);
    ctx.moveTo(w * 0.35, h * 0.35);
    ctx.quadraticCurveTo(w * 0.2, h * 0.3, w * 0.15, h * 0.25);
    ctx.stroke();

    // Draw dense synthetic leaves clusters
    const leafClusters = [
      { x: w * 0.2, y: h * 0.25, r: 90 },
      { x: w * 0.35, y: h * 0.2, r: 110 },
      { x: w * 0.5, y: h * 0.25, r: 120 },
      { x: w * 0.65, y: h * 0.22, r: 100 },
      { x: w * 0.8, y: h * 0.28, r: 95 },
      { x: w * 0.3, y: h * 0.55, r: 100 },
      { x: w * 0.6, y: h * 0.5, r: 115 },
      { x: w * 0.75, y: h * 0.55, r: 90 }
    ];

    leafClusters.forEach(cluster => {
      const leafGrad = ctx.createRadialGradient(cluster.x, cluster.y, 10, cluster.x, cluster.y, cluster.r);
      leafGrad.addColorStop(0, '#15803d');
      leafGrad.addColorStop(0.7, '#166534');
      leafGrad.addColorStop(1, '#064e3b');
      ctx.fillStyle = leafGrad;
      ctx.beginPath();
      ctx.arc(cluster.x, cluster.y, cluster.r, 0, Math.PI * 2);
      ctx.fill();
    });

    // Draw Oranges (Simulating Real Oranges mounted on synthetic tree)
    oranges.forEach(o => {
      const scaleX = w / 900;
      const scaleY = h / 500;
      const cx = o.x * scaleX;
      const cy = o.y * scaleY;
      const radius = o.r * Math.min(scaleX, scaleY);

      // Organic orange gradient rendering
      const orangeGrad = ctx.createRadialGradient(cx - radius * 0.3, cy - radius * 0.3, radius * 0.1, cx, cy, radius);
      if (o.ripe) {
        orangeGrad.addColorStop(0, '#ffbe3b');
        orangeGrad.addColorStop(0.5, '#ff7e1d');
        orangeGrad.addColorStop(1, '#c2410c');
      } else {
        orangeGrad.addColorStop(0, '#a3e635');
        orangeGrad.addColorStop(0.5, '#65a30d');
        orangeGrad.addColorStop(1, '#3f6212');
      }

      ctx.fillStyle = orangeGrad;
      ctx.beginPath();
      ctx.arc(cx, cy, radius, 0, Math.PI * 2);
      ctx.fill();

      // Stem dot
      ctx.fillStyle = '#15803d';
      ctx.beginPath();
      ctx.arc(cx, cy - radius * 0.9, radius * 0.12, 0, Math.PI * 2);
      ctx.fill();
    });
  }

  // Draw Machine Learning AI Detections
  function drawDetections() {
    const w = canvas.width;
    const h = canvas.height;
    const scaleX = w / 900;
    const scaleY = h / 500;

    let detectedTotal = 0;
    let detectedRipe = 0;
    let detectedUnripe = 0;

    oranges.forEach(o => {
      if (o.confidence < currentConfidence) return;

      detectedTotal++;
      if (o.ripe) detectedRipe++; else detectedUnripe++;

      const cx = o.x * scaleX;
      const cy = o.y * scaleY;
      const radius = o.r * Math.min(scaleX, scaleY);

      // Bounding box padding
      const pad = 8;
      const bx = cx - radius - pad;
      const by = cy - radius - pad;
      const bw = (radius + pad) * 2;
      const bh = (radius + pad) * 2;

      // Draw Segmentation Mask
      if (showMasks) {
        ctx.fillStyle = o.ripe ? 'rgba(255, 126, 29, 0.25)' : 'rgba(132, 204, 22, 0.25)';
        ctx.beginPath();
        ctx.arc(cx, cy, radius + 2, 0, Math.PI * 2);
        ctx.fill();
      }

      // Draw Bounding Box
      if (showBoxes) {
        ctx.strokeStyle = o.ripe ? '#ff7e1d' : '#84cc16';
        ctx.lineWidth = 2;
        ctx.setLineDash([4, 4]); // tech style dashed
        ctx.strokeRect(bx, by, bw, bh);
        ctx.setLineDash([]); // reset

        // Bounding Box Corners Accent
        const cornerSize = 8;
        ctx.strokeStyle = o.ripe ? '#ffffff' : '#ecfccb';
        ctx.lineWidth = 2;

        // Top-Left corner
        ctx.beginPath();
        ctx.moveTo(bx, by + cornerSize); ctx.lineTo(bx, by); ctx.lineTo(bx + cornerSize, by);
        // Top-Right corner
        ctx.moveTo(bx + bw - cornerSize, by); ctx.lineTo(bx + bw, by); ctx.lineTo(bx + bw, by + cornerSize);
        // Bottom-Left corner
        ctx.moveTo(bx, by + bh - cornerSize); ctx.lineTo(bx, by + bh); ctx.lineTo(bx + cornerSize, by + bh);
        // Bottom-Right corner
        ctx.moveTo(bx + bw - cornerSize, by + bh); ctx.lineTo(bx + bw, by + bh); ctx.lineTo(bx + bw, by + bh - cornerSize);
        ctx.stroke();
      }

      // Draw Label Badge
      if (showLabels) {
        const confPercent = Math.round(o.confidence * 100);
        const labelText = `${o.label} ${confPercent}%`;
        
        ctx.font = '600 12px "Plus Jakarta Sans", sans-serif';
        const textMetrics = ctx.measureText(labelText);
        const labelW = textMetrics.width + 12;
        const labelH = 20;

        ctx.fillStyle = o.ripe ? '#ff7e1d' : '#65a30d';
        ctx.fillRect(bx, by - labelH, labelW, labelH);

        ctx.fillStyle = '#ffffff';
        ctx.fillText(labelText, bx + 6, by - 5);
      }
    });

    // Update Counter UI
    if (countTotalEl) countTotalEl.innerText = detectedTotal;
    if (countRipeEl) countRipeEl.innerText = detectedRipe;
    if (countUnripeEl) countUnripeEl.innerText = detectedUnripe;
  }

  // Animation Loop
  let lastTime = performance.now();
  let frameCount = 0;

  function drawFrame() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawTreeBackground();
    drawDetections();

    // FPS calculation
    frameCount++;
    const now = performance.now();
    if (now - lastTime >= 1000) {
      if (fpsCounterEl) fpsCounterEl.innerText = `${Math.round((frameCount * 1000) / (now - lastTime))} FPS`;
      frameCount = 0;
      lastTime = now;
    }

    requestAnimationFrame(drawFrame);
  }

  // Event Listeners for Controls
  if (confidenceSlider) {
    confidenceSlider.addEventListener('input', (e) => {
      currentConfidence = parseFloat(e.target.value);
      if (confidenceValue) confidenceValue.innerText = `${Math.round(currentConfidence * 100)}%`;
    });
  }

  if (toggleBoxes) toggleBoxes.addEventListener('change', (e) => showBoxes = e.target.checked);
  if (toggleMasks) toggleMasks.addEventListener('change', (e) => showMasks = e.target.checked);
  if (toggleLabels) toggleLabels.addEventListener('change', (e) => showLabels = e.target.checked);

  // Initialize
  setTimeout(() => {
    resizeCanvas();
  }, 100);
});
