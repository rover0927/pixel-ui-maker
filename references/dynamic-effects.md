# Dynamic Effects Kit — 动态效果组件库

> Distilled motion recipes for the dark-terminal geek style. Three flagship effects distilled
> from the **JIEJOE** design portfolio (jiejoe.com): background pixel-art **parallax float**,
> menu pixel-art **stagger rise**, and a dual-layer **wipe** button. Re-themed to the geek lock
> (olive dark + signal red, 0px corners, hairline borders, ease motion). Both a pure-CSS and a
> GSAP version are provided for the flagship effects, plus a canvas **pixel-particle network**
> (`geek-particle-bg`, from the《粒子背景动画效果实现指南》particle guide, *not* JIEJOE) and a
> compact marquee / CRT-ripple bonus set.

---

## 0. Source Analysis (蒸馏来源)

These recipes were distilled from `HOME - JIEJOE _ 视觉设计者.html` / its compiled CSS:

| JIEJOE effect | Where it lived | What it does | Distilled as |
|---------------|----------------|--------------|--------------|
| **首页背景视差浮动** | `.home_welcome_background` + GSAP `move_ball()` | 2 blurballs (big+small) float in the hero bg; on `mousemove` the whole background **rotates ±15° by mouse Y** while the big ball drifts right / small ball drifts left by a normalized mouse X — soft `power3.out`, `3s` lag | `geek-float-parallax` |
| **菜单像素画上浮** | `menubox_menu_backg img` + GSAP `menu.show()` | 4 pixel-art images hidden at `translateY(100%)`; on menu open they **rise in sequence** (`stagger .1s`, `power3.out`, `.8s`) | `geek-float-rise` |
| **CONTACT 按钮双层擦除** | `.menubox_navigation_contact:before/:after` | on hover two pseudo-element layers **wipe in from the left** (`translateX(-100%)→0`), second layer delayed `.1s`; label slides center + flips color, arrow slides right | `geek-btn-wipe` |
| 四向滚动光带 (bonus) | `.photos_draglines_*` / `home_vision_scrolllines` | green strips of text+icons scroll **8s linear infinite** in 4 directions | `geek-marquee` |
| CRT 水波纹 (bonus) | `videos_resources_wave_screen` SVG filter + rAF | `feTurbulence` + `feDisplacementMap` ripple driven by random seed/scale each frame | `geek-crt-ripple` |

> **Two different background effects, don't conflate them.** `geek-float-parallax` (this doc §4)
> is the *continuous* hero-background float — layers drift with the pointer, always on. `geek-float-rise`
> (§3) is the *one-shot* entrance of menu/section pixel-art — items rise in a wave when the panel
> opens. If you want "背景像素画浮动", that's `geek-float-parallax`.

> **`geek-particle-bg` (this doc §5) is NOT from JIEJOE.** It's a canvas pixel-particle network
> distilled from the《粒子背景动画效果实现指南》(position / velocity / size / color / lifetime,
> mouse interaction, proximity links) and re-themed to the geek lock — pixels are drawn as
> **0px-corner squares** (`fillRect`, integer 1–3px), colors come only from the theme palette,
> and it layers *underneath* `geek-float-parallax` in the hero. Pure Canvas 2D, no libraries.

All four are pure CSS except the GSAP variant of `geek-float-rise` and the ripple driver
(one `requestAnimationFrame` loop). No external libraries required for the CSS versions.

---

## 1. Motion Variables (add to `:root`)

```css
:root {
  /* dynamic-effects motion contract */
  --geek-motion-wipe:    .4s ease;              /* layer wipe on geek-btn-wipe */
  --geek-motion-rise:    .8s ease;              /* float-rise entrance (jiejoe .8s) */
  --geek-motion-marquee: 8s linear infinite;    /* scrolling strips (jiejoe 8s) */
  --geek-stagger:        120ms;                 /* per-item stagger step (jiejoe .1s) */
  --geek-rise-height:    100%;                  /* distance items rise from (jiejoe 100%) */
  --geek-motion-parallax: 3s ease;              /* parallax lag (jiejoe power3.out 3s) */
  --geek-parallax-x:     0px;                   /* pointer X → layer drift (written by JS) */
  --geek-parallax-rot:   0deg;                  /* pointer Y → bg rotation, capped ±15deg */
  /* palette already in use: --geek-color-bg, -bg-soft, -line, -red, -text, ... */
}
```

---

## 2. `geek-btn-wipe` — 双层擦除按钮 (from JIEJOE CONTACT)

**Mechanism.** The button is `overflow:hidden`. Two pseudo-element layers sit at
`translateX(-100%)` (off-screen left). On hover they sweep to `translateX(0)` in sequence —
layer `:before` first (no delay), layer `:after` **.1s later** — so the accent layer visibly
"chases" the base layer across the slab. The mono label slides from `-13%` to center while
flipping color; the arrow icon slides from `+320%` to `+550%`. All in `.4s ease`.

**CSS.**

```css
.geek-btn-wipe {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 14px 22px;
  font-family: var(--geek-font-mono);
  font-size: 14px;
  letter-spacing: .08em;
  color: var(--geek-color-red);              /* red label on transparent slab */
  background: transparent;
  border: 1px solid var(--geek-color-red);
  border-radius: 0;                          /* sharp — geek lock */
  cursor: pointer;
  overflow: hidden;                          /* clip the wipe layers */
  transition: color var(--geek-motion-wipe);
}
.geek-btn-wipe:before,
.geek-btn-wipe:after {
  content: "";
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  transform: translateX(-100%);
  z-index: 0;
}
.geek-btn-wipe:before { background: var(--geek-color-bg-soft); transition: transform var(--geek-motion-wipe); }
.geek-btn-wipe:after  { background: var(--geek-color-red);     transition: transform var(--geek-motion-wipe) .1s; } /* chase */
.geek-btn-wipe:hover:before,
.geek-btn-wipe:hover:after { transform: translateX(0); }
.geek-btn-wipe:hover:after  { transition-delay: .1s; }

.geek-btn-wipe__label {
  position: relative; z-index: 1;
  transform: translateX(-13%);               /* jiejoe: slide from offset */
  transition: color var(--geek-motion-wipe), transform var(--geek-motion-wipe);
}
.geek-btn-wipe__icon {
  position: relative; z-index: 1;
  width: 14px; height: 14px;
  transform: translateX(320%);               /* jiejoe: arrow off-screen right */
  transition: transform var(--geek-motion-wipe);
}
.geek-btn-wipe__icon line,
.geek-btn-wipe__icon polyline {
  fill: none; stroke: var(--geek-color-text);
  stroke-width: 8; stroke-linecap: round;
}
.geek-btn-wipe:hover .geek-btn-wipe__label { color: var(--geek-color-text); transform: translateX(0); }
.geek-btn-wipe:hover .geek-btn-wipe__icon  { transform: translateX(550%); }

.geek-btn-wipe:focus-visible { outline: 3px solid var(--geek-color-red); outline-offset: 2px; }
.geek-btn-wipe:active .geek-btn-wipe__label,
.geek-btn-wipe:active .geek-btn-wipe__icon { transition-duration: .2s; }
```

**Markup.**

```html
<button class="geek-btn-wipe" type="button">
  <span class="geek-btn-wipe__label">CONTACT</span>
  <svg class="geek-btn-wipe__icon" viewBox="0 0 50 50" aria-hidden="true">
    <polyline points="12,25 38,25" />
    <polyline points="28,15 38,25 28,35" />
  </svg>
</button>
```

**Sequence (hover):**
1. `:before` (olive surface) sweeps in from left — `.4s ease`, delay 0.
2. `:after` (signal red) chases it — `.4s ease`, delay `.1s`. Slab ends solid red.
3. Label `CONTACT` slides from `-13%` to center, flips red → white.
4. Arrow slides `320% → 550%`, white stroke.

**Tuning.** Layer order, chase delay and colors are the "signature" — keep two contrasting
layers and a visible stagger (`.1s–.15s`). Source values: jiejoe used `border-radius:1.5rem`
pill, `.4s ease`, `.1s` chase, white→green layers. The geek version sharpens corners to 0px
and uses red as the accent layer.

---

## 3. `geek-float-rise` — 背景像素画浮动上浮 (from JIEJOE menu)

**Mechanism.** A stack of background images (pixel-art tiles, logos, glyphs) starts hidden
`translateY(var(--geek-rise-height))` inside an `overflow:hidden` container. When the
containing panel opens / a section scrolls into view, the images **rise to `translateY(0)`
one after another** — `calc(var(--i) * var(--geek-stagger))` delay per item. The stagger is
the soul: items arrive in a wave, not together.

### 3.1 Pure CSS (no dependencies)

```css
.geek-float-rise {
  position: absolute;
  overflow: hidden;                          /* clip the rising tiles */
  pointer-events: none;
  /* size + offset set by the theme (e.g. right:0; bottom:0; width:480px; height:360px) */
}
.geek-float-rise img {
  position: absolute;
  opacity: 0;
  transform: translateY(var(--geek-rise-height));
  will-change: transform, opacity;
}
/* active = panel open / in viewport; toggle via class, IntersectionObserver, or :target */
.geek-float-rise--active img {
  animation: geek-rise var(--geek-motion-rise) both;
  animation-delay: calc(var(--i) * var(--geek-stagger));
}
@keyframes geek-rise {
  from { transform: translateY(var(--geek-rise-height)); opacity: 0; }
  to   { transform: translateY(0);                       opacity: 1; }
}
```

**Markup.** Position each tile with inline placement and index `--i` (0-based stagger order):

```html
<div class="geek-float-rise geek-float-rise--active">
  <img src="tile_1.png" alt="" style="--i:0; top:12%; left:15%; width:120px;">
  <img src="tile_2.png" alt="" style="--i:1; top:0;   right:2%; width:140px;">
  <img src="tile_3.png" alt="" style="--i:2; top:44%; left:7%;  width:100px;">
  <img src="tile_4.png" alt="" style="--i:3; bottom:-4%; right:-3%; width:180px;">
</div>
```

### 3.2 GSAP variant (matches the original jiejoe menu exactly)

```js
gsap.set(tiles, { yPercent: 100 });                       // hidden below container
gsap.timeline()
  .to(panel,  { y: 0, duration: 1, ease: "power4.out" }) // panel slides up
  .to(tiles,  { y: 0, duration: .8, ease: "power3.out", stagger: .1 }, "<"); // tiles rise in a wave
```

`power3.out` + `stagger:.1` is the jiejoe feel — slightly bouncy ease-out, items land in a
soft wave. For the geek lock (no elastic overshoot) keep `power2/power3.out` and stagger
`.08s–.12s`.

**Reveal trigger.** Toggle `.geek-float-rise--active` when the host panel opens (menu, modal,
accordion) or via an `IntersectionObserver` for scroll-entrance:

```js
const io = new IntersectionObserver(entries => {
  entries.forEach(e => e.target.classList.toggle("geek-float-rise--active", e.isIntersecting));
}, { threshold: .3 });
io.observe(document.querySelector(".geek-float-rise"));
```

---

## 4. `geek-float-parallax` — 背景像素画视差浮动 (from JIEJOE home hero)

**Mechanism.** The hero background is a stack of pixel-art / decoy layers (JIEJOE uses two
"blurballs"). On `pointermove` over the host section the whole background **rotates ±15°** by
mouse Y, while the big layer drifts **with** the cursor and the small layer drifts **against**
it by a normalized mouse-X factor — that opposition is what sells the parallax depth. Every
tween eases **`power3.out`, `3s`**, so the float always *lags* behind the cursor and keeps
drifting a moment after it stops. The "floating" feel comes from the lag, not the distance.

```js
// jiejoe source (a GSAP timeline built per move)
const t  = (mouseX - innerWidth/2) / (innerWidth/innerHeight * 5); // normalized drift
const rt = mouseY / innerHeight * 30 - 15;                          // -15..15 deg
gsap.timeline()
  .to(bg,    { rotate: rt+"deg", duration: 3, ease: "power3.out" })
  .to(big,   { x: t+"px",        duration: 3, ease: "power3.out" }, "<")
  .to(small, { x: -t+"px",       duration: 3, ease: "power3.out" }, "<");
```

### 4.1 Pure CSS (no dependencies)

Same feel with CSS custom properties + `transition`. A pointermove handler writes two vars; the
layers read them and transition slowly (`3s ease` ≈ `power3.out`).

```css
.geek-float-parallax {
  position: absolute; inset: 0; overflow: hidden; pointer-events: none;
}
.geek-float-parallax__bg {            /* the whole canvas — rotates with mouse Y */
  position: absolute; inset: -3%;     /* bleed hides rotation edges */
  transform: rotate(var(--geek-parallax-rot, 0deg));
  transition: transform var(--geek-motion-parallax);
  will-change: transform;
}
.geek-float-parallax__layer {         /* each floating tile */
  position: absolute;
  transition: transform var(--geek-motion-parallax); /* the lag IS the float */
  will-change: transform;
}
.geek-float-parallax__layer--l {      /* big layer — drifts with the cursor */
  left: -6%; bottom: -6%; width: 42vw;
  transform: translateX(var(--geek-parallax-x, 0px));
}
.geek-float-parallax__layer--r {      /* small layer — drifts opposite (depth) */
  right: -4%; top: -4%; width: 26vw;
  transform: translateX(calc(var(--geek-parallax-x, 0px) * -1));
}
```

```js
const host = document.querySelector(".geek-hero");        // the parallax host section
const px   = document.querySelector(".geek-float-parallax");
function onMove(e) {
  const pt = e.touches ? e.touches[0] : e;
  const dx = (pt.clientX - innerWidth/2) / (innerWidth/innerHeight * 5);
  const rt = pt.clientY / innerHeight * 30 - 15;
  px.style.setProperty("--geek-parallax-x",   dx + "px");
  px.style.setProperty("--geek-parallax-rot", rt + "deg");
}
host.addEventListener("mousemove", onMove);
host.addEventListener("touchmove", onMove, { passive: true });
```

**Markup** — layers are pixel-art tiles / decoy glyphs, sized large and bled off the edges:

```html
<div class="geek-hero">
  <div class="geek-float-parallax">
    <div class="geek-float-parallax__bg">
      <img class="geek-float-parallax__layer geek-float-parallax__layer--l" src="tile_big.png" alt="">
      <img class="geek-float-parallax__layer geek-float-parallax__layer--r" src="tile_small.png" alt="">
    </div>
  </div>
  <!-- hero content … -->
</div>
```

### 4.2 GSAP variant (matches the original exactly)

```js
const tl = gsap.timeline();
function onMove(e) {
  const pt = e.touches ? e.touches[0] : e;
  const dx = (pt.clientX - innerWidth/2) / (innerWidth/innerHeight * 5);
  const rt = pt.clientY / innerHeight * 30 - 15;
  tl.to(bg,  { rotate: rt+"deg", duration: 3, ease: "power3.out" }, 0)
    .to(big, { x: dx+"px",       duration: 3, ease: "power3.out" }, 0)
    .to(sma, { x: -dx+"px",      duration: 3, ease: "power3.out" }, 0);
}
host.addEventListener("mousemove", onMove);
```

**Tuning.** Two layers at opposite corners is enough for depth; add a mid-size third layer for
more. Keep the rotation cap at `±15deg` and `3s` lag — that lag is the signature. `power3.out`
means ease-out only, no elastic overshoot (geek lock). Skip the handler under
`prefers-reduced-motion` — layers stay at their static positions.

---

## 5. `geek-particle-bg` — 背景像素粒子网络 (from 粒子指南 × geek lock)

**Mechanism.** A `<canvas>` field of pixel-square particles drifts slowly (ease feel, no
jitter). Particles closer than `linkDist` get linked by semi-transparent lines whose alpha
fades with distance — the classic network look. The cursor pushes particles out of a small
radius (repel), while particles within `mouseLinkDist` draw a cyan link to it. Particles are
drawn as axis-aligned **squares** (`fillRect`) with a soft halo square behind — 0px corners,
integer sizes 1–3px, matching the pixel-art theme. One `requestAnimationFrame` loop, no
libraries.

### 5.1 Engine (Canvas 2D composable)

```js
// Tuning surface (defaults) — palette colors MUST come from the theme :root
const DEFAULTS = {
  colors:        ['#00f0ff', '#ff2bd6', '#00ffd5', '#e6f1ff', '#2e7dff'],
  maxCount:      170,    // cap; actual = clamp(area/14000, 30, maxCount)
  linkDist:      120,    // particle↔particle link threshold (px)
  mouseLinkDist: 200,    // cursor↔particle link threshold (px)
  mouseRepel:    52,     // repel radius (px)
  maxSpeed:      0.6,    // max float speed (px/frame)
  particleAlpha: 0.9,    // core square opacity cap
  linkAlpha:     0.16,   // link line opacity cap
};

function makeParticle(w, h, colors, maxSpeed) {
  return {
    x: Math.random() * w, y: Math.random() * h,
    vx: (Math.random() * 2 - 1) * maxSpeed,
    vy: (Math.random() * 2 - 1) * maxSpeed,
    size: 1 + Math.floor(Math.random() * 3),            // 1..3px squares
    color: colors[(Math.random() * colors.length) | 0],
    alpha: 0.35 + Math.random() * 0.55,
    phase: Math.random() * Math.PI * 2,                 // sine-sway phase
  };
}

function step(particles, dt, w, h, mouse, repel) {      // drift + sway + slow float up
  for (const p of particles) {
    p.phase += 0.012 * dt;
    p.x += p.vx + Math.sin(p.phase) * 0.15;
    p.y += p.vy - 0.04 * dt;
    if (p.x < -8) p.x = w + 8; else if (p.x > w + 8) p.x = -8;   // wrap w/ bleed
    if (p.y < -8) p.y = h + 8; else if (p.y > h + 8) p.y = -8;
  }
  if (mouse.active) {                                   // mouse repel
    for (const p of particles) {
      const dx = p.x - mouse.x, dy = p.y - mouse.y, d2 = dx * dx + dy * dy;
      if (d2 < repel * repel && d2 > 0.01) {
        const d = Math.sqrt(d2), f = (1 - d / repel) * 0.6;
        p.x += (dx / d) * f; p.y += (dy / d) * f;
      }
    }
  }
}

function draw(ctx, parts, w, h, mouse, linkDist, linkAlpha) {
  ctx.clearRect(0, 0, w, h);
  ctx.lineWidth = 1;
  const ld = linkDist;
  for (let i = 0; i < parts.length; i++) {              // proximity links (O(n²), thresholded)
    const a = parts[i];
    for (let j = i + 1; j < parts.length; j++) {
      const b = parts[j], dx = a.x - b.x, dy = a.y - b.y, d2 = dx * dx + dy * dy;
      if (d2 < ld * ld) {
        ctx.globalAlpha = (1 - Math.sqrt(d2) / ld) * linkAlpha;
        ctx.strokeStyle = a.color;
        ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
      }
    }
  }
  if (mouse.active) {                                   // cursor links (cyan)
    for (const p of parts) {
      const dx = p.x - mouse.x, dy = p.y - mouse.y, d = Math.sqrt(dx * dx + dy * dy);
      if (d < linkDist * 1.6) {
        ctx.globalAlpha = (1 - d / (linkDist * 1.6)) * linkAlpha * 1.6;
        ctx.strokeStyle = '#00f0ff';
        ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(mouse.x, mouse.y); ctx.stroke();
      }
    }
  }
  for (const p of parts) {                              // halo square + core square
    ctx.fillStyle = p.color;
    ctx.globalAlpha = p.alpha * 0.18;
    ctx.fillRect(p.x - p.size - 2, p.y - p.size - 2, p.size * 2 + 4, p.size * 2 + 4);
    ctx.globalAlpha = p.alpha * 0.9;
    ctx.fillRect(p.x - p.size / 2, p.y - p.size / 2, p.size, p.size);
  }
  ctx.globalAlpha = 1;
}
```

Loop: `requestAnimationFrame` with a clamped dt (`(now-last)/16.7`, max 2); skip frames while
`document.hidden`; `resize` rebuilds width/height at `dpr = min(devicePixelRatio, 2)`.

### 5.2 Mouse wiring

Attach listeners to the **host section** (the canvas parent — they still fire over content
stacked above the canvas), then convert to canvas space:

```js
const host = canvas.parentElement;
function onMove(e) {
  const r = canvas.getBoundingClientRect();
  mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top;
  mouse.active = true;
}
host.addEventListener('mousemove', onMove);
host.addEventListener('mouseleave', () => (mouse.active = false));
```

### 5.3 Geek lock

- **Squares, not circles** — `fillRect`, integer sizes 1–3px; 0px corners is the style lock.
- Colors only from the theme palette (default = cyber-geek subset: cyan / magenta / teal /
  white / blue).
- Canvas CSS: `position:absolute; inset:0; width:100%; height:100%; pointer-events:none`,
  z-index **below** the parallax layer so `geek-particle-bg` + `geek-float-parallax` stack.
- DPR capped at 2; particle count scales with screen area (fewer on small screens — mobile-safe).
- `prefers-reduced-motion` → draw one static field, no loop (engine-side guard).

---

## 6. Bonus: `geek-marquee` — 四向滚动光带 (from JIEJOE draglines)

Seamless scrolling strips of mono text + glyphs, `8s linear infinite`. Duplicate the content
inside a single track and translate `-50%` for a gapless loop.

```css
.geek-marquee { position: absolute; overflow: hidden; pointer-events: none; }
.geek-marquee__track {
  display: flex; align-items: center;
  white-space: nowrap;
  animation: geek-marquee-x var(--geek-motion-marquee);
}
.geek-marquee--up    .geek-marquee__track,
.geek-marquee--down  .geek-marquee__track { animation-name: geek-marquee-y; }
.geek-marquee--right .geek-marquee__track { animation-direction: reverse; }
.geek-marquee--down  .geek-marquee__track,
.geek-marquee--left  .geek-marquee__track { animation-direction: reverse; }
.geek-marquee__item {
  display: inline-flex; align-items: center; gap: 24px;
  padding-right: 24px;
  font-family: var(--geek-font-mono);
  font-size: 24px; letter-spacing: .12em; color: var(--geek-color-text-mute);
}
.geek-marquee__item svg { width: 18px; height: 18px; }
@keyframes geek-marquee-x { to { transform: translateX(-50%); } }
@keyframes geek-marquee-y { to { transform: translateY(-50%); } }
```

**Markup** — repeat the group twice for a seamless loop:

```html
<div class="geek-marquee geek-marquee--up">
  <div class="geek-marquee__track">
    <span class="geek-marquee__item">PHOTOS →</span><span class="geek-marquee__item">PHOTOS →</span>
    <span class="geek-marquee__item">PHOTOS →</span><span class="geek-marquee__item">PHOTOS →</span>
    <!-- duplicate the same run again for -50% seamlessness -->
  </div>
</div>
```

---

## 7. Bonus: `geek-crt-ripple` — CRT 水波纹 (from JIEJOE video covers)

An SVG turbulence/displacement filter whose seed+scale are nudged every frame produces a
living CRT/water ripple over any element. The filter is pure SVG; the driver is one rAF loop.

```html
<svg width="0" height="0" aria-hidden="true" style="position:absolute">
  <defs>
    <filter id="geek-crt-ripple">
      <feTurbulence type="turbulence" baseFrequency="0 1" numOctaves="2" seed="1" result="n" stitchTiles="stitch" />
      <feDisplacementMap in="SourceGraphic" in2="n" scale="12" xChannelSelector="R" yChannelSelector="G" />
    </filter>
  </defs>
</svg>
```

```js
const el = document.querySelector(".geek-screen");
const turb = document.querySelector("#geek-crt-ripple feTurbulence");
const disp  = document.querySelector("#geek-crt-ripple feDisplacementMap");
(function ripple() {
  turb.setAttribute("seed", Math.random() * 100);
  disp.setAttribute("scale", 10 + Math.random() * 20);
  requestAnimationFrame(ripple);
})();
```

Apply with `.geek-screen { filter: url(#geek-crt-ripple); }`. Respect
`prefers-reduced-motion` and skip the rAF loop when the element is off-screen.

---

## 8. Reduced Motion (mandatory)

```css
@media (prefers-reduced-motion: reduce) {
  .geek-btn-wipe:before, .geek-btn-wipe:after,
  .geek-float-rise img, .geek-marquee__track,
  .geek-float-parallax__bg, .geek-float-parallax__layer {
    animation: none !important;
    transition: none !important;
  }
  .geek-btn-wipe:before, .geek-btn-wipe:after { transform: translateX(0); }  /* reveal final state */
  .geek-float-rise img { transform: translateY(0); opacity: 1; }
  .geek-float-parallax__bg   { transform: rotate(0deg); }   /* layers stay put */
  .geek-float-parallax__layer--l { transform: translateX(0); }
  .geek-float-parallax__layer--r { transform: translateX(0); }
}
```

`geek-float-parallax` also skips its pointermove binding under reduced-motion (JS-side guard).
`geek-particle-bg` draws a single static frame and does not start its rAF loop under
reduced-motion (engine-side guard — no CSS override needed, the canvas just sits still).

---

## 9. Style-Lock Checklist (for these effects)

- [ ] Colors only from declared palette (`--geek-color-*`) — no raw hex outside `:root`
- [ ] `border-radius: 0px` on boxes (button slab stays sharp)
- [ ] Integer px spacing; stagger/duration via `--geek-*` motion vars
- [ ] Mono font for button labels and marquee items
- [ ] Ease motion only (`.2s/.3s/.4s/.8s`; parallax lag `3s`); no bounce/elastic overshoot
- [ ] Every interactive element has hover/active/focus-visible states
- [ ] `geek-` prefix + `--geek-*` properties throughout
- [ ] `prefers-reduced-motion` fallback present
- [ ] `geek-float-parallax` layers at opposite corners, rotation capped `±15deg`, JS guard skips under reduced-motion
- [ ] `geek-particle-bg` pixels drawn as 0px-corner squares (`fillRect`, integer 1–3px), colors from theme palette only
- [ ] `geek-particle-bg` sits below `geek-float-parallax`; DPR capped at 2; rAF skips when `document.hidden`; static frame under reduced-motion
