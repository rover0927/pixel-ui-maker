# Pixel UI Maker

> Pixel-style UI/CSS theme maker — a [Claude Code](https://claude.com/claude-code) skill that converts interface descriptions, wireframes, or reference designs into complete pixel-art UI implementations (CSS + component markup) with strict style consistency.

Covers **pixel buttons and interactions**, **pixel backgrounds**, **container windows**, and **style interaction animations** — all locked to a single shared visual contract.

> 🇨🇳 中文版见 [README.zh-CN.md](README.zh-CN.md) · English is the canonical version.

---

## What It Does

Given a UI description, wireframe, or existing CSS/reference screenshot, the skill produces:

1. A **UI design spec** (`ui_spec.md`) — theme name, pixel style, color palette, style-lock parameters, component inventory, and an animation plan.
2. A **CSS implementation** (`theme.css` or per-family splits) with `--pix-*` custom properties and `pix-` prefixed component classes.
3. **Validation** — automated checks that every component obeys the style-lock rules.

A demo of the core output shape:

```css
:root {
  --pix-color-bg:        #111111;
  --pix-color-surface:   #1E1E1E;
  --pix-color-accent:    #5D8BFF;
  --pix-space-1: 4px;  --pix-space-2: 8px;
}

.pix-btn {           /* button interactions */
  border: 2px solid var(--pix-color-accent-edge);
  border-radius: 2px;
  box-shadow: 0 4px 0 var(--pix-color-accent-shadow);  /* the hard 3D edge */
  transition: transform 60ms linear, box-shadow 60ms linear;
}
.pix-btn:active {
  transform: translateY(3px);
  box-shadow: 0 1px 0 var(--pix-color-accent-shadow);  /* press down the edge */
}
```

---

## When to Use

Invoke this skill when the request mentions any of:

- "pixel-style the UI", "make a pixel theme", "generate pixel CSS"
- **像素风界面**, **像素样式开发**, **像素按钮**, **像素背景**, **像素窗口**
- `pixel-ui-maker`

Typical targets: login pages, dashboards, settings panels, game UI, retro portfolios — in Vue, React, plain HTML+CSS, or mini-programs.

---

## How It Works

The skill runs a **5-step serial pipeline**. Each step's output feeds the next; the two "gates" enforce a hard stop until the user confirms.

```
Input (UI description + requirements)
   │  Step 1 · Input Collection
   ▼
Design Spec  ─────────── Step 2 · Design Specification
   │  ⛔ BLOCKING GATE
   ▼
Style Confirmation  ──── Step 3 · user reviews & approves the UI spec
   │  🚧 GATE
   ▼
Implementation  ──────── Step 4 · CSS + component markup generation
   │
   ▼
Validation & Delivery ── Step 5 · style_validator.py + export
```

| Step | Output | Gate |
|------|--------|------|
| 1. Input Collection | Structured requirements (interface, components, style direction, framework) | 🚧 |
| 2. Design Specification | `ui_spec.md` — palette, style-lock params, component inventory, animation plan | 🚧 |
| 3. Style Confirmation | Approved spec | ⛔ **BLOCKING** — wait for user approval |
| 4. Implementation Generation | CSS + optional component markup | 🚧 |
| 5. Validation & Delivery | Validated theme, `validation.json` | 🚧 |

> ⚠️ **Execution discipline**: steps are executed strictly in order; no cross-phase bundling; style consistency across all components is the top priority.

---

## Core Concepts

### The Style Lock (STRICT)

Every generated component **must** satisfy all of these rules — this is the heart of the skill:

| Rule | Constraint |
|------|------------|
| **Palette** | Every HEX color from the declared palette ONLY |
| **Corners** | `border-radius` 0–2px ONLY, never soft-rounded |
| **Borders** | Integer px weight, consistent per component type |
| **Shadows** | HARD only: `box-shadow: <offsetX> <offsetY> <color>` — NO blur/spread radius |
| **Gradients** | Forbidden for fills; hard-edged `repeating-*` texture patterns allowed |
| **Opacity** | 0 or 1 only (stepped overlay scrims excepted) |
| **Blur** | `filter: blur(...)` forbidden |
| **Grid** | All spacing is a multiple of the base unit (e.g. 4px) |
| **Font** | Monospace or pixel font; `font-smoothing` off for pixel fonts |
| **Image** | `image-rendering: pixelated` for raster assets |
| **Motion** | `steps()` discrete or short linear — no elastic/ease-in-out overshoot; `prefers-reduced-motion` fallback mandatory |
| **Naming** | `pix-` class prefix, `--pix-*` custom properties |

### The Four Component Families

| Family | Covered components |
|--------|--------------------|
| **Button interactions** | `pix-btn` default/hover/active/focus-visible/disabled states, `[aria-pressed]` toggles, variants (solid / outlined / ghost / danger / success), sizes (`--sm` 32px / `--md` 40px / `--lg` 48px), `pix-btn-group` |
| **Backgrounds** | Flat, checkerboard, grid lines, dithered fill, noise/scanlines, vignette, tile border |
| **Container windows** | `pix-window` (title bar + body + buttons), `pix-panel` (+ raised/sunken), `pix-card`, `pix-modal` |
| **Interaction animations** | Pop-in/out, press mechanics, idle bob, shake, focus rings, loading spinners, ambient loops — all stepped |

> For the full generation contract (button press mechanics, background recipes, window anatomy, keyframe recipes) see [`references/generator-pixel-ui.md`](references/generator-pixel-ui.md).

---

## Scripts

Three standalone Python scripts in [`scripts/`](scripts/), **Python standard library only — no install needed** (the `requirements.txt` is a no-op by design).

### palette_extractor.py — extract HEX colors from a CSS file

```bash
python scripts/palette_extractor.py theme.css                          # list colors by usage
python scripts/palette_extractor.py theme.css --format json            # JSON with usage %
python scripts/palette_extractor.py theme.css --analyze-only           # no palette listing
python scripts/palette_extractor.py theme.css --format json --output palette.json
```

### style_validator.py — validate a CSS file against the style lock

```bash
python scripts/style_validator.py theme.css --palette "#111111" "#1E1E1E" "#5D8BFF"
python scripts/style_validator.py theme.css --spec ui_spec.md --grid 4 --prefix pix-
python scripts/style_validator.py theme.css --spec ui_spec.md --strict          # warnings = failures
python scripts/style_validator.py theme.css --spec ui_spec.md --output validation.json
```

Checks: palette membership, `border-radius` ≤ 2px, no gradient fills, hard shadows only, no `filter: blur`, binary opacity, grid-multiple spacing, `pix-` prefix contract. **Exit code 0 = valid, 1 = invalid.**

### theme_scaffolder.py — generate a `theme.css` skeleton from `ui_spec.md`

```bash
python scripts/theme_scaffolder.py ui_spec.md --output theme.css
python scripts/theme_scaffolder.py ui_spec.md --print                   # print to stdout
```

Parses the spec's palette and style tables into `:root` variables, then emits component scaffolds as the starting point for Step 4.

---

## Templates

| Template | Purpose |
|----------|---------|
| [`templates/ui_spec.md`](templates/ui_spec.md) | The human-readable design document: theme info, visual description, palette table, style definition, component inventory, animation plan, output config |
| [`templates/ui_implementation_prompt.md`](templates/ui_implementation_prompt.md) | Structured prompt template for generating the CSS implementation, with per-family component specs |

---

## Workflows (standalone)

Not part of the main pipeline — reusable checklists for common follow-up tasks:

| Workflow | When to use |
|----------|-------------|
| [`workflows/extend-theme.md`](workflows/extend-theme.md) | Add new components to an **existing** pixel theme while keeping style-lock consistency |
| [`workflows/from-reference.md`](workflows/from-reference.md) | Build a theme derived from a **reference** screenshot, wireframe, or existing CSS |

---

## Naming Contract

All generated themes MUST follow (the validator and scaffolder depend on it):

- **Class prefix**: `pix-` → `.pix-btn`, `.pix-window`, `.pix-bg--checker`
- **Custom properties**: `--pix-*` → `--pix-color-accent`, `--pix-space-2`, `--pix-motion-enter`

---

## Output Structure

Single-file mode (`theme.css`) or multi-file mode (one CSS per family):

```
output/<theme_name>_<timestamp>/
├── theme.css              # :root variables + all components
├── components/            # optional per-family splits
│   ├── buttons.css
│   ├── backgrounds.css
│   ├── windows.css
│   └── animations.css
├── ui_spec.md             # final spec
├── theme_manifest.json    # theme name, palette, grid, file map (multi-file mode)
└── validation.json        # style_validator.py output
```

---

## Requirements

- **Claude Code** with the skill installed under `~/.claude/skills/pixel-ui-maker/`.
- **Python 3** for the validation/scaffolding scripts — no third-party packages.

---

## Related Skills

- **pixel-entity-maker** — the companion skill for pixel *characters/animated sprites* (sprite sheets). Use it when the request is about entities and animation frames, not UI chrome.
