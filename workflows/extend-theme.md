---
description: Add new components to an existing pixel UI theme
---

# Extend Theme Workflow

Standalone workflow for adding new components to an existing pixel-style theme while keeping style-lock consistency.

## Steps

1. **Read existing theme** — review `ui_spec.md` (palette, corner, border, shadow, grid) and the generated `theme.css`
2. **Define new components** — component name, family (button/background/window/animation), states needed
3. **Scaffold** — run `theme_scaffolder.py` on the spec, or extend `theme.css` directly following the existing `--pix-*` variables
4. **Generate CSS** — following the style lock from the existing theme (same palette/corners/shadows/grid)
5. **Validate consistency** — run `style_validator.py --spec ui_spec.md --grid N --prefix pix-` to confirm no violations
6. **Update spec** — add the new components to `ui_spec.md` Component Inventory

## Consistency Checklist

- [ ] New components use only existing palette colors (`--pix-color-*`)
- [ ] Corner radius matches the theme (0–2px)
- [ ] Border weight matches component family
- [ ] Shadows are hard (offset only, no blur)
- [ ] Spacing values are grid multiples
- [ ] Every interactive component has hover/active/focus/disabled states
- [ ] Class names follow the `pix-` prefix
- [ ] Animations respect `prefers-reduced-motion`
