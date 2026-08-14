---
description: Add new components to an existing dark-terminal geek theme
---

# Extend Theme Workflow

Standalone workflow for adding new components to an existing dark-terminal theme while keeping style-lock consistency.

## Steps

1. **Read existing theme** — review `ui_spec.md` (palette, corner, border, shadow, spacing) and the generated `theme.css`
2. **Define new components** — component name, family (button/card/window/tag/motif/animation), states needed; if adding motion, consult `references/dynamic-effects.md` (`geek-btn-wipe`, `geek-float-parallax`, `geek-float-rise`, `geek-particle-bg`, `geek-marquee`, `geek-crt-ripple`)
3. **Scaffold** — run `theme_scaffolder.py` on the spec, or extend `theme.css` directly following the existing `--geek-*` variables
4. **Generate CSS** — following the style lock from the existing theme (same palette/corners/shadows/fonts/motion)
5. **Validate consistency** — run `style_validator.py --spec ui_spec.md --prefix geek-` to confirm no violations
6. **Update spec** — add the new components to `ui_spec.md` Component Inventory

## Consistency Checklist

- [ ] New components use only existing palette colors (`--geek-color-*`)
- [ ] Corner radius 0px on boxes (dots 50%, scrollbars 8px, code 2px)
- [ ] Border weight matches component family (1px hairline)
- [ ] Shadows are soft + glow (blur allowed)
- [ ] Spacing values are integer px
- [ ] mono/sans font split respected (mono for labels/numbers/buttons)
- [ ] Signature motifs present where applicable (`.corner`, `//` eyebrow, typewriter caret)
- [ ] Every interactive component has hover/active/focus/disabled states
- [ ] Class names follow the `geek-` prefix
- [ ] Animations respect `prefers-reduced-motion`
