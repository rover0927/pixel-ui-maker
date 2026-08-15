---
name: pixel-ui-maker
description: >
  Pixel Data Stream UI/CSS theme maker ("像素数据流" style). Converts
  interface descriptions, wireframes, or reference designs into pixel data stream UI
  implementations (CSS + component markup) with strict style consistency — olive-dark
  canvas, signal-red accent, sharp 0px corners, red corner brackets, CRT scanlines,
  glitch/typewriter motifs, soft glow shadows, ease motion. Use when user asks to
  "pixel-style the UI", "make a pixel theme", "generate pixel CSS", "像素风界面",
  "像素样式开发", "像素按钮", "像素背景", "像素窗口", "像素数据流", "暗黑终端", "终端极客",
  "黑客风", "terminal style", "hacker theme", "geek UI", "角标", "CRT", "scanline",
  "glitch", "typewriter", "动态按钮", "按钮擦除", "按钮滑动", "背景浮动",
  "背景视差", "视差浮动", "鼠标视差", "像素画浮动", "上浮动画", "wipe button",
  "float-rise", "stagger", "parallax float", "parallax", "背景漂浮",
  "粒子背景", "粒子网络", "粒子浮动", "canvas 粒子", "连线粒子", "particle",
  "particle background", "粒子动画", "流体网格", "fluid grid", "流体背景",
  "grid background", "点阵背景", "像素点阵", "噪声背景", "背景噪声",
  "marquee", "滚动光带", "光带", "动效",
  "动态效果", or mentions "pixel-ui-maker".
---

# Pixel UI Maker (pixel data stream geek lock)

> Pixel Data Stream theme generator. Takes an interface description or reference design, produces a complete "geek lock" UI spec (olive-dark palette, red accent, sharp corners, hairline borders, soft shadows + neon glows, mono/sans typography) and a consistent CSS implementation — buttons with hover invert + glow, cards with red corner brackets, tags, windows, eyebrow labels, timeline, and ease-animated interactions.

**Core Pipeline**: `Input (UI description + requirements) → Design Spec → Style Confirmation → Implementation Generation → Validation & Delivery`

> [!CAUTION]
> ## Global Execution Discipline (MANDATORY)
>
> 1. **SERIAL EXECUTION** — Steps MUST be executed in order; each step's output is the input for the next
> 2. **BLOCKING = HARD STOP** — Steps marked ⛔ BLOCKING require a full stop; wait for explicit user response
> 3. **NO CROSS-PHASE BUNDLING** — Do not prepare content for subsequent Steps before reaching them
> 4. **GATE BEFORE ENTRY** — Each Step has prerequisites (🚧 GATE) that MUST be verified before starting
> 5. **STYLE CONSISTENCY ABOVE ALL** — All generated components MUST share the exact same palette, corner radius, border weight, shadow depth, font split, and transition style
> 6. **PREVIEW IS A STEP-1 SUB-FLOW, NOT A STEP** — The Step 1 dynamic-background preview server is a helper inside Step 1; it never creates a new pipeline step, and must be stopped if the user declines dynamic backgrounds

> [!IMPORTANT]
> ## Language Rule
>
> - **Response language**: match the user's input language
> - **Template format**: templates follow English structure; content values may be in the user's language

## Main Pipeline Scripts

| Script | Purpose |
|--------|---------|
| `${SKILL_DIR}/scripts/palette_extractor.py` | Extract all HEX colors from a reference CSS/design file |
| `${SKILL_DIR}/scripts/style_validator.py` | Validate a CSS file against the geek style-lock rules (palette, sharp corners, integer spacing, naming) |
| `${SKILL_DIR}/scripts/theme_scaffolder.py` | Generate a `theme.css` skeleton (CSS custom properties + component scaffolds) from `ui_spec.md` |
| `${SKILL_DIR}/scripts/preview_backgrounds.py` | Serve the `examples/` background-toolkit gallery + demos over local HTTP (stdlib only): prints reachable URL(s) + effect catalog, `index.html` as landing page |

## Template Index

| Template | Path | Purpose |
|----------|------|---------|
| UI spec | `${SKILL_DIR}/templates/ui_spec.md` | UI design specification template (palette, style-lock params, component inventory, animation plan) |
| Implementation prompt | `${SKILL_DIR}/templates/ui_implementation_prompt.md` | Structured prompt template for generating the CSS/component implementation |

| Reference | Path | Purpose |
|-----------|------|---------|
| Geek generator rules | `${SKILL_DIR}/references/generator-pixel-ui.md` | CSS implementation rules, style lock, component families, signature motifs |
| **Dynamic effects kit** | `${SKILL_DIR}/references/dynamic-effects.md` | **Distilled motion recipes: `geek-btn-wipe` dual-layer wipe button, `geek-float-parallax` background pixel-art mouse-parallax float (CSS + GSAP), `geek-float-rise` pixel-art stagger rise (CSS + GSAP), `geek-particle-bg` canvas pixel-particle network (from 粒子指南), `geek-marquee` scrolling strips, `geek-crt-ripple` CRT filter** |
| **Fluid-grid background** | `${SKILL_DIR}/references/background-fluid-grid.md` | **Canvas pixel-grid background (双引擎): `geek-fluid-grid` flow modes (noise/wave/vortex + mouse swirl-repel) and the disturbance-wave engine (uniform pixels + dual-noise fields + breathing tide, no mouse); 9-field param schema + `geek-copy-params` interaction + control-panel UI; runnable source in `examples/fluid-grid-bg/`** |

---

## Pipeline Steps

### Step 1: Input Collection

🚧 **GATE**: User provides interface description and/or reference design, plus requirements

| Input Type | Processing |
|-----------|-----------|
| Text description | Direct use as design brief |
| Wireframe / mockup | Analyze layout structure, identify component list |
| Existing CSS/theme | Analyze palette via `palette_extractor.py`, identify style to extend |
| Reference screenshot | Extract palette and analyze style characteristics |

**User must specify**:
- **Target interface**: e.g., login page, dashboard, settings panel
- **Platform/framework**: Vue / React / plain HTML+CSS / mini-program
- **Component list**: buttons, cards, windows, nav, tags, inputs, etc.
- **Geek style direction**: pixel data stream / 像素数据流 / Retro terminal / custom
- **Optional**: color palette, spacing base, reference design

**Dynamic background inquiry (proactive — a sub-flow within Step 1, NOT a new step)**:

Before freezing the requirements, **proactively ask** the user whether they need *advanced dynamic backgrounds*. Do it inline in this same turn, in order:

1. **Ask** — use this prompt (match the user's language):
   > "需要为界面加入进阶动态背景吗？可以打开本地预览挑选 —— 粒子网络 / 流体网格 / 像素画视差浮动 / 滚动光带 / CRT 水波纹等。"
2. **Launch instant preview** — immediately start the zero-dependency preview server in the background so the user can browse live while deciding:
   ```bash
   # run as a background task; keep it alive until the user answers
   python3 ${SKILL_DIR}/scripts/preview_backgrounds.py
   ```
   Read the printed URLs from the tool output and hand them to the user — gallery landing `/` and demo `/geek-effects-demo.html`.
3. **Present the toolkit catalog** — summarize `examples/index.html`: `geek-btn-wipe`, `geek-float-parallax`, `geek-float-rise`, `geek-particle-bg`, `geek-marquee`, `geek-crt-ripple`, `geek-fluid-grid`, `geek-copy-params`. Note which are instantly viewable in the static demo (`geek-btn-wipe`, `geek-float-rise`, `geek-marquee`, `geek-crt-ripple`) and which live in the Vue demos `geek-homepage` / `fluid-grid-bg` (require `npm install && npm run dev`; Vite dev port 5173). **Do not start the Vue demos.**
4. **Record the choice** — write the user's selection into the **Output** below (e.g. `dynamic_backgrounds: [geek-particle-bg, geek-btn-wipe]`). If declined, record `dynamic_backgrounds: none`.
5. **If declined → stop the preview** — kill the background server (`TaskStop` / Ctrl+C) and continue the pipeline without dynamic backgrounds.

**Output**: Structured requirements list: interface description, component inventory, style direction, framework target, any reference files, and the recorded dynamic-background selection (effect classes + trigger, or `none`)

---

### Step 2: Design Specification

🚧 **GATE**: Step 1 complete, requirements confirmed

**Theme Definition** — Establish the visual contract:

| Field | Description |
|-------|-------------|
| **Theme name** | Identifier for the theme |
| **Geek style** | pixel data stream / 像素数据流 / Retro terminal / Custom |
| **Color palette** | Exact HEX color list (olive dark bg + signal red accent + status set, each with a role) |
| **Corner style** | 0px on boxes — dots `50%`, scrollbars `8px`, code `2px` |
| **Border weight** | 1px hairline (integer px per component type) |
| **Shadow style** | Soft + neon glow — card `0 8px 32px rgba(0,0,0,.45)`, glow `0 0 24px rgba(201,21,30,.45)` |
| **Spacing** | Integer px, loose (no strict grid) |
| **Transition style** | Smooth `ease` (.2s colors / .3s transform / .6s zoom / .8s reveal) |

**Component Inventory** — the families (see `references/generator-pixel-ui.md`):

| Family | Sub-components |
|--------|---------------|
| **Button interactions** | `geek-btn` default/hover/active/focus/disabled states, variants (primary/ghost/danger), sizes, hover-invert + glow |
| **Cards & windows** | `geek-card` (corner brackets + hover lift), `geek-panel`, `geek-window`, `geek-tag` |
| **Decorative motifs** | `.corner` brackets, `//` eyebrow, timeline, typewriter caret, scanlines, grid, glitch |
| **Interaction animations** | ease transitions, hover lift, scroll reveal, caret/glitch `steps(1)`, reduced-motion |
| **Dynamic effects** | `geek-btn-wipe` dual-layer wipe button, `geek-float-parallax` background pixel-art mouse-parallax float (CSS + GSAP), `geek-float-rise` pixel-art stagger rise (CSS + GSAP), `geek-particle-bg` canvas pixel-particle network (pixel squares + proximity links + mouse repel), `geek-marquee` 4-direction scrolling strips, `geek-crt-ripple` CRT water-ripple filter — recipes in `references/dynamic-effects.md`; `geek-fluid-grid` canvas fluid-grid pixel background (noise/wave/vortex + mouse) and the disturbance-wave dual-noise breathing-tide engine, `geek-copy-params` JSON-copy button — recipe + param schema in `references/background-fluid-grid.md` |

**Animation Plan** (for each interaction):

| Component | Trigger | Motion | Timing | Duration |
|-----------|---------|--------|--------|----------|
| `geek-btn` | hover | color swap + lift | ease | .2s / .3s |
| `geek-card` | hover | lift + red border + deep shadow | ease | .3s |
| section | scroll | fadeUp (opacity + translateY 24px) | ease | .8s |
| `geek-typewriter__caret` | loop | blink | steps(1) | 1s infinite |
| `geek-glitch` | loop | clip-path slices | steps(1) | 3s infinite |
| `geek-btn-wipe` | hover | dual-layer wipe-in (staggered `.1s` chase) + label/icon slide | ease | .4s |
| `geek-float-parallax` | pointermove | bg rotates ±15° by mouse Y; layers drift opposite by mouse X — laggy float | ease | 3s |
| `geek-float-rise` | open/reveal | background tiles rise from `translateY(100%)`, `stagger 120ms` | ease | .8s |
| `geek-particle-bg` | pointermove / loop | canvas pixel squares float; proximity links; mouse repel + cyan cursor links | rAF | — |
| `geek-marquee` | loop | 4-direction scrolling strips | linear | 8s infinite |
| `geek-crt-ripple` | loop | SVG turbulence displacement, rAF-driven seed/scale | — | — |
| `geek-fluid-grid` | loop (+ pointermove in engine A) | fixed grid pixel values flow via fBm noise / wave / vortex; hue follows flow direction; breathing flicker; mouse swirl-repel (A) or uniform pixels + dual-noise fields + breathing tide, no mouse (B) | rAF | — |
| `geek-copy-params` | click | serialize settings → clipboard; button flips `复制参数 → ✓ 已复制` | — | 1.5s feedback |
| ... | ... | ... | ... | ... |

**Output**:
- `ui_spec.md` — complete UI design specification
- Component-by-component style descriptions

---

### Step 3: Style Confirmation

🚧 **GATE**: Step 2 complete, UI spec drafted

⛔ **BLOCKING** — Present the UI design spec and interaction plan to user for confirmation:

- Palette and spacing
- Corner / border / shadow treatment
- Component inventory (buttons, cards, windows, tags, motifs, animations)
- Visual description of the target interface

Wait for user approval or revision before proceeding.

---

### Step 4: Implementation Generation

🚧 **GATE**: Step 3 confirmed by user

**Role**: See `references/generator-pixel-ui.md` for detailed generation rules. When the spec includes dynamic motion (wipe buttons, floating backgrounds, marquees, CRT ripple), follow `references/dynamic-effects.md` — it holds the distilled, style-locked recipes for those effects. When the spec calls for a **canvas fluid-grid / LED-matrix background** (fixed pixel grid, flow-driven), follow `references/background-fluid-grid.md` (`geek-fluid-grid` + `geek-copy-params`; runnable source in `examples/fluid-grid-bg/`).

**Core rules**:
1. Generate CSS **per component family** — complete one family (e.g., buttons) before the next
2. **Style lock**: Every component MUST share the exact same:
   - Color palette (every HEX from declared palette)
   - Corner radius (0px on boxes; dots 50%, scrollbars 8px, code 2px)
   - Border weight per component type
   - Soft shadows + neon glows
   - Integer px spacing
   - mono/sans font split
   - Transition timing style (ease)
3. **Signature motifs required**: `.corner` red brackets on cards, `//` eyebrow labels, CRT scanlines, typewriter caret, glowing dots. **Soft shadows, gradients (grid/scanlines/glows), fractional opacity, and `blur`/`backdrop-filter` are all allowed.**

**Component organization**:

Each generated theme exports CSS custom properties in `:root`, then component classes under the `geek-` prefix:

```
:root {
  --geek-color-bg:        #1d211c;   /* olive dark */
  --geek-color-bg-soft:   #232825;   /* surface */
  --geek-color-red:       #c9151e;   /* primary accent */
  --geek-space-1: 4px;  --geek-space-2: 8px;  ...
}

.geek-btn { ... }          /* button interactions */
.geek-card { ... }         /* cards with .corner brackets */
.geek-window { ... }       /* container windows */
.geek-typewriter__caret { ... }
```

**Output**: CSS files + optional component markup, placed in the target project

---

### Step 5: Validation & Delivery

🚧 **GATE**: Step 4 complete, implementation generated

```bash
# 1. Validate style-lock compliance
python ${SKILL_DIR}/scripts/style_validator.py <theme.css> --palette "#1d211c" "#c9151e" ...
python ${SKILL_DIR}/scripts/style_validator.py <theme.css> --spec ui_spec.md --prefix geek-

# 2. Extract and review the palette actually used
python ${SKILL_DIR}/scripts/palette_extractor.py <theme.css>

# 3. Scaffold a fresh skeleton from the spec (if regenerating)
python ${SKILL_DIR}/scripts/theme_scaffolder.py ui_spec.md --output theme.css
```

**Validation checks**:
- [ ] All HEX colors belong to declared palette
- [ ] No `border-radius` > 0px on boxes (allowed: 1/2px, dots 50%, scrollbars 8px)
- [ ] All spacing values are integer px
- [ ] Class names follow the `geek-` prefix contract
- [ ] Soft shadows / gradients / fractional opacity / blur used deliberately
- [ ] Interaction states present for every interactive component
- [ ] `prefers-reduced-motion` fallback included

**Export structure**:
```
output/<theme_name>_<timestamp>/
├── theme.css              # :root variables + all components
├── components/            # optional per-family CSS splits
│   ├── buttons.css
│   ├── cards.css
│   ├── windows.css
│   └── animations.css
├── ui_spec.md             # Final spec
└── validation.json        # style_validator.py output
```

---

## Output Format

### Single-File Mode (all components in one CSS)

```
theme.css
├── :root variables (palette, fonts, shadows, motion)
├── Reset / base
├── Buttons (states + variants)
├── Cards / windows (corner brackets, tags)
├── Decorative motifs (eyebrow, timeline, typewriter, backgrounds)
├── Animation keyframes + interaction rules
└── Reduced-motion fallback
```

### Multi-File Mode (one CSS per component family)

Preferred for larger interfaces with many components. Each file follows the same style lock.

**Manifest format** (`theme_manifest.json`):
```json
{
  "theme": "geek-terminal",
  "palette": ["#1d211c", "#232825", "#c9151e"],
  "corner_radius": 0,
  "border": 1,
  "files": {
    "theme.css":       "custom properties + base",
    "buttons.css":     "geek-btn states and variants",
    "cards.css":       "geek-card / geek-tag / corner brackets",
    "windows.css":     "geek-window / geek-panel",
    "animations.css":  "keyframes + interaction rules"
  }
}
```

---

## Role Switching

| Phase | Active Role | Reference |
|-------|------------|-----------|
| Step 1-2 | Designer | This file |
| Step 3 | Reviewer (user) | — |
| Step 4 | Generator | `references/generator-pixel-ui.md` |
| Step 5 | Validator | This file + scripts |

**Switching protocol**: Announce `[Role Switch: <Role>]` before starting each phase.
