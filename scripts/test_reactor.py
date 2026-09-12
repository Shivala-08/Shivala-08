#!/usr/bin/env python3
"""
Unit tests for the contribution reactor generator.

Run: python3 scripts/test_reactor.py     (or: python3 -m unittest discover scripts)

The generator is driven by whatever GitHub's contributionCalendar returns, and
the two cases that actually break it are the ones the live API only produces
sometimes: a partial week at either end, and a window with no activity at all.
Those are covered explicitly here rather than left to a manual eyeball after a
workflow run. Geometry is asserted numerically too — an arc that lands off the
canvas or a text row that collides is invisible in a diff but obvious on the
profile, so it is cheaper to catch here.
"""
import contextlib
import importlib.util
import io
import json
import os
import re
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NS = "{http://www.w3.org/2000/svg}"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


reactor = load("generate_reactor", ".github/scripts/generate_reactor.py")
palette = load("check_palette", "scripts/check_palette.py")


def week(start, days):
    return {"start": start, "end": start, "days": days, "total": sum(days)}


def stats(weeks, **overrides):
    """A reactor.json payload shaped like fetch_reactor.py writes it."""
    flat = [d for w in weeks for d in w["days"]]
    payload = {
        "user": "test",
        "window": "last 12 months",
        "weeks": weeks,
        "days": flat,
        "total": sum(flat),
        "longest_run": 0,
        "languages": {"Python": 700, "TypeScript": 200, "HTML": 100},
    }
    payload.update(overrides)
    return payload


FULL = stats([
    week("2025-09-07", [0, 0, 0, 0, 0, 0, 0]),      # quiet week
    week("2025-09-14", [1, 2, 3, 4, 5, 6, 7]),      # peak so far
    week("2025-09-21", [0, 0, 0, 0, 0, 1, 0]),
])


def ramp_tokens(svg):
    """rgb(...) three-argument colours — the ramp's own convention."""
    return re.findall(r'rgb\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)', svg)


def off_ramp_distance(token, theme):
    stops = reactor.RAMPS[theme]
    point = tuple(int(v) for v in re.findall(r"\d+", token))
    return min(palette.dist_to_segment(point, stops[i], stops[i + 1])
               for i in range(len(stops) - 1))


class PartialWeeks(unittest.TestCase):
    """Only the *final* partial week is an in-progress week."""

    def test_in_progress_final_week_is_scaled_to_a_full_week(self):
        # Two days of a seven-day week must not read as a quiet week sitting
        # next to the gold "now" tick while the week is still running.
        partial = stats([week("2025-09-07", [1] * 7), week("2025-09-14", [10, 10])])
        self.assertEqual(reactor.week_values(partial["weeks"]), [7.0, 70.0])

    def test_partial_first_week_is_left_alone(self):
        # Days missing from the first week fall *outside* the window, so that
        # week genuinely had fewer days to accumulate in. Scaling it would
        # invent activity, and it is not in progress either.
        partial = stats([week("2025-09-07", [1, 1, 1]), week("2025-09-14", [7] * 7)])
        self.assertEqual(reactor.week_values(partial["weeks"]), [3.0, 49.0])

    def test_full_weeks_are_never_rescaled(self):
        self.assertEqual(reactor.week_values(FULL["weeks"]), [0.0, 28.0, 1.0])

    def test_week_with_no_days_does_not_divide_by_zero(self):
        self.assertEqual(reactor.week_values([week("2025-09-07", [])]), [0.0])

    def test_scaled_week_feeds_the_ramp_not_the_peak_readout(self):
        # PEAK WEEK must stay a real week's real total; only colour uses the
        # scaled value, because a running week is not a record.
        payload = stats([week("2025-09-07", [5] * 7), week("2025-09-14", [30, 30])])
        svg = reactor.build(payload, "dark")
        self.assertIn("PEAK WEEK", svg)
        self.assertIn('>60<', svg)                  # the raw 30 + 30
        self.assertNotIn('>210<', svg)              # its colour-scaled value
        self.assertIn("peak week 60", svg)          # aria-label agrees


class EmptyAndQuietData(unittest.TestCase):

    def test_no_weeks_raises_a_clear_error(self):
        with self.assertRaises(SystemExit) as ctx:
            reactor.build(stats([]), "dark")
        self.assertIn("no weeks", str(ctx.exception))

    def test_all_zero_weeks_do_not_divide_by_zero(self):
        quiet = stats([week("2025-09-07", [0] * 7), week("2025-09-14", [0] * 7)])
        svg = reactor.build(quiet, "dark")
        ET.fromstring(svg)                                  # still valid XML
        self.assertEqual(ramp_tokens(svg), [])              # no ramp colours at all
        self.assertIn('>0<', svg)                           # headline total is a real 0
        self.assertNotIn("nan", svg.lower())

    def test_missing_languages_skips_the_bar_without_crashing(self):
        svg = reactor.build(stats([week("2025-09-07", [1] * 7)], languages={}), "dark")
        ET.fromstring(svg)
        self.assertNotIn("LANGUAGE MIX", svg)

    def test_single_language_other_bucket_is_omitted(self):
        svg = reactor.build(stats([week("2025-09-07", [1] * 7)], languages={"Python": 10}), "dark")
        self.assertIn("PYTHON 100%", svg)
        self.assertNotIn("OTHER", svg)

    def test_language_names_are_escaped(self):
        svg = reactor.build(stats([week("2025-09-07", [1] * 7)],
                                  languages={"C<script>": 10}), "dark")
        ET.fromstring(svg)
        self.assertIn("&lt;SCRIPT&gt;", svg)
        self.assertNotIn("<script>", svg)


class Ramp(unittest.TestCase):

    def test_endpoints_are_exact(self):
        for theme, stops in reactor.RAMPS.items():
            with self.subTest(theme=theme):
                self.assertEqual(reactor.ramp(0.0, theme), "rgb({},{},{})".format(*stops[0]))
                self.assertEqual(reactor.ramp(1.0, theme), "rgb({},{},{})".format(*stops[-1]))

    def test_midpoint_sits_on_the_path_not_beside_it(self):
        # Light routes through green; a straight cyan -> gold line lands on
        # rgb(84,122,92) at this point, the muddy sage the tune removed.
        for theme in reactor.RAMPS:
            with self.subTest(theme=theme):
                self.assertLessEqual(off_ramp_distance(reactor.ramp(0.5, theme), theme), 1.0)

    def test_out_of_range_input_is_clamped(self):
        self.assertEqual(reactor.ramp(-5, "dark"), reactor.ramp(0.0, "dark"))
        self.assertEqual(reactor.ramp(9, "dark"), reactor.ramp(1.0, "dark"))

    def test_generator_ramps_match_the_palette_gate(self):
        # The gate validates whatever stops it is handed, so if these two ever
        # disagree the check passes while the asset drifts. Assert them equal.
        self.assertEqual(set(reactor.RAMPS), set(palette.RAMP_ASSETS))
        for theme, (_, stops) in palette.RAMP_ASSETS.items():
            with self.subTest(theme=theme):
                self.assertEqual(reactor.RAMPS[theme], stops)

    def test_light_ramp_midpoint_keeps_its_chroma(self):
        # The complaint being fixed was "washed out": measure it rather than
        # trusting the hexes. Chroma must not collapse mid-scale.
        def chroma(token):
            r, g, b = (int(v) / 255 for v in re.findall(r"\d+", token))
            return max(r, g, b) - min(r, g, b)

        mid = chroma(reactor.ramp(0.5, "light"))
        self.assertGreater(mid, 0.4, f"mid-ramp chroma {mid:.2f} is mud again")
        straight = chroma("rgb(84,122,92)")             # the old two-stop midpoint
        self.assertGreater(mid, straight * 1.5)


class Geometry(unittest.TestCase):
    """Rendered output must stay on the canvas and out of its own way."""

    @classmethod
    def setUpClass(cls):
        cls.svg = {theme: reactor.build(FULL, theme) for theme in ("dark", "light")}

    def test_every_colour_is_a_palette_hex_or_a_ramp_rgb(self):
        # Two conventions, mirroring check_palette.py: palette colours are hex
        # (or rgba when they need alpha), and rgb() is reserved for the ramp.
        for theme, svg in self.svg.items():
            with self.subTest(theme=theme):
                allowed = palette.THEME_ALLOW[theme]
                for token in palette.colors_in(svg):
                    if palette.SKIP.match(token):
                        continue
                    if token.startswith("rgba"):
                        self.assertIn(palette.rgb_hex(token), allowed,
                                      f"{theme}: {token} is not a palette colour")
                    elif token.startswith("rgb("):
                        self.assertLessEqual(off_ramp_distance(token, theme), 6.0,
                                             f"{theme}: {token} is off the ramp")
                    else:
                        self.assertIn(token.lstrip("#").upper(), allowed,
                                      f"{theme}: {token} is not a palette colour")

    def test_coordinates_stay_inside_the_canvas(self):
        for theme, svg in self.svg.items():
            with self.subTest(theme=theme):
                root = ET.fromstring(svg)
                limits = [("x", reactor.W), ("y", reactor.H), ("cx", reactor.W), ("cy", reactor.H),
                          ("x1", reactor.W), ("y1", reactor.H), ("x2", reactor.W), ("y2", reactor.H)]
                for el in root.iter():
                    for attr, limit in limits:
                        if el.get(attr) is None:
                            continue
                        value = float(el.get(attr))
                        self.assertGreaterEqual(value, -0.5, f"{el.tag} {attr}")
                        self.assertLessEqual(value, limit + 0.5, f"{el.tag} {attr}")
                for m in re.finditer(r'd="M ([\d.-]+) ([\d.-]+) A', svg):
                    for value, limit in zip((float(m.group(1)), float(m.group(2))),
                                            (reactor.W, reactor.H)):
                        self.assertGreaterEqual(value, -0.5)
                        self.assertLessEqual(value, limit + 0.5)

    def test_one_ring_arc_per_week(self):
        # Matched on the ring's own radius so the dial ticks, which are also
        # <path> elements, are not counted as data.
        signature = rf'A {reactor.R_BAND} {reactor.R_BAND} 0 0 1'
        for theme, svg in self.svg.items():
            with self.subTest(theme=theme):
                self.assertEqual(len(re.findall(signature, svg)), len(FULL["weeks"]))

    def test_every_week_boundary_gets_a_dial_tick(self):
        for theme, svg in self.svg.items():
            with self.subTest(theme=theme):
                dial = re.findall(r'<path d="((?:M [\d.]+ [\d.]+ L [\d.]+ [\d.]+ )+)"', svg)
                self.assertTrue(dial, "dial scale missing")
                self.assertEqual(sum(len(re.findall(r'M ', d)) for d in dial), len(FULL["weeks"]))

    def test_text_rows_do_not_collide(self):
        for theme, svg in self.svg.items():
            with self.subTest(theme=theme):
                rows = {}
                for el in ET.fromstring(svg).iter(NS + "text"):
                    size = float(el.get("font-size", 10))
                    spacing = float(el.get("letter-spacing", 0))
                    text = "".join(el.itertext())
                    width = len(text) * (size * 0.6 + spacing)
                    anchor = el.get("text-anchor", "start")
                    x = float(el.get("x"))
                    left = x - width if anchor == "end" else (x - width / 2 if anchor == "middle" else x)
                    rows.setdefault(float(el.get("y")), []).append((left, left + width, text))
                for y, items in rows.items():
                    items.sort()
                    for (_, right, first), (left, _, second) in zip(items, items[1:]):
                        self.assertLessEqual(right, left + 0.5, f"y={y}: {first!r} runs into {second!r}")
                    self.assertGreaterEqual(items[0][0], 2.0, f"y={y} starts off the margin")
                    self.assertLessEqual(items[-1][1], reactor.W - 2.0, f"y={y} runs off the margin")


class Readouts(unittest.TestCase):

    def test_numbers_match_the_data(self):
        payload = stats([week("2025-09-07", [0] * 7),
                         week("2025-09-14", [7] * 7),
                         week("2025-09-21", [0] * 7)], longest_run=7)
        svg = reactor.build(payload, "dark")
        self.assertIn("ACTIVE WEEKS", svg)
        self.assertIn('>1<', svg)                 # one active week
        self.assertIn('>49<', svg)                # headline total, and the average
        self.assertIn("CONSECUTIVE DAYS", svg)
        self.assertIn(">7</text>", svg)           # longest run readout

    def test_caption_carries_the_stark_reference_not_the_header(self):
        svg = reactor.build(FULL, "dark")
        self.assertIn("CONTRIBUTION.CORE", svg)
        self.assertIn("Stark Industries", svg)
        self.assertNotIn("Stark", svg.split("</text>")[0])

    def test_aria_label_describes_the_instrument(self):
        svg = reactor.build(FULL, "dark")
        label = re.search(r'aria-label="([^"]+)"', svg).group(1)
        for phrase in ("29 contributions", "3 weeks", "2 active weeks", "longest run 0 days"):
            self.assertIn(phrase, label)


class Themes(unittest.TestCase):

    def test_light_theme_fixes_the_tiers_that_wash_out_on_white(self):
        light, dark = reactor.THEMES["light"], reactor.THEMES["dark"]
        self.assertEqual(light["PLATE"], "#F1F5F9")        # not a 1.06:1 cyan wash
        self.assertEqual(light["SUB"], light["MUTED"])     # 4.76:1 for small text
        # Every structural alpha must be stronger on white than on deep space.
        # Enumerated from the themes so a new tier cannot skip the rule.
        structural = [k for k in dark if k.startswith("OP_") or k == "SWEEP"]
        self.assertGreater(len(structural), 10, "tier discovery broke")
        for key in structural:
            if key == "OP_GLOW":
                continue        # asserted below: light mode must *not* bloom
            self.assertGreater(light[key], dark[key], f"{key} must be stronger on white")

    def test_light_mode_keeps_the_bloom_in_check(self):
        # A glow is a deep-space effect. On white it is a grey smudge, so the one
        # tier that goes the other way is asserted explicitly rather than by eye.
        self.assertLess(reactor.THEMES["light"]["OP_GLOW"], reactor.THEMES["dark"]["OP_GLOW"])
        self.assertLessEqual(reactor.THEMES["light"]["OP_CAGE_GLOW"], 0.15)

    def test_small_text_never_uses_the_dim_tier_in_light_mode(self):
        # #94A3B8 is 2.56:1 on white: fine for a quiet arc, unreadable at 9px.
        self.assertNotIn('fill="#94A3B8"', reactor.build(FULL, "light"))

    def test_both_themes_are_written_by_main(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "reactor.json")
            with open(path, "w") as f:
                json.dump(FULL, f)
            argv, sys.argv = sys.argv, ["generate_reactor.py", path, tmp]
            try:
                with contextlib.redirect_stdout(io.StringIO()):   # main() logs what it wrote
                    reactor.main()
            finally:
                sys.argv = argv
            for name in ("reactor.svg", "reactor-light.svg"):
                written = os.path.join(tmp, name)
                self.assertTrue(os.path.exists(written), name)
                with open(written) as f:
                    ET.fromstring(f.read())


if __name__ == "__main__":
    unittest.main(verbosity=2)
