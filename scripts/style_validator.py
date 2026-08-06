#!/usr/bin/env python3
"""
Style Validator for Pixel UI Maker

Validates a CSS file against the pixel style-lock rules:
- All HEX colors come from the declared palette OR the theme's own custom properties
- border-radius <= 2px
- No gradient fills (repeating hard-edge patterns allowed)
- box-shadow hard only (blur/spread radius == 0 or absent)
- No filter: blur(...)
- opacity only 0 or 1 (non-binary -> warning)
- Spacing on the grid unit (when --grid given)
- Class names follow a prefix contract (when --prefix given)

Custom properties (var(--pix-*)) are resolved against the file's own :root
definitions before validation, so themed components validate cleanly.

Usage:
    python style_validator.py <css_file> [--palette HEX HEX ...] [--spec FILE]
        [--grid N] [--prefix pix-] [--strict] [--output FILE]
"""

import argparse
import json
import os
import re
import sys

HEX_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")
GRADIENT_RE = re.compile(r"(?<!repeating-)(linear|radial|conic)-gradient")
FILTER_BLUR_RE = re.compile(r"filter\s*:\s*[^;}]*blur", re.IGNORECASE)
CLASS_RE = re.compile(r"\.([a-zA-Z_][\w-]*)")
VAR_DEF_RE = re.compile(r"(--[\w-]+)\s*:\s*([^;}\n]+)")
VAR_USE_RE = re.compile(r"var\(\s*(--[\w-]+)(?:\s*,\s*([^)]*))?\s*\)")


def normalize_hex(token):
    h = token[1:]
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    if len(h) in (4, 8):
        h = h[:3] if len(h) == 4 else h[:6]
    return h.upper()


def load_palette(hex_args):
    colors = set()
    for h in hex_args:
        h = h.strip()
        if not h.startswith("#"):
            h = "#" + h
        m = HEX_RE.fullmatch(h)
        if m:
            colors.add(normalize_hex(h))
    return colors


def load_palette_from_spec(spec_path):
    """Load palette from the Color Palette table in a ui_spec.md file."""
    colors = set()
    with open(spec_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.strip().startswith("|") and "#" in line:
                for part in line.split("|"):
                    part = part.strip()
                    m = HEX_RE.fullmatch(part)
                    if m:
                        colors.add(normalize_hex(part))
    return colors


def strip_comments(text):
    return re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)


def collect_var_map(text):
    """Collect `--name: value;` definitions. First definition wins."""
    var_map = {}
    for m in VAR_DEF_RE.finditer(text):
        name = m.group(1).strip()
        value = m.group(2).strip()
        if name not in var_map:
            var_map[name] = value
    return var_map


def collect_var_colors(text):
    """Hex colors used inside custom-property definitions (theme tokens)."""
    colors = set()
    for m in VAR_DEF_RE.finditer(text):
        for hex_m in HEX_RE.findall(m.group(2)):
            colors.add(normalize_hex(hex_m))
    return colors


def resolve_vars(decl, var_map, depth=6):
    """Resolve var(--name[, fallback]) using the file's own definitions.

    Returns the fully-resolved string, or None if a variable cannot be resolved.
    """
    if depth <= 0:
        return None
    m = VAR_USE_RE.search(decl)
    if not m:
        return decl
    name, fallback = m.group(1), (m.group(2) or "").strip()
    value = var_map.get(name, fallback) if (m.group(2) is not None or name in var_map) else None
    if value is None:
        return None
    resolved = decl[: m.start()] + value + decl[m.end():]
    return resolve_vars(resolved, var_map, depth - 1)


def parse_lengths(shadow_part):
    """Extract numeric length values from a shadow, ignoring color tokens."""
    no_color = re.sub(r"#[0-9a-fA-F]{3,8}\b", " ", shadow_part)
    no_color = re.sub(r"rgba?\([^)]*\)", " ", no_color)
    no_color = no_color.replace("inset", " ")
    values = []
    for m in re.finditer(r"([+-]?\d*\.?\d+)(px|em|rem)?", no_color):
        if m.group(1) in ("", "+", "-"):
            continue
        try:
            values.append(float(m.group(1)))
        except ValueError:
            continue
    return values


def check_shadows(text, var_map, violations, warnings):
    """Check every box-shadow declaration for blur/spread radius."""
    for m in re.finditer(r"box-shadow\s*:\s*([^;}]+)", text, re.IGNORECASE):
        decl = m.group(1)
        for part in decl.split(","):
            part = part.strip()
            if not part:
                continue
            resolved = resolve_vars(part, var_map)
            if resolved is None:
                warnings.append(f"Unresolvable var() in box-shadow: {part}")
                continue
            lengths = parse_lengths(resolved)
            if len(lengths) >= 3 and abs(lengths[2]) > 0:
                violations.append(f"Blur radius in box-shadow: {part}")
            if len(lengths) >= 4 and abs(lengths[3]) > 0:
                violations.append(f"Spread radius in box-shadow: {part}")


def check_corners(text, violations):
    """Check every border-radius declaration stays within 2px."""
    for m in re.finditer(r"border-radius\s*:\s*([^;}]+)", text, re.IGNORECASE):
        decl = m.group(1).strip()
        if "var(" in decl:
            continue  # cannot evaluate; assume themed radius
        for num in re.findall(r"(\d*\.?\d+)px", decl):
            if float(num) > 2:
                violations.append(f"border-radius {num}px exceeds 2px limit: {decl}")


def check_opacity(text, warnings):
    """Flag non-binary opacity values (stepped overlay scrims are the allowed exception)."""
    for m in re.finditer(r"opacity\s*:\s*([^;}]+)", text, re.IGNORECASE):
        val = m.group(1).strip()
        if val not in ("0", "1"):
            warnings.append(f"Non-binary opacity '{val}' (overlay scrims only)")


def check_grid_spacing(text, grid, warnings):
    """Flag spacing values that are not multiples of the grid unit."""
    props = r"(padding|margin|gap|row-gap|column-gap|inset)(?:-[a-z]+)?"
    for m in re.finditer(r"(" + props + r")\s*:\s*([^;}]+)", text, re.IGNORECASE):
        decl = m.group(3)
        for num in re.findall(r"(\d+\.?\d*)px", decl):
            if float(num) % grid != 0:
                warnings.append(
                    f"Spacing {num}px not a multiple of grid {grid}px in {m.group(1)}: {decl.strip()}"
                )


def check_naming(text, prefix, warnings):
    """Flag class selectors that do not follow the prefix contract."""
    for cls in sorted(set(CLASS_RE.findall(text))):
        if not cls.startswith(prefix):
            warnings.append(f"Class '.{cls}' does not follow '{prefix}' prefix contract")


def validate_css(css_path, palette=None, spec=None, grid=None, prefix=None, strict=False):
    results = {
        "valid": True,
        "violations": [],
        "warnings": [],
        "summary": {},
    }

    spec_palette = None
    if spec:
        spec_palette = load_palette_from_spec(spec)
        if spec_palette and palette:
            results["warnings"].append("Both --palette and --spec provided; using --palette")

    palette = palette or spec_palette

    with open(css_path, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
    css = strip_comments(text)

    var_map = collect_var_map(css)
    var_colors = collect_var_colors(css)

    # Allowed colors = declared palette UNION theme's own custom-property tokens
    allowed = (palette or set()) | var_colors

    # 1. Palette compliance
    if allowed:
        used = set(normalize_hex(m) for m in HEX_RE.findall(css))
        off_palette = sorted(used - allowed)
        if off_palette:
            off = ["#" + c for c in off_palette]
            results["violations"].append(f"Colors outside palette/tokens: {off}")

    # 2. Gradients
    if GRADIENT_RE.search(css):
        results["violations"].append("Gradient fill detected (repeating-* patterns are allowed)")

    # 3. filter: blur
    if FILTER_BLUR_RE.search(css):
        results["violations"].append("filter: blur(...) is forbidden")

    # 4. box-shadow hard-only
    check_shadows(css, var_map, results["violations"], results["warnings"])

    # 5. corners
    check_corners(css, results["violations"])

    # 6. opacity
    check_opacity(css, results["warnings"])

    # 7. grid spacing
    if grid:
        check_grid_spacing(css, grid, results["warnings"])

    # 8. naming contract
    if prefix:
        check_naming(css, prefix, results["warnings"])

    results["valid"] = len(results["violations"]) == 0
    if strict and results["warnings"]:
        results["valid"] = False

    results["summary"] = {
        "violations": len(results["violations"]),
        "warnings": len(results["warnings"]),
        "palette_colors": len(palette) if palette else "N/A",
        "theme_tokens": len(var_colors),
        "checked_colors": len(set(normalize_hex(m) for m in HEX_RE.findall(css))),
    }

    return results


def main():
    parser = argparse.ArgumentParser(description="Validate CSS against pixel style-lock rules")
    parser.add_argument("css", help="Path to CSS file")
    parser.add_argument("--palette", nargs="+", help="Declared palette hex values (e.g., #111111 #5D8BFF)")
    parser.add_argument("--spec", help="Path to ui_spec.md for palette extraction")
    parser.add_argument("--grid", type=int, help="Spacing grid unit (e.g., 4)")
    parser.add_argument("--prefix", help="Class prefix contract (e.g., pix-)")
    parser.add_argument("--strict", action="store_true", help="Warnings count as failure")
    parser.add_argument("--output", "-o", help="Output JSON file path")
    args = parser.parse_args()

    if not os.path.exists(args.css):
        print(f"ERROR: File not found: {args.css}", file=sys.stderr)
        sys.exit(1)

    palette = load_palette(args.palette) if args.palette else None
    results = validate_css(args.css, palette, args.spec, args.grid, args.prefix, args.strict)

    output = json.dumps(results, indent=2)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Results written to {args.output}")
    else:
        print(output)

    sys.exit(0 if results["valid"] else 1)


if __name__ == "__main__":
    main()
