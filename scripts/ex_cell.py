"""Example: cell division, mitosis and meiosis (researched; cells drawn as stained micrographs). Used by examples.py."""
import math, os, sys
K = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(K, '..', 'public', 'skill', 'runik'))
sys.path.insert(0, K)
from runik_object import Obj, smooth, blob
from runik_svg import T, R, L, P, dot, circ

CYTO = ('#fdf2ec', '#f5d2c6', '#c78f82')
NUC = ('#f1e9f8', '#cdb7e6', '#8d70b3')
CHROMATIN = '#8a6cb0'
MAT = ('#f4a0ab', '#d9475d', '#8c1f33')   # from the mother
PAT = ('#a7b5f5', '#4d62d1', '#26338a')   # from the father
SPINDLE = '#5fae7d'
CENT = '#2f6b45'
W = 5.2  # chromatid width


def svg(h, title, desc, body, defs=''):
    return ('<svg viewBox="0 0 760 %d" width="100%%" font-size="13" role="img" aria-label="%s"><title>%s</title><desc>%s</desc>%s%s%s</svg>'
            % (h, title, title, desc, '<defs>%s</defs>' % defs if defs else '', T(24, 30, title, 15, 600), ''.join(body)))


# ---------------------------------------------------------------- drawing parts
def membrane(N, cx, cy, rx, ry, pinch=0.0, seed=1):
    pts = []
    for i in range(28):
        a = 2 * math.pi * i / 28
        j = 1 + 0.025 * math.sin(3 * a + seed) + 0.02 * math.cos(5 * a + seed * 2)
        y = ry * math.sin(a) * (1 - pinch * (1 - abs(math.cos(a))) ** 1.6)
        pts.append((cx + rx * math.cos(a) * j, cy + y * j))
    d = smooth(pts, closed=True, t=0.5)
    N.add(N.shadow(d, 2, 4, 4, 0.14))
    N.add('<path d="%s" fill="%s" stroke="%s" stroke-width="2"/>' % (d, N.radial(*CYTO), CYTO[2]))
    N.add('<path d="%s" fill="none" stroke="#fff" stroke-width="1" opacity="0.6" transform="translate(%.1f %.1f) scale(0.95) translate(%.1f %.1f)"/>' % (d, cx, cy, -cx, -cy))
    for k in range(int(rx * ry / 260)):  # granular cytoplasm
        a, r = (k * 2.39996) % (2 * math.pi), math.sqrt((k * 0.618) % 1)
        N.add('<circle cx="%.1f" cy="%.1f" r="1" fill="%s" opacity="0.35"/>' % (cx + rx * 0.8 * r * math.cos(a), cy + ry * 0.75 * r * math.sin(a) * (1 - pinch * 0.6), CYTO[2]))


def nucleus(N, cx, cy, rx, ry, envelope='solid', chromatin=True, seed=1):
    if envelope == 'solid':
        N.add(N.ball(cx, cy, rx, ry, cols=NUC, stroke=NUC[2], sw=1.6, shadow=0.08, gloss=0.25))
    else:
        N.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" fill-opacity="0.35" stroke="%s" stroke-width="1.4" stroke-dasharray="5 4"/>' % (cx, cy, rx, ry, NUC[1], NUC[2]))
    if chromatin:
        for k in range(7):
            a = (k * 2.3 + seed) % (2 * math.pi)
            x0, y0 = cx + rx * 0.5 * math.cos(a), cy + ry * 0.5 * math.sin(a)
            N.add('<path d="M%.1f,%.1f q%.1f,%.1f %.1f,%.1f t%.1f,%.1f t%.1f,%.1f" fill="none" stroke="%s" stroke-width="1.6" opacity="0.55" stroke-linecap="round"/>' % (
                x0, y0, rx * 0.15, -ry * 0.25, rx * 0.3, 0, rx * 0.25, ry * 0.2, -rx * 0.1, ry * 0.3, CHROMATIN))
        N.add(N.ball(cx + rx * 0.2, cy - ry * 0.1, max(rx, ry) * 0.18, cols=('#b9a0d8', '#8a6cb0', '#5a3f80'), shadow=0, gloss=0.2))


def polyline_coloured(N, pts, segs, w=W):
    '''A chromatid along points pts, coloured by segs [(t0, t1, palette)], with outline, body and a highlight.'''
    lens = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    total = sum(lens) or 1
    pieces = []
    n = 24
    for k in range(n):
        t0, t1 = k / n, (k + 1) / n
        pieces.append((point_at(pts, lens, total, t0), point_at(pts, lens, total, t1), next(c for a, b, c in segs if a <= (t0 + t1) / 2 <= b)))
    for width, idx, op in ((w + 1.8, 2, 1), (w, 1, 1), (w * 0.32, 0, 0.8)):
        N.add(''.join('<path d="M%.1f,%.1f L%.1f,%.1f" stroke="%s" stroke-width="%.1f" stroke-linecap="round" opacity="%g"/>' % (a[0], a[1], b[0], b[1], c[idx], width, op) for a, b, c in pieces))


def point_at(pts, lens, total, t):
    d = t * total
    for i, l in enumerate(lens):
        if d <= l or i == len(lens) - 1:
            f = d / l if l else 0
            return (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f)
        d -= l


def chromosome(N, cx, cy, length, angle, segs_a, segs_b=None, c=0.38, w=W):
    '''Replicated chromosome (two sister chromatids joined at the centromere); segs_b=None draws a single chromatid.'''
    a = math.radians(angle)
    dx, dy, px, py = math.cos(a), math.sin(a), -math.sin(a), math.cos(a)
    top, bot = -length * c, length * (1 - c)
    if segs_b is None:
        polyline_coloured(N, [(cx + dx * top, cy + dy * top), (cx + dx * bot, cy + dy * bot)], segs_a, w)
        return
    for k, segs in ((-1, segs_a), (1, segs_b)):
        s = w * 0.62
        pts = [(cx + dx * top + px * k * s * 1.25, cy + dy * top + py * k * s * 1.25), (cx + px * k * w * 0.42, cy + py * k * w * 0.42),
               (cx + dx * bot + px * k * s * 1.25, cy + dy * bot + py * k * s * 1.25)]
        polyline_coloured(N, pts, segs, w)
    N.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#4a2f3a" opacity="0.55" transform="rotate(%.1f %.1f %.1f)"/>' % (cx, cy, w * 0.5, w * 1.1, angle, cx, cy))


def vee(N, tipx, tipy, length, segs, toward, c=0.38, w=W, spread=0.35):
    '''A single chromatid being pulled: centromere leads toward the pole, the arms trail behind.'''
    back = -1 if toward == 'left' else 1
    up, dn = length * c, length * (1 - c)
    pts = [(tipx + back * up * math.cos(spread), tipy - up * math.sin(spread) - up * 0.55), (tipx, tipy),
           (tipx + back * dn * math.cos(spread), tipy + dn * math.sin(spread) + dn * 0.4)]
    polyline_coloured(N, pts, segs, w)


def centrosome(N, x, y, rays=True):
    if rays:
        for k in range(12):
            a = 2 * math.pi * k / 12
            N.add('<path d="M%.1f,%.1f L%.1f,%.1f" stroke="%s" stroke-width="0.9" opacity="0.55"/>' % (x, y, x + 13 * math.cos(a), y + 13 * math.sin(a), SPINDLE))
    N.add('<rect x="%.1f" y="%.1f" width="7" height="3" rx="1.5" fill="%s"/><rect x="%.1f" y="%.1f" width="3" height="7" rx="1.5" fill="%s"/>' % (x - 4, y - 3, CENT, x + 1, y - 2, CENT))


def fibre(N, x1, y1, x2, y2):
    N.add('<path d="M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" fill="none" stroke="%s" stroke-width="1" opacity="0.75"/>' % (x1, y1, (x1 + x2) / 2, (y1 + y2) / 2 + (y2 - y1) * 0.08, x2, y2, SPINDLE))


ALL_M, ALL_P = [(0, 1, MAT)], [(0, 1, PAT)]
REC_M, REC_P = [(0, 0.62, MAT), (0.62, 1, PAT)], [(0, 0.62, PAT), (0.62, 1, MAT)]
LONG, SHORT = 30, 18


# ---------------------------------------------------------------- 1. overview
def overview():
    title = 'Mitosis copies a cell, meiosis makes four unique halves'
    N = Obj('k20261120-div-ov')
    b = []
    # parent
    membrane(N, 104, 236, 58, 50, seed=2)
    nucleus(N, 104, 236, 34, 28, chromatin=False)
    for (x, y, ln, segs) in ((92, 226, LONG, ALL_M), (116, 226, LONG, ALL_P), (94, 250, SHORT, ALL_M), (114, 250, SHORT, ALL_P)):
        chromosome(N, x, y, ln * 0.7, 90, segs, w=4)
    # mitosis: 2 identical cells
    for k, y in enumerate((96, 168)):
        cx = 470
        membrane(N, cx, y, 44, 32, seed=3 + k)
        nucleus(N, cx, y, 26, 20, chromatin=False)
        for (dx, dy, ln, segs) in ((-8, -4, LONG, ALL_M), (8, -4, LONG, ALL_P), (-6, 9, SHORT, ALL_M), (6, 9, SHORT, ALL_P)):
            chromosome(N, cx + dx, y + dy, ln * 0.5, 90, segs, w=3.4)
    # meiosis: 4 different cells
    gam = [(ALL_M, ALL_P), (REC_M, ALL_P), (REC_P, ALL_M), (ALL_P, ALL_M)]
    for k, (l, s) in enumerate(gam):
        cx, cy = 370 + k * 92, 330
        membrane(N, cx, cy, 32, 28, seed=7 + k)
        nucleus(N, cx, cy, 17, 15, chromatin=False)
        chromosome(N, cx - 4, cy, LONG * 0.5, 90, l, w=3.4)
        chromosome(N, cx + 5, cy + 2, SHORT * 0.5, 90, s, w=3.4)
    b.append(N.group(0, 0, 1))
    b.append(P('M166 220 C240 200 300 132 412 132', 'edge', 1.5))
    b.append('<path d="M412 128.5 L418 132 L412 135.5 Z" fill="var(--edge)"/>')
    b.append(P('M166 256 C240 276 280 330 322 330', 'edge', 1.5))
    b.append('<path d="M322 326.5 L328 330 L322 333.5 Z" fill="var(--edge)"/>')
    b += [T(24, 306, 'Body cell', 13, 600), T(24, 324, '46 chromosomes · 23 pairs', 11.5)]
    b += [T(250, 150, 'Mitosis', 13, 600, 'focus'), T(250, 168, 'one division', 11.5, 400, 'muted')]
    b += [T(200, 298, 'Meiosis', 13, 600, 'focus'), T(200, 316, 'two divisions', 11.5, 400, 'muted')]
    b += [T(530, 128, '2 identical cells', 13, 600), T(530, 146, '46 chromosomes each', 11.5), T(530, 164, 'growth, repair', 11.5, 400, 'muted')]
    b += [T(370, 384, '4 different cells: eggs or sperm', 13, 600), T(370, 402, '23 chromosomes each · no two alike', 11.5)]
    b.append(L(24, 422, 736, 422))
    lx = 24
    for pal, lab in ((MAT, 'from the mother'), (PAT, 'from the father')):
        b.append('<rect x="%d" y="436" width="22" height="7" rx="3.5" fill="%s" stroke="%s" stroke-width="1"/>' % (lx, pal[1], pal[2]))
        b.append(T(lx + 30, 444, lab, 11.5, 400, 'muted'))
        lx += 160
    b.append(T(lx, 444, 'drawn with 2 pairs; human cells have 23', 11.5, 400, 'muted'))
    return svg(458, title, 'A body cell with 23 chromosome pairs (drawn as 2 pairs: one red copy from the mother, one blue from the father). Mitosis, one division, makes 2 identical cells with 46 chromosomes for growth and repair. Meiosis, two divisions, makes 4 cells with 23 chromosomes each, eggs or sperm, every one a different mix of the parents\' chromosomes.', b, N.defs())


# ---------------------------------------------------------------- 2. the cell cycle
def cycle():
    title = 'A dividing human cell spends 23 of 24 hours getting ready'
    phases = [('G1', 11, 'grows', 'edge'), ('S', 8, 'copies its DNA', 'k2'), ('G2', 4, 'checks, prepares', 'edge'), ('M', 1, 'divides', 'focus')]
    cx, cy, ro, ri = 236, 232, 124, 82
    b = []
    a0 = -90.0
    for name, hrs, what, c in phases:
        a1 = a0 + 360 * hrs / 24
        large = 1 if a1 - a0 > 180 else 0
        p = lambda r, a: (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
        (x1, y1), (x2, y2), (x3, y3), (x4, y4) = p(ro, a0), p(ro, a1), p(ri, a1), p(ri, a0)
        b.append('<path d="M%.1f %.1f A%d %d 0 %d 1 %.1f %.1f L%.1f %.1f A%d %d 0 %d 0 %.1f %.1f Z" fill="var(--%s)" fill-opacity="%s" stroke="var(--surface)" stroke-width="2"/>' % (
            x1, y1, ro, ro, large, x2, y2, x3, y3, ri, ri, large, x4, y4, c, '0.45' if c != 'edge' else '0.25'))
        am = (a0 + a1) / 2
        lx, ly = p(ro + 18, am)
        anchor = 'start' if math.cos(math.radians(am)) > 0.2 else 'end' if math.cos(math.radians(am)) < -0.2 else 'middle'
        b.append(T(lx, ly, '%s · ~%d h' % (name, hrs), 13, 600, 'ink', anchor))
        b.append(T(lx, ly + 18, what, 11.5, 400, 'muted', anchor))
        a0 = a1
    b += [T(cx, cy - 6, '~24 h', 15, 600, 'ink', 'middle'), T(cx, cy + 14, 'one cycle', 11.5, 400, 'muted', 'middle')]
    # DNA amount through the cycle
    X = lambda h: 470 + h / 24 * 250
    Y = lambda c: 300 - (c - 1) * 70
    b.append(T(470, 132, 'DNA in the cell', 13, 600))
    b.append(T(470, 150, 'copies of each chromosome', 11.5, 400, 'muted'))
    b.append(L(X(0), Y(1), X(24), Y(1), 'edge', 1))
    for c in (2, 4):
        b.append(T(X(0) - 8, Y(c / 2) + 4, '×%d' % (c // 2), 11.5, 400, 'muted', 'end'))
        b.append(L(X(0), Y(c / 2), X(24), Y(c / 2), 'line', 1))
    b.append(P('M%.1f %.1f H%.1f L%.1f %.1f H%.1f V%.1f' % (X(0), Y(1), X(11), X(19), Y(2), X(23), Y(1)) + ' H%.1f' % X(24), 'k2', 2.5))
    b.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="var(--k2)" fill-opacity="0.12"/>' % (X(11), Y(2) - 6, X(19) - X(11), Y(1) - Y(2) + 12))
    for h, lab in ((0, '0 h'), (11, '11'), (19, '19'), (24, '24 h')):
        b.append(T(X(h), Y(1) + 20, lab, 11.5, 400, 'muted', 'end' if h == 24 else 'middle'))
    b.append(T(X(15), Y(2) - 14, 'S phase', 11.5, 600, 'ink', 'middle'))
    b.append(T(X(23.5), Y(1.5), 'M', 11.5, 600, 'focus', 'middle'))
    b.append(T(24, 396, 'a typical fast-dividing human cell; phase lengths vary from cell to cell', 11.5, 400, 'muted'))
    return svg(406, title, 'Cell cycle of a typical fast-dividing human cell, about 24 hours: G1 about 11 hours (grows), S about 8 hours (copies its DNA, which doubles), G2 about 4 hours (checks and prepares), M about 1 hour (divides, halving the DNA again).', b)


# ---------------------------------------------------------------- 3. mitosis
def panel_frame(b, x, y, w, h, head, sub):
    b.append(R(x, y, w, h, 'edge', 1.25))
    b += [T(x + 14, y + 22, head, 13, 600), T(x + 14, y + h - 12, sub, 11.5, 400, 'muted')]


def mitosis():
    title = 'Mitosis: copied chromosomes are split into two new nuclei'
    N = Obj('k20261120-mit')
    b = []
    heads = [('1 · Interphase', 'DNA already copied'), ('2 · Prophase', 'chromosomes condense'), ('3 · Metaphase', 'line up in the middle'),
             ('4 · Anaphase', 'sisters pulled apart'), ('5 · Telophase', 'two nuclei, cell pinches'), ('6 · Two cells', 'identical to the first')]
    for i, (hd, sub) in enumerate(heads):
        x, y = 24 + (i % 3) * 244, 52 + (i // 3) * 214
        panel_frame(b, x, y, 224, 200, hd, sub)
        cx, cy = x + 112, y + 104
        if i == 0:
            membrane(N, cx, cy, 90, 62, seed=1)
            nucleus(N, cx - 6, cy, 42, 34, seed=1)
            centrosome(N, cx + 50, cy - 36, rays=False)
            centrosome(N, cx + 58, cy - 30, rays=False)
        elif i == 1:
            membrane(N, cx, cy, 90, 62, seed=2)
            nucleus(N, cx, cy, 44, 36, envelope='dashed', chromatin=False)
            for (dx, dy, ln, ang, s) in ((-14, -10, LONG, 70, ALL_M), (14, -6, LONG, 110, ALL_P), (-12, 16, SHORT, 20, ALL_M), (16, 18, SHORT, 150, ALL_P)):
                chromosome(N, cx + dx, cy + dy, ln, ang, s, s)
            centrosome(N, cx - 62, cy - 26)
            centrosome(N, cx + 62, cy - 26)
            for k in range(3):
                fibre(N, cx - 58, cy - 26, cx + 58, cy - 26 - 8 + k * 8)
        elif i == 2:
            membrane(N, cx, cy, 94, 62, seed=3)
            yy = cy - 48
            for ln, s in ((LONG, ALL_M), (SHORT, ALL_M), (LONG, ALL_P), (SHORT, ALL_P)):
                L_ = ln * 0.62
                ccy = yy + L_ * 0.38
                chromosome(N, cx, ccy, L_, 90, s, s, w=4.4)
                fibre(N, cx - 76, cy, cx - 3, ccy)
                fibre(N, cx + 76, cy, cx + 3, ccy)
                yy += L_ + 7
            centrosome(N, cx - 76, cy)
            centrosome(N, cx + 76, cy)
        elif i == 3:
            membrane(N, cx, cy, 100, 58, seed=4)
            ys = [(-33, LONG, ALL_M), (-11, SHORT, ALL_M), (9, LONG, ALL_P), (31, SHORT, ALL_P)]
            for dy, ln, s in ys:
                vee(N, cx - 40, cy + dy, ln * 0.5, s, 'left', w=4.2, spread=0.5)
                vee(N, cx + 40, cy + dy, ln * 0.5, s, 'right', w=4.2, spread=0.5)
                fibre(N, cx - 82, cy, cx - 40, cy + dy)
                fibre(N, cx + 82, cy, cx + 40, cy + dy)
            for k in range(3):
                fibre(N, cx - 30, cy - 4 + k * 4, cx + 30, cy - 4 + k * 4)
            centrosome(N, cx - 82, cy)
            centrosome(N, cx + 82, cy)
        elif i == 4:
            membrane(N, cx, cy, 102, 56, pinch=0.55, seed=5)
            for side in (-1, 1):
                nx = cx + side * 52
                nucleus(N, nx, cy, 26, 24, envelope='dashed', chromatin=False)
                for (dx, dy, ln, s) in ((-8, -6, LONG, ALL_M), (6, -6, LONG, ALL_P), (-7, 10, SHORT, ALL_M), (7, 10, SHORT, ALL_P)):
                    chromosome(N, nx + dx, cy + dy, ln * 0.55, 80, s, w=3.6)
        else:
            for side in (-1, 1):
                ccx = cx + side * 52
                membrane(N, ccx, cy, 48, 44, seed=6 + side)
                nucleus(N, ccx, cy, 26, 22, chromatin=False)
                for (dx, dy, ln, s) in ((-8, -5, LONG, ALL_M), (6, -5, LONG, ALL_P), (-7, 10, SHORT, ALL_M), (7, 10, SHORT, ALL_P)):
                    chromosome(N, ccx + dx, cy + dy, ln * 0.5, 85, s, w=3.4)
        if i < 5 and i % 3 != 2:
            b.append('<path d="M%d %d l6 6 l-6 6" fill="none" stroke="var(--muted)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>' % (x + 231, y + 100))
    b.insert(0, N.group(0, 0, 1))
    b.append(legend(24, 498))
    b.append(T(24, 522, 'whole of M phase ≈ 1 hour · drawn with 2 chromosome pairs', 11.5, 400, 'muted'))
    return svg(532, title, 'Mitosis in six steps. 1 Interphase: the DNA has been copied. 2 Prophase: chromosomes condense into X shapes, the nuclear envelope breaks down, the two centrosomes move apart and build the spindle. 3 Metaphase: chromosomes line up in the middle, each held from both poles. 4 Anaphase: sister chromatids are pulled to opposite poles. 5 Telophase: two nuclei form and the cell pinches in the middle. 6 Two identical cells.', b, N.defs())


def legend(x, y):
    out = []
    for pal, lab in ((MAT, 'from the mother'), (PAT, 'from the father')):
        out.append('<rect x="%d" y="%d" width="22" height="7" rx="3.5" fill="%s" stroke="%s" stroke-width="1"/>' % (x, y - 7, pal[1], pal[2]))
        out.append(T(x + 30, y, lab, 11.5, 400, 'muted'))
        x += 150
    out.append('<path d="M%d %d h22" stroke="%s" stroke-width="1.5"/>' % (x, y - 4, SPINDLE))
    out.append(T(x + 30, y, 'spindle fibres', 11.5, 400, 'muted'))
    x += 140
    out.append('<rect x="%d" y="%d" width="7" height="3" rx="1.5" fill="%s"/><rect x="%d" y="%d" width="3" height="7" rx="1.5" fill="%s"/>' % (x + 4, y - 6, CENT, x + 9, y - 8, CENT))
    out.append(T(x + 24, y, 'centrosome', 11.5, 400, 'muted'))
    return ''.join(out)


# ---------------------------------------------------------------- 4. meiosis
def meiosis():
    title = 'Meiosis: two divisions, four cells, half the chromosomes'
    N = Obj('k20261120-mei')
    b = []
    heads = [('Prophase I', 'pairs swap pieces'), ('Metaphase I', 'pairs line up'), ('Anaphase I · Telophase I', 'pairs separate'),
             ('Metaphase II', 'in both cells'), ('Anaphase II', 'sisters separate'), ('Four cells', '23 chromosomes, all different')]
    b += [T(24, 64, 'MEIOSIS I · THE PAIRS SEPARATE', 11.5, 600, 'muted'), T(24, 294, 'MEIOSIS II · THE SISTERS SEPARATE', 11.5, 600, 'muted')]
    for i, (hd, sub) in enumerate(heads):
        x, y = 24 + (i % 3) * 244, 74 + (i // 3) * 230
        panel_frame(b, x, y, 224, 196, hd, sub)
        cx, cy = x + 112, y + 102
        if i == 0:
            membrane(N, cx, cy, 90, 62, seed=11)
            nucleus(N, cx, cy, 48, 40, envelope='dashed', chromatin=False)
            # long pair, crossing over (the two inner chromatids exchange their tips)
            chromosome(N, cx - 12, cy - 4, LONG * 1.05, 90, ALL_M, REC_M)
            chromosome(N, cx + 2, cy - 4, LONG * 1.05, 90, REC_P, ALL_P)
            N.add('<circle cx="%.1f" cy="%.1f" r="6" fill="none" stroke="#2b1c0e" stroke-width="1.2" stroke-dasharray="2 2"/>' % (cx - 5, cy - 4 + LONG * 1.05 * 0.62 - LONG * 1.05 * 0.38))
            chromosome(N, cx + 22, cy + 4, SHORT, 90, ALL_M, ALL_M)
            chromosome(N, cx + 35, cy + 4, SHORT, 90, ALL_P, ALL_P)
            N.mark('chiasma', cx - 5, cy - 4 + LONG * 1.05 * 0.24)
        elif i == 1:
            membrane(N, cx, cy, 94, 62, seed=12)
            pairs = [(-16, LONG, (ALL_M, REC_M), (REC_P, ALL_P)), (24, SHORT, (ALL_P, ALL_P), (ALL_M, ALL_M))]
            for dy, ln, left, right in pairs:
                chromosome(N, cx - 9, cy + dy, ln * 0.8, 90, *left, w=4.6)
                chromosome(N, cx + 9, cy + dy, ln * 0.8, 90, *right, w=4.6)
                fibre(N, cx - 78, cy, cx - 14, cy + dy)
                fibre(N, cx + 78, cy, cx + 14, cy + dy)
            centrosome(N, cx - 78, cy)
            centrosome(N, cx + 78, cy)
        elif i == 2:
            membrane(N, cx, cy, 100, 56, pinch=0.45, seed=13)
            for side, (lng, sht) in ((-1, ((ALL_M, REC_M), (ALL_P, ALL_P))), (1, ((REC_P, ALL_P), (ALL_M, ALL_M)))):
                nx = cx + side * 50
                chromosome(N, nx - 6, cy - 6, LONG * 0.7, 80, *lng, w=4.2)
                chromosome(N, nx + 10, cy + 6, SHORT * 0.7, 100, *sht, w=4.2)
        elif i == 3:
            for side, (lng, sht) in ((-1, ((ALL_M, REC_M), (ALL_P, ALL_P))), (1, ((REC_P, ALL_P), (ALL_M, ALL_M)))):
                ccx = cx + side * 52
                membrane(N, ccx, cy, 48, 50, seed=14 + side)
                chromosome(N, ccx, cy - 12, LONG * 0.62, 90, *lng, w=4)
                chromosome(N, ccx, cy + 16, SHORT * 0.62, 90, *sht, w=4)
                for dy in (-12, 16):
                    fibre(N, ccx - 36, cy, ccx - 4, cy + dy)
                    fibre(N, ccx + 36, cy, ccx + 4, cy + dy)
                centrosome(N, ccx - 36, cy, rays=False)
                centrosome(N, ccx + 36, cy, rays=False)
        elif i == 4:
            for side, (lng, sht) in ((-1, ((ALL_M, REC_M), (ALL_P, ALL_P))), (1, ((REC_P, ALL_P), (ALL_M, ALL_M)))):
                ccx = cx + side * 52
                membrane(N, ccx, cy, 50, 46, pinch=0.3, seed=16 + side)
                for k, dir_ in ((0, 'left'), (1, 'right')):
                    vx = ccx + (-1 if dir_ == 'left' else 1) * 22
                    vee(N, vx, cy - 8, LONG * 0.55, lng[k], dir_, w=3.6)
                    vee(N, vx, cy + 14, SHORT * 0.55, sht[k], dir_, w=3.6)
        else:
            gam = [(ALL_M, ALL_P), (REC_M, ALL_P), (REC_P, ALL_M), (ALL_P, ALL_M)]
            for k, (l, s) in enumerate(gam):
                gx, gy = cx - 75 + k * 50, cy - 4
                membrane(N, gx, gy, 23, 26, seed=20 + k)
                nucleus(N, gx, gy, 13, 15, chromatin=False)
                chromosome(N, gx - 3, gy - 1, LONG * 0.55, 90, l, w=3.4)
                chromosome(N, gx + 5, gy + 3, SHORT * 0.55, 90, s, w=3.4)
        if i % 3 != 2:
            b.append('<path d="M%d %d l6 6 l-6 6" fill="none" stroke="var(--muted)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>' % (x + 231, y + 98))
    b.insert(0, N.group(0, 0, 1))
    cxm, cym = N.at('chiasma')
    b.append(L(cxm + 4, cym, 196, 214, 'ink', 1))
    b.append(T(200, 218, 'crossover', 11.5, 600, 'ink'))
    b.append(legend(24, 526))
    b.append(T(24, 550, 'drawn with 2 chromosome pairs and one crossover; humans average just over 2 crossovers per pair', 11.5, 400, 'muted'))
    return svg(560, title, 'Meiosis I: in prophase I each chromosome pairs with its partner from the other parent and they swap pieces (crossing over); in metaphase I the pairs line up, each pair facing the poles at random; in anaphase and telophase I the partners separate into two cells. Meiosis II: in both cells the chromosomes line up again and the sister chromatids separate, giving four cells with half the chromosomes, each a different mix.', b, N.defs())


# ---------------------------------------------------------------- 5. crossing over, close up
def crossover():
    title = 'Crossing over: partner chromosomes swap matching pieces'
    N = Obj('k20261120-xo')
    b = []
    steps = [('1 · Partners pair up', [(ALL_M, ALL_M), (ALL_P, ALL_P)], False), ('2 · Inner strands cross', [(ALL_M, ALL_M), (ALL_P, ALL_P)], True),
             ('3 · Pieces swapped', [(ALL_M, REC_M), (REC_P, ALL_P)], False)]
    for i, (hd, chrs, cross) in enumerate(steps):
        x = 24 + i * 244
        b.append(R(x, 52, 224, 220, 'edge', 1.25))
        b.append(T(x + 14, 74, hd, 13, 600))
        cx, cy = x + 112, 170
        if cross:
            chromosome(N, cx - 16, cy, 120, 90, *chrs[0], w=9)
            chromosome(N, cx + 16, cy, 120, 90, *chrs[1], w=9)
            ycr = cy + 120 * 0.4
            N.add('<path d="M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="none" stroke="%s" stroke-width="9" stroke-linecap="round"/>' % (cx - 9, ycr - 16, cx - 9, ycr, cx + 9, ycr, cx + 9, ycr + 16, MAT[1]))
            N.add('<path d="M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="none" stroke="%s" stroke-width="9" stroke-linecap="round"/>' % (cx + 9, ycr - 16, cx + 9, ycr, cx - 9, ycr, cx - 9, ycr + 16, PAT[1]))
            N.mark('x', cx, ycr)
        else:
            chromosome(N, cx - (16 if i == 0 else 22), cy, 120, 90, *chrs[0], w=9)
            chromosome(N, cx + (16 if i == 0 else 22), cy, 120, 90, *chrs[1], w=9)
        if i < 2:
            b.append('<path d="M%d 156 l6 6 l-6 6" fill="none" stroke="var(--muted)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>' % (x + 231))
    b.insert(0, N.group(0, 0, 1))
    mx, my = N.at('x')
    b.append(L(mx + 10, my, 420, my + 70, 'ink', 1))
    b += [T(398, my + 86, 'chiasma: the crossing point', 11.5, 600)]
    b.append(R(24, 330, 712, 50, 'focus', 2, 'focus', 0.1))
    b += [T(40, 352, 'Each sperm or egg carries a new mix of grandparents’ genes', 13, 600), T(40, 370, 'a chromosome can arrive part maternal, part paternal', 11.5)]
    return svg(390, title, 'Crossing over in three steps: the matching chromosomes from mother and father pair up; two inner chromatids cross at a chiasma; they swap the matching pieces, so the chromosomes that leave are part maternal, part paternal.', b, N.defs())


# ---------------------------------------------------------------- 6. why every egg and sperm differs
def diversity():
    title = 'Shuffling alone gives 8.4 million kinds of egg or sperm'
    b = [T(24, 62, 'EACH OF THE 23 PAIRS SENDS ONE COPY, MOTHER’S OR FATHER’S, AT RANDOM', 11.5, 600, 'muted')]
    pick = [1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0]
    for i, p in enumerate(pick):
        x = 30 + i * 30.5
        for k, pal in enumerate((MAT, PAT)):
            ln = 40 - i * 1.1
            on = (k == p)
            b.append('<rect x="%.1f" y="%.1f" width="7" height="%.1f" rx="3.5" fill="%s" fill-opacity="%s" stroke="%s" stroke-width="1"/>' % (
                x + k * 10, 80, ln, pal[1], '1' if on else '0.15', pal[2] if on else 'var(--edge)'))
        b.append(T(x + 8, 140, str(i + 1), 11.5, 400, 'muted', 'middle'))
    b.append('<rect x="560" y="150" width="7" height="14" rx="3.5" fill="%s" stroke="%s" stroke-width="1"/>' % (MAT[1], MAT[2]))
    b.append(T(574, 162, 'passed on', 11.5, 400, 'muted'))
    b.append('<rect x="650" y="150" width="7" height="14" rx="3.5" fill="%s" fill-opacity="0.15" stroke="var(--edge)" stroke-width="1"/>' % MAT[1])
    b.append(T(664, 162, 'left behind', 11.5, 400, 'muted'))
    b.append(L(24, 172, 736, 172))
    rows = [('Independent assortment', '2²³ combinations', 8388608, '8,388,608'), ('Two parents together', '(2²³)² zygotes', 7.0e13, '~70 trillion')]
    for j, (n, d, v, s) in enumerate(rows):
        y = 202 + j * 46
        b += [T(24, y, n, 13, 600), T(24, y + 18, d, 11.5, 400, 'muted'), T(736, y + 6, s, 15, 600, 'focus' if j == 0 else 'ink', 'end')]
    b.append(T(24, 312, 'plus ~2 crossovers per pair, which makes every gamete practically unique', 11.5, 400, 'muted'))
    return svg(322, title, 'Each of the 23 chromosome pairs sends either the mother\'s or the father\'s copy at random, so one person can make 2 to the 23rd, about 8.4 million, different combinations, and two parents about 70 trillion different children, before crossing over adds even more.', b)


# ---------------------------------------------------------------- the example
PROMPT = ('Cell division: examine mitosis and meiosis. Explain the whole process in a more visual way, '
          'with realistic pictures.')
LINE = 'Mitosis makes two identical copies of a cell; meiosis divides twice and makes four eggs or sperm, each with half the chromosomes and a new mix.'

STORY = '''**Where each happens.** Mitosis runs in almost every body cell: skin, gut lining and blood cells are replaced this way all the time. Meiosis happens only in the ovaries and testes, to make eggs and sperm.

**How long it takes.** In a fast-dividing human cell the whole cycle takes about a day, and the visible division (M phase) about an hour. Meiosis is far slower: making a sperm cell takes about two months, and egg cells begin meiosis before birth, then pause in prophase I for decades until ovulation.

**Why halve the chromosomes.** An egg and a sperm each carry 23 chromosomes; together they restore the 46 of a body cell. Without meiosis the number would double every generation.'''


def example():
    ov = overview()
    compare = [['Purpose', 'growth, repair, replacement', 'eggs and sperm'], ['Divisions', 'one', 'two'],
               ['Cells produced', '2', '4'], ['Chromosomes per cell', '46, same as the parent', '23, half'],
               ['Genetically', 'identical to the parent', 'all different'], ['Crossing over', 'no', 'yes, in prophase I'],
               ['Pairs line up', 'no, single chromosomes line up', 'yes, in metaphase I'], ['Where', 'almost all body cells', 'ovaries and testes']]
    sources = ('- Alberts et al., *Molecular Biology of the Cell* (NCBI Bookshelf): a 24-hour human cycle with G1 ~11 h, S ~8 h, G2 ~4 h, M ~1 h.\n'
               '- OpenStax *Biology 2e*, chapters 10 and 11: the cell cycle, mitosis and meiosis.\n'
               '- Embryo Project Encyclopedia (Arizona State University), *Meiosis in humans*: oocytes arrested in prophase I from before birth.\n'
               '- University of Minnesota, *Human Biology*, 5.2 *Meiosis*: 2²³ = 8,388,608 combinations from independent assortment.\n'
               '- Nature Scitable, *Meiosis, genetic recombination and sexual reproduction*: chiasmata and crossing over, about two per chromosome pair in humans.\n'
               '- BioNumbers (Harvard): duration of cell-cycle phases in human cells.')
    pdf = dict(title='Cell division: mitosis and meiosis', subtitle='How one cell becomes two identical cells, or four unique eggs or sperm', cards=[
        dict(type='drawing', title='', data=[ov]),
        dict(type='drawing', title='', data=[cycle()]),
        dict(type='drawing', title='', data=[mitosis()]),
        dict(type='drawing', title='', data=[meiosis()]),
        dict(type='drawing', title='', data=[crossover()]),
        dict(type='drawing', title='', data=[diversity()]),
        dict(type='table', title='Mitosis and meiosis side by side', data=dict(columns=['', 'Mitosis', 'Meiosis'], rows=compare)),
        dict(type='markdown', title='Where, how long, and why', data=STORY),
        dict(type='markdown', title='Sources', data=sources)])
    return dict(slug='cell', kind='Research', title='Cell division: mitosis and meiosis', prompt=PROMPT, question=PROMPT, line=LINE,
                chat=[ov], pdf=pdf, drawings=[c['data'][0] for c in pdf['cards'] if c['type'] == 'drawing'])
