---
description: Build a pixel UI theme from an existing reference design or CSS
---

# Reference-Based Theme Workflow

Standalone workflow for creating a pixel-style theme derived from an existing reference (screenshot, wireframe, or existing CSS) to ensure visual consistency.

## Steps

1. **Provide reference** — user supplies a reference design (screenshot, wireframe, or existing stylesheet)
2. **Extract palette** — run `palette_extractor.py` on the reference CSS, or extract HEX values from a screenshot's design tokens
3. **Analyze style** — identify: corner treatment, border weight, shadow style, spacing rhythm, accent colors
4. **Define theme** — fill `ui_spec.md`: palette roles, grid unit, style-lock params, component inventory
5. **Generate implementation** — follow the main pipeline (Steps 3–4), using the extracted palette and style
6. **Scaffold + compare** — run `theme_scaffolder.py` to produce a skeleton, then compare side-by-side with the reference
7. **Validate** — run `style_validator.py` on the generated CSS

## Consistency Checklist

- [ ] Extracted palette is fully mapped to `--pix-color-*` roles
- [ ] Corner/border/shadow match the reference intent (pixel-locked: no blur, no gradient)
- [ ] All components share the same palette + grid
- [ ] Reference accent colors preserved
- [ ] No violations from `style_validator.py`
