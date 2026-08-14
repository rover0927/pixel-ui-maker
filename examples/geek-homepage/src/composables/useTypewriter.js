// Sequential terminal typewriter. Types `lines` into `el` char-by-char with a
// pause between lines. Returns a stop() to cancel. Respects prefers-reduced-motion.
export function useTypewriter() {
  const reduceMotion = () =>
    window.matchMedia('(prefers-reduced-motion: reduce)').matches

  function type(el, lines, { speed = 40, linePause = 450, loop = false } = {}) {
    if (reduceMotion() || !el) {
      if (el) el.textContent = lines.join('\n')
      return () => {}
    }
    let alive = true
    let line = 0
    let ch = 0
    let timer = 0

    const tick = () => {
      if (!alive) return
      if (line >= lines.length) {
        if (loop) {
          line = 0
          ch = 0
          el.textContent = ''
          timer = setTimeout(tick, linePause)
        }
        return
      }
      if (ch <= lines[line].length) {
        el.textContent = lines[line].slice(0, ch)
        ch += 1
        timer = setTimeout(tick, speed)
      } else {
        line += 1
        ch = 0
        timer = setTimeout(tick, linePause)
      }
    }
    tick()
    return () => {
      alive = false
      clearTimeout(timer)
    }
  }

  return { type }
}
