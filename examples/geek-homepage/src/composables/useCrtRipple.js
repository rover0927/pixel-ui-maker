// CRT / water-ripple driver — nudges feTurbulence seed + feDisplacementMap scale
// every frame so any element with filter: url(#geek-crt-ripple) ripples.
// Returns start() which returns a stop() canceller. Skips under reduced-motion.
export function useCrtRipple(filterId = 'geek-crt-ripple') {
  const reduceMotion = () =>
    window.matchMedia('(prefers-reduced-motion: reduce)').matches

  function start() {
    if (reduceMotion()) return () => {}
    const turb = document.querySelector(`#${filterId} feTurbulence`)
    const disp = document.querySelector(`#${filterId} feDisplacementMap`)
    if (!turb || !disp) return () => {}
    let raf = 0
    const tick = () => {
      turb.setAttribute('seed', Math.random() * 100)
      disp.setAttribute('scale', 8 + Math.random() * 16)
      raf = requestAnimationFrame(tick)
    }
    raf = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(raf)
  }

  return { start }
}
