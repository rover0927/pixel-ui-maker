# Pixel UI Implementation Prompt

> Universal template for generating pixel-art CSS/component implementations with consistent style across all components.

---

## 1. Theme Definition

```
Theme:       [name]
Interface:   [login page / dashboard / settings / ...]
Framework:   [vue / react / plain / mini-program]
Style:       [pixel style]
Grid:        [N]px base unit
Corner:      [0|2]px
Border:      [N]px per component type

Palette (≤ [N] colors):
  background    → #[hex]
  surface       → #[hex]
  line          → #[hex]
  text-primary  → #[hex]
  text-secondary→ #[hex]
  accent        → #[hex]
  accent-hover  → #[hex]
  accent-edge   → #[hex]
  accent-shadow → #[hex]
  danger        → #[hex]
  success       → #[hex]
  overlay       → #[hex]
  ...
```

## 2. Style Lock (ALL components)

```
- Corner radius 0-2px ONLY
- Integer px borders, consistent per component type
- HARD shadows only: box-shadow: offsetX offsetY color (NO blur/spread)
- NO gradients for fills (repeating hard-edge patterns allowed for texture)
- NO filter: blur(...)
- Opacity 0 or 1 (stepped overlay alpha allowed)
- All spacing = multiples of [N]px grid
- Colors from declared palette ONLY
- Class prefix `pix-`, custom properties `--pix-*`
- Motion uses steps() or short linear, with reduced-motion fallback
```

## 3. Custom Properties (`:root`)

```
:root {
  --pix-color-bg:        #[hex];
  --pix-color-surface:   #[hex];
  --pix-color-line:      #[hex];
  --pix-color-text:      #[hex];
  --pix-color-text-dim:  #[hex];
  --pix-color-accent:    #[hex];
  --pix-color-accent-hover: #[hex];
  --pix-color-accent-edge:  #[hex];
  --pix-color-accent-shadow: #[hex];
  --pix-color-danger:    #[hex];
  --pix-color-success:   #[hex];
  --pix-color-overlay:   #[hex];

  --pix-space-1: [N]px;  --pix-space-2: calc([N]*2);  /* keep multiples */
  --pix-radius: [0|2]px;
  --pix-border: [N]px;
  --pix-shadow-panel:  [X]px [Y]px 0 #[hex];
  --pix-shadow-window: [X]px [Y]px 0 #[hex];
  --pix-motion-fast: 80ms linear;
  --pix-motion-hover: 150ms linear;
  --pix-motion-enter: 160ms steps(2, end);
  --pix-motion-exit:  120ms steps(2, end);
}
```

## 4. Component-by-Component Spec

### A. Buttons — `pix-btn`

| State | Value |
|-------|-------|
| base | `background: accent; border: 2px solid accent-edge; border-radius: radius; box-shadow: 0 4px 0 accent-shadow;` |
| hover | `background: accent-hover;` |
| active | `transform: translateY(3px); box-shadow: 0 1px 0 accent-shadow;` |
| focus-visible | `outline: 3px solid accent; outline-offset: 2px;` |
| disabled | desaturated, `cursor: not-allowed`, no shadow |

Variants: `--solid`, `--outlined`, `--ghost`, `--danger`, `--success`. Sizes: `--sm` 32px / `--md` 40px / `--lg` 48px.

### B. Backgrounds — `pix-bg--*`

| Class | Recipe |
|-------|--------|
| `pix-bg--flat` | solid color |
| `pix-bg--checker` | `repeating-conic-gradient` at [N]px cell |
| `pix-bg--grid` | 1px `repeating-linear-gradient` lines at [N]px |
| `pix-bg--scanline` | 3-4px hard line overlay |
| `pix-bg--vignette` | nested hard inset shadows, stepped |

### C. Container Windows — `pix-window` / `pix-panel` / `pix-card`

| Class | Rule |
|-------|------|
| `pix-window` | 2px border, 6px 6px 0 shadow, `--radius`, `overflow: hidden` |
| `pix-window__title` | accent-dark bar, 8px padding, pixel text |
| `pix-window__btn` | 16x16 flat squares, hover invert, active press |
| `pix-window__body` | surface fill, grid padding, square scrollbar |
| `pix-panel` | 2px border, 4px 4px 0 shadow |
| `pix-panel--sunken` | `inset 2px 2px 0` shadow |
| `pix-card` | like panel, optional title |

### D. Interaction Animations

| Class / Keyframe | Recipe |
|------------------|--------|
| `pix-pop` | 0% scale(0) → 50% scale(1.1) → 100% scale(1), `steps(2)` |
| `pix-bob` | translateY 0 / -2px / 0, 2s infinite `steps(2)` |
| `pix-shake` | translateX 0 / -3px / 3px / 0 |
| `[data-open]` | apply pop-in on mount; stagger children 40ms multiples |
| reduced-motion | kill all animations/transitions, show final states |

## 5. Output Format

```
File: theme.css (or components/buttons.css, backgrounds.css, windows.css, animations.css)
Custom properties first in :root, then components grouped by family
Include a `prefers-reduced-motion` fallback block
No external dependencies; plain CSS unless framework requested
```
