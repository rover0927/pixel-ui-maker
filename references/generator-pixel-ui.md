# Generator Pixel Data Stream UI — CSS Implementation Rules

> Execution guidelines for generating pixel data stream web UI styles (pixel data stream language) with strict style consistency. Applies to buttons, cards/windows, tags, backgrounds, decorative motifs, and interaction animations.

---

## 1. Design Parameter Confirmation

Before generating any CSS, output a confirmation listing:
- Palette (all HEX values + roles)
- Corner radius (0px boxes; dots 50%, scrollbars 8px, code 2px)
- Border weight (1px hairline per component type)
- Shadow style (soft + neon glow)
- Spacing (integer px, loose)
- Transition style (ease: .2s colors / .3s transform / .6s zoom / .8s reveal)
- Component inventory (buttons, cards, windows, tags, eyebrow, timeline, typewriter, backgrounds, animations)

---

## 2. Style Lock Rules (STRICT)

Every generated component MUST satisfy ALL of the following:

| Rule | Constraint |
|------|-----------|
| **Palette** | Every HEX color from the declared palette ONLY |
| **Corners** | `border-radius` **0px** on all boxes. Exceptions only: dots/badges `50%`, scrollbar thumb `8px`, code blocks `2px` |
| **Borders** | Integer px weight (1px hairline typical), consistent per component type |
| **Shadows** | **Soft + neon glow allowed**: card `0 8px 32px rgba(0,0,0,.45)`, glow `0 0 24px rgba(201,21,30,.45)`, neon dot `0 0 14px var(--geek-color-red)`. Blur/spread unrestricted |
| **Gradients** | **Allowed** — 56px grid lines (`linear-gradient`), CRT scanlines (`repeating-linear-gradient`), radial glows, scrollbar gradient, timeline gradient |
| **Opacity** | **Fractional alpha allowed** (scanlines `.025`, glows `.45`, scrims `.5`) |
| **Blur** | **Allowed** — nav `backdrop-filter: blur(14px) saturate(140%)`, brand `drop-shadow` (add `-webkit-backdrop-filter` for Safari) |
| **Spacing** | Integer px only. Loose — NO strict grid-multiple enforcement |
| **Fonts** | **mono** for all labels/numbers/dates/tags/buttons/metadata with `letter-spacing .08em–.3em`; **sans** for body/headings. Mono stack: JetBrains Mono / Fira Code / …; sans stack: Inter / PingFang SC / … |
| **Naming** | Class names follow the `geek-` prefix; custom properties `--geek-*`; `.corner` (signature) is unprefixed |
| **Motion** | Smooth `ease` preferred (.2s colors / .3s transform / .6s zoom / .8s reveal); typewriter caret & glitch use `steps(1)`; NO bounce/elastic overshoot |
| **Consistency** | The same palette + corner + border + shadow + font split + motion across ALL components |

---

## 3. Signature Motifs (MANDATORY where applicable)

The following make the theme recognizable — use them on cards, headings, labels, and page heroes:

- **`.corner` red corner brackets** — 14×14px L-shapes, top-left + bottom-right, 1px red borders (verbatim):
  ```css
  .corner { position: relative; }
  .corner:before, .corner:after { content:""; position:absolute; width:14px; height:14px; border:1px solid var(--geek-color-red); }
  .corner:before { top:-1px; left:-1px; border-right:none; border-bottom:none; }
  .corner:after  { bottom:-1px; right:-1px; border-left:none; border-top:none; }
  ```
- **CRT scanlines**: `repeating-linear-gradient(0deg, rgba(255,255,255,.025) 0 1px, transparent 1px 3px)` (+ `mix-blend-mode: overlay; opacity: .6` when used as an overlay).
- **56px sub-page grid**: `background-image: linear-gradient(1px, transparent 1px, rgba(201,21,30,.06) 1px, transparent 2px), linear-gradient(90deg, ...); background-size: 56px 56px;` masked with a radial fade.
- **Glitch title**: two `clip-path`-sliced copies (red `var(--geek-color-red)` + teal `var(--geek-color-teal)`) with `mix-blend-mode: screen`.
- **Typewriter caret**: `▌` in red, `animation: 1s steps(1) infinite`.
- **`//` eyebrow labels**: mono, red, `.18em` uppercase, preceded by a 28px red line. UI copy itself begins with `//` (e.g. `// SYSTEM INITIALIZED · WELCOME, GEEK.`).
- **Left accent bars**: `border-left: 2px solid var(--geek-color-red)` (nav/items), 3px for h3/blockquotes, plus `box-shadow: 0 0 8px var(--geek-color-red)`.
- **Timeline**: vertical red gradient line + glowing red node dots (`border:2px solid bg; border-radius:50%; box-shadow:0 0 14px var(--geek-color-red)`).

---

## 4. Component Family: Buttons (按钮交互)

### 4.1 The terminal button contract

A geek button is a mono outline slab that inverts on hover and lifts `-2px` with a red glow.

```css
.geek-btn {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 14px 22px;
  font-family: var(--geek-font-mono);
  font-size: 14px;
  letter-spacing: .08em;
  background: transparent;
  border: 1px solid var(--geek-color-text);
  border-radius: 0;                 /* sharp, never rounded */
  color: var(--geek-color-text);
  cursor: pointer;
  transition: background-color .2s ease, color .2s ease, border-color .2s ease,
              box-shadow .2s ease, transform .3s ease;
}
.geek-btn:hover  { transform: translateY(-2px); }
.geek-btn:active { transform: translateY(0); }
.geek-btn--primary {
  background: var(--geek-color-red);
  border-color: var(--geek-color-red);
}
.geek-btn--primary:hover:not(:disabled) {
  background: #fff;
  border-color: #fff;
  color: var(--geek-color-red);
  box-shadow: 0 0 24px rgba(201, 21, 30, .45);  /* red glow */
}
```

**State contract** — every interactive component MUST define all of:

| State | Required Behavior |
|-------|-------------------|
| `:hover` | Lift `translateY(-2px)`; primary inverts to white bg + red text + glow; ghost gets `#ffffff14` bg + red border |
| `:active` | Settle back `translateY(0)` |
| `:focus-visible` | `outline: 3px solid var(--geek-color-red); outline-offset: 2px;` |
| `:disabled` | `opacity:.5`, `cursor: not-allowed`, no hover lift |
| `[aria-pressed="true"]` (toggles) | Show pressed/selected visual (red fill or red border) |

### 4.2 Variants & sizes

| Variant | Recipe |
|---------|--------|
| `geek-btn--primary` | Red fill; hover inverts to white/red with glow |
| `geek-btn--ghost` | Transparent; hover `#ffffff14` bg + red border |
| `geek-btn--danger` | Crimson family (`--geek-color-crimson`) |

Sizes: `geek-btn--sm` (`padding:10px 14px; font-size:13px`), base md, `geek-btn--lg` (`padding:16px 28px; font-size:15px`).

---

## 5. Component Family: Cards / Windows (卡片与窗口)

### 5.1 Card recipe

```css
.geek-card {
  position: relative;
  background: var(--geek-color-bg-soft);   /* #232825 */
  border: 1px solid var(--geek-color-line);/* #2c3330 hairline */
  border-radius: 0;
  box-shadow: 0 8px 32px rgba(0, 0, 0, .45);
}
.geek-card:hover {
  transform: translateY(-4px);
  border-color: var(--geek-color-red);
  box-shadow: 0 12px 40px rgba(0, 0, 0, .55);
}
```

Every card also carries the `.corner` brackets (see §3).

### 5.2 Window anatomy

```
┌────────────────────────────────────────┐
│ ▂▂▂▂  4px red top bar                  │  <- title bar: mono title, red top border
│ title                      [×]         │
├────────────────────────────────────────┤  <- 1px hairline border
│                                        │
│               content                  │
│                                        │
└────────────────────────────────────────┘  <- soft card shadow + corner brackets
```

| Part | Class | Rule |
|------|-------|------|
| Window frame | `.geek-window` | `bg-soft`, 1px line border, radius 0, `overflow: hidden`, card shadow, `.corner` |
| Title bar | `.geek-window__title` | `border-top: 4px solid var(--geek-color-red)`, mono title, `padding: 8px 16px` |
| Body | `.geek-window__body` | `bg-soft`, `padding: 16px`, internal scroll with geek scrollbar |
| Modal overlay | `.geek-modal__overlay` | `rgba(0,0,0,.6)` scrim; content fades up via `geek-fade-up` |

---

## 6. Component Family: Tags / Eyebrow / Timeline (标签与装饰)

```css
.geek-tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 0;
  font-family: var(--geek-font-mono);
  font-size: 12px;
  letter-spacing: .08em;
}
.geek-tag--teal    { color: var(--geek-color-teal);    background: rgba(67, 217, 193, .13); }
.geek-tag--blue    { color: var(--geek-color-blue);    background: rgba(122, 166, 255, .13); }
.geek-tag--amber   { color: var(--geek-color-amber);   background: rgba(255, 192, 67, .13); }
.geek-tag--crimson { color: var(--geek-color-crimson); background: rgba(200, 50, 74, .13); }

.geek-eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-family: var(--geek-font-mono);
  font-size: 13px;
  letter-spacing: .18em;
  text-transform: uppercase;
  color: var(--geek-color-red);
}
.geek-eyebrow:before { content: ""; width: 28px; height: 1px; background: var(--geek-color-red); }
```

Timeline: vertical red gradient line (`linear-gradient(180deg, transparent 0%, red 8%, red 92%, transparent 100%)`, 1px wide) + 11px glowing red dots.

---

## 7. Component Family: Backgrounds & Decorative (背景与动效)

| Pattern | Technique |
|---------|-----------|
| **Flat** | Solid `background-color: var(--geek-color-bg)` |
| **Scanlines** | `repeating-linear-gradient(0deg, rgba(255,255,255,.025) 0 1px, transparent 1px 3px)` |
| **Grid** | 56px `linear-gradient` 1px lines, radial-fade masked |
| **Radial glow** | `radial-gradient(ellipse at center, rgba(201,21,30,.18), transparent 70%)` |
| **Glitch** | `.geek-glitch` — two clip-path-sliced pseudo copies (red + teal), `mix-blend-mode: screen`, `steps(1)` animation |

### 7.1 Motion contract

- **Smooth ease preferred**: `.2s ease` colors, `.3s ease` transform/box-shadow, `.6s ease` image zoom, `.8s ease` scroll-reveal (`opacity 0→1, translateY(24px)`).
- **Stepped only for**: typewriter caret (`steps(1)` blink), glitch slices (`steps(1)`).
- **No** elastic / bounce / ease-in-out overshoot.

```css
@keyframes geek-blink { 50% { opacity: 0; } }
@keyframes geek-fade-up {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}
.geek-typewriter__caret {
  display: inline-block;
  width: .6ch;
  color: var(--geek-color-red);
  animation: geek-blink 1s steps(1) infinite;
}
.geek-anim--reveal { animation: geek-fade-up .8s ease both; }
```

### 7.2 Geek scrollbar (signature)

```css
::-webkit-scrollbar { width: 10px; }
::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, var(--geek-color-red), #5a0a10);
  border-radius: 8px;
  border: 2px solid var(--geek-color-bg);
}
```

### 7.3 Reduced motion (mandatory)

```css
@media (prefers-reduced-motion: reduce) {
  .geek-btn, .geek-card, .geek-window, .geek-glitch:before, .geek-glitch:after,
  .geek-typewriter__caret, [class*="geek-anim"] {
    animation: none !important;
    transition: none !important;
  }
}
```

---

## 8. Output Format

- **CSS files**: component-family splits or single `theme.css`. Custom properties in `:root` first.
- **Markup**: minimal component markup included where needed to demonstrate classes.
- **No framework lock-in**: plain CSS by default; provide Vue/React equivalents only when asked.
- **Format**: CSS only, no external image assets unless requested.

---

## 9. Self-Check

Before declaring a theme complete:
- [ ] All HEX colors from declared palette
- [ ] `border-radius` 0px on boxes (dots 50%, scrollbars 8px, code 2px only)
- [ ] Soft shadows + neon glows used; blurs allowed
- [ ] Gradients used for grid/scanlines/glows (not forbidden)
- [ ] All spacing integer px
- [ ] mono/sans font split respected (mono for labels/numbers/buttons, sans for body)
- [ ] `.corner` brackets on cards; `//` eyebrow labels; typewriter caret; scanlines present
- [ ] Every interactive component has hover/active/focus/disabled states
- [ ] All `geek-` class and `--geek-*` property naming
- [ ] Animations use ease + steps(1) with reduced-motion fallback
- [ ] Palette + corner + border + shadow + font + motion identical across all components
