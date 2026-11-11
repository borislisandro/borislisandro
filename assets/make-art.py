#!/usr/bin/env python3
"""Draws the profile artwork: the contribution-graph header.

Run from the repository root:  python3 assets/make-art.py
Everything is plain SVG with no scripts or web fonts, so GitHub renders it.
"""
import random
from pathlib import Path

OUT = Path(__file__).parent

FONT = {
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
}
THEMES = {
    "dark": dict(levels=["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"], text="#8b949e"),
    "light": dict(levels=["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"], text="#57606a"),
}
COLS, ROWS, CELL, PITCH = 53, 7, 12, 15


def header(theme):
    lv, text = THEMES[theme]["levels"], THEMES[theme]["text"]
    rng = random.Random(7)
    word, start = "BORIS", (COLS - 29) // 2
    lit = {}
    for i, ch in enumerate(word):
        for r, row in enumerate(FONT[ch]):
            for c, bit in enumerate(row):
                if bit == "1":
                    lit[(start + i * 6 + c, r)] = rng.choice([3, 4, 4])
    W, H = COLS * PITCH - 3 + 2, ROWS * PITCH + 30
    cells = []
    for c in range(COLS):
        for r in range(ROWS):
            x, y = 1 + c * PITCH, 1 + r * PITCH
            if (c, r) in lit:
                k = lit[(c, r)]
                cells.append(f'<rect class="l{k}" style="animation-delay:{0.3 + (c - start) * 0.07:.2f}s" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" fill="{lv[k]}"/>')
            else:
                k = 0 if start - 2 <= c < start + 31 else rng.choices([0, 1, 2], [70, 22, 8])[0]
                cells.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" fill="{lv[k]}"/>')
    ly = ROWS * PITCH + 10
    legend = "".join(f'<rect x="{W - 118 + i * PITCH}" y="{ly}" width="{CELL}" height="{CELL}" rx="2.5" fill="{c}"/>' for i, c in enumerate(lv))
    keys = "".join(f"@keyframes l{k}{{from{{fill:{lv[0]}}}to{{fill:{lv[k]}}}}}.l{k}{{animation:l{k} .5s ease-out both}}" for k in (3, 4))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="A contribution graph whose squares spell BORIS">
<style>{keys}@media (prefers-reduced-motion:reduce){{.l3,.l4{{animation:none}}}}text{{font:12px -apple-system,'Segoe UI',Helvetica,Arial,sans-serif;fill:{text}}}</style>
{"".join(cells)}
<text x="{W - 124}" y="{ly + 10}" text-anchor="end">Less</text>{legend}<text x="{W}" y="{ly + 10}" text-anchor="end">More</text>
</svg>
'''


if __name__ == "__main__":
    for t in THEMES:
        (OUT / f"header-{t}.svg").write_text(header(t))
    print("done")
