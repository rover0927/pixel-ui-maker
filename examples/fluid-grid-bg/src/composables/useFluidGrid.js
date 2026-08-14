// geek-fluid-grid — 引擎 A：固定网格像素流体动画引擎（原生 Canvas，无依赖）
// 实现自《流体网格粒子动画效果实现指南》：固定网格 + 流场驱动 + 颜色映射 + 呼吸闪烁。
//   - 固定网格布局：像素方块按 cellSize + gap 规则排布，形成 LED 点阵
//   - 流场驱动：Perlin 值噪声(fBm)按时间漂移，或波浪/涡流数学函数 → 平滑"流动"
//   - 颜色映射：流场值 → 亮度；噪声梯度方向 → 色相偏移（深浅随流向）
//   - 闪烁呼吸：正弦 + 每格随机相位 → 一会亮一会灭
//   - 鼠标扰动源：光标附近漩涡/排斥，像素随光标扰动
//   - 性能护栏：像素数按屏幕面积自适应封顶(<5000)、DPR≤2、resize、reduced-motion 静态、hidden 暂停
// 返回 { start } → 控制器 { stop, setOptions, setOnStats }。
export function useFluidGrid(canvasRef, initial = {}) {
  const DEFAULTS = {
    cellSize: 10,      // 小方块尺寸（px）
    gap: 2,            // 方块间隙（px）
    maxPixels: 4500,   // 像素点上限（指南建议 < 5000）
    flowSpeed: 0.06,   // 流场漂移速度
    flowMode: 'noise', // 'noise' | 'wave' | 'vortex'
    flicker: 1.4,      // 呼吸闪烁频率
    brightness: 1.0,   // 整体亮度倍率
    hue: 155,          // 基色相（默认绿）
    hueSpread: 46,     // 流向带来的色相偏移范围(°)
    saturation: 1.0,
    mouse: 'swirl',    // 'swirl' | 'repel' | 'off'
  }
  const opt = {}
  for (const k of Object.keys(DEFAULTS)) {
    opt[k] = initial[k] !== undefined && initial[k] !== null ? initial[k] : DEFAULTS[k]
  }

  function start() {
    const canvas = canvasRef?.value
    if (!canvas) return { stop: () => {} }
    const ctx = canvas.getContext('2d')
    if (!ctx) return { stop: () => {} }

    let w = 0
    let h = 0
    let raf = 0
    let running = true
    let time = 0
    let grid = []
    let gridCols = 0
    let gridRows = 0
    let onStats = null
    const mouse = { x: -1e9, y: -1e9, active: false }
    const host = canvas.parentElement || window

    // ---------- 噪声：2D 值噪声 + fBm（平滑随机流场） ----------
    function hash2(x, y) {
      let h = Math.imul(x, 374761393) + Math.imul(y, 668265263)
      h = h ^ (h >>> 13)
      h = Math.imul(h, 1274126177)
      h = (h ^ (h >>> 16)) >>> 0
      return h / 4294967295
    }
    function smooth(t) {
      return t * t * (3 - 2 * t)
    }
    function noise2(x, y) {
      const xi = Math.floor(x)
      const yi = Math.floor(y)
      const xf = x - xi
      const yf = y - yi
      const a = hash2(xi, yi)
      const b = hash2(xi + 1, yi)
      const c = hash2(xi, yi + 1)
      const d = hash2(xi + 1, yi + 1)
      const u = smooth(xf)
      const v = smooth(yf)
      return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v
    }
    // fBm：3 层噪声叠加，归一化到 0..1
    function fbm(x, y) {
      let v = 0
      let amp = 0.5
      let f = 1
      for (let o = 0; o < 3; o++) {
        v += amp * noise2(x * f, y * f)
        amp *= 0.5
        f *= 2
      }
      return Math.min(1, v / 0.875)
    }

    // ---------- 流场：按模式采样一个点 (px,py) 在时刻 t 的值(0..1) ----------
    function flowAt(px, py, t) {
      const s = 0.008 // 噪声空间频率 → 特征尺度 ~125px
      const dx = px * s
      const dy = py * s
      if (opt.flowMode === 'wave') {
        return 0.5 + 0.5 * Math.sin(dx * 0.45 + t * 2.2) * Math.cos(dy * 0.45 + t * 1.5)
      }
      if (opt.flowMode === 'vortex') {
        const cx = w / 2
        const cy = h / 2
        const ang = Math.atan2(py - cy, px - cx)
        const rad = Math.hypot(px - cx, py - cy)
        return 0.5 + 0.5 * Math.sin(rad * 0.02 - t * 1.7 + ang)
      }
      // noise：坐标随时间沿 +x,+y 漂移 → 斜向流动
      return fbm(dx + t, dy + t * 0.7)
    }
    // 流场梯度角（有限差分）→ "流向"，用于色相偏移
    function flowAngle(px, py, t) {
      const e = 1.6
      return Math.atan2(
        flowAt(px, py + e, t) - flowAt(px, py - e, t),
        flowAt(px + e, py, t) - flowAt(px - e, py, t),
      )
    }

    // ---------- 网格 ----------
    function buildGrid() {
      let pitch = opt.cellSize + opt.gap
      gridCols = Math.max(2, Math.floor(w / pitch))
      gridRows = Math.max(2, Math.floor(h / pitch))
      // 像素数护栏：超限自动加粗网格（大屏 / 小格子时仍流畅）
      if (gridCols * gridRows > opt.maxPixels) {
        const k = Math.sqrt((gridCols * gridRows) / opt.maxPixels)
        pitch *= k
        gridCols = Math.max(2, Math.floor(w / pitch))
        gridRows = Math.max(2, Math.floor(h / pitch))
      }
      const ox = (w - (gridCols * pitch - opt.gap)) / 2
      const oy = (h - (gridRows * pitch - opt.gap)) / 2
      grid = []
      for (let j = 0; j < gridRows; j++) {
        for (let i = 0; i < gridCols; i++) {
          grid.push({
            x: ox + i * pitch,
            y: oy + j * pitch,
            phase: Math.random() * Math.PI * 2, // 呼吸随机相位
          })
        }
      }
    }

    // ---------- 尺寸 / DPR ----------
    function resize() {
      const rect = canvas.parentElement
        ? canvas.parentElement.getBoundingClientRect()
        : null
      w = rect && rect.width ? rect.width : window.innerWidth
      h = rect && rect.height ? rect.height : window.innerHeight
      const dpr = Math.min(window.devicePixelRatio || 1, 2) // 封顶 2 保性能
      canvas.width = Math.round(w * dpr)
      canvas.height = Math.round(h * dpr)
      canvas.style.width = `${w}px`
      canvas.style.height = `${h}px`
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
      buildGrid()
    }

    // ---------- 绘制 ----------
    function draw() {
      ctx.clearRect(0, 0, w, h)
      const t = time * opt.flowSpeed
      const cell = opt.cellSize
      const baseHue = opt.hue
      const spread = opt.hueSpread
      const sat = Math.min(1, 0.85 * opt.saturation)
      const br = opt.brightness
      const mRadius = 130
      const hasMouse = mouse.active && opt.mouse !== 'off'

      const n = grid.length
      for (let i = 0; i < n; i++) {
        const g = grid[i]
        let px = g.x
        let py = g.y

        // 鼠标扰动源：先扭曲采样坐标 → 形成漩涡 / 排斥
        if (hasMouse) {
          const dx = px - mouse.x
          const dy = py - mouse.y
          const d = Math.hypot(dx, dy)
          if (d < mRadius && d > 0.1) {
            const fall = 1 - d / mRadius
            if (opt.mouse === 'repel') {
              const k = fall * 16
              px += (dx / d) * k
              py += (dy / d) * k
            } else {
              const k = fall * fall * 30 // 切向 → 小漩涡
              px += (dy / d) * k
              py += (-dx / d) * k
            }
          }
        }

        const nv = flowAt(px, py, t) // 流场值 0..1
        const ang = flowAngle(px, py, t) // 流向角
        const hue = (baseHue + (ang / (Math.PI * 2)) * spread + 360) % 360

        // 深浅随流向：流场值 → 亮度；闪烁呼吸：正弦 + 随机相位
        g.phase += 0.012 * opt.flicker
        const breath = 0.5 + 0.5 * Math.sin(g.phase)
        const light = Math.min(1.15, (0.14 + 0.86 * nv * nv) * (0.25 + 0.75 * breath) * br)

        ctx.fillStyle = `hsl(${hue.toFixed(1)} ${(sat * 100).toFixed(0)}% ${Math.min(100, 30 + 55 * light).toFixed(0)}%)`
        ctx.globalAlpha = light > 1 ? 1 : light
        ctx.fillRect(g.x - cell / 2, g.y - cell / 2, cell, cell)
      }
      ctx.globalAlpha = 1
    }

    // ---------- 主循环 ----------
    let last = performance.now()
    let lastReport = 0
    let fps = 60
    function frame(now) {
      if (!running) return
      const dtMs = now - last
      last = now
      const dt = Math.min(dtMs / 16.7, 2) // 归一化到 ~60fps，夹住跳帧
      fps = fps * 0.92 + (1000 / Math.max(dtMs, 1)) * 0.08
      time += dt
      if (!document.hidden) draw()
      if (onStats && now - lastReport > 400) {
        lastReport = now
        onStats({ fps: Math.round(fps), pixels: grid.length, cols: gridCols, rows: gridRows })
      }
      raf = requestAnimationFrame(frame)
    }

    // ---------- 鼠标 ----------
    function onMove(e) {
      const rect = canvas.getBoundingClientRect()
      mouse.x = e.clientX - rect.left
      mouse.y = e.clientY - rect.top
      mouse.active = true
    }
    function onLeave() {
      mouse.active = false
      mouse.x = -1e9
      mouse.y = -1e9
    }
    function onResize() {
      resize()
      buildGrid()
    }

    // ---------- 实时更新参数 ----------
    function setOptions(patch) {
      if (!patch) return
      for (const k of Object.keys(DEFAULTS)) {
        if (patch[k] !== undefined) opt[k] = patch[k]
      }
      if ('cellSize' in patch || 'gap' in patch || 'maxPixels' in patch) buildGrid()
    }
    function setOnStats(fn) {
      onStats = fn
    }

    // ---------- 启动 ----------
    resize()
    host.addEventListener('pointermove', onMove)
    host.addEventListener('pointerleave', onLeave)
    window.addEventListener('resize', onResize)

    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      time = 1.5 // 静止但非零的流场，画一帧静态图
      draw()
    } else {
      raf = requestAnimationFrame(frame)
    }

    return {
      stop() {
        running = false
        cancelAnimationFrame(raf)
        host.removeEventListener('pointermove', onMove)
        host.removeEventListener('pointerleave', onLeave)
        window.removeEventListener('resize', onResize)
        ctx.clearRect(0, 0, w, h)
      },
      setOptions,
      setOnStats,
    }
  }

  return { start }
}
