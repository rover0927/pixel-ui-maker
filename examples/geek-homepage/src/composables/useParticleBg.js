// geek-particle-bg — 背景像素粒子网络引擎（原生 Canvas，无依赖）
// 蒸馏自《粒子背景动画效果实现指南》的粒子系统，套上 geek lock：
//   - 粒子画成"像素方块"（fillRect），不是圆点 —— 0 圆角，契合像素主题
//   - 调色板只取 cyber-geek 的 --geek-* 霓虹色（青/洋红/teal/白/蓝）
//   - 慢速漂浮（ease 感），不上蹿下跳；邻近粒子连线 + 鼠标排斥/连线
//   - prefers-reduced-motion 时画一帧静态粒子场后停（不带动画）
//   - DPR 适配、resize、document.hidden 暂停
// 返回 start() → 返回 stop() 取消器。
export function useParticleBg(canvasRef, options = {}) {
  const reduceMotion = () =>
    window.matchMedia('(prefers-reduced-motion: reduce)').matches

  // 默认值 —— colors 为 cyber-geek 调色板子集（:root 里已声明的 HEX）
  const DEFAULTS = {
    colors: ['#00f0ff', '#ff2bd6', '#00ffd5', '#e6f1ff', '#2e7dff'],
    maxCount: 170,          // 粒子数上限（实际按屏幕面积折算）
    linkDist: 120,          // 粒子-粒子连线阈值（px）
    mouseLinkDist: 200,     // 鼠标-粒子连线阈值（px）
    mouseRepel: 52,         // 鼠标排斥半径（px）
    particleAlpha: 0.9,     // 粒子核心不透明度上限
    linkAlpha: 0.16,        // 连线不透明度上限
    maxSpeed: 0.6,          // 漂浮速度上限（px/帧，慢速）
  }
  const opt = {}
  for (const k of Object.keys(DEFAULTS)) {
    opt[k] = options[k] !== undefined && options[k] !== null ? options[k] : DEFAULTS[k]
  }

  function start() {
    const canvas = canvasRef?.value
    if (!canvas) return () => {}
    const ctx = canvas.getContext('2d')
    if (!ctx) return () => {}

    let w = 0
    let h = 0
    let raf = 0
    let running = true
    let particles = []
    const mouse = { x: -9999, y: -9999, active: false }
    const host = canvas.parentElement || window

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
    }

    // ---------- 粒子 ----------
    function makeParticle() {
      return {
        x: Math.random() * w,
        y: Math.random() * h,
        vx: (Math.random() * 2 - 1) * opt.maxSpeed,
        vy: (Math.random() * 2 - 1) * opt.maxSpeed,
        size: 1 + Math.floor(Math.random() * 3),       // 1..3px 方块，整数
        color: opt.colors[(Math.random() * opt.colors.length) | 0],
        alpha: 0.35 + Math.random() * 0.55,
        phase: Math.random() * Math.PI * 2,            // 正弦漂浮相位
      }
    }

    function init() {
      const count = Math.min(
        opt.maxCount,
        Math.max(30, Math.round((w * h) / 14000)),     // 屏幕越大粒子越多
      )
      particles = Array.from({ length: count }, makeParticle)
    }

    // ---------- 运动 ----------
    function step(dt) {
      const n = particles.length
      for (let i = 0; i < n; i++) {
        const p = particles[i]
        p.phase += 0.012 * dt
        // 慢速漂移 + 轻微正弦摆动 + 轻微上浮（"浮动"感）
        p.x += p.vx + Math.sin(p.phase) * 0.15
        p.y += p.vy - 0.04 * dt
        // 边界回绕（带出血，避免边缘突现）
        if (p.x < -8) p.x = w + 8; else if (p.x > w + 8) p.x = -8
        if (p.y < -8) p.y = h + 8; else if (p.y > h + 8) p.y = -8
      }
      // 鼠标排斥（粒子被推开，形成空洞跟随光标）
      if (mouse.active) {
        const r = opt.mouseRepel
        for (let i = 0; i < n; i++) {
          const p = particles[i]
          const dx = p.x - mouse.x
          const dy = p.y - mouse.y
          const d2 = dx * dx + dy * dy
          if (d2 < r * r && d2 > 0.01) {
            const d = Math.sqrt(d2)
            const f = (1 - d / r) * 0.6
            p.x += (dx / d) * f
            p.y += (dy / d) * f
          }
        }
      }
    }

    // ---------- 绘制 ----------
    function draw() {
      ctx.clearRect(0, 0, w, h)
      const n = particles.length
      const ld = opt.linkDist
      const ld2 = ld * ld
      ctx.lineWidth = 1

      // 近邻连线（O(n²)，n ≤ maxCount；只在阈值内画，透明度随距离衰减）
      for (let i = 0; i < n; i++) {
        const a = particles[i]
        for (let j = i + 1; j < n; j++) {
          const b = particles[j]
          const dx = a.x - b.x
          const dy = a.y - b.y
          const d2 = dx * dx + dy * dy
          if (d2 < ld2) {
            const t = 1 - Math.sqrt(d2) / ld
            ctx.globalAlpha = t * opt.linkAlpha
            ctx.strokeStyle = a.color
            ctx.beginPath()
            ctx.moveTo(a.x, a.y)
            ctx.lineTo(b.x, b.y)
            ctx.stroke()
          }
        }
      }

      // 鼠标连线（最近的粒子与光标之间，青色）
      if (mouse.active && n) {
        const ml = opt.mouseLinkDist
        for (let i = 0; i < n; i++) {
          const p = particles[i]
          const dx = p.x - mouse.x
          const dy = p.y - mouse.y
          const d = Math.sqrt(dx * dx + dy * dy)
          if (d < ml) {
            const t = 1 - d / ml
            ctx.globalAlpha = t * opt.linkAlpha * 1.6
            ctx.strokeStyle = '#00f0ff'
            ctx.beginPath()
            ctx.moveTo(p.x, p.y)
            ctx.lineTo(mouse.x, mouse.y)
            ctx.stroke()
          }
        }
      }

      // 像素方块粒子：外围柔光方块（低透明度大一圈）+ 核心方块
      ctx.globalAlpha = 1
      for (let i = 0; i < n; i++) {
        const p = particles[i]
        ctx.fillStyle = p.color
        ctx.globalAlpha = p.alpha * 0.18
        ctx.fillRect(p.x - p.size - 2, p.y - p.size - 2, p.size * 2 + 4, p.size * 2 + 4)
        ctx.globalAlpha = p.alpha * opt.particleAlpha
        ctx.fillRect(p.x - p.size / 2, p.y - p.size / 2, p.size, p.size)
      }
      ctx.globalAlpha = 1
    }

    // ---------- 主循环 ----------
    let last = performance.now()
    function frame(now) {
      if (!running) return
      const dt = Math.min((now - last) / 16.7, 2) // 归一化到 ~60fps，夹住跳帧
      last = now
      if (!document.hidden) {
        step(dt)
        draw()
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
      mouse.x = -9999
      mouse.y = -9999
    }
    function onResize() {
      resize()
      if (particles.length) init() // 尺寸变了重新铺满
    }

    // ---------- 启动 ----------
    resize()
    init()
    host.addEventListener('mousemove', onMove)
    host.addEventListener('mouseleave', onLeave)
    window.addEventListener('resize', onResize)

    if (reduceMotion()) {
      draw() // 一帧静态粒子场（无连线动画也可看，纯静止）
    } else {
      raf = requestAnimationFrame(frame)
    }

    return () => {
      running = false
      cancelAnimationFrame(raf)
      host.removeEventListener('mousemove', onMove)
      host.removeEventListener('mouseleave', onLeave)
      window.removeEventListener('resize', onResize)
      ctx.clearRect(0, 0, w, h)
    }
  }

  return { start }
}
