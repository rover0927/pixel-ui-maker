// geek-fluid-grid — 引擎 B：固定网格像素点阵 + 双噪声场 + 呼吸潮汐（原生 Canvas，无依赖）
// 核心语义：
//   1. 网格方块位置固定、大小统一（cell×cell），只表现「亮灭 + 颜色」的变化
//   2. 双噪声场分层：亮度场（较高频、细腻光斑）与颜色场（较低频、米白↔主色渐变）
//      各自独立漂移，层次丰富而不突兀
//   3. 呼吸潮汐：极慢的整体明暗起伏，速度由「呼吸频率」控制
//   4. 主题主色：渐变的一端（主色）由 hue 决定，随「颜色主题」切换
// 纯黑背景，暖米白 #f8f6e8 ↔ 主题主色平滑过渡；无鼠标交互；
// DPR、resize、prefers-reduced-motion、document.hidden 暂停。
// 返回 { start } → 控制器 { stop, setOptions, setOnStats }。
export function useDisturbanceWave(canvasRef, initial = {}) {
  const DEFAULTS = {
    cellSize: 10,      // 方块尺寸（px，位置固定）
    gap: 2,            // 方块间隙（px）
    maxPixels: 4500,   // 方块数上限（大屏自动加粗网格）
    flowSpeed: 0.06,   // 噪声场漂移速度（默认慢）
    brightness: 1.0,   // 整体亮度倍率
    hue: 155,          // 主题主色相（渐变另一端，随「颜色主题」切换）
    flicker: 1.4,      // 呼吸潮汐速度（越小越慢，0 = 静止）
  }
  const opt = {}
  for (const k of Object.keys(DEFAULTS)) {
    opt[k] = initial[k] !== undefined && initial[k] !== null ? initial[k] : DEFAULTS[k]
  }

  // 高光端：固定暖米白；渐变另一端为主题主色（HSV 由 hue 决定，柔和亮度）
  const C_WHITE = [0xf8, 0xf6, 0xe8]
  function hsv2rgb(h, s, v) {
    const c = v * s
    const hh = h / 60
    const x = c * (1 - Math.abs((hh % 2) - 1))
    const m = v - c
    let r = 0
    let g = 0
    let b = 0
    if (hh < 1) { r = c; g = x }
    else if (hh < 2) { r = x; g = c }
    else if (hh < 3) { g = c; b = x }
    else if (hh < 4) { g = x; b = c }
    else if (hh < 5) { r = x; b = c }
    else { r = c; b = x }
    return [Math.round((r + m) * 255), Math.round((g + m) * 255), Math.round((b + m) * 255)]
  }
  // t ∈ [0,1] → 颜色在暖米白 ↔ 主色之间线性过渡
  function colorLerp(t, main) {
    const r = Math.round(C_WHITE[0] + (main[0] - C_WHITE[0]) * t)
    const g = Math.round(C_WHITE[1] + (main[1] - C_WHITE[1]) * t)
    const b = Math.round(C_WHITE[2] + (main[2] - C_WHITE[2]) * t)
    return `rgb(${r},${g},${b})`
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

    // ---------- 噪声：2D 值噪声 + fBm（全局扰动场，与流体网格噪声场同源） ----------
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

    // ---------- 固定网格（与流体网格一致，位置固定、大小统一） ----------
    function buildGrid() {
      let pitch = opt.cellSize + opt.gap
      gridCols = Math.max(2, Math.floor(w / pitch))
      gridRows = Math.max(2, Math.floor(h / pitch))
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
          grid.push({ x: ox + i * pitch, y: oy + j * pitch })
        }
      }
    }

    function resize() {
      const rect = canvas.parentElement
        ? canvas.parentElement.getBoundingClientRect()
        : null
      w = rect && rect.width ? rect.width : window.innerWidth
      h = rect && rect.height ? rect.height : window.innerHeight
      const dpr = Math.min(window.devicePixelRatio || 1, 2)
      canvas.width = Math.round(w * dpr)
      canvas.height = Math.round(h * dpr)
      canvas.style.width = `${w}px`
      canvas.style.height = `${h}px`
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
      buildGrid()
    }

    function draw() {
      ctx.fillStyle = '#000000'
      ctx.fillRect(0, 0, w, h)

      const cell = opt.cellSize
      const br = opt.brightness
      const n = grid.length
      const main = hsv2rgb(opt.hue % 360, 0.55, 0.9) // 主题主色（渐变另一端）
      // 慢速漂移（跟随「流动速度」）：亮度场细腻、颜色场更慢且反向漂移
      const t = time * (0.05 + opt.flowSpeed * 0.8)
      const tc = time * (0.03 + opt.flowSpeed * 0.5)
      // 呼吸潮汐：整体明暗起伏，速度跟随「呼吸频率」
      const tide = 0.5 + 0.5 * Math.sin(time * 0.015 * opt.flicker)

      // 方块：位置固定、大小统一（cell×cell），只表现「亮灭 + 颜色」。
      // 亮度场驱动明暗（细腻光斑游走），颜色场驱动米白↔主色平滑渐变，二者分层流动。
      for (let i = 0; i < n; i++) {
        const g = grid[i]
        const nv = fbm(g.x * 0.012 + t, g.y * 0.012 + t * 0.7) // 亮度场
        const cn = fbm(g.x * 0.006 + tc, g.y * 0.006 - tc * 0.5) // 颜色场
        const light = (0.06 + 0.42 * nv) * (0.85 + 0.15 * tide) // 柔和亮度 + 潮汐
        ctx.fillStyle = colorLerp(cn, main)
        ctx.globalAlpha = Math.min(1, light * br)
        ctx.fillRect(g.x - cell / 2, g.y - cell / 2, cell, cell)
      }
      ctx.globalAlpha = 1
    }

    let last = performance.now()
    let lastReport = 0
    let fps = 60
    function frame(now) {
      if (!running) return
      const dtMs = now - last
      last = now
      const dt = Math.min(dtMs / 16.7, 2)
      fps = fps * 0.92 + (1000 / Math.max(dtMs, 1)) * 0.08
      time += dt

      if (!document.hidden) draw()

      if (onStats && now - lastReport > 400) {
        lastReport = now
        onStats({ fps: Math.round(fps), pixels: grid.length, cols: gridCols, rows: gridRows })
      }
      raf = requestAnimationFrame(frame)
    }

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

    function onResize() {
      resize()
    }

    resize()
    window.addEventListener('resize', onResize)

    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      draw() // 一帧静态
    } else {
      raf = requestAnimationFrame(frame)
    }

    return {
      stop() {
        running = false
        cancelAnimationFrame(raf)
        window.removeEventListener('resize', onResize)
        ctx.clearRect(0, 0, w, h)
      },
      setOptions,
      setOnStats,
    }
  }

  return { start }
}
