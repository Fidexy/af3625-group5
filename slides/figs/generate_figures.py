#!/usr/bin/env python3
"""Generate the AF3625 Group 5 deck diagrams as standalone SVGs.

Fixed colour code (per the assignment's design guidelines):
  neutral  #0a2540  axes, domestic curves, text
  --cs     #1d4ed8  consumer surplus / consumer loss
  --ps     #0e9f6e  producer surplus / producer gain
  --gov    #d97706  government revenue / quota rent
  --dwl    #dc2626  deadweight loss (hatched)
"""
import os
import re

NEU, NEU2 = "#0a2540", "#7b8ba0"
CS, PS, GOV, DWL = "#1d4ed8", "#0e9f6e", "#d97706", "#dc2626"
INK = NEU
OUT = os.path.dirname(os.path.abspath(__file__))   # figures live next to this script
os.makedirs(OUT, exist_ok=True)
FONT = "Inter, 'Helvetica Neue', Helvetica, Arial, sans-serif"
TXT = 1.38   # global text scale — labels must survive a projector
HALO = 'paint-order="stroke" stroke="#ffffff" stroke-width="6" stroke-linejoin="round"'


def head(w, h):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" font-family="{FONT}">
<defs>
  <pattern id="hatch" width="9" height="9" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">
    <rect width="9" height="9" fill="{DWL}" fill-opacity="0.10"/>
    <line x1="0" y1="0" x2="0" y2="9" stroke="{DWL}" stroke-width="2.6" stroke-opacity="0.6"/>
  </pattern>
  <marker id="arws" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="7" markerHeight="7" orient="auto">
    <path d="M10,0 L0,5 L10,10 z" fill="{NEU2}"/>
  </marker>
  <marker id="arwe" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
    <path d="M0,0 L10,5 L0,10 z" fill="{NEU2}"/>
  </marker>
  <marker id="cs_a" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="7" markerHeight="7" orient="auto">
    <path d="M10,0 L0,5 L10,10 z" fill="{CS}"/>
  </marker>
  <marker id="cs_b" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
    <path d="M0,0 L10,5 L0,10 z" fill="{CS}"/>
  </marker>
  <marker id="gv_a" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="7" markerHeight="7" orient="auto">
    <path d="M10,0 L0,5 L10,10 z" fill="{GOV}"/>
  </marker>
  <marker id="gv_b" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
    <path d="M0,0 L10,5 L0,10 z" fill="{GOV}"/>
  </marker>
</defs>
"""


def txt(x, y, s, size=17, fill=None, weight=500, anchor="start", halo=True):
    fill = fill or INK
    size *= TXT
    h = HALO if halo else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" '
            f'font-weight="{weight}" text-anchor="{anchor}" {h}>{s}</text>')


SUB_W = {"P": 0.66, "Q": 0.80, "C": 0.72, "S": 0.67, "D": 0.77}


def tsub(x, y, base, sub, size=18, fill=None, weight=700, anchor="start"):
    """base + subscript, as two <text> nodes (SVG has no <sub>)."""
    fill = fill or INK
    size *= TXT
    base_w = len(base) * SUB_W.get(base[0], 0.62) * size
    sub_w = 0.62 * size * 0.72
    ox = x if anchor == "start" else (x - (base_w + sub_w) / 2 if anchor == "middle" else x - base_w - sub_w)
    out = txt(ox, y, base, size, fill, weight, "start")
    out += f'<text x="{ox + base_w:.1f}" y="{y + size * 0.22:.1f}" font-size="{size * 0.72:.1f}" fill="{fill}" font-weight="{weight}" {HALO}>{sub}</text>'
    return out


def lbl(x, y, base, sub, rest, size=17, fill=None, weight=700, anchor="start"):
    """`P` + subscript + ` = 300` as one laid-out group (estimated widths)."""
    fill = fill or INK
    size *= TXT
    bw = len(base) * SUB_W.get(base[0], 0.62) * size
    sw = (0.62 * size * 0.72) if sub else 0
    rw = len(rest) * 0.52 * size
    ox = x if anchor == "start" else (x - bw - sw - rw if anchor == "end" else x - (bw + sw + rw) / 2)
    out = txt(ox, y, base, size, fill, weight, "start")
    if sub:
        out += f'<text x="{ox + bw:.1f}" y="{y + size * 0.22:.1f}" font-size="{size * 0.72:.1f}" fill="{fill}" font-weight="{weight}" {HALO}>{sub}</text>'
    if rest:
        out += txt(ox + bw + sw, y, rest, size, fill, weight, "start")
    return out


class Plot:
    def __init__(self, ox, oy, pxq, pyp):
        self.ox, self.oy, self.pxq, self.pyp = ox, oy, pxq, pyp

    def X(self, q):
        return self.ox + q * self.pxq

    def Y(self, p):
        return self.oy - p * self.pyp

    def P(self, q, p):
        return f"{self.X(q):.1f},{self.Y(p):.1f}"

    def poly(self, pts, **kw):
        s = " ".join(self.P(q, p) for q, p in pts)
        at = " ".join(f'{k.replace("_","-")}="{v}"' for k, v in kw.items())
        return f'<polygon points="{s}" {at}/>'

    def line(self, q1, p1, q2, p2, **kw):
        at = " ".join(f'{k.replace("_","-")}="{v}"' for k, v in kw.items())
        return (f'<line x1="{self.X(q1):.1f}" y1="{self.Y(p1):.1f}" '
                f'x2="{self.X(q2):.1f}" y2="{self.Y(p2):.1f}" {at}/>')

    def lead(self, q1, p1, q2, p2, col=NEU2):
        return (f'<line x1="{self.X(q1):.1f}" y1="{self.Y(p1):.1f}" '
                f'x2="{self.X(q2):.1f}" y2="{self.Y(p2):.1f}" stroke="{col}" stroke-width="1.4" '
                f'stroke-dasharray="4 4"/>')


def axes(pl, qmax, pmax, xlabel, ylabel, qticks=(), pticks=()):
    s = [f'<line x1="{pl.X(0):.1f}" y1="{pl.Y(0):.1f}" x2="{pl.X(qmax):.1f}" y2="{pl.Y(0):.1f}" stroke="{NEU}" stroke-width="2"/>',
         f'<line x1="{pl.X(0):.1f}" y1="{pl.Y(0):.1f}" x2="{pl.X(0):.1f}" y2="{pl.Y(pmax):.1f}" stroke="{NEU}" stroke-width="2"/>']
    for q, lab in qticks:
        if q:
            s.append(f'<line x1="{pl.X(q):.1f}" y1="{pl.Y(0):.1f}" x2="{pl.X(q):.1f}" y2="{pl.Y(0)+7:.1f}" stroke="{NEU}" stroke-width="1.6"/>')
        s.append(txt(pl.X(q), pl.Y(0) + 34, lab, 15, NEU2, 400, "middle", halo=False))
    for p, lab in pticks:
        if p:
            s.append(f'<line x1="{pl.X(0):.1f}" y1="{pl.Y(p):.1f}" x2="{pl.X(0)-7:.1f}" y2="{pl.Y(p):.1f}" stroke="{NEU}" stroke-width="1.6"/>')
        s.append(txt(pl.X(0) - 18, pl.Y(p) + 6, lab, 15, NEU2, 400, "end", halo=False))
    s.append(txt((pl.X(0) + pl.X(qmax)) / 2, pl.Y(0) + 76, xlabel, 19, INK, 600, "middle"))
    cy = (pl.Y(0) + pl.Y(pmax)) / 2
    s.append(f'<text x="{pl.X(0)-74:.1f}" y="{cy:.1f}" font-size="19" fill="{INK}" font-weight="600" '
             f'text-anchor="middle" transform="rotate(-90 {pl.X(0)-74:.1f} {cy:.1f})">{ylabel}</text>')
    return "\n".join(s)


def swatch(x, y, fill, label, dash=False, w=26):
    r = f'<rect x="{x}" y="{y-14}" width="{w}" height="18" fill="{fill}" fill-opacity="0.5" stroke="{fill}" stroke-width="1.6" rx="3"/>'
    if dash:
        r += f'<rect x="{x}" y="{y-14}" width="{w}" height="18" fill="none" stroke="#fff" stroke-width="0"/>'
    return r + txt(x + w + 10, y + 1, label, 16, INK, 600)


def write(name, parts):
    with open(f"{OUT}/{name}.svg", "w") as f:
        f.write("\n".join(parts) + "\n</svg>")
    print("wrote", name)


QT = [(0, "0"), (20, "20"), (40, "40"), (60, "60"), (80, "80"), (100, "100"), (120, "120"), (140, "140"), (160, "160")]
PT175 = [(0, "0"), (25, "25"), (50, "50"), (75, "75"), (100, "100"), (125, "125"), (150, "150"), (175, "175")]


# ================================================================ F1: import / export rule
def f1_rule():
    def panel(ox, mode):
        pl = Plot(ox + 110, 430, 3.2, 3.0)
        p = [axes(pl, 100, 110, "Quantity", "", qticks=[], pticks=[])]
        p.append(pl.line(0, 110, 100, 30, stroke=NEU, stroke_width="3"))
        p.append(pl.line(0, 20, 100, 100, stroke=NEU, stroke_width="3"))
        p.append(txt(pl.X(99), pl.Y(36), "D", 20, NEU, 700))
        p.append(txt(pl.X(99), pl.Y(94), "S", 20, NEU, 700))
        pw = 45 if mode == "import" else 85
        col = CS if mode == "import" else PS
        p.append(pl.line(0, pw, 106, pw, stroke=col, stroke_width="3", stroke_dasharray="10 6"))
        p.append(txt(pl.X(104), pl.Y(pw) - 12, "World price", 17, col, 700, "end"))
        p.append(pl.line(0, 65, 56.25, 65, stroke=NEU2, stroke_width="2", stroke_dasharray="5 5"))
        p.append(tsub(pl.X(60), pl.Y(65) + 22, "P", "0", 17, NEU2, 600))
        qd = (110 - pw) / 0.8
        qs = (pw - 20) / 0.8
        p.append(pl.line(qs, 0, qs, pw, stroke=NEU2, stroke_width="1.6", stroke_dasharray="5 5"))
        p.append(pl.line(qd, 0, qd, pw, stroke=NEU2, stroke_width="1.6", stroke_dasharray="5 5"))
        lbl = "Imports" if mode == "import" else "Exports"
        p.append(f'<line x1="{pl.X(qs):.1f}" y1="{pl.Y(pw)+24:.1f}" x2="{pl.X(qd):.1f}" y2="{pl.Y(pw)+24:.1f}" '
                 f'stroke="{col}" stroke-width="3" marker-start="url(#arws)" marker-end="url(#arwe)"/>')
        p.append(txt((pl.X(qs) + pl.X(qd)) / 2, pl.Y(pw) + 50, lbl, 18, col, 700, "middle"))
        hx, hy = pl.X(0), pl.Y(112) - 22
        p.append(tsub(hx, hy, "P", "0", 19, col, 700))
        p.append(txt(hx + 30, hy, "&gt;" if mode == "import" else "&lt;", 19, col, 700))
        p.append(tsub(hx + 46, hy, "P", "w", 19, col, 700))
        p.append(txt(hx + 76, hy, "→ imports" if mode == "import" else "→ exports", 19, col, 700))
        return "\n".join(p)

    p = [head(1000, 570), '<rect width="100%" height="100%" fill="#ffffff"/>']
    p.append(panel(0, "import"))
    p.append('<line x1="548" y1="70" x2="548" y2="520" stroke="#dbe2ec" stroke-width="2"/>')
    p.append(panel(515, "export"))
    write("f1-rule", p)


# ================================================================ F2: CS / PS concept
def f2_surplus():
    pl = Plot(140, 560, 6.2, 3.3)
    p = [head(900, 660)]
    p.append(axes(pl, 120, 140, "Quantity (units per year)", "Price ($ per unit)", qticks=[(60, "Q₀")], pticks=[(80, "P₀")]))
    p.append(pl.poly([(0, 140), (0, 80), (60, 80)], fill=CS, fill_opacity="0.18", stroke=CS, stroke_width="1.5"))
    p.append(txt(pl.X(8), pl.Y(124), "Consumer", 19, CS, 700))
    p.append(txt(pl.X(8), pl.Y(110), "surplus", 19, CS, 700))
    p.append(pl.poly([(0, 80), (0, 20), (60, 80)], fill=PS, fill_opacity="0.22", stroke=PS, stroke_width="1.5"))
    p.append(txt(pl.X(10), pl.Y(52), "Producer", 19, PS, 700))
    p.append(txt(pl.X(10), pl.Y(38), "surplus", 19, PS, 700))
    p.append(pl.line(0, 140, 120, 20, stroke=NEU, stroke_width="3.4"))
    p.append(pl.line(0, 20, 120, 140, stroke=NEU, stroke_width="3.4"))
    p.append(txt(pl.X(112), pl.Y(32), "D", 22, NEU, 700))
    p.append(txt(pl.X(112), pl.Y(134), "S", 22, NEU, 700))
    p.append(pl.line(0, 80, 60, 80, stroke=NEU2, stroke_width="2", stroke_dasharray="6 5"))
    p.append(pl.line(60, 80, 60, 0, stroke=NEU2, stroke_width="2", stroke_dasharray="6 5"))
    p.append(f'<circle cx="{pl.X(60):.1f}" cy="{pl.Y(80):.1f}" r="6" fill="{NEU}"/>')
    p.append(txt(pl.X(60), pl.Y(140) - 8, "Social surplus = CS + PS", 19, INK, 700, "middle"))
    write("f2-surplus", p)


# ================================================================ Q5.1  (D: P = 225 − 1.25Q, S: P = 50 + 1.25Q)
def q51_base(pl):
    p = [axes(pl, 160, 175, "Quantity of TVs (thousands)", "Price of TVs ($)", qticks=QT, pticks=PT175)]
    p.append(pl.line(40, 175, 144, 45, stroke=NEU, stroke_width="3.4"))
    p.append(pl.line(0, 50, 100, 175, stroke=NEU, stroke_width="3.4"))
    p.append(txt(pl.X(146), pl.Y(50), "D", 22, NEU, 700))
    p.append(txt(pl.X(96), pl.Y(168), "S", 22, NEU, 700))
    return p


def f3_q51_freetrade(mode="trade"):
    pl = Plot(150, 575, 4.8, 2.6)
    p = [head(1010, 665)] + q51_base(pl)
    p.append(pl.line(0, 137.5, 70, 137.5, stroke=NEU2, stroke_width="1.8", stroke_dasharray="7 5"))
    p.append(pl.line(70, 0, 70, 137.5, stroke=NEU2, stroke_width="1.8", stroke_dasharray="7 5"))
    p.append(f'<circle cx="{pl.X(70):.1f}" cy="{pl.Y(137.5):.1f}" r="6" fill="{NEU}"/>')
    p.append(txt(pl.X(70), pl.Y(163), "Autarky price", 17, NEU, 700, "middle"))
    p.append(txt(pl.X(70), pl.Y(150), "$137.50", 17, NEU, 700, "middle"))
    p.append(lbl(pl.X(68), pl.Y(122), "Q", "0", " = 70 thousand", 16, NEU2, 600, "end"))
    p.append(pl.line(0, 75, 172, 75, stroke=NEU, stroke_width="3"))
    p.append(txt(pl.X(166), pl.Y(75) - 12, "World price $75", 19, NEU, 700, "end"))
    if mode == "market":
        return p
    p.append(pl.line(20, 0, 20, 75, stroke=NEU2, stroke_width="1.8", stroke_dasharray="7 5"))
    p.append(pl.line(120, 0, 120, 75, stroke=NEU2, stroke_width="1.8", stroke_dasharray="7 5"))
    p.append(f'<circle cx="{pl.X(20):.1f}" cy="{pl.Y(75):.1f}" r="6" fill="{NEU}"/>')
    p.append(f'<circle cx="{pl.X(120):.1f}" cy="{pl.Y(75):.1f}" r="6" fill="{NEU}"/>')
    p.append(tsub(pl.X(21), pl.Y(70), "Q", "s", 17, NEU, 700))
    p.append(txt(pl.X(21) + 34, pl.Y(70), "= 20", 17, NEU, 700))
    p.append(lbl(pl.X(119), pl.Y(70), "Q", "d", " = 120", 17, NEU, 700, "end"))
    p.append(pl.poly([(0, 75), (0, 50), (20, 75)], fill=PS, fill_opacity="0.32", stroke=PS, stroke_width="1.8"))
    p.append(txt(pl.X(5), pl.Y(57), "PS", 16, PS, 800))
    y = pl.Y(75) + 46
    p.append(f'<line x1="{pl.X(20):.1f}" y1="{y:.1f}" x2="{pl.X(120):.1f}" y2="{y:.1f}" stroke="{CS}" stroke-width="3" '
             f'marker-start="url(#cs_a)" marker-end="url(#cs_b)"/>')
    p.append(tsub(pl.X(58), y + 34, "Q", "import", 19, CS, 700))
    p.append(txt(pl.X(58) + 78, y + 34, "= 120 \u2212 20 = 100 (thousand)", 19, CS, 700))
    return p


def f3c_q51_ps_zoom():
    pl = Plot(190, 560, 20.0, 3.7)
    p = [head(1000, 660)]
    p.append(axes(pl, 40, 140, "Quantity of TVs (thousands)", "Price of TVs ($)",
                  qticks=[(0, "0"), (10, "10"), (20, "20"), (30, "30"), (40, "40")],
                  pticks=[(0, "0"), (25, "25"), (50, "50"), (75, "75"), (100, "100"), (125, "125")]))
    p.append(pl.poly([(0, 75), (0, 50), (20, 75)], fill=PS, fill_opacity="0.34", stroke=PS, stroke_width="2"))
    p.append(pl.line(0, 50, 32, 90, stroke=NEU, stroke_width="3.4"))
    p.append(txt(pl.X(29), pl.Y(74), "S", 20, NEU, 700))
    p.append(pl.line(0, 75, 40, 75, stroke=NEU, stroke_width="3"))
    p.append(txt(pl.X(0.6), pl.Y(84), "World price $75", 18, NEU, 700))
    p.append(pl.line(20, 0, 20, 75, stroke=NEU2, stroke_width="1.8", stroke_dasharray="7 5"))
    p.append(f'<circle cx="{pl.X(20):.1f}" cy="{pl.Y(75):.1f}" r="6" fill="{NEU}"/>')
    p.append(f'<line x1="{pl.X(25):.1f}" y1="{pl.Y(50):.1f}" x2="{pl.X(25):.1f}" y2="{pl.Y(75):.1f}" stroke="{PS}" stroke-width="2.4" marker-start="url(#gv_a)" marker-end="url(#gv_b)"/>')
    p.append(txt(pl.X(27), pl.Y(66), "height", 17, PS, 700))
    p.append(txt(pl.X(27), pl.Y(57), "= $25", 17, PS, 700))
    p.append(f'<line x1="{pl.X(0):.1f}" y1="{pl.Y(9):.1f}" x2="{pl.X(20):.1f}" y2="{pl.Y(9):.1f}" stroke="{PS}" stroke-width="2.4" marker-start="url(#gv_a)" marker-end="url(#gv_b)"/>')
    p.append(txt(pl.X(10), pl.Y(20), "base = 20,000 TVs", 17, PS, 700, "middle"))
    p.append(txt(pl.X(0.5), pl.Y(133), "Shaded triangle = producer surplus at the world price", 18, PS, 700))
    return p


def f4_q51_quota():
    pl = Plot(150, 575, 4.8, 2.6)
    p = [head(1010, 665)] + q51_base(pl)
    p.append(pl.line(0, 75, 172, 75, stroke=NEU, stroke_width="3"))
    p.append(txt(pl.X(166), pl.Y(75) - 12, "World price $75", 19, NEU, 700, "end"))
    p.append(f'<path d="M {pl.P(0,50)} L {pl.P(20,75)} L {pl.P(40,75)} L {pl.P(120,175)}" fill="none" stroke="{GOV}" stroke-width="3.8"/>')
    p.append(txt(pl.X(122), pl.Y(172), "S + quota", 21, GOV, 700))
    p.append(pl.poly([(60, 75), (80, 75), (80, 125), (60, 125)], fill=GOV, fill_opacity="0.30", stroke=GOV, stroke_width="2"))
    p.append(pl.line(0, 125, 80, 125, stroke=NEU2, stroke_width="1.8", stroke_dasharray="7 5"))
    p.append(pl.line(80, 0, 80, 125, stroke=NEU2, stroke_width="1.8", stroke_dasharray="7 5"))
    p.append(pl.line(60, 0, 60, 75, stroke=NEU2, stroke_width="1.8", stroke_dasharray="7 5"))
    p.append(f'<circle cx="{pl.X(80):.1f}" cy="{pl.Y(125):.1f}" r="6.5" fill="{NEU}"/>')
    p.append(txt(pl.X(0) - 14, pl.Y(125) + 6, "125", 18, NEU, 700, "end"))
    p.append(txt(pl.X(80), pl.Y(131), "$125", 17, NEU, 700, "middle"))
    p.append(pl.lead(108, 152, 82, 126, GOV))
    p.append(txt(pl.X(110), pl.Y(155), "post-quota price", 17, GOV, 700))
    p.append(txt(pl.X(60), pl.Y(0) + 32, "60", 17, NEU2, 600, "middle"))
    p.append(txt(pl.X(80), pl.Y(0) + 32, "80", 17, NEU2, 600, "middle"))
    p.append(txt(pl.X(70), pl.Y(88), "Quota rent", 15, GOV, 700, "middle"))
    p.append(f'<line x1="{pl.X(20):.1f}" y1="{pl.Y(66):.1f}" x2="{pl.X(40):.1f}" y2="{pl.Y(66):.1f}" stroke="{GOV}" '
             f'stroke-width="3" marker-start="url(#gv_a)" marker-end="url(#gv_b)"/>')
    p.append(txt(pl.X(30), pl.Y(56), "quota = 20", 16, GOV, 700, "middle"))
    write("f4-q51-quota", p)


def f5_q51_trap():
    def panel(ox, correct):
        pl = Plot(ox + 150, 500, 3.1, 2.1)
        p = [axes(pl, 150, 175, "Quantity of TVs (thousands)", "",
                  qticks=[(0, "0"), (40, "40"), (80, "80"), (120, "120")],
                  pticks=[(25, "25"), (75, "75"), (125, "125"), (175, "175")])]
        p.append(pl.line(35, 175, 144, 45, stroke=NEU, stroke_width="3"))
        p.append(pl.line(0, 50, 100, 175, stroke=NEU, stroke_width="3"))
        p.append(pl.line(0, 75, 160, 75, stroke=NEU2, stroke_width="2.4"))
        p.append(txt(pl.X(96), pl.Y(30), "D", 19, NEU, 700))
        p.append(txt(pl.X(90), pl.Y(172), "S", 19, NEU, 700))
        if not correct:
            p.append(pl.line(0, 25, 120, 175, stroke=DWL, stroke_width="3.6"))
            p.append(txt(pl.X(104), pl.Y(148), "S + quota", 18, DWL, 700))
            p.append(f'<circle cx="{pl.X(0):.1f}" cy="{pl.Y(25):.1f}" r="10" fill="none" stroke="{DWL}" stroke-width="3"/>')
            p.append(f'<line x1="{pl.X(0)-18:.1f}" y1="{pl.Y(25)-18:.1f}" x2="{pl.X(0)+18:.1f}" y2="{pl.Y(25)+18:.1f}" stroke="{DWL}" stroke-width="3"/>')
            p.append(txt(pl.X(8), pl.Y(11), "starts at $25 — below the world price,", 15, DWL, 700))
            p.append(txt(pl.X(8), pl.Y(-2), "so it implies imports there too", 15, DWL, 700))
        else:
            p.append(f'<path d="M {pl.P(0,50)} L {pl.P(20,75)} L {pl.P(40,75)} L {pl.P(115,169)}" fill="none" stroke="{GOV}" stroke-width="3.6"/>')
            p.append(txt(pl.X(96), pl.Y(140), "S + quota", 18, GOV, 700))
            p.append(pl.line(20, 0, 20, 75, stroke=NEU2, stroke_width="1.6", stroke_dasharray="6 4"))
            p.append(pl.line(40, 0, 40, 75, stroke=NEU2, stroke_width="1.6", stroke_dasharray="6 4"))
            p.append(f'<path d="M {pl.P(20,75)} L {pl.P(40,75)}" stroke="{GOV}" stroke-width="6"/>')
            p.append(txt(pl.X(24), pl.Y(66), "= quota 20,000", 15, GOV, 700))
            p.append(txt(pl.X(6), pl.Y(52), "follows S below the world price,", 15, GOV, 700))
            p.append(txt(pl.X(6), pl.Y(38), "then shifts right by the quota", 15, GOV, 700))
        return "\n".join(p)

    p = [head(1200, 570)]
    p.append(panel(0, False))
    p.append('<line x1="590" y1="70" x2="590" y2="510" stroke="#dbe2ec" stroke-width="2"/>')
    p.append(panel(600, True))
    write("f5-q51-trap", p)


# ================================================================ F6: Q5.2 quantity-gap chart
def f6_q52_gap():
    p = [head(1000, 460)]
    x0, x1 = 270, 920
    lo, hi = 33000, 40000

    def X(q):
        return x0 + (q - lo) / (hi - lo) * (x1 - x0)

    p.append(txt(x0, 52, "Quantity of handbags per year", 17, NEU2, 600))
    for i, (lbl, qs, qd, col) in enumerate([("Free trade:  P = $600", 34000, 38800, CS),
                                            ("With tariff:  P = $625", 35150, 38750, GOV)]):
        y = 140 + i * 150
        p.append(txt(x0 - 26, y - 52, lbl, 20, col, 700, "end"))
        p.append(f'<line x1="{X(qs):.1f}" y1="{y:.1f}" x2="{X(qd):.1f}" y2="{y:.1f}" stroke="{col}" stroke-width="12" stroke-linecap="round" opacity="0.5"/>')
        p.append(f'<circle cx="{X(qs):.1f}" cy="{y:.1f}" r="7" fill="{col}"/>')
        p.append(f'<circle cx="{X(qd):.1f}" cy="{y:.1f}" r="7" fill="{col}"/>')
        for q in (qs, qd):
            p.append(f'<line x1="{X(q):.1f}" y1="{y:.1f}" x2="{X(q):.1f}" y2="{y+30:.1f}" stroke="{col}" stroke-width="1.5" stroke-dasharray="4 4"/>')
        p.append(tsub(X(qs), y + 52, "Q", "s", 17, INK, 600, "middle"))
        p.append(txt(X(qs) + 20, y + 52, f" = {qs:,}", 17, INK, 600))
        p.append(tsub(X(qd) - 60, y + 52, "Q", "d", 17, INK, 600))
        p.append(txt(X(qd) - 40, y + 52, f" = {qd:,}", 17, INK, 600))
        p.append(f'<line x1="{X(qs):.1f}" y1="{y-34:.1f}" x2="{X(qd):.1f}" y2="{y-34:.1f}" stroke="{col}" stroke-width="2.4" '
                 f'marker-start="url(#arws)" marker-end="url(#arwe)"/>')
        p.append(txt((X(qs) + X(qd)) / 2, y - 46, f"Imports = {qd-qs:,}", 19, col, 700, "middle"))
    p.append(txt(40, 430, "Reduction in imports = 1,200   →   DWL = ½ × $25 × 1,200 = $15,000", 18, DWL, 700))
    write("f6-q52-gap", p)


# ================================================================ F7: Q5.3 Egypt tariff (to scale)
def f7_q53():
    pl = Plot(180, 560, 0.074, 0.60)
    p = [head(1100, 710)]
    p.append(axes(pl, 10000, 700, "Quantity of generators per year", "Price (US$ per generator)",
                  qticks=[(0, "0"), (2000, "2,000"), (4000, "4,000"), (6000, "6,000"), (8000, "8,000"), (10000, "10,000")],
                  pticks=[(100, "100"), (200, "200"), (300, "300"), (400, "400"), (500, "500"), (600, "600")]))
    p.append(pl.poly([(0, 300), (7000, 300), (6000, 400), (0, 400)], fill=CS, fill_opacity="0.14",
                     stroke=CS, stroke_width="2", stroke_dasharray="8 5"))
    p.append(pl.poly([(0, 300), (4000, 300), (5000, 400), (0, 400)], fill=PS, fill_opacity="0.38",
                     stroke=PS, stroke_width="2", stroke_dasharray="8 5"))
    p.append(pl.line(10000, 0, 3000, 700, stroke=NEU, stroke_width="3.4"))
    p.append(pl.line(1000, 0, 8000, 700, stroke=NEU, stroke_width="3.4"))
    p.append(txt(pl.X(2900), pl.Y(690), "D", 21, NEU, 700))
    p.append(txt(pl.X(8120), pl.Y(690), "S", 21, NEU, 700))
    p.append(pl.line(0, 300, 10400, 300, stroke=NEU, stroke_width="2.6"))
    p.append(lbl(pl.X(10550), pl.Y(300) - 12, "P", "w", " = 300", 18, NEU, 700, "end"))
    p.append(pl.line(0, 400, 10400, 400, stroke=NEU, stroke_width="2.6", stroke_dasharray="10 5"))
    p.append(lbl(pl.X(10550), pl.Y(400) - 12, "P", "w", " + t = 400", 18, NEU, 700, "end"))
    p.append(pl.poly([(5000, 300), (6000, 300), (6000, 400), (5000, 400)], fill=GOV, fill_opacity="0.65", stroke=GOV, stroke_width="1.6"))
    p.append(pl.poly([(4000, 300), (5000, 300), (5000, 400)], fill="url(#hatch)", stroke=DWL, stroke_width="1.8"))
    p.append(pl.poly([(6000, 300), (6000, 400), (7000, 300)], fill="url(#hatch)", stroke=DWL, stroke_width="1.8"))
    p.append(txt(pl.X(5500), pl.Y(332), "C", 18, "#ffffff", 800, "middle", halo=False))
    p.append(pl.lead(5600, 330, 7100, 260, GOV))
    p.append(txt(pl.X(7200), pl.Y(266), "tariff revenue", 16, GOV, 700))
    p.append(pl.lead(4600, 350, 1500, 470, PS))
    p.append(txt(pl.X(900), pl.Y(476), "A  gain to producers", 16, PS, 700, "middle"))
    p.append(pl.lead(3800, 180, 2600, 330, CS))
    p.append(txt(pl.X(3600), pl.Y(175), "B  loss to consumers", 16, CS, 700))
    p.append(pl.lead(4400, 240, 4520, 310, DWL))
    p.append(txt(pl.X(4360), pl.Y(246), "D  DWL", 16, DWL, 700, "end"))
    p.append(pl.lead(6650, 190, 6520, 290, DWL))
    p.append(txt(pl.X(6700), pl.Y(196), "D  DWL", 16, DWL, 700))
    for q in (4000, 5000, 6000, 7000):
        p.append(pl.line(q, 0, q, 300, stroke=NEU2, stroke_width="1.3", stroke_dasharray="5 4"))
    p.append(txt(pl.X(4000), pl.Y(0) - 12, "4,000", 15, NEU2, 600, "middle"))
    p.append(txt(pl.X(5000), pl.Y(0) - 12, "5,000", 15, NEU2, 600, "middle"))
    p.append(txt(pl.X(6000), pl.Y(0) - 12, "6,000", 15, NEU2, 600, "middle"))
    p.append(txt(pl.X(7000), pl.Y(0) - 12, "7,000", 15, NEU2, 600, "middle"))
    p.append(swatch(60, 645, CS, "loss to consumers (ΔCS)", w=30))
    p.append(swatch(430, 645, PS, "gain to producers (ΔPS)", w=30))
    p.append(swatch(830, 645, GOV, "tariff revenue", w=30))
    p.append(swatch(150, 683, DWL, "deadweight loss (two triangles)", w=30))
    p.append(txt(500, 684, "dashed outlines = change in surplus, not a new cost", 15, NEU2, 500))
    write("f7-q53", p)


f1_rule()
f2_surplus()
write("f3a-q51-market", f3_q51_freetrade("market"))
write("f3b-q51-trade", f3_q51_freetrade("trade"))
write("f3c-q51-ps", f3c_q51_ps_zoom())
f4_q51_quota()
f5_q51_trap()
f6_q52_gap()
f7_q53()
