#!/usr/bin/env python3
"""
Palette Extractor for Pixel UI Maker

Extracts all HEX colors used in a CSS file and reports their usage counts,
so you can verify the implementation stays on the declared palette.

Usage:
    python palette_extractor.py <css_file> [--format hex|json] [--output FILE]
"""

import argparse
import json
import os
import re
import sys
from collections import Counter

HEX_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")


def extract_colors(css_path):
    """Count all HEX color tokens in a CSS file, normalized to 6-digit uppercase."""
    with open(css_path, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()

    counter = Counter()
    for match in HEX_RE.findall(text):
        h = match[1:]
        if len(h) == 3:  # shorthand #abc -> #aabbcc
            h = "".join(ch * 2 for ch in h)
        elif len(h) in (4, 8):  # #rgba / #rrggbbaa -> drop alpha
            h = h[:3] if len(h) == 4 else h[:6]
        counter[h.upper()] += 1

    return counter


def analyze_css(css_path):
    """Analyze a CSS file for size and style characteristics."""
    with open(css_path, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()

    return {
        "filename": os.path.basename(css_path),
        "size_bytes": os.path.getsize(css_path),
        "lines": len(text.splitlines()),
        "unique_colors": len(extract_colors(css_path)),
        "has_gradient": bool(re.search(r"(linear|radial|conic)-gradient", text)),
        "has_filter_blur": bool(re.search(r"filter\s*:\s*[^;}]*blur", text)),
        "class_count": len(re.findall(r"\.geek-[\w-]+", text)),
    }


def main():
    parser = argparse.ArgumentParser(description="Extract pixel UI palette from a CSS file")
    parser.add_argument("css", help="Path to CSS file")
    parser.add_argument("--format", choices=["hex", "json"], default="hex",
                        help="Output format (default: hex)")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")
    parser.add_argument("--analyze-only", action="store_true",
                        help="Only analyze file characteristics, skip palette listing")
    args = parser.parse_args()

    if not os.path.exists(args.css):
        print(f"ERROR: File not found: {args.css}", file=sys.stderr)
        sys.exit(1)

    result = {}
    result["analysis"] = analyze_css(args.css)

    if not args.analyze_only:
        counter = extract_colors(args.css)
        total = sum(counter.values())
        colors = []
        for hex_color, count in counter.most_common():
            colors.append({
                "hex": f"#{hex_color}",
                "occurrences": count,
                "usage_pct": round(count / total * 100, 1) if total else 0,
            })
        result["palette"] = colors
        result["formatted"] = [c["hex"] for c in colors]

    output = json.dumps(result, indent=2) if args.format == "json" else str(result)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Palette written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
