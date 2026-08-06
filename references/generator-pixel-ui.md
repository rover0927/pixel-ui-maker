# Generator Pixel UI — CSS Implementation Rules

> Execution guidelines for generating pixel-art web UI styles with strict style consistency. Applies to buttons, backgrounds, container windows, and interaction animations.

---

## 1. Design Parameter Confirmation

Before generating any CSS, output a confirmation listing:
- Palette (all HEX values + roles)
- Corner radius (0 or 2px)
- Border weight per component type
- Shadow style (hard offset, no blur)
- Spacing grid unit
- Transition style (steps vs linear, durations)
- Component inventory (buttons, backgrounds, containers, animations)

---

## 2. Style Lock Rules (STRICT)

Every generated component MUST satisfy ALL of the following:

| Rule | Constraint |
|------|-----------|
| **Palette** | Every HEX color from the declared palette ONLY |
| **Corners** | `border-radius` 0–2px ONLY. No soft rounding |
| **Borders** | Integer px weight (1–3px typical), consistent per component type |
| **Shadows** | HARD only: `box-shadow: <offsetX> <offsetY> <color>`. NO blur radius, NO spread |
| **Gradients** | FORBIDDEN for fills (`linear-gradient`/`radial-gradient`/`conic-gradient`). Dithering patterns via hard-edged repeating layers are allowed |
| **Opacity** | 0 or 1 only. No fractional alpha fills; borders/text may use solid colors |
| **Blur** | `filter: blur(...)` FORBIDDEN |
| **Grid** | All spacing/margins/paddings are multiples of the base unit |
| **Font** | Monospace or pixel font for headings; `font-smoothing` off for pixel fonts |
| **Image** | `image-rendering: pixelated` for any raster assets |
| **Naming** | Class names follow the `pix-` prefix; custom properties `--pix-*` |
| **Motion** | Animations use discrete steps (`steps()`) or short linear; no elastic/ease-in-out overshoot |
| **Consistency** | The same palette + corner + border + shadow + grid across ALL components |

---

## 3. Component Family: Button Interactions (按钮交互)

### 3.1 Press Mechanics (the pixel button contract)

A pixel button is a flat slab with a hard offset "edge" shadow. Pressing it slides the slab down the edge.

```css
.pix-btn {
  height: 40px;
  padding: 0 16px;
  background-color: var(--pix-color-accent);
  border: 2px solid var(--pix-color-accent-edge);   /* 1px darker edge tone */
  border-radius: 2px;
  color: var(--pix-color-text);
  font-weight: 700;
  letter-spacing: 1px;
  cursor: pointer;
  box-shadow: 0 4px 0 var(--pix-color-accent-shadow);  /* the 3D edge */
  transition: background-color 120ms linear, box-shadow 60ms linear, transform 60ms linear;
}
.pix-btn:hover {
  background-color: var(--pix-color-accent-hover);
}
.pix-btn:active {
  transform: translateY(3px);              /* slide down the edge */
  box-shadow: 0 1px 0 var(--pix-color-accent-shadow);
  background-color: var(--pix-color-accent-active);
}
```

**State contract** — every interactive component MUST define all of:

| State | Required Behavior |
|-------|-------------------|
| `:hover` | Brighten fill or raise edge (+1px shadow depth) |
| `:active` | Press down: `translateY(N-1px)` + shadow shrinks to 1px depth. N = resting edge depth |
| `:focus-visible` | Hard focus ring: `outline: 3px solid`, `outline-offset: 2px`, OR `box-shadow: 0 0 0 3px` flat ring |
| `:disabled` | Desaturate/darken, `cursor: not-allowed`, remove edge shadow, NO active state |
| `[aria-pressed="true"]` (toggles) | Show pressed/selected visual |

### 3.2 Variants

| Variant | Recipe |
|---------|--------|
| `pix-btn--solid` | Filled accent + edge shadow (above) |
| `pix-btn--outlined` | Transparent fill, 2px border in accent, no edge shadow; hover fills |
| `pix-btn--ghost` | Transparent, no border; hover adds flat translucent bg |
| `pix-btn--danger` | Red accent family (bg/edge/shadow triple) |
| `pix-btn--success` | Green accent family |

### 3.3 Sizes

All on the spacing grid: `pix-btn--sm` (32px), `pix-btn--md` (40px), `pix-btn--lg` (48px). Heights are grid multiples; padding derived from grid.

### 3.4 Grouped / Split buttons

`pix-btn-group` — children joined with no gap, 1px overlap border, active item shown by shadow removal.

---

## 4. Component Family: Backgrounds (背景)

### 4.1 Layering contract

Backgrounds are flat surfaces + hard-edged pattern layers. Never gradient fills.

| Pattern | Technique |
|---------|-----------|
| **Flat** | Solid `background-color` from palette |
| **Checkerboard** | `background-image: repeating-conic-gradient(#color 0% 25%, #color2 0% 50%)` + `background-size: 8px 8px` (each 8px cell = 2 grid units) |
| **Grid lines** | `repeating-linear-gradient(0deg, ...)` + `repeating-linear-gradient(90deg, ...)` with `background-size` on the grid unit; 1px lines only |
| **Dithered fill** | Layered hard `box-shadow` dots or a repeating pattern at 1–2px steps |
| **Noise/scanlines** | `repeating-linear-gradient(0deg, transparent 0 3px, rgba(0,0,0,0.5) 3px 4px)` — scanlines allowed (hard edges, no blur) |
| **Vignette** | 2–3 nested hard `box-shadow` insets with stepped opacity, not radial-gradient |
| **Tile border** | Corner tiles via nested elements with solid colors (top-left light, bottom-right dark) |

### 4.2 Pattern rules

- Cell sizes MUST be grid-unit multiples (e.g., 8px, 12px, 16px).
- Pattern colors MUST come from the declared palette.
- Scanline/checker alpha: prefer solid or stepped alpha (e.g., `rgba(0,0,0,0.5)` step is allowed for overlay texture only).

```css
.pix-bg--checker {
  background-color: var(--pix-color-bg);
  background-image: repeating-conic-gradient(
    var(--pix-color-bg) 0% 25%,
    var(--pix-color-surface) 0% 50%
  );
  background-size: 8px 8px;
}
.pix-bg--grid {
  background-color: var(--pix-color-bg);
  background-image:
    repeating-linear-gradient(0deg, var(--pix-color-line) 0 1px, transparent 1px 8px),
    repeating-linear-gradient(90deg, var(--pix-color-line) 0 1px, transparent 1px 8px);
}
```

---

## 5. Component Family: Container Windows (容器窗口)

### 5.1 Window anatomy

```
┌────────────────────────────────────────┐  <- title bar (accent-dark)
│ ▢ ▣ ▮     窗口标题            │  <- title bar buttons
├────────────────────────────────────────┤  <- 2px body border
│                                        │
│               content                  │
│                                        │
└────────────────────────────────────────┘  <- 6px hard drop shadow
```

| Part | Class | Rule |
|------|-------|------|
| Window frame | `.pix-window` | 2px solid border (darker tone), 0–2px radius, hard drop shadow `6px 6px 0` |
| Title bar | `.pix-window__title` | Full-width bar, accent-dark fill, pixel text, `padding: 8px` (grid multiple) |
| Title bar buttons | `.pix-window__btn` | Small `16x16` flat squares, hover inverts, active pushes down |
| Body | `.pix-window__body` | Surface fill, padding grid-multiple, internal scroll with square scrollbar |
| Modal overlay | `.pix-modal__overlay` | Flat `rgba(0,0,0,0.7)` (stepped overlay allowed), content pops in via 2-step scale |
| Status corner | `.pix-window__corner` | Optional diagonal corner via `clip-path` or nested 1px tiles |

### 5.2 Panel / Card

```css
.pix-panel {
  background-color: var(--pix-color-surface);
  border: 2px solid var(--pix-color-line);
  border-radius: 2px;
  box-shadow: 4px 4px 0 var(--pix-color-shadow);
  padding: calc(var(--pix-space-2) * 3);
}
.pix-panel--raised { box-shadow: 6px 6px 0 var(--pix-color-shadow); }  /* deeper */
.pix-panel--sunken { box-shadow: inset 2px 2px 0 var(--pix-color-shadow); }  /* inset hard only */
```

### 5.3 Layout contract

- Containers size on the grid; border box always on.
- Overflow areas get the square `::-webkit-scrollbar` styling (2px radius thumb).
- Fixed/variable sizes are both allowed, but all internal offsets are grid multiples.

---

## 6. Component Family: Interaction Animations (样式交互动画)

### 6.1 Motion contract

- **Discrete preferred**: `transition-timing-function: steps(2, end)` or `steps(4, end)` for a stepped pixel feel.
- **Allowed smooth**: short linear moves (60–200ms) for color/bg changes. NO `ease-in-out`, NO elastic, NO bounce overshoot.
- **Durations**: state press ≤ 80ms, hover ≤ 150ms, enter/exit 120–240ms, ambient loops 1.5–3s.

### 6.2 Keyframe recipes

```css
/* Pop-in: pixel steps, not smooth scale */
@keyframes pix-pop {
  0%   { transform: scale(0); }
  50%  { transform: scale(1.1); }   /* overshoot ON the grid, stepped */
  100% { transform: scale(1); }
}
.pix-window[data-open] { animation: pix-pop 160ms steps(2, end); }

/* Idle bob (buttons/indicators) */
@keyframes pix-bob {
  0%, 100% { transform: translateY(0); }
  50%      { transform: translateY(-2px); }  /* 2px = grid unit */
}
.pix-btn--idle { animation: pix-bob 2s steps(2, end) infinite; }

/* Shake (error feedback) */
@keyframes pix-shake {
  0%, 100% { transform: translateX(0); }
  25%      { transform: translateX(-3px); }
  75%      { transform: translateX(3px); }
}
```

### 6.3 Interaction rules

| Interaction | Recipe |
|-------------|--------|
| Hover | Color swap OR edge raise (shadow depth +1), stepped |
| Active/press | translate + edge shrink (see buttons) |
| Open/close | 2-step pop-in / pop-out, staggered children via `animation-delay: 40ms` multiples |
| Slide | `translateX/Y` in grid-unit steps (`steps(N)`) |
| Focus ring | Flat 3px hard ring, stepped appear |
| Loading | Spinner = rotating 8-dot square tile, or stepped progress bar with hard block fill |
| Reduced motion | `@media (prefers-reduced-motion: reduce)`: kill all animations, show final states instantly |

```css
@media (prefers-reduced-motion: reduce) {
  .pix-btn, .pix-window, [class*="pix-"] {
    animation: none !important;
    transition: none !important;
  }
}
```

### 6.4 Ambient / decorative

- Background scanline drift, blinking cursor block, marching-ants selection — all at grid-unit step sizes.
- Never animate `left/top` for layout (use transform) — GPU-friendly and keeps the grid stable.

---

## 7. Output Format

- **CSS files**: component-family splits or single `theme.css`. Custom properties in `:root` first.
- **Markup**: minimal component markup included where needed to demonstrate classes.
- **No framework lock-in**: plain CSS by default; provide Vue/React equivalents only when asked.
- **Format**: CSS only, no external image assets unless requested.

---

## 8. Self-Check

Before declaring a theme complete:
- [ ] All HEX colors from declared palette
- [ ] No `border-radius` > 2px anywhere
- [ ] No gradient fills (only allowed: hard-edged repeating patterns)
- [ ] No `box-shadow` blur/spread radius
- [ ] No `filter: blur` or fractional `opacity`
- [ ] All spacing on the grid unit
- [ ] Every interactive component has hover/active/focus/disabled states
- [ ] All `pix-` class and `--pix-*` property naming
- [ ] Animations use `steps()` or short linear, with reduced-motion fallback
- [ ] Palette + corner + border + shadow + grid identical across all components
