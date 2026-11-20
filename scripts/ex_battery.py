"""Example: how a lithium-ion battery works (researched, multi-page). Used by examples.py."""
import math, os, sys
K = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(K, '..', 'public', 'skill', 'runik'))
sys.path.insert(0, K)
from runik_object import Obj, rrect
from runik_svg import T, R, L, P, dot, circ

STEEL = ('#f4f6f8', '#c3cad3', '#6d7783')
WRAP = ('#7fa6e0', '#3f6fbf', '#22457e')
CATH = ('#5a6170', '#3a404b', '#1f232a')      # metal-oxide coating, dark grey
ANOD = ('#3b3d40', '#232426', '#101112')      # graphite coating, black
ALU = ('#f3f5f7', '#c9d0d8', '#8a939e')
CU = ('#f8cfaa', '#d98b4e', '#9a5428')
SEP = ('#ffffff', '#eceff3', '#b8bfc8')
ELEC = ('#fdf9ea', '#f1e8c6', '#c2b383')
ION = ('#fff6cf', '#f2c94c', '#9b7612')
OXY = ('#f7b2a6', '#e05a45', '#9a2a1c')
TM = ('#b9c6ea', '#6a7fc4', '#34478a')       # transition metal (cobalt, nickel)
CARBON = '#2a2b2e'


def svg(h, title, desc, body, defs=''):
    return ('<svg viewBox="0 0 760 %d" width="100%%" font-size="13" role="img" aria-label="%s"><title>%s</title><desc>%s</desc>%s%s%s</svg>'
            % (h, title, title, desc, '<defs>%s</defs>' % defs if defs else '', T(24, 30, title, 15, 600), ''.join(body)))


def arrowhead(x, y, ang, c):
    a = math.radians(ang)
    p = lambda dx, dy: (x + dx * math.cos(a) - dy * math.sin(a), y + dx * math.sin(a) + dy * math.cos(a))
    (x1, y1), (x2, y2) = p(-7, -4), p(-7, 4)
    return '<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f Z" fill="var(--%s)"/>' % (x, y, x1, y1, x2, y2, c)


# ---------------------------------------------------------------- 1. inside an 18650 cell
def cell_cutaway():
    title = 'Inside a cylindrical cell: a rolled-up sandwich of foils'
    N = Obj('k20261120-18650')
    S = 5.2                       # px per mm: 18 x 65 mm cell
    cx, top = 236, 72
    r, h = 9 * S, 65 * S
    bot = top + h
    # shadow and the outer can, left half intact, right half cut open
    N.add(N.shadow(rrect(cx - r, top, 2 * r, h, 6), 6, 10, 8, 0.2))
    N.add('<path d="%s" fill="%s" stroke="%s" stroke-width="1.5"/>' % (rrect(cx - r, top + 10, r + 1, h - 10, 4), N.linear(WRAP[0], WRAP[2], 0, 0, 1, 0), WRAP[2]))
    N.add('<path d="M%.1f,%.1f h%.1f" stroke="#fff" stroke-width="3" opacity="0.45" stroke-linecap="round"/>' % (cx - r + 8, top + 30, 0))
    N.add('<path d="M%.1f,%.1f V%.1f" stroke="#fff" stroke-width="5" opacity="0.35" stroke-linecap="round"/>' % (cx - r + 12, top + 24, bot - 14))
    # cut face: can wall, then the wound layers out from the centre pin
    N.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>' % (cx, top + 12, r, h - 18, N.linear(*ELEC[:2])))
    x = cx + 3
    N.add('<rect x="%.1f" y="%.1f" width="3" height="%.1f" fill="%s"/>' % (cx - 1, top + 26, h - 40, N.linear(STEEL[0], STEEL[2], 0, 0, 1, 0)))
    layers = [(ALU, 0.6), (CATH, 2.2), (SEP, 0.9), (ANOD, 2.2), (CU, 0.6), (SEP, 0.9)]
    while x < cx + r - 5:
        for pal, w in layers:
            if x >= cx + r - 5:
                break
            N.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>' % (x, top + 26, w, h - 44, pal[1]))
            x += w
    N.add('<rect x="%.1f" y="%.1f" width="4" height="%.1f" fill="%s"/>' % (cx + r - 4, top + 10, h - 10, N.linear(STEEL[0], STEEL[2], 0, 0, 1, 0)))
    N.add('<rect x="%.1f" y="%.1f" width="%.1f" height="4" fill="%s"/>' % (cx, bot - 4, r, STEEL[2]))
    # top cap assembly (section on the right half)
    N.add('<path d="M%.1f,%.1f h%.1f v-8 h%.1f v-6 h%.1f v14 z" fill="%s" stroke="%s" stroke-width="1.2"/>' % (cx - r * 0.45, top + 12, r * 0.9, -r * 0.15, -r * 0.6, N.linear(STEEL[0], STEEL[1]), STEEL[2]))
    N.add('<rect x="%.1f" y="%.1f" width="%.1f" height="5" fill="#2b2b2b"/>' % (cx, top + 12, r - 4))              # gasket
    N.add('<rect x="%.1f" y="%.1f" width="%.1f" height="3" fill="#8fc4a8"/>' % (cx + 2, top + 17, r * 0.7))         # PTC disc
    N.add('<path d="M%.1f,%.1f q%.1f,-6 %.1f,0" fill="none" stroke="%s" stroke-width="2"/>' % (cx + 2, top + 23, r * 0.35, r * 0.7, STEEL[2]))  # vent disc
    N.add('<path d="M%.1f,%.1f V%.1f" stroke="%s" stroke-width="2"/>' % (cx + 6, top + 24, top + 30, ALU[2]))    # positive tab
    N.add('<path d="M%.1f,%.1f V%.1f" stroke="%s" stroke-width="2"/>' % (cx + 6, bot - 18, bot - 4, CU[2]))      # negative tab
    N.add('<path d="M%.1f,%.1f H%.1f" stroke="%s" stroke-width="1.5"/>' % (cx, top + 10, cx + r, WRAP[2]))
    marks = dict(cap=(cx - 4, top + 2), ptc=(cx + r * 0.5, top + 18), vent=(cx + r * 0.62, top + 21), gasket=(cx + r - 8, top + 14),
                 can=(cx + r - 2, top + h * 0.75), roll=(cx + r * 0.55, top + h * 0.45), pin=(cx, top + h * 0.3), neg=(cx, bot + 2), wrap=(cx - r + 6, top + h * 0.6))
    b = [N.group(0, 0, 1)]
    rows = [('cap', 'Positive cap', '+ terminal', 'r'), ('vent', 'Safety vent', 'opens if pressure builds', 'r'), ('ptc', 'PTC disc', 'limits current when hot', 'r'),
            ('gasket', 'Gasket', 'seals and insulates', 'r'), ('roll', 'Jelly roll', 'wound electrodes', 'r'), ('can', 'Steel can', '− terminal', 'r'),
            ('pin', 'Centre pin', 'keeps the roll round', 'l'), ('wrap', 'Plastic wrap', 'insulation', 'l'), ('neg', 'Base', '− contact', 'l')]
    ry = {'r': 76, 'l': 220}
    for key, name, what, side in rows:
        mx, my = marks[key]
        y = ry[side]
        if side == 'r':
            b.append('<path d="M%.1f %.1f L324 %.1f H332" fill="none" stroke="var(--ink)" stroke-width="0.9"/>' % (mx, my, y - 4))
            b += [T(336, y, name, 13, 600), T(336, y + 16, what, 11.5, 400, 'muted')]
            ry['r'] += 46
        else:
            b.append('<path d="M%.1f %.1f L150 %.1f H142" fill="none" stroke="var(--ink)" stroke-width="0.9"/>' % (mx, my, y - 4))
            b += [T(24, y, name, 13, 600), T(24, y + 16, what, 11.5, 400, 'muted')]
            ry['l'] += 70
        b.append(dot(mx, my, 2.6, 'ink'))
    # end view of the roll: a spiral of the same layers
    M = Obj('k20261120-18650top')
    ex, ey, er = 620, 140, 70
    M.add(M.ball(ex, ey, er + 4, cols=STEEL, shadow=0.15, gloss=0.2))
    M.add('<circle cx="%d" cy="%d" r="%d" fill="%s"/>' % (ex, ey, er, ELEC[1]))
    for pal, off, wdt in ((CATH, 0, 2.6), (SEP, 2.4, 1.2), (ANOD, 3.6, 2.6), (CU, 5.6, 0.9)):
        pts = []
        for i in range(0, 720):
            th = math.radians(i * 2.2)
            rr = 6 + off * 0.9 + 6.6 * th / (2 * math.pi)
            if rr > er - 2:
                break
            pts.append((ex + rr * math.cos(th), ey + rr * math.sin(th)))
        M.add('<path d="M%s" fill="none" stroke="%s" stroke-width="%.1f"/>' % (' L'.join('%.1f,%.1f' % p for p in pts), pal[1], wdt))
    M.add('<circle cx="%d" cy="%d" r="4" fill="%s"/>' % (ex, ey, STEEL[1]))
    b.append(M.group(0, 0, 1))
    b += [T(ex, ey + er + 26, 'Seen from the end', 13, 600, 'ink', 'middle'), T(ex, ey + er + 42, 'one long strip, wound ~20 times', 11.5, 400, 'muted', 'middle')]
    # the unrolled sandwich
    y0 = 300
    b.append(T(520, y0, 'The strip, unrolled', 13, 600))
    seq = [(ALU, 'aluminium foil', 6), (CATH, 'cathode (+)', 18), (SEP, 'separator', 9), (ANOD, 'anode (−)', 18), (CU, 'copper foil', 6)]
    yy = y0 + 14
    Q = Obj('k20261120-18650strip')
    for pal, lab, th in seq:
        Q.add('<rect x="520" y="%.1f" width="70" height="%d" fill="%s" stroke="%s" stroke-width="0.8"/>' % (yy, th, Q.linear(pal[0], pal[1]), pal[2]))
        b.append(L(594, yy + th / 2, 604, yy + th / 2, 'ink', 0.9))
        b.append(T(608, yy + th / 2 + 4, lab, 11.5, 400))
        yy += th
    b.append(Q.group(0, 0, 1))
    b.append(T(520, yy + 22, 'cathode: metal oxide · anode: graphite', 11.5, 400, 'muted'))
    b.append(T(520, yy + 40, 'all soaked in a lithium-salt electrolyte', 11.5, 400, 'muted'))
    b.append(P('M%.1f %.1f H%.1f M%.1f %.1f v6 M%.1f %.1f v6' % (cx - r, bot + 24, cx + r, cx - r, bot + 21, cx + r, bot + 21), 'ink', 1.25))
    b.append(T(cx, bot + 42, '18 mm', 11.5, 400, 'muted', 'middle'))
    b.append(P('M%.1f %.1f V%.1f M%.1f %.1f h6 M%.1f %.1f h6' % (cx - r - 22, top, bot, cx - r - 25, top, cx - r - 25, bot), 'ink', 1.25))
    b.append('<text x="%.1f" y="%.1f" font-size="11.5" fill="var(--muted)" text-anchor="middle" transform="rotate(-90 %.1f %.1f)">65 mm</text>' % (cx - r - 30, top + h / 2, cx - r - 30, top + h / 2))
    b.append(T(24, bot + 72, '18650 cell, 3.6 V nominal, cut open · drawn to scale except the layer thickness', 11.5, 400, 'muted'))
    return svg(bot + 82, title, 'Cutaway of an 18650 lithium-ion cell, 18 by 65 mm: positive cap with a safety vent, a PTC disc and a gasket; a steel can that is the negative terminal; inside, a jelly roll around a centre pin. The roll is one long strip, wound about 20 times: aluminium foil, metal-oxide cathode, porous separator, graphite anode, copper foil, soaked in electrolyte.', b, N.defs() + M.defs() + Q.defs())


# ---------------------------------------------------------------- 2. what the ions do
def lattice(N, x0, y0, w, h, li_in_graphite, li_in_oxide):
    '''Graphite sheets (left) and layered metal oxide (right) with lithium ions where they sit.'''
    g = []
    for k in range(6):  # graphite: hexagon chains seen edge-on
        y = y0 + 14 + k * (h - 28) / 5
        pts = ' L'.join('%.1f,%.1f' % (x0 + 6 + i * 7, y + (3 if i % 2 else -3)) for i in range(int((w * 0.32) / 7)))
        g.append('<path d="M%s" fill="none" stroke="%s" stroke-width="2.2" stroke-linejoin="round"/>' % (pts, CARBON))
    N.add(''.join(g))
    ox = x0 + w * 0.62
    for k in range(6):  # oxide: rows of metal (blue) between oxygen (red)
        y = y0 + 14 + k * (h - 28) / 5
        for i in range(int((w * 0.34) / 12)):
            N.add(N.ball(ox + 6 + i * 12, y - 4, 2.6, cols=OXY, shadow=0, gloss=0.3))
            N.add(N.ball(ox + 12 + i * 12, y, 3.4, cols=TM, shadow=0, gloss=0.3))
            N.add(N.ball(ox + 6 + i * 12, y + 4, 2.6, cols=OXY, shadow=0, gloss=0.3))
    for (x, y) in li_in_graphite + li_in_oxide:
        N.add(N.ball(x, y, 4, cols=ION, stroke=ION[2], sw=0.8, shadow=0, gloss=0.5))


def ions():
    title = 'Charging pushes lithium into graphite; using the battery lets it flow back'
    N = Obj('k20261120-ions')
    b = []
    for i, (name, sub, full) in enumerate((('Charging', 'charger pushes', True), ('In use', 'phone draws power', False))):
        x0, y0, w, h = 24 + i * 368, 96, 344, 190
        b.append(R(x0, y0 - 44, w, h + 112, 'edge', 1.25))
        b += [T(x0 + 14, y0 - 22, name, 13, 600)]
        N.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>' % (x0 + w * 0.34, y0, w * 0.26, h, N.linear(ELEC[0], ELEC[1])))
        N.add('<path d="M%.1f,%.1f V%.1f" stroke="%s" stroke-width="3" stroke-dasharray="5 4"/>' % (x0 + w * 0.47, y0, y0 + h, SEP[2]))
        rows = [y0 + 14 + k * (h - 28) / 5 for k in range(6)]
        gx = [x0 + 18 + j * 22 for j in range(4)]
        oxx = [x0 + w * 0.62 + 10 + j * 24 for j in range(4)]
        if full:
            lg = [(gx[j], rows[k] + 15) for k in range(5) for j in range(4) if (j + k) % 2 == 0]
            lo = [(oxx[j], rows[k] + 15) for k in range(5) for j in range(4) if (j + k) % 4 == 1][:3]
            mid = [(x0 + w * 0.42, y0 + 60), (x0 + w * 0.52, y0 + 120)]
        else:
            lo = [(oxx[j], rows[k] + 15) for k in range(5) for j in range(4) if (j + k) % 2 == 0]
            lg = [(gx[j], rows[k] + 15) for k in range(5) for j in range(4) if (j + k) % 4 == 1][:3]
            mid = [(x0 + w * 0.42, y0 + 80), (x0 + w * 0.52, y0 + 140)]
        lattice(N, x0 + 8, y0, w - 16, h, lg, lo + mid)
        # ion and electron flow
        d = -1 if full else 1
        ymid = y0 + h / 2
        b.append(P('M%.1f %.1f H%.1f' % (x0 + w * 0.47 - d * 36, ymid, x0 + w * 0.47 + d * 30), 'focus', 3))
        b.append(arrowhead(x0 + w * 0.47 + d * 38, ymid, 0 if d > 0 else 180, 'focus'))
        top = y0 - 8
        b.append(P('M%.1f %.1f V%.1f H%.1f V%.1f' % (x0 + 14, y0, top, x0 + w - 14, y0), 'edge', 1.5))
        b.append(R(x0 + w / 2 - 20, top - 16, 40, 30, 'ink', 0, 'surface', 1, rx=6))
        if full:
            b += [R(x0 + w / 2 - 10, top - 8, 20, 16, 'ink', 1.5, rx=4), L(x0 + w / 2 - 4, top - 8, x0 + w / 2 - 4, top - 14, 'ink', 1.5), L(x0 + w / 2 + 4, top - 8, x0 + w / 2 + 4, top - 14, 'ink', 1.5)]
        else:
            b += [R(x0 + w / 2 - 8, top - 14, 16, 26, 'ink', 1.5, rx=3)]
        for ex in (x0 + 60, x0 + w - 60):
            b.append(arrowhead(ex, top, 180 if full else 0, 'ink'))
        b += [T(x0 + 14, y0 + h + 22, 'Graphite (−)', 13, 600), T(x0 + w * 0.34, y0 + h + 22, 'Electrolyte', 13, 600),
              T(x0 + w - 14, y0 + h + 22, 'Metal oxide (+)', 13, 600, 'ink', 'end')]
        b.append(T(x0 + 14, y0 + h + 44, ('ions pile into the graphite layers · voltage rises to 4.2 V' if full else 'ions return to the oxide · voltage falls to ~3.0 V'), 11.5, 400, 'muted'))
    b.insert(0, N.group(0, 0, 1))
    lx, ly = 24, 380
    items = [(ION, 'lithium ion'), (TM, 'cobalt, nickel or manganese'), (OXY, 'oxygen')]
    for pal, lab in items:
        b.append('<circle cx="%d" cy="%d" r="5" fill="%s" stroke="%s" stroke-width="0.8"/>' % (lx + 5, ly - 4, pal[1], pal[2]))
        b.append(T(lx + 16, ly, lab, 11.5, 400, 'muted'))
        lx += 16 + len(lab) * 6.4 + 24
    b.append('<path d="M%d %d h18" stroke="%s" stroke-width="2.2"/>' % (lx, ly - 4, CARBON))
    b.append(T(lx + 24, ly, 'graphite sheet', 11.5, 400, 'muted'))
    b.append(T(24, 404, 'blue arrow = lithium ions through the electrolyte · black arrows = electrons through the wire · atoms not to scale', 11.5, 400, 'muted'))
    return svg(414, title, 'Atomic view. Charging: the charger pulls electrons through the wire and lithium ions leave the metal oxide, cross the electrolyte and separator, and slot between the graphite sheets; the voltage rises to 4.2 V. In use: the ions flow back into the layered oxide of cobalt, nickel or manganese and oxygen while electrons power the phone; the voltage falls to about 3.0 V.', b, N.defs())


# ---------------------------------------------------------------- 3. chemistries
CHEM = [('LCO', 'lithium cobalt oxide', (150, 200), (500, 1000), 150, 'phones, laptops, cameras'),
        ('LMO', 'lithium manganese oxide', (100, 150), (300, 700), 250, 'power tools, medical devices'),
        ('NMC', 'nickel manganese cobalt', (150, 220), (1000, 2000), 210, 'e-bikes, EVs, industrial'),
        ('LFP', 'lithium iron phosphate', (90, 120), (1000, 2000), 270, 'stationary storage, buses'),
        ('NCA', 'nickel cobalt aluminium', (200, 260), (500, 500), 150, 'EVs, medical, industrial'),
        ('LTO', 'lithium titanate anode', (70, 80), (3000, 7000), None, 'UPS, EVs, street lighting')]


def chemistries():
    title = 'NCA packs the most energy, LTO lasts the longest'
    b = [T(24, 62, 'TYPE', 11.5, 600, 'muted'), T(250, 62, 'ENERGY, WH/KG', 11.5, 600, 'muted'), T(500, 62, 'CYCLE LIFE, LOG', 11.5, 600, 'muted')]
    XE = lambda v: 250 + v / 280 * 220
    XC = lambda v: 500 + (math.log10(v) - 2) / (math.log10(8000) - 2) * 220
    for i, (ab, name, e, c, tr, use) in enumerate(CHEM):
        y = 92 + i * 46
        b += [T(24, y, ab, 13, 600), T(66, y, name, 11.5, 400), T(24, y + 17, use, 11.5, 400, 'muted')]
        b.append('<rect x="%.1f" y="%d" width="%.1f" height="12" rx="6" fill="var(--focus)" fill-opacity="0.35" stroke="var(--focus)" stroke-width="1.5"/>' % (XE(e[0]), y - 10, max(XE(e[1]) - XE(e[0]), 12)))
        b.append(T(XE(e[1]) + 8, y, '%d–%d' % e, 11.5, 600))
        b.append('<rect x="%.1f" y="%d" width="%.1f" height="12" rx="6" fill="var(--k2)" fill-opacity="0.4" stroke="var(--k2)" stroke-width="1.5"/>' % (XC(c[0]), y - 10, max(XC(c[1]) - XC(c[0]), 12)))
        lab = '{:,}–{:,}'.format(*c) if c[0] != c[1] else '~{:,}'.format(c[0])
        if XC(c[1]) + 8 + len(lab) * 6.4 > 736:
            b.append(T(XC(c[0]) - 8, y, lab, 11.5, 600, 'ink', 'end'))
        else:
            b.append(T(XC(c[1]) + 14, y, lab, 11.5, 600))
        b.append(L(24, y + 27, 736, y + 27))
    yb = 92 + len(CHEM) * 46
    for v in (0, 100, 200):
        b.append(T(XE(v), yb, str(v), 11.5, 400, 'muted', 'middle'))
    for v in (100, 1000, 7000):
        b.append(T(XC(v), yb, '{:,}'.format(v), 11.5, 400, 'muted', 'middle'))
    b.append(T(24, yb + 30, 'Battery University BU-216 · typical cells; newer cells, especially LFP, now exceed these figures', 11.5, 400, 'muted'))
    return svg(yb + 40, title, 'Six lithium-ion chemistries, energy per kilogram and cycle life: LCO 150-200 Wh/kg, 500-1,000 cycles (phones, laptops); LMO 100-150, 300-700 (power tools); NMC 150-220, 1,000-2,000 (e-bikes, EVs); LFP 90-120, 1,000-2,000 (storage); NCA 200-260, about 500 (EVs); LTO 70-80, 3,000-7,000 (UPS, EVs).', b)


# ---------------------------------------------------------------- 4. why batteries wear out
def ageing():
    title = 'Shallow cycles and cool storage keep a battery young'
    b = [T(24, 62, 'CYCLES UNTIL 70% CAPACITY, BY HOW DEEP EACH DISCHARGE GOES', 11.5, 600, 'muted')]
    dod = [('100%', (300, 500)), ('50%', (1200, 1500)), ('25%', (2000, 2500)), ('10%', (3750, 4700))]
    X = lambda v: 150 + v / 5000 * 520
    for i, (d, (lo, hi)) in enumerate(dod):
        y = 88 + i * 30
        b.append(T(24, y + 4, '%s discharge' % d, 13, 600))
        b.append('<rect x="150" y="%d" width="%.1f" height="14" rx="3" fill="var(--focus)" fill-opacity="0.3" stroke="var(--focus)" stroke-width="1.5"/>' % (y - 8, X(lo) - 150))
        b.append('<rect x="%.1f" y="%d" width="%.1f" height="14" rx="3" fill="var(--focus)" fill-opacity="0.12" stroke="var(--focus)" stroke-width="1" stroke-dasharray="3 2"/>' % (X(lo), y - 8, X(hi) - X(lo)))
        b.append(T(X(hi) + 8, y + 4, '{:,}–{:,}'.format(lo, hi), 11.5, 600))
    b.append(L(24, 214, 736, 214))
    b.append(T(24, 242, 'CAPACITY LEFT AFTER ONE YEAR IN STORAGE', 11.5, 600, 'muted'))
    data = [('0 °C', 98, 94), ('25 °C', 96, 80), ('40 °C', 85, 65)]
    b += [T(250, 266, 'kept at 40% charge', 11.5, 600, 'ink', 'middle'), T(520, 266, 'kept at 100% charge', 11.5, 600, 'ink', 'middle')]
    for i, (t, a, f) in enumerate(data):
        y = 296 + i * 44
        b.append(T(24, y + 4, t, 13, 600))
        for v, x0 in ((a, 150), (f, 420)):
            c = 'good' if v >= 90 else 'warn' if v >= 75 else 'bad'
            b.append('<rect x="%d" y="%d" width="200" height="22" rx="4" fill="none" stroke="var(--edge)" stroke-width="1.25"/>' % (x0, y - 13))
            b.append('<rect x="%d" y="%d" width="%.1f" height="22" rx="4" fill="var(--%s)" fill-opacity="0.35" stroke="var(--%s)" stroke-width="1.5"/>' % (x0, y - 13, 2 * v, c, c))
            b.append(T(x0 + 208, y + 3, '%d%% %s' % (v, '✓' if v >= 90 else '!' if v >= 75 else '✗'), 11.5, 600, c))
    b.append(T(24, 440, 'cobalt-based cells · Battery University BU-808, estimated values', 11.5, 400, 'muted'))
    return svg(450, title, 'Cycles before capacity drops to 70%: 300-500 at 100% depth of discharge, 1,200-1,500 at 50%, 2,000-2,500 at 25%, 3,750-4,700 at 10%. Capacity left after a year of storage: at 0 °C 98% (40% charge) or 94% (full); at 25 °C 96% or 80%; at 40 °C 85% or 65%.', b)


def causes():
    title = 'Three things eat a battery from the inside'
    N = Obj('k20261120-age')
    b = []
    heads = [('A crust grows on the graphite', 'the SEI layer traps lithium for good'), ('Metal lithium plates out', 'fast charging in the cold'),
             ('The cathode cracks', 'swelling and shrinking each cycle')]
    for i, (hd, sub) in enumerate(heads):
        x = 24 + i * 244
        b.append(R(x, 52, 224, 190, 'edge', 1.25))
        b += [T(x + 14, 74, hd, 12.5, 600), T(x + 14, 226, sub, 11.5, 400, 'muted')]
        cx, cy = x + 112, 150
        if i == 0:
            for k in range(5):
                N.add('<path d="M%d,%d H%d" stroke="%s" stroke-width="5"/>' % (x + 30, cy - 30 + k * 14, x + 150, CARBON))
            N.add('<path d="M%d,%d C%d,%d %d,%d %d,%d V%d C%d,%d %d,%d %d,%d Z" fill="#c9b07a" opacity="0.8"/>' % (
                x + 150, cy - 40, x + 162, cy - 30, x + 158, cy - 10, x + 166, cy, cy + 40, x + 158, cy + 30, x + 162, cy + 20, x + 150, cy + 30))
            for (dx, dy) in ((156, -24), (160, 2), (158, 22)):
                N.add(N.ball(x + dx, cy + dy, 3.5, cols=ION, stroke=ION[2], sw=0.6, shadow=0, gloss=0.4))
            for (dx, dy) in ((186, -20), (196, 10), (182, 30)):
                N.add(N.ball(x + dx, cy + dy, 4, cols=ION, stroke=ION[2], sw=0.6, shadow=0, gloss=0.4))
        elif i == 1:
            for k in range(5):
                N.add('<path d="M%d,%d H%d" stroke="%s" stroke-width="5"/>' % (x + 30, cy - 30 + k * 14, x + 130, CARBON))
            for k in range(4):
                yy = cy - 26 + k * 16
                N.add('<path d="M%d,%d l12,-3 l8,4 l10,-6 l6,3" fill="none" stroke="#b8bec7" stroke-width="3" stroke-linecap="round"/>' % (x + 132, yy))
            N.add('<path d="M%d,%d V%d" stroke="%s" stroke-width="3" stroke-dasharray="5 4"/>' % (x + 176, cy - 44, cy + 44, SEP[2]))
            b.append(T(x + 186, cy - 30, 'cold', 11.5, 600, 'focus'))
        else:
            N.add(N.ball(cx, cy, 44, cols=('#8b93a3', '#5b6372', '#2f343d'), shadow=0.15, gloss=0.25))
            for d in ('M%d,%d l10,12 l-4,14 l12,18' % (cx - 20, cy - 40), 'M%d,%d l-8,14 l6,10 l-10,12' % (cx + 24, cy - 36), 'M%d,%d l14,-4 l10,8' % (cx - 40, cy + 10)):
                N.add('<path d="%s" fill="none" stroke="#1a1d22" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>' % d)
    b.insert(0, N.group(0, 0, 1))
    b.append(T(24, 268, 'all three are faster when the cell is hot, full, or charged and drained hard', 11.5, 400, 'muted'))
    return svg(278, title, 'Three ageing mechanisms: a solid-electrolyte interphase layer keeps growing on the graphite and permanently traps lithium; fast charging in the cold plates metallic lithium on the anode; the cathode particles crack as they swell and shrink every cycle. All three speed up with heat, high charge and hard use.', b, N.defs())


# ---------------------------------------------------------------- 5. history
EVENTS = [(1976, 'Whittingham', 'rechargeable lithium cell, TiS₂', 0), (1980, 'Goodenough', 'cobalt-oxide cathode, ~4 V', 2),
          (1985, 'Yoshino', 'carbon anode makes it safe', 1), (1991, 'Sony', 'first lithium-ion battery on sale', 3),
          (1997, 'LFP', 'iron-phosphate cathode', 0), (2019, 'Nobel Prize', 'Chemistry, to all three', 2)]


def history():
    title = 'From lab cell to Nobel Prize in 43 years'
    X = lambda y: 60 + (y - 1970) / 55 * 640
    axis = 132
    levels = {0: 62, 1: 100, 2: 172, 3: 210}
    b = [L(X(1970), axis, X(2025), axis, 'edge', 1.5)]
    for yr, who, what, lv in EVENTS:
        ty = levels[lv]
        end = yr > 2010
        b.append(L(X(yr), axis, X(yr), ty + 18 if lv < 2 else ty - 12, 'focus', 1.25))
        b.append(dot(X(yr), axis, 6, 'focus'))
        tx = X(yr) + (-8 if end else 8)
        b.append(T(tx, ty, '%d · %s' % (yr, who), 13, 600, 'ink', 'end' if end else None))
        b.append(T(tx, ty + 16, what, 11.5, 400, 'muted', 'end' if end else None))
    for yr in (1970, 1980, 1990, 2000, 2010, 2020):
        b.append(T(X(yr), 256, str(yr), 11.5, 400, 'muted', 'middle'))
    b.append(L(X(1970), 240, X(2025), 240, 'line', 1))
    return svg(268, title, 'History: 1976 Stanley Whittingham builds a rechargeable lithium cell with a titanium disulfide cathode; 1980 John Goodenough finds the cobalt-oxide cathode at about 4 volts; 1985 Akira Yoshino makes a safe cell with a carbon anode; 1991 Sony sells the first lithium-ion battery; 1997 the iron-phosphate cathode; 2019 Nobel Prize in Chemistry to Whittingham, Goodenough and Yoshino.', b)


# ---------------------------------------------------------------- the example
PROMPT = ('How does a lithium-ion battery work? Show what is inside a real cell, what happens during charging and discharging down to the atoms, '
          'how the main battery chemistries compare, why batteries wear out and how to make one last, and where the technology came from. '
          'Research it, then build the document.')
LINE = 'Lithium ions shuttle between graphite and a metal oxide through the electrolyte, while electrons take the long way through your device.'
TIPS = '''- **Keep it between about 20% and 80%** for daily use; full charges and deep discharges wear it faster.
- **Keep it cool.** Heat is the biggest accelerator: don't charge it under a pillow or leave it in a hot car.
- **Store it half charged**, around 40–50%, in a cool place if it will sit for weeks.
- **Avoid fast charging in the cold**, which can plate metallic lithium on the anode.
- **Partial top-ups are fine.** Lithium-ion has no memory effect; there is no need to drain it first.'''


def example():
    cut = cell_cutaway()
    sources = ('- Battery University, *BU-216: Summary table of lithium-based batteries*: voltages, specific energy, cycle life, thermal runaway temperatures, uses.\n'
               '- Battery University, *BU-205: Types of lithium-ion* and *BU-808: How to prolong lithium-based batteries*: cycle life by depth of discharge, storage losses by temperature and charge.\n'
               '- The Nobel Prize in Chemistry 2019 (nobelprize.org): Whittingham, Goodenough and Yoshino; Sony\'s 1991 commercial cell.\n'
               '- Patent literature on cylindrical cells (USPTO): jelly-roll construction, current-interrupt vent and PTC devices.')
    pdf = dict(title='How a lithium-ion battery works', subtitle='Inside a cell, the chemistry of charging, the main types, why they age and where they came from', cards=[
        dict(type='drawing', title='', data=[cut]),
        dict(type='drawing', title='', data=[ions()]),
        dict(type='drawing', title='', data=[chemistries()]),
        dict(type='drawing', title='', data=[ageing()]),
        dict(type='drawing', title='', data=[causes()]),
        dict(type='markdown', title='How to make one last', data=TIPS),
        dict(type='drawing', title='', data=[history()]),
        dict(type='markdown', title='Sources', data=sources)])
    return dict(slug='battery', kind='Research', title='How a lithium-ion battery works', prompt=PROMPT, question=PROMPT, line=LINE,
                chat=[cut], pdf=pdf, drawings=[c['data'][0] for c in pdf['cards'] if c['type'] == 'drawing'])
