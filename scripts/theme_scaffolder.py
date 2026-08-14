#!/usr/bin/env python3
"""
Theme Scaffolder for Pixel UI Maker (dark terminal / geek lock)

Reads a ui_spec.md and generates a theme.css skeleton:
- :root custom properties (--geek-color-*, --geek-space-*, fonts, shadows, motion)
- Component class scaffolds (buttons, corner brackets, cards/windows, tags,
  eyebrow, backgrounds, glitch, timeline, typewriter, animations)
- prefers-reduced-motion fallback

The generated skeleton is a STARTING POINT for Step 4 Implementation Generation —
colors/properties come from the spec; interaction details are filled in by the generator.

Usage:
    python theme_scaffolder.py <ui_spec.md> [--output theme.css]
"""

import argparse
import os
import re
import sys

ROLE_TO_PROP = {
    "background": "bg",
    "bg": "bg",
    "surface": "bg-soft",
    "bg-soft": "bg-soft",
    "line": "line",
    "line / border": "line",
    "border": "line",
    "text primary": "text",
    "text": "text",
    "text secondary": "text-dim",
    "text-secondary": "text-dim",
    "text muted": "text-mute",
    "text-muted": "text-mute",
    "text mute": "text-mute",
    "red accent": "red",
    "accent": "red",
    "red": "red",
    "accent hover": "red-hover",
    "accent-hover": "red-hover",
    "primary": "red",
    "primary hover": "red-hover",
    "danger": "crimson",
    "crimson": "crimson",
    "success": "teal",
    "teal": "teal",
    "info": "blue",
    "blue": "blue",
    "warn": "amber",
    "amber": "amber",
    "overlay": "overlay",
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
    "bg": "#1d211c",
    "bg-soft": "#232825",
    "line": "#2c3330",
    "red": "#c9151e",
    "text": "#ffffff",
    "text-dim": "#c9cfca",
    "text-mute": "#8a918d",
}

FONT_MONO = (
    '"JetBrains Mono", "Fira Code", "SFMono-Regular", Consolas, '
    '"Liberation Mono", Menlo, "PingFang SC", "Hiragino Sans GB", '
    '"Microsoft YaHei", "WenQuanYi Micro Hei", monospace'
)
FONT_SANS = (
    '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", '
    '"PingFang SC", "Microsoft YaHei", "Helvetica Neue", Arial, sans-serif'
)


def build_root_vars(palette, spacing_base, radius, border):
    props = []
    used_keys = set()
    for entry in palette:
        key = ROLE_TO_PROP.get(entry["role"].lower(), slugify(entry["role"]))
        props.append(f"  --geek-color-{key}: {entry['hex']};")
        used_keys.add(key)

    # Ensure scaffold-referenced tokens exist even when the spec omits them
    for key, default in DEFAULT_TOKENS.items():
        if key not in used_keys:
            props.append(f"  --geek-color-{key}: {default};  /* default token */")

    space = [f"  --geek-space-{i}: {max(1, spacing_base) * i}px;" for i in range(1, 7)]
    fonts = (
        f"  --geek-font-mono: {FONT_MONO};\n"
        f"  --geek-font-sans: {FONT_SANS};"
    )
    shadows = (
        "\n  --geek-shadow-glow: 0 0 24px rgba(201, 21, 30, .45);\n"
        "  --geek-shadow-card: 0 8px 32px rgba(0, 0, 0, .45);\n"
        "  --geek-shadow-card-hover: 0 12px 40px rgba(0, 0, 0, .55);"
    )
    motion = (
        "\n  --geek-motion-color: .2s ease;\n"
        "  --geek-motion-transform: .3s ease;\n"
        "  --geek-motion-zoom: .6s ease;\n"
        "  --geek-motion-reveal: .8s ease;"
    )

    return (
        ":root {\n"
        + "\n".join(props)
        + "\n"
        + "\n".join(space)
        + f"\n  --geek-radius: {radius}px;"
        + f"\n  --geek-border: {border}px;"
        + shadows
        + "\n"
        + fonts
        + motion
        + "\n}\n"
    )


def component_scaffolds():
    return """/* ========== Buttons ========== */
.geek-btn {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 14px 22px;
  font-family: var(--geek-font-mono);
  font-size: 14px;
  letter-spacing: .08em;
  background: transparent;
  border: 1px solid var(--geek-color-text);
  border-radius: var(--geek-radius);
  color: var(--geek-color-text);
  cursor: pointer;
  transition: background-color var(--geek-motion-color),
              color var(--geek-motion-color),
              border-color var(--geek-motion-color),
              box-shadow var(--geek-motion-color),
              transform var(--geek-motion-transform);
}
.geek-btn:hover { transform: translateY(-2px); }
.geek-btn:active { transform: translateY(0); }
.geek-btn:focus-visible {
  outline: 3px solid var(--geek-color-red);
  outline-offset: 2px;
}
.geek-btn:disabled { opacity: .5; cursor: not-allowed; }
.geek-btn--primary {
  background: var(--geek-color-red);
  border-color: var(--geek-color-red);
  color: var(--geek-color-text);
}
.geek-btn--primary:hover:not(:disabled) {
  background: var(--geek-color-text);
  border-color: var(--geek-color-text);
  color: var(--geek-color-red);
  box-shadow: var(--geek-shadow-glow);
}
.geek-btn--ghost:hover:not(:disabled) {
  background: #ffffff14;
  border-color: var(--geek-color-red);
}
.geek-btn--sm { padding: 10px 14px; font-size: 13px; }
.geek-btn--lg { padding: 16px 28px; font-size: 15px; }

/* ========== Corner brackets (signature motif) ========== */
.corner { position: relative; }
.corner:before, .corner:after {
  content: "";
  position: absolute;
  width: 14px;
  height: 14px;
  border: 1px solid var(--geek-color-red);
}
.corner:before { top: -1px; left: -1px; border-right: none; border-bottom: none; }
.corner:after  { bottom: -1px; right: -1px; border-left: none; border-top: none; }

/* ========== Cards / panels / windows ========== */
.geek-card {
  position: relative;
  background: var(--geek-color-bg-soft);
  border: 1px solid var(--geek-color-line);
  border-radius: var(--geek-radius);
  box-shadow: var(--geek-shadow-card);
}
.geek-card:hover {
  transform: translateY(-4px);
  border-color: var(--geek-color-red);
  box-shadow: var(--geek-shadow-card-hover);
}
.geek-panel {
  position: relative;
  background: var(--geek-color-bg-soft);
  border: 1px solid var(--geek-color-line);
  border-radius: var(--geek-radius);
  box-shadow: var(--geek-shadow-card);
  padding: 16px;
}
.geek-window {
  position: relative;
  background: var(--geek-color-bg-soft);
  border: 1px solid var(--geek-color-line);
  border-radius: var(--geek-radius);
  box-shadow: var(--geek-shadow-card);
  overflow: hidden;
}
.geek-window__title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 16px;
  border-top: 4px solid var(--geek-color-red);
  font-family: var(--geek-font-mono);
  color: var(--geek-color-text);
}
.geek-window__body { padding: 16px; background: var(--geek-color-bg-soft); }

/* ========== Tags ========== */
.geek-tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: var(--geek-radius);
  font-family: var(--geek-font-mono);
  font-size: 12px;
  letter-spacing: .08em;
}
.geek-tag--teal    { color: var(--geek-color-teal);    background: rgba(67, 217, 193, .13); }
.geek-tag--blue    { color: var(--geek-color-blue);    background: rgba(122, 166, 255, .13); }
.geek-tag--amber   { color: var(--geek-color-amber);   background: rgba(255, 192, 67, .13); }
.geek-tag--crimson { color: var(--geek-color-crimson); background: rgba(200, 50, 74, .13); }
.geek-tag--muted   { color: var(--geek-color-text-mute); background: rgba(138, 145, 141, .14); }

/* ========== Eyebrow label (// label) ========== */
.geek-eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-family: var(--geek-font-mono);
  font-size: 13px;
  letter-spacing: .18em;
  text-transform: uppercase;
  color: var(--geek-color-red);
}
.geek-eyebrow:before {
  content: "";
  width: 28px;
  height: 1px;
  background: var(--geek-color-red);
}

/* ========== Backgrounds ========== */
.geek-bg--flat { background-color: var(--geek-color-bg); }
.geek-bg--scanline {
  background-image: repeating-linear-gradient(
    0deg, rgba(255, 255, 255, .025) 0 1px, transparent 1px 3px
  );
}
.geek-bg--grid {
  background-image:
    linear-gradient(1px, transparent 1px, rgba(201, 21, 30, .06) 1px, transparent 2px),
    linear-gradient(90deg, transparent 1px, rgba(201, 21, 30, .06) 1px, transparent 2px);
  background-size: 56px 56px;
}
.geek-bg--radial {
  background: radial-gradient(ellipse at center, rgba(201, 21, 30, .18), transparent 70%);
}

/* ========== Glitch title ========== */
.geek-glitch { position: relative; }
.geek-glitch:before, .geek-glitch:after {
  content: attr(data-text);
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
}
.geek-glitch:before { color: var(--geek-color-red);  mix-blend-mode: screen; animation: geek-glitch-a 3s steps(1) infinite; }
.geek-glitch:after  { color: var(--geek-color-teal); mix-blend-mode: screen; animation: geek-glitch-b 3s steps(1) infinite; }

/* ========== Timeline ========== */
.geek-timeline {
  position: relative;
  padding-left: 24px;
  background: linear-gradient(180deg, transparent 0%, var(--geek-color-red) 8%, var(--geek-color-red) 92%, transparent 100%);
  background-position: left top;
  background-size: 1px 100%;
  background-repeat: no-repeat;
}
.geek-timeline__node {
  width: 11px;
  height: 11px;
  border-radius: 50%;
  border: 2px solid var(--geek-color-bg);
  background: var(--geek-color-red);
  box-shadow: 0 0 14px var(--geek-color-red);
}

/* ========== Typewriter caret ========== */
.geek-typewriter__caret {
  display: inline-block;
  width: .6ch;
  color: var(--geek-color-red);
  animation: geek-blink 1s steps(1) infinite;
}

/* ========== Animations ========== */
@keyframes geek-blink { 50% { opacity: 0; } }
@keyframes geek-fade-up {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes geek-glitch-a {
  0%, 87%, 100% { transform: translate(0); clip-path: inset(0); }
  88% { transform: translate(-3px); clip-path: inset(0 0 60% 0); }
  92% { transform: translate(3px);  clip-path: inset(40% 0 0 0); }
  96% { transform: translate(-2px); clip-path: inset(0 0 80% 0); }
}
@keyframes geek-glitch-b {
  0%, 87%, 100% { transform: translate(0); clip-path: inset(0); }
  90% { transform: translate(3px);  clip-path: inset(55% 0 0 0); }
  94% { transform: translate(-3px); clip-path: inset(0 0 45% 0); }
  98% { transform: translate(2px);  clip-path: inset(60% 0 0 0); }
}
.geek-anim--reveal { animation: geek-fade-up var(--geek-motion-reveal) ease both; }

@media (prefers-reduced-motion: reduce) {
  .geek-btn, .geek-card, .geek-panel, .geek-window, .geek-glitch:before,
  .geek-glitch:after, .geek-typewriter__caret, [class*="geek-anim"] {
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

    spacing_base = parse_positive_int(
        field_in_table(text, "Grid Unit") or field_in_table(text, "Spacing base"), 4
    )
    radius = parse_positive_int(field_in_table(text, "Corner radius"), 0)
    border = parse_positive_int(field_in_table(text, "Border weight"), 1)

    root = build_root_vars(palette, spacing_base, radius, border)
    css = (
        "/* Generated by pixel-ui-maker theme_scaffolder.py (geek lock) — skeleton, extend in Step 4 */\n"
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
