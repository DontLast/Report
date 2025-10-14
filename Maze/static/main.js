const canvas = document.getElementById('maze');
const ctx = canvas.getContext('2d');
const statusEl = document.getElementById('status');
const buttons = document.querySelectorAll('.difficulty button');

let mazeData = null;
let scale = 0;
let startCell = null;
let endCell = null;
let gameActive = false; // активна ли текущая попытка (после клика по старту)
let startedInside = false; // зафиксирован ли старт

// позиция указателя мыши внутри canvas
let pointer = { x: 0, y: 0 };
// угол вращения треугольника
let angle = 0;
// требуется ли рисовать треугольный курсор (прячем системный)
let drawTriangleCursor = false;

buttons.forEach(btn => {
  btn.addEventListener('click', async (e) => {
    const level = parseInt(e.currentTarget.dataset.level, 10);
    await loadMaze(level);
  });
});

async function loadMaze(level) {
  statusEl.textContent = 'Загрузка лабиринта...';
  const res = await fetch(`/api/maze?level=${level}`);
  mazeData = await res.json();
  startCell = { r: mazeData.start[0], c: mazeData.start[1] };
  endCell = { r: mazeData.end[0], c: mazeData.end[1] };
  startedInside = false;
  gameActive = false;
  drawTriangleCursor = false;
  canvas.style.cursor = 'default';
  drawMaze();
  statusEl.textContent = 'Кликните по зелёной клетке, чтобы начать.';
}

function drawMaze() {
  const { width, height, grid } = mazeData;
  const cellSize = Math.floor(Math.min(canvas.width / width, canvas.height / height));
  scale = cellSize;
  const offsetX = Math.floor((canvas.width - width * cellSize) / 2);
  const offsetY = Math.floor((canvas.height - height * cellSize) / 2);

  ctx.fillStyle = '#111';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  for (let r = 0; r < height; r++) {
    for (let c = 0; c < width; c++) {
      const x = offsetX + c * cellSize;
      const y = offsetY + r * cellSize;
      if (grid[r][c] === 0) {
        ctx.fillStyle = '#1f2937';
      } else {
        ctx.fillStyle = '#e5e7eb';
      }
      ctx.fillRect(x, y, cellSize, cellSize);
    }
  }

  // start
  ctx.fillStyle = '#10b981';
  ctx.fillRect(offsetX + startCell.c * cellSize, offsetY + startCell.r * cellSize, cellSize, cellSize);
  // end
  ctx.fillStyle = '#ef4444';
  ctx.fillRect(offsetX + endCell.c * cellSize, offsetY + endCell.r * cellSize, cellSize, cellSize);

  // store offsets for hit-testing
  canvas.dataset.offsetX = offsetX;
  canvas.dataset.offsetY = offsetY;
}

function eventToCell(ev) {
  const rect = canvas.getBoundingClientRect();
  const x = ev.clientX - rect.left;
  const y = ev.clientY - rect.top;
  const offsetX = parseInt(canvas.dataset.offsetX, 10) || 0;
  const offsetY = parseInt(canvas.dataset.offsetY, 10) || 0;
  const c = Math.floor((x - offsetX) / scale);
  const r = Math.floor((y - offsetY) / scale);
  return { r, c };
}

canvas.addEventListener('mousemove', (ev) => {
  if (!mazeData) return;
  const rect = canvas.getBoundingClientRect();
  pointer.x = ev.clientX - rect.left;
  pointer.y = ev.clientY - rect.top;
});

canvas.addEventListener('click', (ev) => {
  if (!mazeData) return;
  const cell = eventToCell(ev);
  const { grid, width, height } = mazeData;
  if (cell.r < 0 || cell.c < 0 || cell.r >= height || cell.c >= width) return;
  if (!startedInside && cell.r === startCell.r && cell.c === startCell.c) {
    startedInside = true;
    gameActive = true;
    drawTriangleCursor = true;
    canvas.style.cursor = 'none';
    statusEl.textContent = 'Ведите треугольник к финишу. Стена сбрасывает попытку!';
    // обновим позицию указателя для корректного первого кадра
    const rect = canvas.getBoundingClientRect();
    pointer.x = ev.clientX - rect.left;
    pointer.y = ev.clientY - rect.top;
  }
});

window.addEventListener('resize', () => {
  if (!mazeData) return;
  drawMaze();
});

function pointToCell(x, y) {
  const offsetX = parseInt(canvas.dataset.offsetX, 10) || 0;
  const offsetY = parseInt(canvas.dataset.offsetY, 10) || 0;
  const c = Math.floor((x - offsetX) / scale);
  const r = Math.floor((y - offsetY) / scale);
  return { r, c };
}

function getEquilateralVertices() {
  // Равносторонний треугольник с центром в pointer, направлен по angle
  // Уменьшаем примерно в 2 раза
  const side = Math.max(8, Math.floor(scale * 0.45));
  const h = side * Math.sqrt(3) / 2; // высота
  // В локальных координатах (до поворота):
  // вершина 0 направлена вперёд по X, две другие симметрично сзади
  const local = [
    { x:  2 * h / 3, y:  0 },        // нос
    { x: -h / 3,     y:  side / 2 }, // левый задний
    { x: -h / 3,     y: -side / 2 }, // правый задний
  ];
  const cosA = Math.cos(angle);
  const sinA = Math.sin(angle);
  return local.map(p => ({
    x: pointer.x + p.x * cosA - p.y * sinA,
    y: pointer.y + p.x * sinA + p.y * cosA,
  }));
}

function drawTriangle() {
  const verts = getEquilateralVertices();
  ctx.save();
  ctx.beginPath();
  ctx.moveTo(verts[0].x, verts[0].y);
  ctx.lineTo(verts[1].x, verts[1].y);
  ctx.lineTo(verts[2].x, verts[2].y);
  ctx.closePath();
  // чёрный равносторонний треугольник с тёмной аурой
  ctx.fillStyle = '#000000';
  ctx.shadowColor = 'rgba(0,0,0,0.75)';
  ctx.shadowBlur = 16;
  ctx.shadowOffsetX = 0;
  ctx.shadowOffsetY = 0;
  ctx.fill();
  ctx.restore();
}

function sampleEdge(a, b, steps = 12) {
  const points = [];
  for (let i = 0; i <= steps; i++) {
    const t = i / steps;
    points.push({ x: a.x + (b.x - a.x) * t, y: a.y + (b.y - a.y) * t });
  }
  return points;
}

function performCollisionAndWin() {
  if (!gameActive || !mazeData) return;
  const { grid, width, height } = mazeData;
  const verts = getEquilateralVertices();

  // Проверка по вершинам
  for (const v of verts) {
    const cell = pointToCell(v.x, v.y);
    if (cell.r >= 0 && cell.c >= 0 && cell.r < height && cell.c < width) {
      if (grid[cell.r][cell.c] === 0) return lose();
    }
  }

  // Проверка по рёбрам (семплирование точек на рёбрах)
  const edges = [ [verts[0], verts[1]], [verts[1], verts[2]], [verts[2], verts[0]] ];
  for (const [a, b] of edges) {
    const samples = sampleEdge(a, b, 14);
    for (const p of samples) {
      const cell = pointToCell(p.x, p.y);
      if (cell.r >= 0 && cell.c >= 0 && cell.r < height && cell.c < width) {
        if (grid[cell.r][cell.c] === 0) return lose();
      }
    }
  }

  // Победа — когда центр (указатель) в финишной клетке
  const centerCell = pointToCell(pointer.x, pointer.y);
  if (centerCell.r === endCell.r && centerCell.c === endCell.c) return win();
}

function lose() {
  statusEl.textContent = 'Столкновение со стеной! Кликните старт, чтобы попробовать снова.';
  startedInside = false;
  gameActive = false;
  drawTriangleCursor = false;
  canvas.style.cursor = 'default';
}

function win() {
  statusEl.textContent = 'Победа! Вы выбрались из лабиринта.';
  gameActive = false;
  drawTriangleCursor = false;
  canvas.style.cursor = 'default';
}

function frame() {
  if (!mazeData) return requestAnimationFrame(frame);
  // перерисуем всё, чтобы не оставались следы курсора
  drawMaze();
  if (drawTriangleCursor) {
    drawTriangle();
    performCollisionAndWin();
    angle += 0.06; // вращение
  }
  requestAnimationFrame(frame);
}

requestAnimationFrame(frame);


