#!/usr/bin/env python3
"""
Theme Scaffolder for Pixel UI Maker

Reads a ui_spec.md and generates a theme.css skeleton:
- :root custom properties (--pix-color-*, --pix-space-*, style-lock params)
- Component class scaffolds (buttons, backgrounds, windows, animations)
- prefers-reduced-motion fallback

The generated skeleton is a STARTING POINT for Step 4 Implementation Generation —
colors/properties come from the spec; interaction details are filled in by the generator.

Usage:
    python theme_scaffolder.py <ui_spec.md> [--output theme.css]
"""

import argparse
import json
import os
import re
import sys

ROLE_TO_PROP = {
    "background": "bg",
    "surface": "surface",
    "line": "line",
    "line / border": "line",
    "border": "line",
    "text primary": "text",
    "text": "text",
    "text secondary": "text-dim",
    "text-secondary": "text-dim",
    "accent": "accent",
    "accent hover": "accent-hover",
    "accent-hover": "accent-hover",
    "accent edge": "accent-edge",
    "accent-edge": "accent-edge",
    "accent shadow": "accent-shadow",
    "accent-shadow": "accent-shadow",
    "danger": "danger",
    "success": "success",
    "overlay": "overlay",
    "primary": "accent",
    "primary hover": "accent-hover",
}


def slugify(role):
    """Fallback slug for unmapped roles."""
    slug = re.sub(r"[^a-z0-9]+", "-", role.lower()).strip("-")
    return slug or "color"


def field_in_table(text, label):
    """Extract the value cell for a row like `| **Label** | Value |`."""
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip().lstrip("*").strip() for c in line.split("|")]
        if len(cells) >= 3 and label.lower() in cells[1].lower():
            return cells[2]
    return None


def parse_palette(text):
    """Parse the Color Palette table: rows of `| N | #HEX | Role | Used On |`."""
    palette = []
    in_table = False
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            in_table = False
            continue
        cells = [c.strip() for c in line.split("|")]
        cells = [c for c in cells if c != ""]  # drop empty leading/trailing
        if not cells:
            continue
        if cells[0].startswith("**Total"):
            continue
        if cells[0].lower() in ("index", "#"):
            continue
        hex_match = None
        for cell in cells:
            m = re.fullmatch(r"#[0-9a-fA-F]{6}", cell)
            if m:
                hex_match = cell
                break
        if hex_match:
            # role is the cell after the hex: `| N | #HEX | Role | Used On |`
            try:
                idx = cells.index(hex_match)
                role = cells[idx + 1] if idx + 1 < len(cells) else "color"
            except (ValueError, IndexError):
                role = "color"
            palette.append({"hex": hex_match.upper(), "role": role})

    return palette


def parse_positive_int(field_text, default):
    m = re.search(r"(\d+)", field_text or "")
    return int(m.group(1)) if m else default


# Defaults for theme tokens that scaffolds reference but specs often omit.
DEFAULT_TOKENS = {
    "text": "#FFFFFF",
    "text-dim": "#8F92A1",
    "shadow": "#000000",
}


def build_root_vars(palette, grid, radius, border, panel_shadow, window_shadow, edge_depth):
    props = []
    used_keys = set()
    for entry in palette:
        key = ROLE_TO_PROP.get(entry["role"].lower(), slugify(entry["role"]))
        props.append(f"  --pix-color-{key}: {entry['hex']};")
        used_keys.add(key)

    # Ensure scaffold-referenced tokens exist even when the spec omits them
    for key, default in DEFAULT_TOKENS.items():
        if key not in used_keys:
            props.append(f"  --pix-color-{key}: {default};  /* default token */")

    space = [f"  --pix-space-{i}: {grid * i}px;" for i in range(1, 7)]
    motion = (
        "  --pix-motion-fast: 80ms linear;\n"
        "  --pix-motion-hover: 150ms linear;\n"
        "  --pix-motion-enter: 160ms steps(2, end);\n"
        "  --pix-motion-exit: 120ms steps(2, end);"
    )
    shadow_vars = (
        f"\n  --pix-shadow-panel: {panel_shadow or '4px 4px 0 var(--pix-color-shadow)'};"
        f"\n  --pix-shadow-window: {window_shadow or '6px 6px 0 var(--pix-color-shadow)'};"
    )

    return (
        ":root {\n"
        + "\n".join(props)
        + "\n"
        + "\n".join(space)
        + f"\n  --pix-radius: {radius}px;"
        + f"\n  --pix-border: {border}px;"
        + f"\n  --pix-edge: {edge_depth}px;"
        + shadow_vars
        + "\n"
        + motion
        + "\n}\n"
    )


def component_scaffolds():
    return """/* ========== Button interactions ========== */
.pix-btn {
  height: 40px;
  padding: 0 16px;
  background-color: var(--pix-color-accent);
  border: var(--pix-border) solid var(--pix-color-accent-edge);
  border-radius: var(--pix-radius);
  color: var(--pix-color-text);
  font-weight: 700;
  letter-spacing: 1px;
  cursor: pointer;
  box-shadow: 0 var(--pix-edge) 0 var(--pix-color-accent-shadow);
  transition: background-color var(--pix-motion-hover),
              box-shadow var(--pix-motion-fast),
              transform var(--pix-motion-fast);
}
.pix-btn:hover {
  background-color: var(--pix-color-accent-hover);
}
.pix-btn:active {
  transform: translateY(calc(var(--pix-edge) - 1px));
  box-shadow: 0 1px 0 var(--pix-color-accent-shadow);
  background-color: var(--pix-color-accent-shadow);
}
.pix-btn:focus-visible {
  outline: 3px solid var(--pix-color-accent);
  outline-offset: 2px;
}
.pix-btn:disabled {
  opacity: 1;
  background-color: var(--pix-color-line);
  border-color: var(--pix-color-line);
  color: var(--pix-color-text-dim);
  cursor: not-allowed;
  box-shadow: none;
}
.pix-btn--solid { /* filled (default) */ }
.pix-btn--outlined {
  background-color: transparent;
  color: var(--pix-color-accent);
  box-shadow: none;
}
.pix-btn--ghost {
  background-color: transparent;
  border-color: transparent;
  box-shadow: none;
}
.pix-btn--danger {
  background-color: var(--pix-color-danger);
  border-color: var(--pix-color-danger);
  box-shadow: 0 var(--pix-edge) 0 var(--pix-color-danger);
}
.pix-btn-group { display: inline-flex; gap: 0; }
.pix-btn-group .pix-btn { border-radius: 0; }
.pix-btn-group .pix-btn + .pix-btn { border-left-width: 0; }

/* ========== Backgrounds ========== */
.pix-bg--flat { background-color: var(--pix-color-bg); }
.pix-bg--checker {
  background-color: var(--pix-color-bg);
  background-image: repeating-conic-gradient(
    var(--pix-color-bg) 0% 25%,
    var(--pix-color-surface) 0% 50%
  );
  background-size: 8px 8px;
}
.pix-bg--grid {
  background-color: var(--pix-color-bg);
  background-image:
    repeating-linear-gradient(0deg, var(--pix-color-line) 0 1px, transparent 1px 8px),
    repeating-linear-gradient(90deg, var(--pix-color-line) 0 1px, transparent 1px 8px);
}
.pix-bg--scanline {
  background-image: repeating-linear-gradient(
    0deg, transparent 0 3px, rgba(0, 0, 0, 0.5) 3px 4px
  );
}

/* ========== Container windows ========== */
.pix-window {
  background-color: var(--pix-color-surface);
  border: var(--pix-border) solid var(--pix-color-line);
  border-radius: var(--pix-radius);
  box-shadow: var(--pix-shadow-window);
  overflow: hidden;
}
.pix-window__title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px;
  background-color: var(--pix-color-accent-shadow);
  color: var(--pix-color-text);
  font-weight: 700;
}
.pix-window__btn {
  width: 16px;
  height: 16px;
  border: 1px solid var(--pix-color-text);
  background-color: var(--pix-color-accent);
  cursor: pointer;
}
.pix-window__body {
  padding: 16px;
  background-color: var(--pix-color-surface);
  overflow-y: auto;
}
.pix-panel {
  background-color: var(--pix-color-surface);
  border: var(--pix-border) solid var(--pix-color-line);
  border-radius: var(--pix-radius);
  box-shadow: var(--pix-shadow-panel);
  padding: 16px;
}
.pix-panel--sunken {
  box-shadow: inset 2px 2px 0 var(--pix-color-shadow);
}
.pix-card {
  background-color: var(--pix-color-surface);
  border: var(--pix-border) solid var(--pix-color-line);
  border-radius: var(--pix-radius);
  box-shadow: var(--pix-shadow-panel);
  padding: 16px;
}

/* ========== Interaction animations ========== */
@keyframes pix-pop {
  0%   { transform: scale(0); }
  50%  { transform: scale(1.1); }
  100% { transform: scale(1); }
}
@keyframes pix-bob {
  0%, 100% { transform: translateY(0); }
  50%      { transform: translateY(-2px); }
}
@keyframes pix-shake {
  0%, 100% { transform: translateX(0); }
  25%      { transform: translateX(-3px); }
  75%      { transform: translateX(3px); }
}
.pix-anim--pop   { animation: pix-pop 160ms steps(2, end); }
.pix-anim--bob   { animation: pix-bob 2s steps(2, end) infinite; }
.pix-anim--shake { animation: pix-shake 240ms steps(2, end); }

@media (prefers-reduced-motion: reduce) {
  .pix-btn, .pix-window, .pix-panel, .pix-card, [class*="pix-anim"] {
    animation: none !important;
    transition: none !important;
  }
}
"""


def main():
    parser = argparse.ArgumentParser(description="Generate a theme.css skeleton from ui_spec.md")
    parser.add_argument("spec", help="Path to ui_spec.md")
    parser.add_argument("--output", "-o", default="theme.css", help="Output CSS path")
    parser.add_argument("--print", action="store_true", help="Print CSS to stdout instead of writing")
    args = parser.parse_args()

    if not os.path.exists(args.spec):
        print(f"ERROR: Spec not found: {args.spec}", file=sys.stderr)
        sys.exit(1)

    with open(args.spec, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()

    palette = parse_palette(text)
    if not palette:
        print("WARNING: No palette entries found in spec; generating with placeholders", file=sys.stderr)

    grid = parse_positive_int(field_in_table(text, "Grid Unit"), 4)
    radius = parse_positive_int(field_in_table(text, "Corner radius"), 2)
    border = parse_positive_int(field_in_table(text, "Border weight"), 2)
    edge_depth = parse_positive_int(field_in_table(text, "Button edge depth"), 4)

    panel_shadow = field_in_table(text, "Panel shadow")
    window_shadow = field_in_table(text, "Window shadow")

    root = build_root_vars(palette, grid, radius, border, panel_shadow, window_shadow, edge_depth)
    css = (
        "/* Generated by pixel-ui-maker theme_scaffolder.py — skeleton, extend in Step 4 */\n"
        "/* Palette extracted from ui_spec.md */\n"
        + root
        + "\n"
        + component_scaffolds()
    )

    if args.print:
        print(css)
    else:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(css)
        print(f"theme.css skeleton written to {args.output}")
        print(f"Palette: {[p['hex'] for p in palette]}")


if __name__ == "__main__":
    main()
