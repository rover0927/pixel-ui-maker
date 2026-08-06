# <Theme Name> — Pixel UI Design Spec

> Human-readable pixel UI design specification. Input for CSS implementation generation.

---

## I. Theme Information

| Field | Value |
|-------|-------|
| **Name** | |
| **Target Interface** | e.g., Login page / Dashboard / Settings panel |
| **Platform / Framework** | Vue / React / Plain HTML+CSS / Mini-program |
| **Pixel Style** | NES 8-bit / Modern pixel minimal / Retro terminal / Minimalist |
| **Grid Unit** | e.g., 4px / 8px |
| **Target Use** | Web app / Game UI / Portfolio / Demo |

---

## II. Visual Description

```
[Detailed visual description of the interface]

- Overall mood: [e.g., dark retro console, bright arcade, terminal green]
- Layout structure: [header / sidebar / content split, etc.]
- Component list: [buttons, inputs, windows, panels, nav, modals, ...]
- Distinctive features: [what makes this theme recognizable]
- Background treatment: [flat / checkerboard / grid / scanline / vignette]
```

---

## III. Color Palette

| Index | HEX | Role | Used On |
|-------|-----|------|---------|
| 0 | #______ | Background | Page / app root |
| 1 | #______ | Surface | Panels, windows, cards |
| 2 | #______ | Line / border | All 2px borders |
| 3 | #______ | Text primary | Headings, labels |
| 4 | #______ | Text secondary | Subtitles, placeholders |
| 5 | #______ | Accent | Primary buttons, active nav |
| 6 | #______ | Accent hover | Hover states |
| 7 | #______ | Accent edge | Button 3D edge tone |
| 8 | #______ | Accent shadow | Button hard shadow |
| 9 | #______ | Danger | Error / destructive actions |
| 10 | #______ | Success | Confirm / positive states |
| 11 | #______ | Overlay | Modal scrim |
| ... | ... | ... | ... |

**Total colors**: N

---

## IV. Style Definition

| Property | Value |
|----------|-------|
| **Corner radius** | 0px / 2px |
| **Border weight** | 2px (panels, windows, buttons) |
| **Shadow style** | HARD — `offsetX offsetY color`, no blur |
| **Panel shadow** | `4px 4px 0 #______` |
| **Window shadow** | `6px 6px 0 #______` |
| **Button edge depth** | 4px (rest) → 1px (pressed) |
| **Focus ring** | 3px flat solid outline |
| **Spacing grid** | Multiples of N px |
| **Transition** | `steps(2, end)` discrete / short linear |

---

## V. Component Inventory

### A. Button Interactions

| Component | States | Variants | Edge depth |
|-----------|--------|----------|------------|
| `pix-btn` | hover / active / focus-visible / disabled | solid, outlined, ghost, danger | 4px |
| `pix-btn--sm/md/lg` | same | — | 3px / 4px / 5px |
| `pix-btn-group` | selected item | — | — |

### B. Backgrounds

| Pattern | Cell Size | Colors |
|---------|-----------|--------|
| Flat | — | #______ |
| Checkerboard | 8px | #______ / #______ |
| Grid | 8px | line #______ |
| Scanlines | 4px | rgba(0,0,0,0.5) step |
| Vignette | — | 2–3 hard inset steps |

### C. Container Windows

| Component | Border | Shadow | Title bar |
|-----------|--------|--------|-----------|
| `pix-window` | 2px | 6px 6px 0 | accent-dark + title |
| `pix-panel` | 2px | 4px 4px 0 | none |
| `pix-panel--sunken` | 2px | inset 2px 2px 0 | none |
| `pix-card` | 2px | 4px 4px 0 | optional |

### D. Interaction Animations

| Interaction | Motion | Timing | Duration |
|-------------|--------|--------|----------|
| Button hover | brighten / edge raise | linear | ≤ 150ms |
| Button press | translateY(3px) + edge 1px | linear | ≤ 80ms |
| Window open | pop-in 2-step scale | steps(2) | 160ms |
| Window close | pop-out | steps(2) | 120ms |
| Modal overlay | fade 0→1 flat | linear | 120ms |
| Shake (error) | translateX ±3px | steps | 240ms |
| Idle bob | translateY ±2px loop | steps(2) | 2s infinite |

---

## VI. Output Configuration

| Option | Value |
|--------|-------|
| **Output mode** | Single `theme.css` / Per-family CSS files |
| **Custom properties** | `--pix-*` prefix in `:root` |
| **Class prefix** | `pix-` |
| **Framework markup** | Include component markup / CSS only |
| **Reduced motion** | Include `prefers-reduced-motion` fallback |
