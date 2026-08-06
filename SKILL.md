---
name: pixel-ui-maker
description: >
  Pixel-style UI/CSS theme maker. Converts interface descriptions, wireframes, or
  reference designs into pixel-art UI implementations (CSS + component markup) with
  strict style consistency — covering pixel buttons/interactions, pixel backgrounds,
  container windows, and style interaction animations. Use when user asks to
  "pixel-style the UI", "make a pixel theme", "generate pixel CSS", "像素风界面",
  "像素样式开发", "像素按钮", "像素背景", "像素窗口", or mentions "pixel-ui-maker".
---

# Pixel UI Maker

> Focused pixel-art UI theme generator. Takes an interface description or reference design, produces a complete pixel-style UI spec (palette, corners, borders, hard shadows, spacing grid) and a consistent CSS implementation — buttons with interaction states, backgrounds, container windows, and step-animated interactions.

**Core Pipeline**: `Input (UI description + requirements) → Design Spec → Style Confirmation → Implementation Generation → Validation & Delivery`

> [!CAUTION]
> ## Global Execution Discipline (MANDATORY)
>
> 1. **SERIAL EXECUTION** — Steps MUST be executed in order; each step's output is the input for the next
> 2. **BLOCKING = HARD STOP** — Steps marked ⛔ BLOCKING require a full stop; wait for explicit user response
> 3. **NO CROSS-PHASE BUNDLING** — Do not prepare content for subsequent Steps before reaching them
> 4. **GATE BEFORE ENTRY** — Each Step has prerequisites (🚧 GATE) that MUST be verified before starting
> 5. **STYLE CONSISTENCY ABOVE ALL** — All generated components MUST share the exact same palette, corner radius, border weight, shadow depth, spacing grid, and transition style

> [!IMPORTANT]
> ## Language Rule
>
> - **Response language**: match the user's input language
> - **Template format**: templates follow English structure; content values may be in the user's language

## Main Pipeline Scripts

| Script | Purpose |
|--------|---------|
| `${SKILL_DIR}/scripts/palette_extractor.py` | Extract all HEX colors from a reference CSS/design file |
| `${SKILL_DIR}/scripts/style_validator.py` | Validate a CSS file against the pixel style-lock rules (palette, corners, hard shadows, no gradients) |
| `${SKILL_DIR}/scripts/theme_scaffolder.py` | Generate a `theme.css` skeleton (CSS custom properties + component scaffolds) from `ui_spec.md` |

## Template Index

| Template | Path | Purpose |
|----------|------|---------|
| UI spec | `${SKILL_DIR}/templates/ui_spec.md` | UI design specification template (palette, style-lock params, component inventory, animation plan) |
| Implementation prompt | `${SKILL_DIR}/templates/ui_implementation_prompt.md` | Structured prompt template for generating the CSS/component implementation |

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
- **Component list**: buttons, panels, windows, nav, inputs, etc.
- **Pixel style direction**: NES 8-bit retro / Modern pixel minimal / Retro terminal / custom
- **Optional**: color palette, spacing grid unit, reference design

**Output**: Structured requirements list: interface description, component inventory, style direction, framework target, any reference files

---

### Step 2: Design Specification

🚧 **GATE**: Step 1 complete, requirements confirmed

**Theme Definition** — Establish the visual contract:

| Field | Description |
|-------|-------------|
| **Theme name** | Identifier for the theme |
| **Pixel style** | NES 8-bit / Modern pixel minimal / Retro terminal / Minimalist |
| **Color palette** | Exact HEX color list (≤ 16 colors typical, each with a role) |
| **Corner style** | 0px (sharp) / 2px (micro corner) — never rounded |
| **Border weight** | Integer px per component type (e.g., 2px panels, 2px buttons) |
| **Shadow style** | HARD only — `offsetX offsetY color`, NO blur radius |
| **Spacing grid** | Base unit (e.g., 4px), all spacing is a multiple of it |
| **Transition style** | `steps()` discrete motion vs short linear; duration budget |

**Component Inventory** — the four families (see `references/generator-pixel-ui.md`):

| Family | Sub-components |
|--------|---------------|
| **Button interactions** | `pix-btn` default/hover/active/focus/disabled states, variants (solid/outlined/ghost/danger), sizes, press mechanics |
| **Backgrounds** | Flat solid, dithered pattern, grid, checkerboard, noise, vignette |
| **Container windows** | `pix-window` (title bar + body), `pix-panel`, `pix-card`, `pix-modal` |
| **Interaction animations** | Transitions, hover/active moves, pop-in/out, idle bob, shake, keyframe design, reduced-motion |

**Animation Plan** (for each interaction):

| Component | Trigger | Motion | Frames/Steps | Duration |
|-----------|---------|--------|--------------|----------|
| `pix-btn` | hover | brighten bg | 1 step | 100ms |
| `pix-btn` | active | press down 3px, shadow shrinks | 1 step | 60ms |
| `pix-window` | open | pop-in (scale 0→1 in 2 steps) | 2 steps | 120ms |
| ... | ... | ... | ... | ... |

**Output**:
- `ui_spec.md` — complete UI design specification
- Component-by-component style descriptions

---

### Step 3: Style Confirmation

🚧 **GATE**: Step 2 complete, UI spec drafted

⛔ **BLOCKING** — Present the UI design spec and interaction plan to user for confirmation:

- Palette and spacing grid
- Corner / border / shadow treatment
- Component inventory (buttons, backgrounds, containers, animations)
- Visual description of the target interface

Wait for user approval or revision before proceeding.

---

### Step 4: Implementation Generation

🚧 **GATE**: Step 3 confirmed by user

**Role**: See `references/generator-pixel-ui.md` for detailed generation rules.

**Core rules**:
1. Generate CSS **per component family** — complete one family (e.g., buttons) before the next
2. **Style lock**: Every component MUST share the exact same:
   - Color palette (every HEX from declared palette)
   - Corner radius (0–2px max)
   - Border weight per component type
   - Hard shadows only (no blur radius)
   - Spacing grid multiples
   - Transition timing style
3. **No gradients, no blurred shadows, no soft rounding, no fractional-opacity fills**

**Component organization**:

Each generated theme exports CSS custom properties in `:root`, then component classes under the `pix-` prefix:

```
:root {
  --pix-color-bg:        #111111;
  --pix-color-surface:   #1E1E1E;
  --pix-color-accent:    #5D8BFF;
  --pix-space-1: 4px;  --pix-space-2: 8px;  ...
}

.pix-btn { ... }          /* button interactions */
.pix-bg--checker { ... }  /* backgrounds */
.pix-window { ... }       /* container windows */
.pix-window__title { ... }
```

**Output**: CSS files + optional component markup, placed in the target project

---

### Step 5: Validation & Delivery

🚧 **GATE**: Step 4 complete, implementation generated

```bash
# 1. Validate style-lock compliance
python ${SKILL_DIR}/scripts/style_validator.py <theme.css> --palette "#111111" "#1E1E1E" ...

# 2. Extract and review the palette actually used
python ${SKILL_DIR}/scripts/palette_extractor.py <theme.css>

# 3. Scaffold a fresh skeleton from the spec (if regenerating)
python ${SKILL_DIR}/scripts/theme_scaffolder.py ui_spec.md --output theme.css
```

**Validation checks**:
- [ ] All HEX colors belong to declared palette
- [ ] No `border-radius` greater than 2px
- [ ] No gradients (`linear-gradient`, `radial-gradient`, `conic-gradient`)
- [ ] No `box-shadow` with a blur radius (hard shadows only)
- [ ] No `filter: blur(...)` or non-binary `opacity`
- [ ] All spacing values are multiples of the grid unit
- [ ] All class names follow the `pix-` prefix contract
- [ ] Interaction states present for every interactive component

**Export structure**:
```
output/<theme_name>_<timestamp>/
├── theme.css              # :root variables + all components
├── components/            # optional per-family CSS splits
│   ├── buttons.css
│   ├── backgrounds.css
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
├── :root variables (palette, grid, style-lock params)
├── Reset / base
├── Buttons (states + variants)
├── Backgrounds (patterns)
├── Container windows (window/panel/card/modal)
├── Animation keyframes + interaction rules
└── Reduced-motion fallback
```

### Multi-File Mode (one CSS per component family)

Preferred for larger interfaces with many components. Each file follows the same style lock.

**Manifest format** (`theme_manifest.json`):
```json
{
  "theme": "retro-console",
  "palette": ["#111111", "#1E1E1E", "#5D8BFF"],
  "grid_unit": 4,
  "corner_radius": 2,
  "files": {
    "theme.css":       "custom properties + base",
    "buttons.css":     "pix-btn states and variants",
    "backgrounds.css": "pix-bg patterns",
    "windows.css":     "pix-window / pix-panel / pix-card",
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
