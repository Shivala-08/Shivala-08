#!/usr/bin/env python3
"""
Render the contribution reactor core — the profile's activity instrument.

Reads reactor.json (written by fetch_reactor.py) and writes a theme-aware pair:

    out/reactor.svg        dark  — deep space #05060A
    out/reactor-light.svg  light — #F8FAFC

Why this replaced the 3D contribution graph: the extruded-cube calendar is the
single most template-looking asset on a dev profile, and its cubes are hard to
read as volume. This panel shows the same 53 weeks as a heat ring where colour
is the only encoding — low weeks are cyan, the peak week is gold, quiet weeks
are plain graphite. On top of that it adds numbers the old graph never showed
(peak week, active weeks, average, longest daily run) and a measured language
mix, so everything in it is data rather than decoration.

Palette rules (Phase 1) are respected literally: every paint token is either a
palette hex or a computed rgb() on that theme's cyan -> gold ramp, with alpha
carried in a separate opacity attribute. scripts/check_palette.py verifies both
before this file is published.

The Stark reference stays in the caption line. The header names the instrument.

Light mode is not the dark theme with different hexes. On deep space the accents
are luminous, so structure can sit at 20-35% alpha. On white that same alpha
disappears (a 0.22 titanium ring measures 1.32:1 against #FFFFFF), so every
structural and text tier below is tuned per theme and measured against the
surface it actually sits on — see the comments on THEMES.
"""
import datetime
import html
import json
import math
import os
import sys

W, H = 580, 620
CX, CY = 290, 340
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

R_BAND = 170        # radius of the 53-week heat ring
BAND_W = 9          # stroke width of that ring
BAND_GAP = 1.6      # degrees of dead space between week arcs
R_CAGE = 158        # cyan cage edge; spokes and the sweep end here
R_MID = 140
R_IN = 104          # cage floor; also the inner limit of the sweep annulus
R_SWEEP_IN = 108
R_SWEEP_OUT = 152
R_PLATE = 92        # opaque plate so the headline number never sits on motion

# Ramp stops — must match scripts/check_palette.py RAMP_ASSETS (asserted by
# scripts/test_reactor.py, so the palette gate cannot silently drift from here).
#
# Dark is a straight two-stop cyan -> gold segment. Light cannot be: cyan and
# gold are near-complementary, so interpolating between them on a light surface
# collapses chroma to ~23 at mid-scale (a muddy sage at 47.6 L*), which is what
# "washed out" actually was. Routing the light ramp through the palette's own
# green holds chroma at 33-47 across the whole path while staying cyan -> gold
# at the ends. All three stops are Phase 1 palette colours.
RAMPS = {
    "dark": ((0, 229, 255), (255, 200, 87)),
    "light": ((8, 145, 178), (5, 150, 105), (161, 98, 7)),
}

# Opacities are floats and get formatted at the point of use. Every value below
# is the result of measuring the composited colour against its own surface; the
# dark column is the original tuning, the light column is tuned for #FFFFFF.
# SUB is the small-text tier: light's #94A3B8 dim grey measures 2.56:1 on white
# — below legibility for 9px text — so light uses titanium #64748B (4.76:1).
THEMES = {
    "dark": {
        "BG": "#05060A", "PANEL": "#080C14",
        "CYAN": "#00E5FF", "GOLD": "#FFC857", "GREEN": "#2ED573",
        "MUTED": "#8892A6", "DIM": "#4E5868", "TEXT": "#F8FAFC",
        "SUB": "#4E5868",                       # 2.72:1 on the panel
        "QUIET": "#4E5868",                     # quiet weeks — 1.24:1, deliberately recessive
        "PLATE": "rgba(0,229,255,0.06)",
        "OP_QUIET": 0.30, "OP_RING_IN": 0.22, "OP_RING_MID": 0.14,
        "OP_SPOKE": 0.20, "OP_CAGE": 0.35, "OP_CAGE_LO": 0.16,
        "OP_PLATE": 0.45, "OP_PLATE_LO": 0.18, "SWEEP": 0.55,
    },
    "light": {
        "BG": "#F8FAFC", "PANEL": "#FFFFFF",
        "CYAN": "#0891B2", "GOLD": "#A16207", "GREEN": "#059669",
        "MUTED": "#64748B", "DIM": "#94A3B8", "TEXT": "#0F172A",
        "SUB": "#64748B",                       # 4.76:1 on white
        "QUIET": "#64748B",                     # quiet weeks — visible on white, still recessive
        "PLATE": "#F1F5F9",                     # a real surface, not a 1.06:1 wash
        "OP_QUIET": 0.45, "OP_RING_IN": 0.34, "OP_RING_MID": 0.24,
        "OP_SPOKE": 0.30, "OP_CAGE": 0.58, "OP_CAGE_LO": 0.30,
        "OP_PLATE": 0.60, "OP_PLATE_LO": 0.32, "SWEEP": 0.70,
    },
}

# Language-bar segments are large areas, so the recessive tiers can sit lower
# than the text tiers above. Palette colours only, never GitHub's brand colours.
BAR_COLORS = ("CYAN", "GOLD", "GREEN", "MUTED", "DIM")
STEP = 360.0 / 53.0


def esc(s):
    return html.escape(str(s), quote=True)


def ramp(t, theme):
    """Point on that theme's ramp, walked as a polyline and clamped to [0, 1]."""
    stops = RAMPS[theme]
    spans = len(stops) - 1
    t = max(0.0, min(1.0, t))
    seg = min(int(t * spans), spans - 1)
    local = (t - seg / spans) * spans
    a, b = stops[seg], stops[seg + 1]
    return "rgb({},{},{})".format(*[round(a[i] + (b[i] - a[i]) * local) for i in range(3)])


def polar(radius, deg):
    a = math.radians(deg)
    return CX + radius * math.cos(a), CY + radius * math.sin(a)


def arc(radius, a0, a1):
    """SVG arc path between two angles at a fixed radius."""
    x0, y0 = polar(radius, a0)
    x1, y1 = polar(radius, a1)
    return f"M {x0:.1f} {y0:.1f} A {radius} {radius} 0 0 1 {x1:.1f} {y1:.1f}"


def week_values(weeks):
    """Volume used for colour, one value per week.

    A partial *final* week is in progress rather than quiet, so it is scaled to
    a full week — otherwise the arc next to the gold "now" tick would read as a
    collapse in activity every day except Saturday. A partial *first* week is
    made of days that fall outside the window, so it is left alone.
    """
    out, last = [], len(weeks) - 1
    for i, w in enumerate(weeks):
        n = len(w.get("days") or []) or 7
        total = float(w.get("total") or 0)
        out.append(total * 7 / n if (i == last and n < 7) else total)
    return out


def date_range(start, end):
    if not start or not end:
        return ""
    a = datetime.date.fromisoformat(start)
    b = datetime.date.fromisoformat(end)
    ma, mb = a.strftime("%b").upper(), b.strftime("%b").upper()
    if (a.month, a.year) == (b.month, b.year):
        return f"{a.day:02d}–{b.day:02d} {ma} {b.year}"
    return f"{a.day:02d} {ma} – {b.day:02d} {mb} {b.year}"


def readout(label, value, sub, x, y, anchor, t, gold=False):
    """One instrument readout: grey label, value, dim sub-line."""
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="9" letter-spacing="1.2" '
        f'fill="{t["MUTED"]}">{label}</text>'
        f'<text x="{x}" y="{y + 26}" text-anchor="{anchor}" font-size="22" font-weight="700" '
        f'fill="{t["GOLD"] if gold else t["TEXT"]}">{value}</text>'
        f'<text x="{x}" y="{y + 40}" text-anchor="{anchor}" font-size="8.5" letter-spacing="0.6" '
        f'fill="{t["SUB"]}">{sub}</text>'
    )


def language_bar(langs, t):
    """Segmented byte-share bar plus a legend, top four languages and the rest."""
    items = list(langs.items())[:4]
    other = sum(int(v) for _, v in list(langs.items())[4:])
    if other:
        items.append(("Other", other))
    if not items:
        return ""

    total = sum(int(v) for _, v in items) or 1
    x0, y, w, h = 20, 548, W - 40, 12
    e = []
    a = e.append
    a(f'<text x="{x0}" y="{y - 10}" font-size="9" letter-spacing="1.2" fill="{t["MUTED"]}">LANGUAGE MIX</text>')
    a(f'<text x="{W - x0}" y="{y - 10}" text-anchor="end" font-size="9" letter-spacing="1.2" '
      f'fill="{t["SUB"]}">MEASURED BYTES · {len(langs)} LANGUAGES</text>')
    a(f'<rect x="{x0}" y="{y}" width="{w}" height="{h}" rx="6" fill="{t["PLATE"]}"/>')

    cursor = float(x0)
    for i, (name, size) in enumerate(items):
        seg = w * int(size) / total
        # keep a hairline gap so segments stay distinguishable at any share
        draw = max(seg - (1.5 if i < len(items) - 1 else 0), 2.0)
        a(f'<rect x="{cursor:.1f}" y="{y}" width="{draw:.1f}" height="{h}" rx="3" '
          f'fill="{t[BAR_COLORS[i % len(BAR_COLORS)]]}"/>')
        cursor += seg

    cursor = float(x0)
    for i, (name, size) in enumerate(items):
        colour = t[BAR_COLORS[i % len(BAR_COLORS)]]
        label = f"{name.upper()} {round(100 * int(size) / total)}%"
        a(f'<rect x="{cursor:.1f}" y="{y + 24}" width="7" height="7" rx="1.5" fill="{colour}"/>')
        a(f'<text x="{cursor + 11:.1f}" y="{y + 31}" font-size="9.5" fill="{t["MUTED"]}">{esc(label)}</text>')
        # monospace: 9.5px glyphs advance ~5.7px, so the layout stays exact
        cursor += 11 + len(label) * 5.7 + 16
    return "".join(e)


def build(stats, theme):
    t = THEMES[theme]
    weeks = stats.get("weeks") or []
    if not weeks:
        raise SystemExit("reactor.json has no weeks — did fetch_reactor.py run?")

    values = week_values(weeks)
    raw = [float(w.get("total") or 0) for w in weeks]
    denom = max(values) or 1.0
    peak = max(raw)
    peak_i = raw.index(peak)
    active = sum(1 for v in raw if v > 0)
    total = int(stats.get("total") or sum(raw))
    avg = round(total / active) if active else 0
    langs = stats.get("languages") or {}
    window = esc(stats.get("window", "last 12 months")).upper()
    since = (weeks[0].get("start") or "")
    sweep = t["SWEEP"]

    s = []
    a = s.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
      f'font-family="{FONT}" role="img" aria-label="Contribution reactor core: {total} contributions over '
      f'{len(weeks)} weeks, peak week {int(peak)} ({date_range(weeks[peak_i].get("start"), weeks[peak_i].get("end"))}), '
      f'{active} active weeks, average {avg} per active week, longest run {stats.get("longest_run", 0)} days">')
    a(f'<rect width="{W}" height="{H}" rx="14" fill="{t["BG"]}"/>')
    a(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="13.5" fill="{t["PANEL"]}" '
      f'stroke="{t["CYAN"]}" stroke-opacity="0.28"/>')

    # ---- header: instrument name, invocation, window ------------------------
    a(f'<text x="18" y="22" font-size="11" letter-spacing="2" fill="{t["CYAN"]}">CONTRIBUTION.CORE</text>')
    a(f'<text x="180" y="22" font-size="10" fill="{t["SUB"]}">$ ./reactor.sh --window=12mo</text>')
    a(f'<text x="{W - 18}" y="22" text-anchor="end" font-size="10" fill="{t["MUTED"]}">'
      f'{len(weeks)} WEEKS · {window}</text>')
    a(f'<line x1="0" y1="34" x2="{W}" y2="34" stroke="{t["MUTED"]}" stroke-opacity="0.08"/>')

    # ---- caption line: the Stark reference lives here, not in the title -----
    a(f'<text x="18" y="54" font-size="9.5" letter-spacing="0.8" fill="{t["MUTED"]}">'
      f'Stark Industries · Mk IV arc core</text>')
    a(f'<text x="{W - 18}" y="54" text-anchor="end" font-size="9.5" letter-spacing="0.8" fill="{t["SUB"]}">'
      f'gold tick = current week · ramp cyan → gold</text>')

    # ---- readouts ----------------------------------------------------------
    a(readout("PEAK WEEK", f"{int(peak)}", date_range(weeks[peak_i].get("start"), weeks[peak_i].get("end")),
              20, 100, "start", t, gold=True))
    a(readout("ACTIVE WEEKS", f"{active}", f"OF {len(weeks)} TRACKED", 20, 176, "start", t))
    a(readout("AVG / ACTIVE WEEK", f"{avg}", "CONTRIBUTIONS", W - 20, 100, "end", t))
    a(readout("LONGEST RUN", f'{int(stats.get("longest_run") or 0)}', "CONSECUTIVE DAYS", W - 20, 176, "end", t))

    # ---- cage: structural rings + six spokes -------------------------------
    a(f'<circle cx="{CX}" cy="{CY}" r="{R_IN}" fill="none" stroke="{t["MUTED"]}" '
      f'stroke-opacity="{t["OP_RING_IN"]:.2f}"/>')
    a(f'<circle cx="{CX}" cy="{CY}" r="{R_MID}" fill="none" stroke="{t["MUTED"]}" '
      f'stroke-opacity="{t["OP_RING_MID"]:.2f}"/>')
    a(f'<circle cx="{CX}" cy="{CY}" r="{R_CAGE}" fill="none" stroke="{t["CYAN"]}" '
      f'stroke-opacity="{t["OP_CAGE"]:.2f}">'
      f'<animate attributeName="stroke-opacity" '
      f'values="{t["OP_CAGE"]:.2f};{t["OP_CAGE_LO"]:.2f};{t["OP_CAGE"]:.2f}" dur="4.5s" '
      f'repeatCount="indefinite"/></circle>')
    for i in range(6):
        x0, y0 = polar(R_IN, -90 + i * 60)
        x1, y1 = polar(R_CAGE, -90 + i * 60)
        a(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" '
          f'stroke="{t["MUTED"]}" stroke-opacity="{t["OP_SPOKE"]:.2f}"/>')

    # ---- sweep: a slow comet rotating inside the cage ----------------------
    trail = [(0.0, sweep, 1.6), (-4.0, sweep * 0.4, 1.3),
             (-8.0, sweep * 0.24, 1.1), (-12.5, sweep * 0.13, 0.9)]
    a(f'<g><animateTransform attributeName="transform" type="rotate" '
      f'values="0 {CX} {CY};360 {CX} {CY}" dur="14s" repeatCount="indefinite"/>')
    for offset, opacity, width in trail:
        x0, y0 = polar(R_SWEEP_IN, -90 + offset)
        x1, y1 = polar(R_SWEEP_OUT, -90 + offset)
        a(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{t["CYAN"]}" '
          f'stroke-opacity="{opacity:.2f}" stroke-width="{width}"/>')
    tx, ty = polar(R_SWEEP_OUT, -90)
    a(f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="3" fill="{t["CYAN"]}" opacity="0.9"/>')
    a('</g>')

    # ---- the ring: 53 weeks of volume, cyan -> gold, quiet weeks graphite ---
    for i, value in enumerate(values):
        a0 = -90 + i * STEP + BAND_GAP / 2
        a1 = -90 + (i + 1) * STEP - BAND_GAP / 2
        if raw[i] <= 0:
            a(f'<path d="{arc(R_BAND, a0, a1)}" fill="none" stroke="{t["QUIET"]}" '
              f'stroke-opacity="{t["OP_QUIET"]:.2f}" stroke-width="{BAND_W}"/>')
            continue
        a(f'<path d="{arc(R_BAND, a0, a1)}" fill="none" stroke="{ramp(value / denom, theme)}" '
          f'stroke-width="{BAND_W}"/>')

    # current week: gold tick + pulsing dot, outside the ring so it reads as a marker
    now = -90 + (len(weeks) - 0.5) * STEP
    x0, y0 = polar(R_BAND + BAND_W / 2 + 3, now)
    x1, y1 = polar(R_BAND + 20, now)
    a(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{t["GOLD"]}" stroke-width="3"/>')
    dx, dy = polar(R_BAND + 11, now)
    a(f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="3.5" fill="{t["GOLD"]}">'
      f'<animate attributeName="opacity" values="1;0.25;1" dur="2s" repeatCount="indefinite"/></circle>')

    # ---- core plate: the one number worth emphasising ----------------------
    a(f'<circle cx="{CX}" cy="{CY}" r="{R_PLATE}" fill="{t["PLATE"]}" stroke="{t["CYAN"]}" '
      f'stroke-opacity="{t["OP_PLATE"]:.2f}" stroke-width="2">'
      f'<animate attributeName="stroke-opacity" '
      f'values="{t["OP_PLATE"]:.2f};{t["OP_PLATE_LO"]:.2f};{t["OP_PLATE"]:.2f}" dur="4s" '
      f'repeatCount="indefinite"/></circle>')
    a(f'<text x="{CX}" y="{CY - 18}" text-anchor="middle" font-size="8" letter-spacing="1.6" '
      f'fill="{t["MUTED"]}">TOTAL CONTRIBUTIONS</text>')
    a(f'<text x="{CX}" y="{CY + 14}" text-anchor="middle" font-size="36" font-weight="700" '
      f'fill="{t["GOLD"]}">{total:,}</text>')
    a(f'<text x="{CX}" y="{CY + 36}" text-anchor="middle" font-size="8" letter-spacing="1" '
      f'fill="{t["SUB"]}">SINCE {esc(since)}</text>')

    # ---- language mix ------------------------------------------------------
    a(language_bar(langs, t))

    a('</svg>')
    return "".join(s)


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "reactor.json"
    outdir = sys.argv[2] if len(sys.argv) > 2 else "out"
    with open(src) as f:
        stats = json.load(f)
    os.makedirs(outdir, exist_ok=True)
    for theme, name in (("dark", "reactor.svg"), ("light", "reactor-light.svg")):
        svg = build(stats, theme)
        path = os.path.join(outdir, name)
        with open(path, "w") as f:
            f.write(svg)
        print(f"wrote {path}: {theme}, {len(svg) // 1024}KB")


if __name__ == "__main__":
    main()
