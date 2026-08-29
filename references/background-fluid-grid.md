# Background: Fluid Grid — 流体网格粒子背景 (Canvas 2D + rAF, 双引擎)

> Distilled recipe for a **full-screen canvas pixel-grid background** in the geek lock: a fixed
> LED-dot-matrix grid (`cellSize` + `gap`) whose pixels are driven by a Perlin-style value-noise
> flow field — with color, brightness, breathing, and optional mouse disturbance. Ships **two
> engines**: `geek-fluid-grid` (`useFluidGrid`) for the classic flow modes (noise / wave / vortex
> + mouse swirl-repel), and a **disturbance-wave** engine (`useDisturbanceWave`) for a calmer
> "uniform pixels + layered dual-noise fields + breathing tide" look with **no mouse interaction**.
> Pure Canvas 2D, zero dependencies (works in Vue composables, React, or vanilla).
> Source project (full source): `<skill-dir>/examples/fluid-grid-bg/` — a runnable
> Vue 3 + Vite demo (`npm install && npm run dev`).

> **Don't conflate with `geek-particle-bg` (dynamic-effects.md §5).** That one is a sparse network
> of *freely floating* pixel squares with proximity links. `geek-fluid-grid` is a *fixed grid* of
> pixels whose values flow — it reads like an LED matrix / data display, not a particle cloud.

---

## 1. Origin (蒸馏来源)

| Piece | Where it lived | What it does |
|-------|----------------|--------------|
| `geek-fluid-grid` | `examples/fluid-grid-bg/src/composables/useFluidGrid.js` | Fixed grid + flow-field drive (noise/wave/vortex) + color mapping + breathing flicker + mouse swirl/repel |
| Disturbance engine | `examples/fluid-grid-bg/src/composables/useDisturbanceWave.js` | Uniform cell×cell pixels + **dual-noise-field layering** + breathing tide, no mouse |
| Engine switch | `examples/fluid-grid-bg/src/components/GeekFluidGrid.vue` | `<GeekFluidGrid :options>` picks engine by `options.flowMode === 'disturb'` |
| Control panel | `examples/fluid-grid-bg/src/App.vue` + `assets/geek-fluid-grid.css` | Live param panel: theme chips, seg controls, sliders, copy-params button |

Both engines return `{ start() → { stop, setOptions(patch), setOnStats(fn) } }` and are fully
reactive — pass a Vue `reactive` settings object and deep-watch it into `setOptions`. Stats callback
fires every ~400ms with `{ fps, pixels, cols, rows }`.

---

## 2. Engine A — `geek-fluid-grid` (useFluidGrid)

**Mechanism.** A fixed grid of squares; each frame every square samples a time-drifted flow field:
- **`flowAt(px,py,t)`** — three modes:
  - `noise`: `fbm(px*0.008 + t, py*0.008 + t*0.7)` (drifts diagonally)
  - `wave`: `0.5 + 0.5*sin(dx*0.45 + t*2.2)*cos(dy*0.45 + t*1.5)`
  - `vortex`: `0.5 + 0.5*sin(rad*0.02 - t*1.7 + ang)` around canvas center
- **`flowAngle`** — finite difference of the field → hue shift: `hue = baseHue + (ang/2π)*hueSpread`
- **Breathing** — per-pixel random phase `g.phase += 0.012*flicker`, `breath = 0.5+0.5*sin(phase)`
- **Brightness** — `light = min(1.15, (0.14 + 0.86*nv²) * (0.25 + 0.75*breath) * brightness)`
- **Mouse disturbance** — before sampling, warp the sample point near the cursor: `swirl`
  (tangential kick `fall²*30`) or `repel` (radial kick `fall*16`), radius 130px. Disabled when
  `mouse === 'off'`.

**Per-pixel draw:**
```js
const nv = flowAt(px, py, t)                 // 0..1 field value
const ang = flowAngle(px, py, t)             // gradient → "flow direction"
const hue = (baseHue + (ang / (Math.PI * 2)) * spread + 360) % 360
g.phase += 0.012 * opt.flicker
const breath = 0.5 + 0.5 * Math.sin(g.phase)
const light = Math.min(1.15, (0.14 + 0.86 * nv * nv) * (0.25 + 0.75 * breath) * opt.brightness)
ctx.fillStyle = `hsl(${hue.toFixed(1)} ${(sat*100).toFixed(0)}% ${Math.min(100, 30 + 55*light).toFixed(0)}%)`
ctx.globalAlpha = light > 1 ? 1 : light
ctx.fillRect(g.x - cell/2, g.y - cell/2, cell, cell)
```

---

## 3. Engine B — Disturbance wave (useDisturbanceWave)

Designed as the *calm, non-abrupt* counterpoint: **every pixel is the same size, position fixed**,
only brightness + color vary. This is the "方块大小要一样、不能太突兀" iteration outcome — do **not**
add per-pixel size / spread here.

**Dual-noise-field layering** — two independent, differently-paced fBm fields sample each pixel:
```js
const t  = time * (0.05 + opt.flowSpeed * 0.8)   // brightness field time (fast drift)
const tc = time * (0.03 + opt.flowSpeed * 0.5)   // color field time (slower, reverse drift)
const nv = fbm(g.x * 0.012 + t,  g.y * 0.012 + t * 0.7)   // brightness field (higher freq)
const cn = fbm(g.x * 0.006 + tc, g.y * 0.006 - tc * 0.5)  // color field (lower freq)
```
- **Brightness field** → fine light/dark blobs wandering across the grid.
- **Color field** → smooth gradient between **warm off-white `#f8f6e8`** and the **theme primary**
  color (from `hue`): `colorLerp(cn, main)` where `main = hsv2rgb(hue%360, 0.55, 0.9)`.
- **Breathing tide** — whole-screen slow luminance swell: `tide = 0.5 + 0.5*sin(time*0.015*flicker)`.
- **Soft luminance** — `light = (0.06 + 0.42*nv) * (0.85 + 0.15*tide)` then `globalAlpha = min(1, light*brightness)`.
- Background is solid `#000`; **no mouse interaction**.

**Flicker is a speed, not an intensity**: `flicker` scales the tide *velocity* (`0 = frozen`),
so a "呼吸频率" slider maps directly to it.

---

## 4. Parameter schema (the copy-params JSON)

The full 9-field settings object — this exact JSON is what `geek-copy-params` copies, and the
engine consumes the subset it needs (extra keys are ignored):

```json
{
  "flowMode": "noise",      // noise | wave | vortex | disturb
  "hue": 155,               // 基色相（0-360；theme chips preset: green 155 / cyan 185 / magenta 320 / teal 168 / amber 40 / blue 215）
  "hueSpread": 46,          // 流向色相偏移范围(°) —— engine A only
  "flowSpeed": 0.06,        // 流场漂移速度 (0-0.3)
  "flicker": 1.4,           // 呼吸闪烁频率/潮汐速度 (0-6)
  "brightness": 1.0,        // 整体亮度倍率 (0.2-1.8)
  "mouse": "swirl",         // swirl | repel | off —— engine A only
  "cellSize": 10,           // 方块尺寸 px (4-24)
  "gap": 2                  // 方块间隙 px (0-8)
}
```

Grid sizing guard shared by both engines: `maxPixels ≈ 4500`; if `cols*rows` exceeds it, pitch is
scaled up by `√(cols*rows/maxPixels)` so big screens stay smooth. `cellSize`/`gap`/`maxPixels`
changes rebuild the grid (`buildGrid()`).

---

## 5. Control-panel UI & interaction style (geek-locked)

The demo panel is itself a mini geek component kit — reuse these when a spec asks for a
"live parameter panel over a canvas background". All colors map to the standard geek tokens
(`--geek-color-bg`, `--geek-color-bg-soft`, `--geek-color-line`, `--geek-color-accent` for the
hue-driven accent).

| Piece | Recipe |
|-------|--------|
| `.panel` | bottom-right, `width: 292px`, `max-height: 82vh`, `background: color-mix(bg-soft 84%, transparent)`, `border: 1px line`, `backdrop-filter: blur(10px)`, card shadow, radius 0, mono type, `letter-spacing: .2em` |
| `.panel__head` | collapsible (click to close), accent-colored, `letter-spacing: .2em` |
| `.row` | one labeled slider per param: label left, live `.val` right (accent), `input[type=range]` below — 2px hairline track, **square** 10px thumb (`border-radius: 0`), accent fill |
| `.seg` | segmented choice control: grid of equal buttons, `.active` = accent text + `color-mix(accent 12%, transparent)` bg + stronger border |
| `.theme-chip` | hue preset chips; `.active` uses per-chip `--chip` var for a `color-mix` wash |
| `.disturb-note` | contextual explainer strip (10px muted, hairline border) shown only in `disturb` mode |
| `.disabled` | `opacity: .4; pointer-events: none` on rows/controls that don't apply to the current engine |
| `.gear` | when panel closed: a small "⚙ 控制" button in the same corner to reopen |
| scrollbar | 6px, hairline thumb (`--geek-color-line-strong`) |

Interaction contract: **every setting applies live** (deep-watch → `setOptions`); the mode
selector (`flowMode`) hot-swaps the engine; controls irrelevant to the active mode get the
`.disabled` treatment instead of being hidden.

---

## 6. `geek-copy-params` — 复制参数交互

One button that serializes the whole settings object and copies it to the clipboard, so a user
can **paste it back to the agent to reproduce the exact effect** ("复制参数 → 粘贴给 agent → 复现").

```js
async function copyParams(settings) {
  const json = JSON.stringify(settings, null, 2)
  try {
    await navigator.clipboard.writeText(json)
  } catch {
    // non-secure context (http, not localhost) fallback
    const ta = document.createElement('textarea')
    ta.value = json
    ta.style.position = 'fixed'; ta.style.opacity = '0'
    document.body.appendChild(ta); ta.select()
    document.execCommand('copy'); ta.remove()
  }
  copied.value = true
  setTimeout(() => (copied.value = false), 1500)
}
```

Button UX: text `复制参数` → `✓ 已复制` for ~1.5s; success state = accent border + `color-mix`
wash (`.btn.geek-copy-params.copied`). Emit the **full** settings object (engines ignore keys they
don't consume) so the same JSON works for any mode.

---

## 7. Gotcha — signed-shift noise bias (`>>` vs `>>>`)

The value-noise `hash2` must use **unsigned** `>>>` when normalizing:

```js
// WRONG — arithmetic shift biases output to [0, 0.5): avg ≈ 0.25, max 0.5
h = h ^ (h >> 13) ... ; return h / 4294967295
// CORRECT — zero-fill shift keeps full 0..1 range: avg ≈ 0.5
h = h ^ (h >>> 13) ... ; return (h ^ (h >>> 16)) >>> 0 / 4294967295
```

With the biased hash, an `fbm`-driven brightness gate only lights ~16% of the grid (values above
~0.5 threshold are rare) — the effect looks dead. Symptom: "global disturbance field barely lights
any pixels". Both engines ship the fixed `>>>` version. If you ever copy this noise out, verify the
shifts.

---

## 8. Performance & correctness guards (all engines)

- **DPR** capped at `2` (`Math.min(devicePixelRatio || 1, 2)`), `canvas.width = w*dpr`, `ctx.setTransform(dpr,0,0,dpr,0,0)`.
- **`maxPixels`** ceiling (~4500) with automatic grid thickening on big screens / small cells.
- **Resize** rebuilds the grid; engine re-parented via `canvas.parentElement.getBoundingClientRect()`.
- **`prefers-reduced-motion: reduce`** → draw exactly **one static frame** (engine B uses the
  current noise offset; engine A sets `time = 1.5` for a nonzero field) and no rAF loop.
- **`document.hidden`** → skip `draw()` while hidden (rAF throttles naturally), still reports stats.
- Frame delta clamped to `dt = min(dtMs/16.7, 2)` so tab switches don't explode the animation.
