#!/usr/bin/env python3
"""Verify every text/background pair in styles.css against WCAG AA.

The palette has failed by eye before, so contrast is computed here rather
than judged. Run this after changing ANY colour token:

    python tools/check-contrast.py

Exits non-zero if any pair falls below its threshold, so it can gate a commit.
Translucent tokens (--accent-soft, used behind chip text) are composited over
each surface they can actually appear on before measuring.
"""
import re
import sys
from pathlib import Path

CSS = Path(__file__).resolve().parent.parent / "assets" / "css" / "styles.css"

AA_NORMAL = 4.5   # body text
AA_LARGE = 3.0    # >=24px, or >=18.7px bold


# ---------- colour maths ----------
def parse(c):
    """'#rgb' | '#rrggbb' | 'rgba(r, g, b, a)' -> (r, g, b, a)."""
    c = c.strip()
    if c.startswith("#"):
        h = c[1:]
        if len(h) == 3:
            h = "".join(ch * 2 for ch in h)
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 1.0)
    m = re.match(r"rgba?\(([^)]+)\)", c)
    if not m:
        raise ValueError(f"cannot parse colour: {c!r}")
    parts = [p.strip() for p in m.group(1).split(",")]
    r, g, b = (int(float(p)) for p in parts[:3])
    a = float(parts[3]) if len(parts) > 3 else 1.0
    return (r, g, b, a)


def over(fg, bg):
    """Composite fg (may be translucent) onto opaque bg."""
    fr, fg_, fb, fa = fg
    br, bg_, bb, _ = bg
    return (
        round(fr * fa + br * (1 - fa)),
        round(fg_ * fa + bg_ * (1 - fa)),
        round(fb * fa + bb * (1 - fa)),
        1.0,
    )


def luminance(c):
    def chan(v):
        v /= 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b, _ = c
    return 0.2126 * chan(r) + 0.7152 * chan(g) + 0.0722 * chan(b)


def ratio(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


# ---------- token extraction ----------
def tokens_for(selector_src):
    return dict(re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", selector_src))


def block(name, css):
    """Return the body of the first CSS block whose selector matches `name`."""
    i = css.index(name)
    start = css.index("{", i) + 1
    depth, j = 1, start
    while depth:
        if css[j] == "{":
            depth += 1
        elif css[j] == "}":
            depth -= 1
        j += 1
    return css[start:j - 1]


css = CSS.read_text(encoding="utf-8")
light = tokens_for(block(':root[data-theme="light"]', css))
dark = tokens_for(block(':root[data-theme="dark"]', css))

# Surfaces text can sit on, and which foregrounds land there.
SURFACES = ["--bg", "--bg-alt", "--bg-card", "--bg-sunken"]
BODY_FG = ["--fg", "--fg-mid", "--fg-dim", "--accent"]

failures = []
rows = []

for theme, tok in (("light", light), ("dark", dark)):
    def col(name):
        return parse(tok[name])

    # 1. plain body text on every surface
    for s in SURFACES:
        for f in BODY_FG:
            r = ratio(col(f), col(s))
            rows.append((theme, f, s, r, AA_NORMAL))

    # 2. chip text: --accent over translucent --accent-soft over each surface
    for s in SURFACES:
        bgc = over(col("--accent-soft"), col(s))
        r = ratio(col("--accent"), bgc)
        rows.append((theme, "--accent on --accent-soft", s, r, AA_NORMAL))

    # 3. white text on the solid accent fill (buttons, logo mark)
    r = ratio(col("--accent-fg"), col("--accent-fill"))
    rows.append((theme, "--accent-fg", "--accent-fill", r, AA_NORMAL))

    # 4. large display text (hero name, section titles) uses --fg on surfaces
    #    — already covered above at the stricter normal threshold.

print(f"{'theme':<6} {'foreground':<28} {'background':<14} {'ratio':>6}  need   ")
print("-" * 74)
for theme, f, s, r, need in rows:
    ok = r >= need
    if not ok:
        failures.append((theme, f, s, r, need))
    print(f"{theme:<6} {f:<28} {s:<14} {r:>6.2f}  {need:.1f}   {'ok' if ok else 'FAIL'}")

print("-" * 74)
if failures:
    print(f"\n{len(failures)} pair(s) below WCAG AA:")
    for theme, f, s, r, need in failures:
        print(f"  {theme}: {f} on {s} = {r:.2f}:1 (need {need}:1)")
    sys.exit(1)

worst = min(rows, key=lambda t: t[3])
print(f"\nAll {len(rows)} pairs pass WCAG AA.")
print(f"Tightest: {worst[0]} {worst[1]} on {worst[2]} = {worst[3]:.2f}:1")
