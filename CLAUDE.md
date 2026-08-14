# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

pixel-ui-maker is a Claude Code skill for generating dark-hacker/terminal web UI themes (SJTU SITA "暗黑终端极客" style) from interface descriptions or reference designs. It defines a serial pipeline and provides supporting Python scripts for palette extraction, style-lock validation, and theme scaffolding. It covers button interactions, cards/windows, tags, decorative motifs (corner brackets, `//` eyebrows, timeline, typewriter, scanlines, glitch), and ease-animated interactions.

## Commands

```bash
# Extract palette actually used in a CSS file
python scripts/palette_extractor.py theme.css

# Analyze CSS without palette listing
python scripts/palette_extractor.py theme.css --analyze-only

# Validate style-lock compliance
python scripts/style_validator.py theme.css --palette "#1d211c" "#232825" "#c9151e"

# Validate using palette from ui_spec.md (plus naming contract)
python scripts/style_validator.py theme.css --spec ui_spec.md --prefix geek-

# Generate a theme.css skeleton from ui_spec.md
python scripts/theme_scaffolder.py ui_spec.md --output theme.css
```

No dependencies required — all scripts use the Python standard library only.

## Architecture

### Pipeline (defined in SKILL.md)

The skill follows a 5-step serial pipeline: Input Collection → Design Specification → Style Confirmation (blocking, user) → Implementation Generation → Validation & Delivery.

- **Step 3 is a blocking user confirmation gate** — always present the UI spec and wait for approval before generating CSS.
- **Style Lock is the hardest rule** (the "geek lock"): every component must share palette, corner radius (0px boxes; dots 50%, scrollbars 8px, code 2px), border weight (1px hairline), soft shadows + neon glows, integer px spacing, mono/sans font split, and ease transition style.
- **Generation order**: complete one component family (buttons → cards/windows → tags/motifs → animations) before the next.

### Python Scripts

Three independent scripts that share no common library:

| Script | Purpose | Key Contract |
|--------|---------|-------------|
| `palette_extractor.py` | Extract HEX colors used in a CSS file with usage counts | Reads any CSS file, outputs hex/json palette + analysis |
| `style_validator.py` | Validate a CSS file against the geek style-lock rules | Reads CSS + palette spec; checks palette, corners (0px boxes), integer spacing, naming |
| `theme_scaffolder.py` | Generate a `theme.css` skeleton from `ui_spec.md` | Reads spec, outputs CSS with `--geek-*` variables + component scaffolds |

**Critical naming contract**: all generated themes follow `geek-` class prefix and `--geek-*` custom property names — e.g., `.geek-btn`, `.geek-card`, `.geek-window`, `--geek-color-red`, `--geek-shadow-glow`. `style_validator.py` and `theme_scaffolder.py` rely on this contract. The `.corner` helper is unprefixed by design.

### Templates

- `templates/ui_spec.md` — design document that bridges the "Design Spec" and "Implementation Generation" steps; includes palette table, style-lock params, component inventory, and animation plan
- `templates/ui_implementation_prompt.md` — structured prompt template for generating the CSS implementation, with per-family component specs

### Workflows (standalone, not part of main pipeline)

- `workflows/extend-theme.md` — add new components to an existing dark-terminal theme
- `workflows/from-reference.md` — build a theme from an existing reference design/CSS

#### Dynamic Effects Reference

`references/dynamic-effects.md` holds the distilled motion recipes (originally distilled from the JIEJOE design portfolio) and is part of the generator's reference set alongside `references/generator-pixel-ui.md`:

| Effect | Class / Pattern | Source |
|--------|-----------------|--------|
| Dual-layer wipe button | `geek-btn-wipe` | JIEJOE `menubox_navigation_contact` |
| Background pixel-art mouse-parallax float | `geek-float-parallax` (CSS + GSAP) | JIEJOE home hero `move_ball()` |
| Pixel-art stagger rise | `geek-float-rise` (CSS + GSAP) | JIEJOE menu background |
| Canvas pixel-particle network | `geek-particle-bg` (Canvas 2D + rAF) | 《粒子背景动画效果实现指南》(not JIEJOE) |
| 4-direction scrolling strips | `geek-marquee` | JIEJOE `photos_draglines_*` |
| CRT water-ripple filter | `geek-crt-ripple` (SVG + rAF) | JIEJOE video cover filter |
| Fluid-grid pixel background | `geek-fluid-grid` (Canvas 2D + rAF, 双引擎) | 流体网格像素背景 Vue demo (`examples/fluid-grid-bg/`) — `useFluidGrid` flow modes (noise/wave/vortex + mouse) + `useDisturbanceWave` uniform pixels / dual-noise fields / breathing tide; see `references/background-fluid-grid.md` |
| Copy-params interaction | `geek-copy-params` | same demo — one click serializes the settings to JSON and copies it, so the user can paste it back to an agent to reproduce the effect |

> Runnable source: `examples/geek-homepage/` is the full Vue 3 + Vite implementation of the JIEJOE effects above (11 `Geek*` components + 3 `use*` composables + `assets/geek-homepage.css`), alongside the fluid-grid demo in `examples/fluid-grid-bg/`. See `examples/README.md` for the index.

Naming contract: `geek-btn-wipe`, `geek-float-parallax`, `geek-float-rise`, `geek-particle-bg`, `geek-marquee` classes; `--geek-motion-*`, `--geek-stagger`, `--geek-rise-height`, `--geek-parallax-x`, `--geek-parallax-rot` custom properties. All effects are plain CSS except the GSAP variants (optional) and the three `requestAnimationFrame` drivers (the ripple's seed/scale, `geek-particle-bg`'s particle loop, `geek-fluid-grid`'s flow loop). `geek-float-parallax` (hero background float), `geek-float-rise` (menu/section entrance), `geek-particle-bg` (canvas particle network, layers *under* the parallax) and `geek-fluid-grid` (fixed LED-matrix pixel grid, flow-driven) are **different background effects** — don't conflate them. Every effect ships a `prefers-reduced-motion` fallback (canvas backgrounds render one static frame).

## Key Design Decisions

- **No shared script library** — each script is standalone with its own `if __name__ == "__main__": main()` block. This keeps them independently runnable without a package init.
- **No dependencies** — CSS is text-only, so all scripts use the Python standard library. No `requirements.txt` install needed.
- **Reference generation** — the actual CSS implementation is written by the generator following `references/generator-pixel-ui.md`; scripts handle post-generation validation and scaffolding.
- **Geek-lock validation rules**: `border-radius` 0px on boxes (dots 50%, scrollbars 8px, code 2px allowed); soft shadows + neon glows allowed (blur unrestricted); gradients allowed (grid lines, CRT scanlines, radial glows); fractional opacity allowed; spacing integer px (not grid-multiple locked); class prefix `geek-`.
- **Motion contract**: smooth `ease` (.2s colors / .3s transform / .6s zoom / .8s reveal); typewriter caret and glitch use `steps(1)`; a `prefers-reduced-motion` fallback block is mandatory.
