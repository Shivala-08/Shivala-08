#!/usr/bin/env python3
"""
Render the profile activity radar (Phase 4 of the revamp) in the unified palette.

Reads stats.json (written by fetch_stats.py) and writes a theme-aware pair:
    out/radar.svg        dark  — deep space #05060A
    out/radar-light.svg  light — #F8FAFC

Palette rules (Phase 1): cyan carries structure (grid, spokes, shape), gold
carries the one number worth emphasising (the centre total), titanium grey
carries axis labels and grid lines.
"""
import html
import json
import math
import os
import sys

W, H = 560, 452
CX, CY, R = 262, 248, 132
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

THEMES = {
    "dark": {
        "BG": "#05060A", "PANEL": "#080C14", "BAR": "#0A0E16",
        "CYAN": "#00E5FF", "GOLD": "#FFC857", "MUTED": "#8892A6",
        "DIM": "#4E5868", "TEXT": "#F8FAFC",
        "GRID": "rgba(136,146,166,0.30)", "SPOKE": "rgba(136,146,166,0.22)",
        "FILL": "rgba(0,229,255,0.16)", "STROKE": "rgba(0,229,255,0.28)",
        "BARLINE": "rgba(136,146,166,0.08)", "PLATE": "rgba(0,229,255,0.06)",
    },
    "light": {
        "BG": "#F8FAFC", "PANEL": "#FFFFFF", "BAR": "#F1F5F9",
        "CYAN": "#0891B2", "GOLD": "#A16207", "MUTED": "#64748B",
        "DIM": "#94A3B8", "TEXT": "#0F172A",
        "GRID": "rgba(100,116,139,0.30)", "SPOKE": "rgba(100,116,139,0.22)",
        "FILL": "rgba(8,145,178,0.16)", "STROKE": "rgba(8,145,178,0.30)",
        "BARLINE": "rgba(100,116,139,0.08)", "PLATE": "rgba(8,145,178,0.05)",
    },
}

# axis label, key in stats.json
AXES = [
    ("COMMITS", "commits"),
    ("ISSUES", "issues"),
    ("PULL REQS", "pulls"),
    ("REVIEWS", "reviews"),
    ("REPOS", "repos"),
]

RINGS = (0.25, 0.5, 0.75, 1.0)


def esc(s):
    return html.escape(str(s), quote=True)


def vertex(i, frac=1.0, radius=R):
    angle = math.radians(-90 + i * 72)
    return (CX + radius * frac * math.cos(angle), CY + radius * frac * math.sin(angle))


def polygon(fracs):
    pts = [vertex(i, f) for i, f in enumerate(fracs)]
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def label_anchor(i):
    """Text anchoring + dy so labels sit outside the pentagon without colliding."""
    if i == 0:
        return "middle", -6
    if i == 1:
        return "start", 2
    if i == 2:
        return "start", 8
    if i == 3:
        return "end", 8
    return "end", 2


def build(stats, theme):
    t = THEMES[theme]
    values = [int(stats.get(key, 0) or 0) for _, key in AXES]
    # Log scaling: raw counts on these axes span two orders of magnitude
    # (1.2k commits vs 16 pull requests), so a linear radar collapses every
    # axis but the largest into the centre. The header says so out loud.
    biggest = max(values) or 1
    scale = math.log1p(biggest)
    fracs = [max(math.log1p(v) / scale, 0.06) for v in values]
    total = sum(values)
    window = esc(stats.get("window", "last 12 months"))

    s = []
    a = s.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
      f'font-family="{FONT}" role="img" '
      f'aria-label="GitHub activity radar: commits {values[0]}, issues {values[1]}, '
      f'pull requests {values[2]}, reviews {values[3]}, repositories {values[4]}">')
    a(f'<rect width="{W}" height="{H}" rx="14" fill="{t["BG"]}"/>')
    a(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="13.5" fill="{t["PANEL"]}" stroke="{t["STROKE"]}"/>')
    a(f'<path d="M0 34 H{W} " stroke="{t["BARLINE"]}"/>')

    # header — mirrors the banner / projects panel chrome
    a(f'<text x="18" y="22" font-size="11" letter-spacing="2" fill="{t["CYAN"]}">ACTIVITY.RADAR</text>')
    a(f'<text x="168" y="22" font-size="10" fill="{t["DIM"]}">$ ./stats.sh --radar</text>')
    a(f'<text x="{W - 18}" y="22" font-size="10" text-anchor="end" fill="{t["MUTED"]}">{window} · log scale</text>')

    # grid rings + spokes
    for frac in RINGS:
        outer = ' opacity="0.55"' if frac == 1.0 else ""
        a(f'<polygon points="{polygon([frac] * 5)}" fill="none" stroke="{t["GRID"]}" '
          f'stroke-width="1"{outer}/>')
    for i in range(5):
        x, y = vertex(i)
        a(f'<line x1="{CX}" y1="{CY}" x2="{x:.1f}" y2="{y:.1f}" stroke="{t["SPOKE"]}" stroke-width="1"/>')

    # the shape itself — cyan, gently pulsing like the rest of the profile
    a(f'<polygon points="{polygon(fracs)}" fill="{t["FILL"]}" stroke="{t["CYAN"]}" stroke-width="1.8" '
      f'stroke-linejoin="round">'
      f'<animate attributeName="fill-opacity" values="1;0.55;1" dur="3.6s" repeatCount="indefinite"/></polygon>')

    # vertex dots — cyan, staggered pulse
    for i, frac in enumerate(fracs):
        x, y = vertex(i, frac)
        a(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.2" fill="{t["CYAN"]}">'
          f'<animate attributeName="opacity" values="1;0.45;1" dur="1.8s" begin="{i * 0.22:.2f}s" '
          f'repeatCount="indefinite"/></circle>')

    # axis labels (grey) + values (gold — the emphasis in this panel)
    for i, ((label, _), value) in enumerate(zip(AXES, values)):
        lx, ly = vertex(i, 1.0, R + 30)
        anchor, dy = label_anchor(i)
        a(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" font-size="9.5" '
          f'letter-spacing="1.2" fill="{t["MUTED"]}">{label}</text>')
        a(f'<text x="{lx:.1f}" y="{ly + 15:.1f}" text-anchor="{anchor}" font-size="14" '
          f'font-weight="700" fill="{t["GOLD"]}">{value:,}</text>')

    # centre plate — the single headline number, in gold
    a(f'<circle cx="{CX}" cy="{CY}" r="44" fill="{t["PLATE"]}" stroke="{t["STROKE"]}"/>')
    a(f'<text x="{CX}" y="{CY + 2}" text-anchor="middle" font-size="22" font-weight="700" '
      f'fill="{t["GOLD"]}">{total:,}</text>')
    a(f'<text x="{CX}" y="{CY + 18}" text-anchor="middle" font-size="8.5" letter-spacing="1.4" '
      f'fill="{t["MUTED"]}">TOTAL</text>')

    a('</svg>')
    return "".join(s)


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "stats.json"
    outdir = sys.argv[2] if len(sys.argv) > 2 else "out"
    with open(src) as f:
        stats = json.load(f)
    os.makedirs(outdir, exist_ok=True)
    for theme, name in (("dark", "radar.svg"), ("light", "radar-light.svg")):
        svg = build(stats, theme)
        path = os.path.join(outdir, name)
        with open(path, "w") as f:
            f.write(svg)
        print(f"wrote {path}: {theme}, {len(svg) // 1024}KB")


if __name__ == "__main__":
    main()
