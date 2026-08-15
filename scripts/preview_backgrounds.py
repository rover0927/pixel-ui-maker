#!/usr/bin/env python3
"""
Preview Backgrounds for Pixel UI Maker

Zero-dependency local HTTP server (Python stdlib only) that serves the
skill's background toolkit gallery + demos from the examples/ directory.
Use it during Step 1 of the pipeline to let the user browse the dynamic
background effects live before deciding which to include.

Usage:
    python preview_backgrounds.py [--host 127.0.0.1] [--port 8000]

Serves:
    /                          -> examples/index.html            (gallery landing)
    /geek-effects-demo.html    -> the flat, no-build effect demo
    /geek-effects-demo.css     -> the flat demo stylesheet

Prints the reachable URL(s) and an effect catalog immediately, then keeps
serving until Ctrl+C. Ports are auto-incremented if the requested one is busy.
"""

import argparse
import socket
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

# ---------------------------------------------------------------------------
# Effect catalog (name, description, trigger, source, preview target)
# preview target: a "/..." URL for effects in the flat demo, or an npm command
# hint for effects that only exist in the Vue demos (not started by this server).
# ---------------------------------------------------------------------------
CATALOG = [
    # class, zh description, trigger, source, preview target
    ("geek-btn-wipe",      "双层擦除按钮",            "hover",            "geek 动效库",            "/geek-effects-demo.html"),
    ("geek-float-rise",    "背景像素画错峰上浮",       "panel open/scroll", "geek 动效库",            "/geek-effects-demo.html"),
    ("geek-marquee",       "四向滚动光带",            "loop",             "geek 动效库",            "/geek-effects-demo.html"),
    ("geek-crt-ripple",    "CRT 水波纹",              "loop",             "geek 动效库",            "/geek-effects-demo.html"),
    ("geek-float-parallax", "背景像素画视差浮动",      "pointermove",      "geek 动效库",            "Vue demo `geek-homepage/` (npm install && npm run dev)"),
    ("geek-particle-bg",   "像素粒子网络背景",         "pointermove/loop", "粒子指南",          "Vue demo `geek-homepage/` (npm install && npm run dev)"),
    ("geek-fluid-grid",    "流体网格像素背景",         "loop/pointermove", "流体网格 demo",     "Vue demo `fluid-grid-bg/` (npm install && npm run dev)"),
    ("geek-copy-params",   "复制参数交互",            "click",            "流体网格 demo",     "Vue demo `fluid-grid-bg/` (npm install && npm run dev)"),
]

EXAMPLES_DIR = (Path(__file__).resolve().parent.parent / "examples").resolve()


class QuietHandler(SimpleHTTPRequestHandler):
    """SimpleHTTPRequestHandler that serves EXAMPLES_DIR and logs briefly."""

    directory = str(EXAMPLES_DIR)

    def __init__(self, *args, directory=None, **kwargs):
        # Pass the target directory explicitly: SimpleHTTPRequestHandler.__init__
        # (3.7+) otherwise resets self.directory to os.getcwd().
        super().__init__(*args, directory=self.directory if directory is None else directory, **kwargs)

    def log_message(self, fmt, *args):  # keep stdout clean for URL capture
        sys.stderr.write("[preview] %s\n" % (fmt % args))


def pick_free_port(base):
    """Return the first free port in [base, base+49], or None if none free."""
    for port in range(base, base + 50):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
            except OSError:
                continue
            return port
    return None


def main():
    parser = argparse.ArgumentParser(description="Serve the pixel-ui-maker background toolkit locally (stdlib only)")
    parser.add_argument("--host", default="127.0.0.1", help="Bind host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="Base port (default: 8000, auto-increments if busy)")
    args = parser.parse_args()

    if not EXAMPLES_DIR.is_dir():
        print("ERROR: examples/ not found at %s" % EXAMPLES_DIR, file=sys.stderr)
        sys.exit(1)

    port = pick_free_port(args.port)
    if port is None:
        print("ERROR: no free port in %d..%d" % (args.port, args.port + 49), file=sys.stderr)
        sys.exit(1)
    if port != args.port:
        print("(port %d busy -> using %d)" % (args.port, port), file=sys.stderr)

    ThreadingHTTPServer.allow_reuse_address = 1
    server = ThreadingHTTPServer((args.host, port), QuietHandler)
    display_host = "127.0.0.1" if args.host in ("0.0.0.0", "") else args.host
    url_root = "http://%s:%d" % (display_host, server.server_address[1])

    bar = "=" * 70
    print(bar, flush=True)
    print("  pixel-ui-maker · 背景工具包本地预览 (local background toolkit)", flush=True)
    print("-" * 70, flush=True)
    print("  GALLERY  %s/" % url_root, flush=True)
    print("  DEMO     %s/geek-effects-demo.html" % url_root, flush=True)
    print("  (Ctrl+C 停止 / stop with Ctrl+C)", flush=True)
    print(bar, flush=True)

    print("\n 效果目录 / effect catalog:", flush=True)
    print("  %-22s %-18s %-16s %-12s %s" % ("class", "说明", "trigger", "source", "preview"), flush=True)
    print("  " + "-" * 66, flush=True)
    for name, desc, trigger, source, target in CATALOG:
        print("  %-22s %-18s %-16s %-12s %s" % (name, desc, trigger, source, target), flush=True)
    print(flush=True)
    print("  (Vue demo 效果不被本服务器启动，需自行运行所列 npm 命令；Vite dev 默认端口 5173)", flush=True)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nPreview stopped.", flush=True)
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
