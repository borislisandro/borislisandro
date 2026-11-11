#!/usr/bin/env python3
"""Draws the profile artwork: the waveform header and the chip cards.

Run from the repository root:  python3 assets/make-art.py
Everything is plain SVG with no scripts or web fonts, so GitHub renders it.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).parent
FONT = "'JetBrains Mono','Cascadia Code','SF Mono',Menlo,Consolas,monospace"

BG, GRID, TEXT, DIM = "#0f1b2d", "#1c2b45", "#d3deee", "#7d91ae"
AMBER, TEAL, BLUE, BUSFILL, PINK = "#f0b445", "#4fd1c5", "#8fb8ff", "#15284a", "#ff6b8b"

# ---------------------------------------------------------------- waveform
W, X0, P, N = 840, 132, 29, 24          # width, wave origin, clock period, cycles
X1 = X0 + P * N


def x(c):
    return X0 + P * c


def level(y, h, spans):
    """A one-bit signal that is high during each (start, end) span, in cycles."""
    lo, hi, s = y + h, y, 3
    d = f"M{x(0)} {hi if spans[0][0] == 0 else lo}"
    for a, b in spans:
        if a > 0:
            d += f" H{x(a) - s} L{x(a) + s} {hi}"
        if b < N:
            d += f" H{x(b) - s} L{x(b) + s} {lo}"
    return d + f" H{X1}"


def bus(y, h, cells):
    out, mid, s, prev = [], y + h / 2, 4, 0
    for a, b, label in cells:
        if a > prev:
            out.append(f'<path d="M{x(prev)} {mid} H{x(a)}" stroke="{DIM}" stroke-dasharray="2 4"/>')
        xa, xb = x(a), x(b)
        out.append(
            f'<path d="M{xa} {mid} L{xa + s} {y} H{xb - s} L{xb} {mid} L{xb - s} {y + h} H{xa + s} Z" '
            f'fill="{BUSFILL}" stroke="{BLUE}"/>'
            f'<text x="{(xa + xb) / 2}" y="{mid + 4}" text-anchor="middle" fill="{TEXT}">{escape(label)}</text>')
        prev = b
    if prev < N:
        out.append(f'<path d="M{x(prev)} {mid} H{X1}" stroke="{DIM}" stroke-dasharray="2 4"/>')
    return "".join(out)


def header():
    rows = [("clk", 52), ("valid", 86), ("ready", 120), ("who", 158), ("work", 196), ("stack", 234), ("now", 272)]
    H = 318
    clk = f"M{x(0)} 68" + "".join(f" V52 H{x(c) + P / 2} V68 H{x(c + 1)}" for c in range(N))
    grid = "".join(f'<path d="M{x(c)} 40 V300"/>' for c in range(N + 1))
    ticks = "".join(f'<text x="{x(c)}" y="32" text-anchor="middle">{c * 10}</text>' for c in range(0, N + 1, 4))
    labels = "".join(f'<text x="{X0 - 16}" y="{y + 14}" text-anchor="end">{n}</text>' for n, y in rows)
    span = X1 - X0
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img"
 aria-label="A waveform trace. who: borislisandro, ASIC design verification engineer. work: memory controller IP, UVM, SVA, constrained-random, coverage. stack: SystemVerilog, UVM, SVA, Rust, Python, TypeScript, Verilator. now: rv32-core, claude-deck, JobScraper.">
<style>
text{{font:12px {FONT}}}
.cur{{animation:sweep 14s linear infinite}}
@keyframes sweep{{from{{transform:translateX(0)}}to{{transform:translateX({span}px)}}}}
@media (prefers-reduced-motion:reduce){{.cur{{animation:none;transform:translateX({P * 9.5}px)}}}}
</style>
<rect width="{W}" height="{H}" rx="10" fill="{BG}"/>
<text x="16" y="32" fill="{DIM}">boris.fst</text>
<g fill="{DIM}">{ticks}<text x="{X0 - 16}" y="32" text-anchor="end">ns</text></g>
<g stroke="{GRID}">{grid}</g>
<g fill="{TEXT}">{labels}</g>
<g fill="none" stroke-width="1.5" stroke-linejoin="round">
<path d="{clk}" stroke="{AMBER}"/>
<path d="{level(86, 16, [(1, 9), (10, 23)])}" stroke="{TEAL}"/>
<path d="{level(120, 16, [(0, 5), (7, 24)])}" stroke="{TEAL}"/>
{bus(156, 22, [(1, 9, "borislisandro"), (10, 23, "ASIC design verification engineer")])}
{bus(194, 22, [(1, 9, "memory controller IP"), (10, 23, "UVM, SVA, constrained-random, coverage")])}
{bus(232, 22, [(1, 5, "SystemVerilog"), (5, 7, "UVM"), (7, 9, "SVA"), (10, 13, "Rust"), (13, 16, "Python"), (16, 20, "TypeScript"), (20, 23, "Verilator")])}
{bus(270, 22, [(1, 9, "rv32-core"), (10, 16, "claude-deck"), (16, 23, "JobScraper")])}
</g>
<g class="cur"><path d="M{X0} 40 V304" stroke="{PINK}" stroke-width="1.5"/><path d="M{X0 - 5} 304 h10 l-5 -7 z" fill="{PINK}"/></g>
</svg>
'''


# ------------------------------------------------------------------- chips
BODY, EDGE, PIN, MARK, MARKDIM = "#1a2333", "#33415c", "#b9c4d6", "#e4ebf5", "#8a9bb8"


def chip(name, part, code, width, pins):
    H, top, bot = 132, 16, 116
    step = (width - 48) / (pins - 1)
    legs = "".join(
        f'<rect x="{24 + i * step - 4:.1f}" y="2" width="8" height="14" rx="1"/>'
        f'<rect x="{24 + i * step - 4:.1f}" y="{bot}" width="8" height="14" rx="1"/>' for i in range(pins))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {H}" width="{width}" height="{H}" role="img" aria-label="{escape(name)}: {escape(part)}">
<g fill="{PIN}">{legs}</g>
<rect x="6" y="{top}" width="{width - 12}" height="{bot - top}" rx="4" fill="{BODY}" stroke="{EDGE}"/>
<circle cx="24" cy="{bot - 16}" r="5" fill="none" stroke="{MARKDIM}"/>
<text x="24" y="52" fill="{MARK}" style="font:700 22px {FONT}">{escape(name)}</text>
<text x="24" y="74" fill="{MARK}" style="font:13px {FONT}">{escape(part)}</text>
<text x="{width - 24}" y="{bot - 12}" text-anchor="end" fill="{MARKDIM}" style="font:11px {FONT}">{escape(code)}</text>
</svg>
'''


CHIPS = [
    ("rv32-core", "RV32IM, 5-stage pipeline, formally checked", "SystemVerilog  2611", 820, 28),
    ("claude-deck", "Claude Code sessions on the Plasma panel", "Rust  2611", 404, 14),
    ("JobScraper", "Semiconductor job boards, tracked locally", "Tauri + React  2611", 404, 14),
    ("gmk67-led-arcade", "Games on a keyboard's RGB lighting", "Python  2611", 404, 14),
    ("spi-slave-ram-tb", "Class-based testbench under Verilator", "SystemVerilog  2610", 404, 14),
]

if __name__ == "__main__":
    (OUT / "wave.svg").write_text(header())
    for name, part, code, width, pins in CHIPS:
        (OUT / f"chip-{name}.svg").write_text(chip(name, part, code, width, pins))
    print("wrote", len(CHIPS) + 1, "files to", OUT)
