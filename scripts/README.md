# Pixel UI Maker - Scripts Reference

## Overview

Scripts are in `skills/pixel-ui-maker/scripts/`. Run from the containing project directory. All scripts use the Python standard library only — no install needed.

## Scripts

### palette_extractor.py

Extract all HEX colors used in a CSS file with usage counts.

```bash
# List colors used, most frequent first
python skills/pixel-ui-maker/scripts/palette_extractor.py theme.css

# Export as JSON with usage percentages
python skills/pixel-ui-maker/scripts/palette_extractor.py theme.css --format json

# Analyze only (no palette listing)
python skills/pixel-ui-maker/scripts/palette_extractor.py theme.css --analyze-only

# Save to file
python skills/pixel-ui-maker/scripts/palette_extractor.py theme.css --format json --output palette.json
```

### style_validator.py

Validate a CSS file against the pixel style-lock rules.

```bash
# Validate against an explicit palette
python skills/pixel-ui-maker/scripts/style_validator.py theme.css --palette "#111111" "#1E1E1E" "#5D8BFF"

# Validate using palette from ui_spec.md, plus grid and naming contract
python skills/pixel-ui-maker/scripts/style_validator.py theme.css --spec ui_spec.md --grid 4 --prefix pix-

# Strict mode (warnings count as failures)
python skills/pixel-ui-maker/scripts/style_validator.py theme.css --spec ui_spec.md --strict

# Save validation results
python skills/pixel-ui-maker/scripts/style_validator.py theme.css --spec ui_spec.md --output validation.json
```

Checks performed:
- All HEX colors from declared palette
- `border-radius` ≤ 2px
- No gradient fills (`repeating-*` texture patterns allowed)
- `box-shadow` hard only (blur/spread radius must be 0 or absent)
- No `filter: blur(...)`
- `opacity` 0 or 1 (non-binary → warning)
- Spacing on the grid unit (with `--grid N`)
- Class names follow prefix contract (with `--prefix pix-`)

Exit code 0 = valid, 1 = invalid.

### theme_scaffolder.py

Generate a `theme.css` skeleton from `ui_spec.md`.

```bash
# Generate skeleton to theme.css
python skills/pixel-ui-maker/scripts/theme_scaffolder.py ui_spec.md --output theme.css

# Print to stdout instead of writing
python skills/pixel-ui-maker/scripts/theme_scaffolder.py ui_spec.md --print
```

The skeleton parses the spec's Color Palette table and Style Definition table to build `:root` custom properties, then emits component class scaffolds (buttons, backgrounds, windows, animations) as a starting point for Step 4 Implementation Generation.

## Naming Contract

Generated themes MUST follow:
- Class prefix: `pix-` (e.g., `.pix-btn`, `.pix-window`)
- Custom properties: `--pix-*` (e.g., `--pix-color-accent`, `--pix-space-2`)

`style_validator.py` and `theme_scaffolder.py` rely on this contract.
