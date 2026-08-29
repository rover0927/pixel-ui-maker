# Pixel UI Maker - Scripts Reference (pixel data stream geek lock)

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

Validate a CSS file against the geek style-lock rules.

```bash
# Validate against an explicit palette
python skills/pixel-ui-maker/scripts/style_validator.py theme.css --palette "#f8f9fa" "#e9ecef" "#3b82f6"

# Validate using palette from ui_spec.md, plus the naming contract
python skills/pixel-ui-maker/scripts/style_validator.py theme.css --spec ui_spec.md --prefix geek-

# Strict mode (warnings count as failures)
python skills/pixel-ui-maker/scripts/style_validator.py theme.css --spec ui_spec.md --strict

# Save validation results
python skills/pixel-ui-maker/scripts/style_validator.py theme.css --spec ui_spec.md --output validation.json
```

Checks performed:
- All HEX colors from declared palette
- `border-radius` 0px on boxes (allowed: 1/2px, dots 50%, scrollbars 8px)
- Integer px spacing (non-integer → warning, or violation under `--strict`)
- Class names follow prefix contract (default `--prefix geek-`)
- Soft shadows / gradients / fractional opacity / blur are allowed (no violations)

`--grid` is accepted and ignored for backward compatibility (spacing is integer px, not grid-locked).

Exit code 0 = valid, 1 = invalid.

### theme_scaffolder.py

Generate a `theme.css` skeleton from `ui_spec.md`.

```bash
# Generate skeleton to theme.css
python skills/pixel-ui-maker/scripts/theme_scaffolder.py ui_spec.md --output theme.css

# Print to stdout instead of writing
python skills/pixel-ui-maker/scripts/theme_scaffolder.py ui_spec.md --print
```

The skeleton parses the spec's Color Palette table and Style Definition table to build `:root` custom properties (`--geek-*`), then emits component class scaffolds (buttons, corner brackets, cards/windows, tags, eyebrow, backgrounds, glitch, timeline, typewriter, animations) as a starting point for Step 4 Implementation Generation.

## Naming Contract

Generated themes MUST follow:
- Class prefix: `geek-` (e.g., `.geek-btn`, `.geek-card`, `.geek-window`)
- Custom properties: `--geek-*` (e.g., `--geek-color-blue`, `--geek-space-2`, `--geek-shadow-glow`)
- Signature `.corner` helper is unprefixed by design

`style_validator.py` and `theme_scaffolder.py` rely on this contract.
