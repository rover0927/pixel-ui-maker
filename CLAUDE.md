# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

pixel-ui-maker is a Claude Code skill for generating pixel-art web UI themes from interface descriptions or reference designs. It defines a serial pipeline and provides supporting Python scripts for palette extraction, style-lock validation, and theme scaffolding. It covers four component families: button interactions, backgrounds, container windows, and interaction animations.

## Commands

```bash
# Extract palette actually used in a CSS file
python scripts/palette_extractor.py theme.css

# Analyze CSS without palette listing
python scripts/palette_extractor.py theme.css --analyze-only

# Validate style-lock compliance
python scripts/style_validator.py theme.css --palette "#111111" "#1E1E1E" "#5D8BFF"

# Validate using palette from ui_spec.md (plus grid and naming contract)
python scripts/style_validator.py theme.css --spec ui_spec.md --grid 4 --prefix pix-

# Generate a theme.css skeleton from ui_spec.md
python scripts/theme_scaffolder.py ui_spec.md --output theme.css
```

No dependencies required — all scripts use the Python standard library only.

## Architecture

### Pipeline (defined in SKILL.md)

The skill follows a 5-step serial pipeline: Input Collection → Design Specification → Style Confirmation (blocking, user) → Implementation Generation → Validation & Delivery.

- **Step 3 is a blocking user confirmation gate** — always present the UI spec and wait for approval before generating CSS.
- **Style Lock is the hardest rule**: every component must share palette, corner radius (0–2px), border weight, hard shadows (no blur), spacing grid, and transition style.
- **Generation order**: complete one component family (buttons → backgrounds → containers → animations) before the next.

### Python Scripts

Three independent scripts that share no common library:

| Script | Purpose | Key Contract |
|--------|---------|-------------|
| `palette_extractor.py` | Extract HEX colors used in a CSS file with usage counts | Reads any CSS file, outputs hex/json palette + analysis |
| `style_validator.py` | Validate a CSS file against pixel style-lock rules | Reads CSS + palette spec; checks corners, shadows, gradients, opacity, grid, naming |
| `theme_scaffolder.py` | Generate a `theme.css` skeleton from `ui_spec.md` | Reads spec, outputs CSS with `--pix-*` variables + component scaffolds |

**Critical naming contract**: all generated themes follow `pix-` class prefix and `--pix-*` custom property names — e.g., `.pix-btn`, `.pix-window`, `--pix-color-accent`, `--pix-space-2`. `style_validator.py` and `theme_scaffolder.py` rely on this contract.

### Templates

- `templates/ui_spec.md` — design document that bridges the "Design Spec" and "Implementation Generation" steps; includes palette table, style-lock params, component inventory, and animation plan
- `templates/ui_implementation_prompt.md` — structured prompt template for generating the CSS implementation, with per-family component specs

### Workflows (standalone, not part of main pipeline)

- `workflows/extend-theme.md` — add new components to an existing pixel theme
- `workflows/from-reference.md` — build a theme from an existing reference design/CSS

### Key Design Decisions

- **No shared script library** — each script is standalone with its own `if __name__ == "__main__": main()` block. This keeps them independently runnable without a package init.
- **No dependencies** — unlike pixel-entity-maker (Pillow), CSS is text-only, so all scripts use the Python standard library. No `requirements.txt` install needed.
- **Reference generation** — the actual CSS implementation is written by the generator following `generator-pixel-ui.md`; scripts handle post-generation validation and scaffolding.
- **Style-lock validation rules**: `border-radius` ≤ 2px; `box-shadow` offset-only (blur/spread radius must be 0 or absent); gradient fills forbidden (hard-edged `repeating-*` texture patterns allowed); `filter: blur` forbidden; opacity 0/1 only (stepped overlay scrims excepted); spacing multiples of the grid unit.
- **Motion contract**: animations use `steps()` or short linear timing; a `prefers-reduced-motion` fallback block is mandatory.
