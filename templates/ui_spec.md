# <Theme Name> — Pixel Data Stream UI Design Spec

> Human-readable pixel data stream design specification (pixel data stream style). Input for CSS implementation generation.

---

## I. Theme Information

| Field | Value |
|-------|-------|
| **Name** | |
| **Target Interface** | e.g., Login page / Dashboard / Settings panel |
| **Platform / Framework** | Vue / React / Plain HTML+CSS / Mini-program |
| **Geek Style** | pixel data stream / 像素数据流 / Retro terminal / Custom |
| **Spacing base** | e.g., 4px (integer px, loose — not enforced as a strict grid) |
| **Target Use** | Web app / Student-club site / Portfolio / Demo |

---

## II. Visual Description

```
[Detailed visual description of the interface]

- Overall mood: [e.g., pixel data stream, light canvas + signal blue accent]
- Layout structure: [header / sidebar / content split, etc.]
- Component list: [buttons, cards, tags, windows, nav, timeline, modals, ...]
- Distinctive features: [blue corner brackets, // eyebrow labels, CRT scanlines,
  glitch title, typewriter caret, glowing timeline nodes]
- Background treatment: [flat / scanlines / 56px grid / radial glow]
```

---

## III. Color Palette

| Index | HEX | Role | Used On |
|-------|-----|------|---------|
| 0 | #______ | Background | Page / app root (`--geek-color-bg`) |
| 1 | #______ | Surface | Panels, cards, windows (`--geek-color-bg-soft`) |
| 2 | #______ | Line / border | Hairline 1px borders (`--geek-color-line`) |
| 3 | #______ | Blue accent | Primary buttons, active nav, corner brackets (`--geek-color-blue`) |
| 4 | #______ | Text primary | Headings, body copy (`--geek-color-text`) |
| 5 | #______ | Text secondary | Subtitles, meta (`--geek-color-text-dim`) |
| 6 | #______ | Text muted | Captions, line numbers (`--geek-color-text-mute`) |
| 7 | #______ | Teal | Success / published / 研究 (`--geek-color-teal`) |
| 8 | #______ | Blue | Info / in-dev links (`--geek-color-blue`) |
| 9 | #______ | Amber | Warning / 科普 (`--geek-color-amber`) |
| 10 | #______ | Crimson | Danger / destructive (`--geek-color-crimson`) |
| ... | ... | ... | ... |

**Total colors**: N

> Default geek palette: `#f8f9fa` bg · `#e9ecef` surface · `#dee2e6` line ·
> `#3b82f6` blue accent · `#1e293b` text · `#475569` text-dim · `#94a3b8` text-mute ·
> `#10b981` teal · `#8b5cf6` purple · `#f59e0b` amber · `#ef4444` crimson.

---

## IV. Style Definition

| Property | Value |
|----------|-------|
| **Corner radius** | 0px on boxes (dots `50%`, scrollbars `8px`, code `2px`) |
| **Border weight** | 1px hairline (integer px, consistent per component type) |
| **Shadow style** | Soft + neon glow — card `0 8px 32px rgba(0,0,0,.45)`, glow `0 0 24px rgba(59,130,246,.45)` |
| **Hover lift** | `translateY(-2px)` buttons / `translateY(-4px)` cards |
| **Gradients** | Allowed — grid lines, CRT scanlines, radial glows, scrollbar |
| **Focus ring** | `outline: 3px solid blue`, `outline-offset: 2px` |
| **Spacing** | Integer px, loose (base `N` px; NOT enforced as a strict grid) |
| **Transition** | `.2s ease` colors / `.3s ease` transform / `.6s ease` zoom / `.8s ease` reveal |

---

## V. Component Inventory

### A. Buttons

| Component | States | Variants | Hover |
|-----------|--------|----------|-------|
| `geek-btn` | hover / active / focus-visible / disabled | primary, outline, ghost, danger | translateY(-2px) + glow |
| `geek-btn--sm/md/lg` | same | — | — |

### B. Cards / Windows

| Component | Border | Shadow | Corner brackets |
|-----------|--------|--------|-----------------|
| `geek-card` | 1px line | card | `.corner` |
| `geek-panel` | 1px line | card | optional |
| `geek-window` | 1px line | card | `.corner`, 4px blue top bar |

### C. Tags / Eyebrow / Timeline / Typewriter

| Component | Rule |
|-----------|------|
| `geek-tag` | mono, radius 0, status color (teal/blue/amber/crimson) + soft bg |
| `geek-eyebrow` | mono blue `// 标签`, 28px blue leading line, `.18em` uppercase |
| `geek-timeline` | blue gradient line + glowing blue dots |
| `geek-typewriter__caret` | `▌` blue, `1s steps(1)` blink |

### D. Backgrounds / Decorative

| Pattern | Technique |
|---------|-----------|
| Flat | solid `--geek-color-bg` |
| Scanlines | `repeating-linear-gradient(0deg, rgba(255,255,255,.025) 0 1px, transparent 1px 3px)` |
| Grid | 56px `linear-gradient` lines, radial-fade masked |
| Radial glow | `radial-gradient(ellipse, rgba(59,130,246,.18), transparent 70%)` |
| Glitch title | red + teal clip-path slices, `mix-blend-mode: screen` |

### E. Interaction Animations

| Interaction | Motion | Timing | Duration |
|-------------|--------|--------|----------|
| Button hover | color swap + lift | ease | .2s / .3s |
| Card hover | lift + blue border | ease | .3s |
| Image zoom | scale | ease | .6s |
| Scroll reveal | fadeUp (opacity + translateY 24px) | ease | .8s |
| Typewriter caret | blink | steps(1) | 1s infinite |
| Glitch | clip-path slices | steps(1) | 3s infinite |

### F. Dynamic Effects (蒸馏动效 + 粒子指南 + 流体网格像素背景 demo — recipes in `references/dynamic-effects.md` / `references/background-fluid-grid.md`)

| Effect | Class | Trigger | Motion | Timing | Duration |
|--------|-------|---------|--------|--------|----------|
| 双层擦除按钮 | `geek-btn-wipe` | hover | dual-layer wipe-in (staggered `.1s` chase) + label/icon slide | ease | .4s |
| 背景像素画视差浮动 | `geek-float-parallax` | pointermove | bg rotates ±15° by mouse Y; layers drift opposite by mouse X (laggy float) | ease | 3s |
| 像素画上浮 | `geek-float-rise` | panel open / scroll reveal | tiles rise from `translateY(100%)`, `stagger 120ms` | ease | .8s |
| 像素粒子网络背景 | `geek-particle-bg` | pointermove / loop | canvas pixel squares float; proximity links; mouse repel + cyan cursor links | rAF | — |
| 四向滚动光带 | `geek-marquee` | loop | 4-direction scrolling strips (text + glyphs) | linear | 8s infinite |
| CRT 水波纹 | `geek-crt-ripple` | loop | SVG turbulence displacement, rAF seed/scale | — | — |
| 流体网格像素背景 | `geek-fluid-grid` | loop / pointermove | fixed-grid pixel values flow via fBm noise / wave / vortex; hue follows flow direction; breathing flicker; mouse swirl-repel (engine A) or uniform pixels + dual-noise fields + breathing tide, no mouse (engine B) | rAF | — |
| 复制参数 | `geek-copy-params` | click | serialize settings → clipboard; button flips `复制参数 → ✓ 已复制` | — | 1.5s feedback |

---

## VI. Output Configuration

| Option | Value |
|--------|-------|
| **Output mode** | Single `theme.css` / Per-family CSS files |
| **Custom properties** | `--geek-*` prefix in `:root` |
| **Class prefix** | `geek-` (`.geek-btn`, `.geek-card`, `.geek-tag`) |
| **Framework markup** | Include component markup / CSS only |
| **Reduced motion** | Include `prefers-reduced-motion` fallback |
