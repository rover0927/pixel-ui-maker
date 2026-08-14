#!/usr/bin/env python3
"""
Style Validator for Pixel UI Maker (dark terminal / geek lock)

Validates a CSS file against the "geek lock" rules (SJTU SITA dark-hacker-terminal language):
- All HEX colors come from the declared palette OR the theme's own custom properties
- border-radius: 0px on boxes (allowed: 0/1/2px, 50% on dots, 8px on scrollbars)
- Soft shadows + neon glows allowed (blur/spread unrestricted)
- Gradients allowed (grid lines, CRT scanlines, radial glows)
- filter: blur / backdrop-filter allowed (blurred nav)
- Fractional opacity allowed
- Spacing: integer px only (no strict grid enforcement)
- Class names follow a prefix contract (when --prefix given)

Custom properties (var(--geek-*)) are resolved against the file's own :root
definitions before validation, so themed components validate cleanly.

Usage:
    python style_validator.py <css_file> [--palette HEX HEX ...] [--spec FILE]
        [--prefix geek-] [--strict] [--output FILE]
    (--grid is accepted and ignored for backward compatibility)
"""

import argparse
import json
import os
import re
import sys

HEX_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")
CLASS_RE = re.compile(r"\.([a-zA-Z_][\w-]*)")
VAR_DEF_RE = re.compile(r"(--[\w-]+)\s*:\s*([^;}\n]+)")
VAR_USE_RE = re.compile(r"var\(\s*(--[\w-]+)(?:\s*,\s*([^)]*))?\s*\)")
# Ruleset = selector { body } where the body has no nested braces (works inside @media too)
RULESET_RE = re.compile(r"([^{}]+)\{([^{}]*)\}", re.DOTALL)


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


def check_corners(text, violations):
    """Every border-radius is 0 on boxes; allow 1/2px, 50% (dots), 8px (scrollbars)."""
    for m in RULESET_RE.finditer(text):
        selector, body = m.group(1), m.group(2)
        for dm in re.finditer(r"border-radius\s*:\s*([^;}]+)", body, re.IGNORECASE):
            decl = dm.group(1).strip()
            if "var(" in decl:
                continue  # cannot evaluate; assume themed radius
            for value, unit in re.findall(r"(\d*\.?\d+)(px|%)\b", decl):
                fv = float(value)
                if unit == "%":
                    if fv != 50:
                        violations.append(f"border-radius {value}% must be 50% (dots) only: {decl}")
                else:
                    is_scrollbar = "scrollbar" in selector.lower()
                    if fv > 2 or (is_scrollbar and fv not in (0, 1, 2, 8)):
                        violations.append(
                            f"border-radius {value}px exceeds the 0px geek limit "
                            f"(allowed 0/1/2px, 50% dots, 8px scrollbars): {decl}"
                        )


def check_shadows(text, var_map, warnings):
    """Shadows are unrestricted (soft + glow). Only warn on unresolvable var()."""
    for m in re.finditer(r"box-shadow\s*:\s*([^;}]+)", text, re.IGNORECASE):
        decl = m.group(1)
        for part in decl.split(","):
            part = part.strip()
            if not part:
                continue
            if resolve_vars(part, var_map) is None:
                warnings.append(f"Unresolvable var() in box-shadow: {part}")


def check_spacing(text, warnings, violations, strict):
    """Flag non-integer px in padding/margin/gap/inset (warning; violation under --strict)."""
    props = r"(padding|margin|gap|row-gap|column-gap|inset)(?:-[a-z]+)?"
    for m in re.finditer(r"(" + props + r")\s*:\s*([^;}]+)", text, re.IGNORECASE):
        decl = m.group(3)
        for num in re.findall(r"(\d+\.?\d*)px", decl):
            if float(num) % 1 != 0:
                msg = f"Non-integer spacing {num}px in {m.group(1)}: {decl.strip()}"
                if strict:
                    violations.append(msg)
                else:
                    warnings.append(msg)


def check_naming(text, prefix, warnings):
    """Flag class selectors that do not follow the prefix contract.

    The signature `.corner` helper is unprefixed by design and exempt.
    """
    exempt = {"corner"}
    for cls in sorted(set(CLASS_RE.findall(text))):
        if cls in exempt:
            continue
        if not cls.startswith(prefix):
            warnings.append(f"Class '.{cls}' does not follow '{prefix}' prefix contract")


def validate_css(css_path, palette=None, spec=None, prefix=None, strict=False, grid=None):
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

    # 2. Corners (geek: 0px boxes, dots 50%, scrollbars 8px)
    check_corners(css, results["violations"])

    # 3. box-shadow — unrestricted (soft + glow), warn on unresolvable vars
    check_shadows(css, var_map, results["warnings"])

    # 4. Spacing — integer px (warn; violation under --strict)
    check_spacing(css, results["warnings"], results["violations"], strict)

    # 5. naming contract
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
    parser = argparse.ArgumentParser(description="Validate CSS against geek style-lock rules")
    parser.add_argument("css", help="Path to CSS file")
    parser.add_argument("--palette", nargs="+", help="Declared palette hex values (e.g., #1d211c #c9151e)")
    parser.add_argument("--spec", help="Path to ui_spec.md for palette extraction")
    parser.add_argument("--grid", type=int, help="Deprecated (ignored) — spacing is integer px, not grid-locked")
    parser.add_argument("--prefix", default="geek-", help="Class prefix contract (default: geek-)")
    parser.add_argument("--strict", action="store_true", help="Warnings count as failure")
    parser.add_argument("--output", "-o", help="Output JSON file path")
    args = parser.parse_args()

    if not os.path.exists(args.css):
        print(f"ERROR: File not found: {args.css}", file=sys.stderr)
        sys.exit(1)

    palette = load_palette(args.palette) if args.palette else None
    results = validate_css(args.css, palette, args.spec, args.prefix, args.strict, args.grid)

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
