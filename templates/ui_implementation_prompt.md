# Pixel Data Stream UI Implementation Prompt

> Universal template for generating pixel data stream CSS/component implementations (pixel data stream style) with consistent style across all components.

---

## 1. Theme Definition

```
Theme:       [name]
Interface:   [login page / dashboard / settings / ...]
Framework:   [vue / react / plain / mini-program]
Style:       [pixel data stream / 像素数据流 / retro terminal]
Corner:      [0]px (boxes; dots 50%, scrollbars 8px, code 2px)
Border:      [1]px hairline per component type
Spacing:     integer px, loose (base [N]px)

Palette (≤ [N] colors):
  background   → #[hex]   /* light canvas, default #f8f9fa */
  surface      → #[hex]   /* default #e9ecef */
  line         → #[hex]   /* default #dee2e6 */
  blue-accent  → #[hex]   /* primary, default #3b82f6 */
  text         → #[hex]   /* default #1e293b */
  text-secondary→ #[hex]  /* default #475569 */
  text-muted   → #[hex]   /* default #94a3b8 */
  teal         → #[hex]   /* success / 研究, default #10b981 */
  purple       → #[hex]   /* info, default #8b5cf6 */
  amber        → #[hex]   /* warn, default #f59e0b */
  crimson      → #[hex]   /* danger, default #ef4444 */
  ...
```

## 2. Style Lock (ALL components)

```
- Corner radius: 0px on boxes (dots 50%, scrollbars 8px, code 2px)
- 1px hairline borders, consistent per component type
- Soft shadows + neon glows allowed: card 0 8px 32px rgba(0,0,0,.45),
  glow 0 0 24px rgba(59,130,246,.45)
- Gradients allowed (grid lines, CRT scanlines, radial glows)
- filter: blur / backdrop-filter allowed (blurred nav)
- Fractional opacity allowed (scanlines .025, glows .45)
- Spacing: integer px (loose, no strict grid)
- Colors from declared palette ONLY
- Class prefix `geek-`, custom properties `--geek-*`
- Motion: smooth ease (.2s colors / .3s transform / .6s zoom / .8s reveal);
  typewriter caret & glitch use steps(1); reduced-motion fallback mandatory
- Signature motifs MUST be used: `.corner` blue brackets on cards,
  `//` eyebrow labels, CRT scanlines, typewriter caret, glowing dots
```

## 3. Custom Properties (`:root`)

```
:root {
  --geek-color-bg:        #[hex];   /* default #f8f9fa */
  --geek-color-bg-soft:   #[hex];   /* default #e9ecef */
  --geek-color-line:      #[hex];   /* default #dee2e6 */
  --geek-color-blue:      #[hex];   /* default #3b82f6 */
  --geek-color-blue-soft: rgba(59, 130, 246, .13);
  --geek-color-text:      #[hex];   /* default #1e293b */
  --geek-color-text-dim:  #[hex];   /* default #475569 */
  --geek-color-text-mute: #[hex];   /* default #94a3b8 */
  --geek-color-teal:      #[hex];   /* default #10b981 */
  --geek-color-purple:    #[hex];   /* default #8b5cf6 */
  --geek-color-amber:     #[hex];   /* default #f59e0b */
  --geek-color-crimson:   #[hex];   /* default #ef4444 */

  --geek-font-mono: "JetBrains Mono","Fira Code",Consolas,...,monospace;
  --geek-font-sans: "Inter",-apple-system,...,"PingFang SC",sans-serif;

  --geek-space-1: [N]px; ... --geek-space-6: [N*6]px;
  --geek-radius: 0px;
  --geek-border: 1px;

  --geek-shadow-glow: 0 0 24px rgba(59, 130, 246, .45);
  --geek-shadow-card: 0 8px 32px rgba(0, 0, 0, .45);
  --geek-shadow-card-hover: 0 12px 40px rgba(0, 0, 0, .55);

  --geek-motion-color: .2s ease;
  --geek-motion-transform: .3s ease;
  --geek-motion-zoom: .6s ease;
  --geek-motion-reveal: .8s ease;

  /* dynamic effects (see references/dynamic-effects.md) */
  --geek-motion-wipe:    .4s ease;
  --geek-motion-rise:    .8s ease;
  --geek-motion-marquee: 8s linear infinite;
  --geek-motion-parallax: 3s ease;
  --geek-parallax-x:     0px;   /* pointer X → layer drift (written by JS) */
  --geek-parallax-rot:   0deg;  /* pointer Y → bg rotation, capped ±15deg */
  --geek-stagger:        120ms;
  --geek-rise-height:    100%;
}
```

## 4. Component-by-Component Spec

### A. Buttons — `geek-btn`

| State | Value |
|-------|-------|
| base | `font-family: mono; font-size:14px; letter-spacing:.08em; background: transparent; border:1px solid text; radius 0; padding:14px 22px;` |
| hover | `transform: translateY(-2px);` (primary inverts: white bg + blue text + glow) |
| active | `transform: translateY(0);` |
| focus-visible | `outline: 3px solid blue; outline-offset: 2px;` |
| disabled | `opacity:.5; cursor: not-allowed;` |

Variants: `--primary` (blue fill), `--ghost` (hover `#ffffff14` + blue border), `--danger` (crimson). Sizes: `--sm` / `--lg`.

### B. Cards / Windows — `geek-card` / `geek-panel` / `geek-window`

| Class | Rule |
|-------|------|
| `geek-card` | `position:relative; bg-soft; 1px line; radius 0; card shadow`; hover `translateY(-4px)` + blue border; `.corner` brackets |
| `.corner` | 14×14 blue L-brackets (top-left `:before` + bottom-right `:after`) |
| `geek-window` | like card + `overflow:hidden`; `__title` = 4px blue top bar + mono title |
| `geek-tag` | mono 12px, radius 0, status color + 13% alpha soft bg |

### C. Eyebrow / Timeline / Typewriter / Backgrounds

| Class | Recipe |
|-------|--------|
| `geek-eyebrow` | mono 13px blue `.18em` uppercase; `:before` = 28px blue line; text begins with `//` |
| `geek-timeline` | blue vertical gradient line + 11px glowing blue dot (`0 0 14px`) |
| `geek-typewriter__caret` | `▌` blue, `1s steps(1) infinite` blink |
| `geek-bg--scanline` | `repeating-linear-gradient(0deg, rgba(255,255,255,.025) 0 1px, transparent 1px 3px)` |
| `geek-bg--grid` | 56px `linear-gradient` lines |
| `geek-glitch` | blue + teal clip-path slices, `mix-blend-mode: screen` |

### D. Interaction Animations

| Keyframe | Recipe |
|----------|--------|
| `geek-blink` | `50% { opacity: 0 }`, `1s steps(1) infinite` |
| `geek-fade-up` | opacity 0→1 + translateY(24px)→0, `.8s ease` (scroll reveal) |
| `geek-glitch-a/b` | clip-path slices + translate, `3s steps(1) infinite` |
| `geek-rise` | translateY(var(--geek-rise-height))→0 + opacity 0→1, `--geek-motion-rise`, delay `calc(var(--i) * var(--geek-stagger))` |
| `geek-marquee-x/y` | `to { transform: translateX(-50%) }` / `translateY(-50%)`, `--geek-motion-marquee` |

### E. Dynamic Effects (recipes in `references/dynamic-effects.md` / `references/background-fluid-grid.md`)

| Effect | Recipe |
|--------|--------|
| `geek-btn-wipe` | `overflow:hidden`; `:before`/`:after` layers at `translateX(-100%)` → wipe to `0` on hover, `:after` delayed `.1s`; label `-13%→0` + color flip; icon `320%→550%` |
| `geek-float-parallax` | layers at opposite corners inside `overflow:hidden`; on pointermove write `--geek-parallax-x`/`--geek-parallax-rot`; bg `rotate(var(--geek-parallax-rot))`, big layer `translateX(var(--geek-parallax-x))`, small layer `translateX(calc(var(--geek-parallax-x) * -1))`, all `--geek-motion-parallax`; JS skips under reduced-motion |
| `geek-float-rise` | container `overflow:hidden`; tiles `translateY(var(--geek-rise-height))`; `.geek-float-rise--active img` animates `geek-rise` with `--i` stagger; GSAP variant `power3.out` + `stagger:.1` |
| `geek-particle-bg` | canvas 2D pixel **squares** (`fillRect`, integer 1–3px) in palette colors; proximity links under `linkDist` (alpha fades with distance); mouse repel radius + cyan cursor links; DPR capped 2; rAF loop; static frame under reduced-motion |
| `geek-marquee` | duplicate content in one track, `translate(-50%)` for seamless loop; `--up/--down/--left/--right` directions |
| `geek-crt-ripple` | SVG `feTurbulence` + `feDisplacementMap`; rAF loop nudges `seed`/`scale`; `filter: url(#geek-crt-ripple)` |
| `geek-fluid-grid` | Canvas 2D + rAF; fixed grid `cellSize`+`gap`, `maxPixels≈4500` auto-thicken; value-noise fBm flow (`noise`/`wave`/`vortex`), `flowAngle` gradient → hue shift `baseHue + (ang/2π)*hueSpread`, per-pixel breathing phase, mouse swirl-repel (engine A); engine B = uniform pixels, dual-noise fields (`nv` brightness `fbm .012`, `cn` color `fbm .006`), `colorLerp` off-white `#f8f6e8` ↔ theme primary (HSV `.55/.9`), tide `0.5+0.5*sin(t*0.015*flicker)`; DPR≤2 — recipe in `references/background-fluid-grid.md` |
| `geek-copy-params` | click serializes full settings `JSON.stringify(s, null, 2)` → `navigator.clipboard` (fallback: textarea + `execCommand('copy')`); button flips `复制参数 → ✓ 已复制` for 1.5s; success = accent border + `color-mix` wash |
| reduced-motion | kill all animations/transitions, reveal final states (`transform: translateX(0)` / `translateY(0)` / opacity 1); canvas backgrounds render one static frame |

## 5. Output Format

```
File: theme.css (or components/buttons.css, backgrounds.css, windows.css, animations.css)
Custom properties first in :root, then components grouped by family
Include a `prefers-reduced-motion` fallback block
No external dependencies; plain CSS unless framework requested
```
