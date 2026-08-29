# Pixel UI Maker

> Pixel Data Stream UI/CSS theme maker — a [Claude Code](https://claude.com/claude-code) skill that converts interface descriptions, wireframes, or reference designs into complete **pixel data stream** UI implementations (CSS + component markup) with strict style consistency.

Design language: light canvas + signal-blue accent, sharp 0px geometry, blue corner brackets, CRT scanline / glitch / typewriter terminal motifs, soft glow shadows, and smooth ease motion.

> 🇨🇳 中文版见 [README.md](README.md) · English is the canonical version.

---

## What It Does

Given a UI description, wireframe, or existing CSS/reference screenshot, the skill produces:

1. A **UI design spec** (`ui_spec.md`) — theme name, geek style, color palette, style-lock parameters, component inventory, and an animation plan.
2. A **CSS implementation** (`theme.css` or per-family splits) with `--geek-*` custom properties and `geek-` prefixed component classes.
3. **Dynamic effects** (distilled motion recipes + the particle-background guide; see `references/dynamic-effects.md`) — `geek-btn-wipe` dual-layer wipe button, `geek-float-parallax` mouse-parallax background float (pure CSS / GSAP), `geek-float-rise` staggered pixel-art rise (pure CSS / GSAP), `geek-particle-bg` canvas pixel-particle network (pixel squares + proximity links + mouse repel), `geek-marquee` 4-direction scrolling strips, `geek-crt-ripple` CRT water-ripple filter. Plus the **fluid-grid pixel background** `geek-fluid-grid` (Canvas dual-engine: noise/wave/vortex flow + mouse swirl-repel, or uniform pixels + dual-noise fields + breathing tide; includes the `geek-copy-params` copy-params button; see `references/background-fluid-grid.md`, runnable source in `examples/fluid-grid-bg/`). A complete Vue implementation of these effects lives in `examples/geek-homepage/` (the CYBER GEEK homepage); see `examples/README.md` for the full runnable-example index.
4. **Validation** — automated checks that every component obeys the style-lock rules.

A demo of the core output shape:

```css
:root {
  --geek-color-bg:        #f8f9fa;   /* light canvas */
  --geek-color-bg-soft:   #e9ecef;   /* surface */
  --geek-color-blue:      #3b82f6;   /* primary accent */
  --geek-shadow-glow:     0 0 24px rgba(59, 130, 246, .45);
  --geek-space-1: 4px;  --geek-space-2: 8px;
}

.geek-btn {           /* mono outline button, hover inverts + blue glow + lift */
  font-family: var(--geek-font-mono);
  border: 1px solid var(--geek-color-text);
  border-radius: 0;
  transition: box-shadow .2s ease, transform .3s ease;
}
.geek-btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--geek-shadow-glow);
}
.corner:before, .corner:after { ... }   /* red L-shaped corner brackets */
```

---

## When to Use

Invoke this skill when the request mentions any of:

- "pixel-style the UI", "make a pixel theme", "generate pixel CSS"
- "terminal style", "hacker theme", "geek UI"
- **像素数据流**, **像素风界面**, **像素样式开发**, **像素按钮**, **像素背景**, **像素窗口** (backward-compatible aliases)
- "fluid grid", "grid background", "particle background" — **流体网格**, **点阵背景**, **背景噪声**, **粒子背景** (canvas backgrounds)
- **暗黑终端**, **终端极客**, **黑客风**, **角标**, **CRT**, **scanline**, **glitch**, **typewriter**
- `pixel-ui-maker`

Typical targets: login pages, dashboards, settings panels, club sites, geek portfolios — in Vue, React, plain HTML+CSS, or mini-programs.

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

### The Style Lock (STRICT) — the "geek lock"

Every generated component **must** satisfy all of these rules — this is the heart of the skill:

| Rule | Constraint |
|------|------------|
| **Palette** | Every HEX color from the declared palette ONLY (light `#f8f9fa` + blue `#3b82f6` + status set) |
| **Corners** | **0px** on boxes (sharp); exceptions: dots `50%`, scrollbars `8px`, code `2px` |
| **Borders** | 1px hairline, consistent per component type |
| **Shadows** | **Soft + neon glow allowed**: card `0 8px 32px rgba(0,0,0,.45)`, glow `0 0 24px rgba(59,130,246,.45)` |
| **Gradients** | **Allowed**: grid lines, CRT scanlines, radial glows, scrollbars |
| **Opacity** | **Fractional alpha allowed** (scanlines `.025`, glows `.45`) |
| **Blur** | **Allowed** `filter: blur` / `backdrop-filter` (blurred nav) |
| **Spacing** | Integer px, loose (no strict grid-multiple lock) |
| **Fonts** | **mono** for labels/numbers/buttons/metadata + wide letter-spacing; **sans** for body/headings |
| **Motion** | Smooth `ease` (.2s colors / .3s transform / .6s zoom / .8s reveal); caret/glitch use `steps(1)`; `prefers-reduced-motion` fallback mandatory |
| **Naming** | `geek-` class prefix, `--geek-*` custom properties (`.corner` excepted) |

### Signature motifs (must use)

- **`.corner` red L-brackets** (14×14, top-left + bottom-right)
- **`//` eyebrow labels** (mono red, `.18em` uppercase, 28px red leading line)
- **CRT scanlines** (`repeating-linear-gradient(0deg, rgba(255,255,255,.025) 0 1px, transparent 1px 3px)`)
- **56px grid backgrounds**, **glitch titles** (red + teal clip-path slices), **typewriter caret `▌`**, **glowing timeline dots**

### The Component Families

| Family | Covered components |
|--------|--------------------|
| **Button interactions** | `geek-btn` default/hover/active/focus-visible/disabled states, variants (primary / ghost / danger), sizes (`--sm`/`--lg`), hover-invert + blue glow + lift |
| **Cards & windows** | `geek-card` (corner brackets + hover lift + blue border), `geek-panel`, `geek-window` (4px blue top-bar title), `geek-tag` |
| **Decorative motifs** | `.corner` brackets, `//` eyebrow, timeline, typewriter caret, scanlines, grid, glitch |
| **Interaction animations** | ease transitions, hover invert/lift, scroll reveal fadeUp, card lift, stepped caret/glitch — all ease + `steps(1)` |

> For the full generation contract (button recipes, card/window anatomy, background recipes, motion table) see [`references/generator-pixel-ui.md`](references/generator-pixel-ui.md).

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

### style_validator.py — validate a CSS file against the geek style lock

```bash
python scripts/style_validator.py theme.css --palette "#f8f9fa" "#e9ecef" "#3b82f6"
python scripts/style_validator.py theme.css --spec ui_spec.md --prefix geek-
python scripts/style_validator.py theme.css --spec ui_spec.md --strict          # warnings = failures
python scripts/style_validator.py theme.css --spec ui_spec.md --output validation.json
```

Checks: palette membership, `border-radius` 0px on boxes (dots 50%, scrollbars 8px, code 2px), integer px spacing, `geek-` prefix contract. **Exit code 0 = valid, 1 = invalid.** (`--grid` is accepted but ignored — spacing is no longer grid-locked.)

### theme_scaffolder.py — generate a `theme.css` skeleton from `ui_spec.md`

```bash
python scripts/theme_scaffolder.py ui_spec.md --output theme.css
python scripts/theme_scaffolder.py ui_spec.md --print                   # print to stdout
```

Parses the spec's palette and style tables into `:root` variables (`--geek-*`), then emits component scaffolds (buttons, corner brackets, cards/windows, tags, eyebrow, backgrounds, glitch, timeline, typewriter, animations) as the starting point for Step 4.

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
| [`workflows/extend-theme.md`](workflows/extend-theme.md) | Add new components to an **existing** pixel data stream theme while keeping style-lock consistency |
| [`workflows/from-reference.md`](workflows/from-reference.md) | Build a theme derived from a **reference** screenshot, wireframe, or existing CSS |

---

## Naming Contract

All generated themes MUST follow (the validator and scaffolder depend on it):

- **Class prefix**: `geek-` → `.geek-btn`, `.geek-card`, `.geek-window`
- **Custom properties**: `--geek-*` → `--geek-color-blue`, `--geek-space-2`, `--geek-shadow-glow`
- **Signature corner helper**: `.corner` (unprefixed by design)

---

## Output Structure

Single-file mode (`theme.css`) or multi-file mode (one CSS per family):

```
output/<theme_name>_<timestamp>/
├── theme.css              # :root variables + all components
├── components/            # optional per-family splits
│   ├── buttons.css
│   ├── cards.css
│   ├── windows.css
│   └── animations.css
├── ui_spec.md             # final spec
├── theme_manifest.json    # theme name, palette, file map (multi-file mode)
└── validation.json        # style_validator.py output
```

---

## Requirements

- **Claude Code** with the skill installed under `~/.claude/skills/pixel-ui-maker/`.
- **Python 3** for the validation/scaffolding scripts — no third-party packages.

---

## Related Skills

- **pixel-entity-maker** — the companion skill for pixel *characters/animated sprites* (sprite sheets). Use it when the request is about entities and animation frames, not UI chrome.
