"""Detailed animal cell: the whole cell with its organelles, close-ups and a size scale. Used by ex_cell.py."""
import math, os, sys
K = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(K, '..', 'public', 'skill', 'runik'))
sys.path.insert(0, K)
from runik_object import Obj, smooth
from runik_svg import T, R, L, P, dot

CYTO = ('#fff4ee', '#f8dbd0', '#c9897b')
MEMB = ('#f2c2b4', '#d9907e', '#a65d4c')
NUC = ('#f3ecfa', '#d2bfe9', '#8a6cb0')
NUCLEOLUS = ('#b79fd8', '#8566b5', '#553a82')
HETERO = '#7a5aa6'
RER = ('#f6c7d6', '#e39ab4', '#a85476')
SER = ('#f9d9e3', '#efb4c8', '#b77892')
GOLGI = ('#fff0c2', '#f2c04a', '#a87a14')
MITO = ('#ffe1cc', '#f2a072', '#b65f38')
CRISTA = '#c96a3c'
LYSO = ('#e7f4d9', '#a8d483', '#5d913f')
PEROX = ('#fdf6c9', '#ead35a', '#9c8a1c')
VESICLE = ('#fffbe9', '#f6dc8e', '#b89530')
ENDO = ('#e5eefb', '#a9c2ea', '#5a7bb5')
RIBO = '#6e3550'
MT = '#6ea98a'
ACTIN = '#d77b6a'
CENT = ('#cfe9d9', '#5fa47b', '#2f6b45')

CX, CY, RX, RY = 382, 318, 216, 188
NX, NY, NRX, NRY = 330, 318, 86, 74


def svg(h, title, desc, body, defs=''):
    return ('<svg viewBox="0 0 760 %d" width="100%%" font-size="13" role="img" aria-label="%s"><title>%s</title><desc>%s</desc>%s%s%s</svg>'
            % (h, title, title, desc, '<defs>%s</defs>' % defs if defs else '', T(24, 30, title, 15, 600), ''.join(body)))


def rnd(seed):
    while True:
        seed = (seed * 1103515245 + 12345) & 0x7fffffff
        yield seed / 0x7fffffff


def edge(a, k=1.0):
    j = 1 + 0.022 * math.sin(3 * a + 1) + 0.018 * math.cos(5 * a + 2)
    return (CX + RX * k * math.cos(a) * j, CY + RY * k * math.sin(a) * j)


def inside_cell(x, y, margin=0.9):
    return ((x - CX) / (RX * margin)) ** 2 + ((y - CY) / (RY * margin)) ** 2 < 1


def in_nucleus(x, y, pad=1.18):
    return ((x - NX) / (NRX * pad)) ** 2 + ((y - NY) / (NRY * pad)) ** 2 < 1


def mitochondrion(N, cx, cy, rot, L=36, Wd=15):
    o = [N.ball(cx, cy, L, Wd, cols=MITO, stroke=MITO[2], sw=1.8, shadow=0.14, gloss=0.25)]
    o.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="none" stroke="%s" stroke-width="1.1" opacity="0.8"/>' % (cx, cy, L - 3.5, Wd - 3.5, CRISTA))
    for k in range(7):
        x = cx - L * 0.72 + k * L * 0.24
        side = 1 if k % 2 else -1
        h = (Wd - 3.5) * math.sqrt(max(0, 1 - ((x - cx) / (L - 3.5)) ** 2))
        o.append('<path d="M%.1f,%.1f q-3,%.1f 0,%.1f q3,%.1f 0,%.1f" fill="none" stroke="%s" stroke-width="1.3" stroke-linecap="round"/>' % (
            x, cy + side * h, -side * h * 0.35, -side * h * 0.7, -side * h * 0.35, -side * h * 0.6, CRISTA))
    o.append('<circle cx="%.1f" cy="%.1f" r="1.4" fill="%s"/>' % (cx + L * 0.3, cy + 2, '#7a3a1c'))
    N.add('<g transform="rotate(%d %.1f %.1f)">%s</g>' % (rot, cx, cy, ''.join(o)))


def centriole(N, x, y, rot):
    o = ['<rect x="%.1f" y="%.1f" width="18" height="9" rx="2" fill="%s" stroke="%s" stroke-width="1"/>' % (x - 9, y - 4.5, N.linear(CENT[0], CENT[1]), CENT[2])]
    o += ['<path d="M%.1f,%.1f v9" stroke="%s" stroke-width="0.9"/>' % (x - 7 + k * 2.2, y - 4.5, CENT[2]) for k in range(7)]
    N.add('<g transform="rotate(%d %.1f %.1f)">%s</g>' % (rot, x, y, ''.join(o)))


def cell_body(prefix):
    N = Obj(prefix)
    r = rnd(7)
    outline = smooth([edge(2 * math.pi * i / 40) for i in range(40)], closed=True, t=0.5)
    N.add(N.shadow(outline, 4, 8, 7, 0.16))
    N.add('<path d="%s" fill="%s"/>' % (outline, N.radial(*CYTO)))
    # cytoskeleton: microtubules from the centrosome, actin cortex under the membrane
    cs = (440, 214)
    for k in range(18):
        a = 2 * math.pi * k / 18 + 0.15
        ex, ey = edge(a, 0.93)
        mx, my = (cs[0] + ex) / 2 + 18 * math.sin(a * 3), (cs[1] + ey) / 2 + 18 * math.cos(a * 2)
        N.add('<path d="M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" fill="none" stroke="%s" stroke-width="1" opacity="0.55"/>' % (cs[0], cs[1], mx, my, ex, ey, MT))
    N.add('<path d="%s" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="3 2" opacity="0.45" transform="translate(%d %d) scale(0.955) translate(%d %d)"/>' % (outline, ACTIN, CX, CY, -CX, -CY))
    # smooth ER: branching tubes, lower left
    for d in ('M218,392 C240,380 262,404 286,392 S324,404 338,396', 'M226,412 C250,420 270,402 296,418 S330,428 350,414',
              'M250,392 C252,404 246,414 252,424', 'M296,394 C300,404 292,412 298,420', 'M212,430 C236,440 262,430 280,444 S314,448 330,440'):
        N.add(N.tube(d, SER[2], SER[1], 7, 4.5))
    # rough ER: flattened sacs wrapped round the nucleus, studded with ribosomes
    for j, rr in enumerate((1.16, 1.3, 1.44)):
        pts = [(NX + NRX * rr * math.cos(math.radians(a)), NY + NRY * rr * math.sin(math.radians(a))) for a in range(-50, 116, 5)]
        d = 'M' + ' L'.join('%.1f,%.1f' % p for p in pts)
        N.add(N.tube(d, RER[2], RER[1], 8, 5))
        for k, (x, y) in enumerate(pts[::2]):
            for s in (-1, 1):
                nx_, ny_ = (x - NX), (y - NY)
                ln = math.hypot(nx_, ny_)
                N.add('<circle cx="%.1f" cy="%.1f" r="1.6" fill="%s"/>' % (x + s * 5 * nx_ / ln, y + s * 5 * ny_ / ln, RIBO))
    N.mark('rer', NX + NRX * 1.44 * math.cos(math.radians(30)), NY + NRY * 1.44 * math.sin(math.radians(30)))
    N.mark('ser', 300, 432)
    # nucleus: double envelope with pores, chromatin, nucleolus
    N.add(N.ball(NX, NY, NRX, NRY, cols=NUC, stroke=NUC[2], sw=2.2, shadow=0.12, gloss=0.2))
    N.add('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="none" stroke="%s" stroke-width="1.2"/>' % (NX, NY, NRX - 5, NRY - 5, NUC[2]))
    for k in range(9):  # heterochromatin hugging the envelope
        a = 2 * math.pi * k / 9 + 0.3
        x, y = NX + (NRX - 14) * math.cos(a), NY + (NRY - 14) * math.sin(a)
        N.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="5" fill="%s" opacity="0.32" transform="rotate(%.1f %.1f %.1f)"/>' % (x, y, 10 + 4 * next(r), HETERO, math.degrees(a) + 90, x, y))
    for k in range(16):  # euchromatin threads
        x, y = NX - 50 + next(r) * 90, NY - 40 + next(r) * 80
        if in_nucleus(x, y, 0.8):
            N.add('<path d="M%.1f,%.1f q6,-8 12,0 t12,2 t10,-6" fill="none" stroke="%s" stroke-width="1.3" opacity="0.45" stroke-linecap="round"/>' % (x, y, HETERO))
    for k in range(22):  # pores
        a = 2 * math.pi * k / 22
        x1, y1 = NX + (NRX - 6) * math.cos(a), NY + (NRY - 6) * math.sin(a)
        x2, y2 = NX + (NRX + 1) * math.cos(a), NY + (NRY + 1) * math.sin(a)
        N.add('<path d="M%.1f,%.1f L%.1f,%.1f" stroke="%s" stroke-width="3.2" stroke-linecap="round"/>' % (x1, y1, x2, y2, NUC[0]))
        N.add('<circle cx="%.1f" cy="%.1f" r="1.1" fill="%s"/>' % ((x1 + x2) / 2, (y1 + y2) / 2, NUC[2]))
    N.add(N.ball(NX + 18, NY - 6, 22, 20, cols=NUCLEOLUS, shadow=0.05, gloss=0.25))
    for k in range(26):
        a, rr = 2 * math.pi * next(r), 18 * math.sqrt(next(r))
        N.add('<circle cx="%.1f" cy="%.1f" r="1.2" fill="%s" opacity="0.6"/>' % (NX + 18 + rr * math.cos(a), NY - 6 + rr * 0.9 * math.sin(a), NUCLEOLUS[2]))
    N.mark('nucleolus', NX + 6, NY - 12)
    N.mark('envelope', NX - NRX * 0.72, NY - NRY * 0.69)
    N.mark('chromatin', NX - 40, NY + 30)
    # Golgi: stacked cisternae, cis face toward the nucleus, vesicles budding from the trans face
    for k in range(6):
        x = 486 + k * 9
        h = 52 - abs(k - 2.5) * 6
        N.add(N.tube('M%d,%.1f Q%.1f,%d %d,%.1f' % (x, 290 - h, x + 20, 290, x, 290 + h), GOLGI[2], GOLGI[1], 8, 5))
    for (x, y, rr) in ((548, 254, 5), (556, 276, 4.5), (552, 310, 5), (562, 330, 4), (470, 262, 3.5), (474, 322, 3.5)):
        N.add(N.ball(x, y, rr, cols=VESICLE, stroke=VESICLE[2], sw=1, shadow=0.1, gloss=0.5))
    N.mark('golgi', 520, 248)
    # secretory vesicles and one fusing with the membrane (exocytosis)
    for (x, y, rr) in ((572, 226, 6.5), (586, 248, 5.5)):
        N.add(N.ball(x, y, rr, cols=VESICLE, stroke=VESICLE[2], sw=1, shadow=0.1, gloss=0.5))
    ex, ey = edge(math.radians(-38), 1.0)
    N.add('<path d="M%.1f,%.1f a8,8 0 1 0 12,6" fill="%s" stroke="%s" stroke-width="1.2"/>' % (ex - 12, ey + 4, VESICLE[1], VESICLE[2]))
    N.mark('exo', ex - 4, ey + 6)
    # mitochondria
    for (x, y, rot) in ((232, 214, -28), (206, 336, 72), (334, 462, 8), (448, 452, -24), (566, 372, 82), (476, 150, 14)):
        mitochondrion(N, x, y, rot)
    N.mark('mito', 232, 214)
    # lysosomes, peroxisomes, endosome
    for (x, y, rr) in ((236, 270, 10), (522, 430, 9), (398, 432, 8)):
        N.add(N.ball(x, y, rr, cols=LYSO, stroke=LYSO[2], sw=1.3, shadow=0.12, gloss=0.4))
        for k in range(5):
            N.add('<circle cx="%.1f" cy="%.1f" r="1.2" fill="%s" opacity="0.7"/>' % (x - rr * 0.4 + next(r) * rr * 0.8, y - rr * 0.4 + next(r) * rr * 0.8, LYSO[2]))
    N.mark('lyso', 236, 270)
    for (x, y, rr) in ((544, 410, 8), (300, 178, 7)):
        N.add(N.ball(x, y, rr, cols=PEROX, stroke=PEROX[2], sw=1.2, shadow=0.12, gloss=0.4))
        N.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" opacity="0.7" transform="rotate(20 %.1f %.1f)"/>' % (x - rr * 0.35, y - rr * 0.35, rr * 0.7, rr * 0.7, PEROX[2], x, y))
    N.mark('perox', 544, 410)
    N.add(N.ball(372, 186, 13, cols=ENDO, stroke=ENDO[2], sw=1.3, shadow=0.12, gloss=0.3))
    for (dx, dy) in ((-4, -3), (4, 2), (-2, 5), (5, -5)):
        N.add('<circle cx="%d" cy="%d" r="2.6" fill="none" stroke="%s" stroke-width="0.9"/>' % (372 + dx, 186 + dy, ENDO[2]))
    N.mark('endo', 372, 186)
    # free ribosomes and polysomes in the cytosol
    count = 0
    while count < 170:
        x, y = CX - RX + next(r) * 2 * RX, CY - RY + next(r) * 2 * RY
        if inside_cell(x, y, 0.88) and not in_nucleus(x, y, 1.55) and not (472 < x < 566 and 230 < y < 350):
            N.add('<circle cx="%.1f" cy="%.1f" r="1.5" fill="%s" opacity="0.75"/>' % (x, y, RIBO))
            count += 1
    for k in range(5):
        x0, y0 = 470 + k * 6, 392 + k * 3
        N.add('<path d="M%d,%d q8,-6 16,0 t16,0" fill="none" stroke="%s" stroke-width="0.6" opacity="0.6"/>' % (x0, y0, RIBO))
        N.add(''.join('<circle cx="%d" cy="%.1f" r="1.6" fill="%s"/>' % (x0 + j * 4, y0 - 2 * math.sin(j), RIBO) for j in range(9)))
    N.mark('ribo', 486, 396)
    # centrosome: two centrioles at right angles in a halo
    N.add('<circle cx="%d" cy="%d" r="15" fill="%s" opacity="0.25"/>' % (cs[0], cs[1], CENT[1]))
    centriole(N, cs[0] - 4, cs[1] - 2, 20)
    centriole(N, cs[0] + 5, cs[1] + 4, 110)
    N.mark('centrosome', cs[0], cs[1])
    N.mark('mt', 600, 300)
    # plasma membrane: bilayer with embedded proteins
    N.add('<path d="%s" fill="none" stroke="%s" stroke-width="6"/>' % (outline, MEMB[2]))
    N.add('<path d="%s" fill="none" stroke="%s" stroke-width="3.2"/>' % (outline, MEMB[0]))
    for k in range(34):
        a = 2 * math.pi * k / 34 + 0.05
        x, y = edge(a)
        N.add('<ellipse cx="%.1f" cy="%.1f" rx="2.4" ry="5" fill="%s" stroke="%s" stroke-width="0.8" transform="rotate(%.1f %.1f %.1f)"/>' % (
            x, y, '#b9a3d6' if k % 3 else '#8fc4a8', MEMB[2], math.degrees(a) + 90, x, y))
    N.mark('membrane', *edge(math.radians(48)))
    return N


LABELS = {'left': [('endo', 'Endosome', 'sorts what comes in'), ('mito', 'Mitochondrion', 'makes ATP, the energy'),
                   ('envelope', 'Nuclear envelope', 'double membrane, pores'), ('lyso', 'Lysosome', 'digests and recycles'),
                   ('chromatin', 'Chromatin', 'DNA wound on proteins'), ('ser', 'Smooth ER', 'lipids, detox')],
          'right': [('centrosome', 'Centrosome', 'microtubule hub'), ('golgi', 'Golgi apparatus', 'packs proteins'),
                    ('exo', 'Secretory vesicle', 'releases cargo'), ('nucleolus', 'Nucleolus', 'builds ribosomes'),
                    ('rer', 'Rough ER', 'folds new proteins'), ('ribo', 'Ribosomes', 'make proteins'),
                    ('perox', 'Peroxisome', 'breaks down fats'), ('membrane', 'Plasma membrane', 'decides what passes')]}


def anatomy():
    title = 'One animal cell, a dozen specialised parts'
    N = cell_body('k20261120-cellmap')
    b = [N.group(0, 0, 1)]
    for side, items in LABELS.items():
        pts = sorted(items, key=lambda it: N.at(it[0])[1])
        n = len(pts)
        for i, (key, name, what) in enumerate(pts):
            y = 82 + i * (470 / (n - 1))
            mx, my = N.at(key)
            if side == 'left':
                b.append('<path d="M%.1f %.1f L150 %.1f H142" fill="none" stroke="var(--ink)" stroke-width="0.9"/>' % (mx, my, y - 4))
                b += [T(24, y, name, 13, 600), T(24, y + 17, what, 11.5, 400, 'muted')]
            else:
                b.append('<path d="M%.1f %.1f L606 %.1f H612" fill="none" stroke="var(--ink)" stroke-width="0.9"/>' % (mx, my, y - 4))
                b += [T(616, y, name, 13, 600), T(616, y + 17, what, 11.5, 400, 'muted')]
            b.append(dot(mx, my, 2.6, 'ink'))
    b.append(P('M%d 600 V606 H%.1f V600' % (24, 24 + 2 * RX * 4 / 20), 'ink', 1.25))
    b.append(T(24 + 2 * RX * 4 / 20 + 8, 606, '~4 µm', 11.5, 400, 'muted'))
    b.append(T(24, 630, 'simplified section through a typical animal cell, ~20 µm across · organelle counts reduced', 11.5, 400, 'muted'))
    return svg(640, title, 'Section through an animal cell. Nucleus with a double envelope and pores, chromatin and a nucleolus; rough endoplasmic reticulum with ribosomes wrapped around it; smooth ER; Golgi apparatus with budding vesicles; a secretory vesicle fusing with the plasma membrane; mitochondria; lysosomes; peroxisomes; an endosome; free ribosomes and polysomes; a centrosome with two centrioles and microtubules spreading from it; an actin cortex under the plasma membrane, a lipid bilayer with embedded proteins.', b, N.defs())


# ---------------------------------------------------------------- close-ups
def closeups():
    title = 'Zoomed in: membrane, mitochondrion, nuclear pore, Golgi'
    N = Obj('k20261120-zoom')
    b = []
    heads = [('Plasma membrane', 'a lipid bilayer ~7 nm thick'), ('Mitochondrion', 'inner membrane folds into cristae'),
             ('Nuclear pore', 'gate between nucleus and cytoplasm'), ('Golgi apparatus', 'proteins pass from cis to trans')]
    for i, (hd, sub) in enumerate(heads):
        x, y = 24 + (i % 2) * 368, 52 + (i // 2) * 250
        b.append(R(x, y, 344, 230, 'edge', 1.25))
        b += [T(x + 14, y + 22, hd, 13, 600), T(x + 14, y + 214, sub, 11.5, 400, 'muted')]
        cx, cy = x + 172, y + 118
        if i == 0:
            for k in range(22):
                hx = x + 22 + k * 14
                if 132 < hx - x < 186:
                    continue
                for s, yy in ((1, cy - 30), (-1, cy + 30)):
                    N.add('<path d="M%.1f,%.1f q-2,%d 0,%d M%.1f,%.1f q2,%d 0,%d" fill="none" stroke="%s" stroke-width="1.5"/>' % (hx - 2, yy + s * 6, s * 12, s * 24, hx + 2, yy + s * 6, s * 12, s * 24, MEMB[2]))
                    N.add(N.ball(hx, yy, 6, cols=MEMB, stroke=MEMB[2], sw=1, shadow=0, gloss=0.4))
            N.add('<path d="M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f Z" fill="%s" stroke="#5a4a8a" stroke-width="1.4"/>' % (
                x + 150, cy - 50, x + 140, cy - 10, x + 140, cy + 10, x + 150, cy + 50, x + 160, cy + 56, x + 184, cy + 56, x + 194, cy + 50, x + 204, cy + 10, x + 194, cy - 50, x + 150, cy - 50, N.linear('#e3dcf6', '#a796d6')))
            N.add('<rect x="%.1f" y="%.1f" width="10" height="100" rx="5" fill="#f8f4ff" stroke="#5a4a8a" stroke-width="1"/>' % (x + 167, cy - 50))
            N.add(N.ball(x + 172, cy - 66, 4, cols=('#fff6cf', '#f2c94c', '#9b7612'), shadow=0, gloss=0.4))
            b += [T(x + 18, cy - 54, 'outside', 11.5, 400, 'muted'), T(x + 18, cy + 64, 'inside the cell', 11.5, 400, 'muted')]
            b.append(L(x + 230, cy - 30, x + 262, cy - 52, 'ink', 0.9))
            b.append(T(x + 262, cy - 56, 'lipid head', 11.5, 600))
            b.append(L(x + 200, cy + 30, x + 230, cy + 60, 'ink', 0.9))
            b.append(T(x + 232, cy + 66, 'channel protein', 11.5, 600))
        elif i == 1:
            N.add(N.ball(cx, cy, 140, 62, cols=MITO, stroke=MITO[2], sw=2.4, shadow=0.15, gloss=0.25))
            N.add('<ellipse cx="%d" cy="%d" rx="130" ry="53" fill="#ffe9d9" stroke="%s" stroke-width="2"/>' % (cx, cy, CRISTA))
            for k in range(11):
                xx = cx - 112 + k * 22.4
                side = 1 if k % 2 else -1
                h = 53 * math.sqrt(max(0, 1 - ((xx - cx) / 130) ** 2))
                dd = 'M%.1f,%.1f c-7,%.1f 7,%.1f 0,%.1f' % (xx, cy + side * h, -side * h * 0.4, -side * h * 0.8, -side * h * 1.1)
                N.add('<path d="%s" fill="none" stroke="%s" stroke-width="6" stroke-linecap="round"/><path d="%s" fill="none" stroke="#ffd9bf" stroke-width="2.6" stroke-linecap="round"/>' % (dd, CRISTA, dd))
            N.add('<path d="M%d,%d c6,-8 14,-2 10,6 c-3,6 -12,4 -10,-6" fill="none" stroke="#7a3a1c" stroke-width="1.4"/>' % (cx + 40, cy + 10))
            for k in range(14):
                N.add('<circle cx="%.1f" cy="%.1f" r="1.6" fill="#8a4a2a" opacity="0.6"/>' % (cx - 90 + (k * 37) % 180, cy - 20 + (k * 23) % 40))
            b.append(L(cx - 120, cy - 52, x + 40, y + 46, 'ink', 0.9))
            b.append(T(x + 14, y + 44, 'outer membrane', 11.5, 600))
            b.append(L(cx + 18, cy - 30, x + 250, y + 44, 'ink', 0.9))
            b.append(T(x + 252, y + 44, 'crista', 11.5, 600))
            b.append(L(cx + 52, cy + 12, x + 300, y + 192, 'ink', 0.9))
            b.append(T(x + 238, y + 198, 'DNA ring', 11.5, 600))
        elif i == 2:
            N.add('<rect x="%d" y="%d" width="316" height="62" fill="%s"/>' % (x + 14, cy + 6, N.linear(NUC[0], NUC[1])))
            for k in range(26):
                N.add('<path d="M%d,%d q6,-8 12,0 t12,2" fill="none" stroke="%s" stroke-width="1.3" opacity="0.4"/>' % (x + 24 + (k * 47) % 280, cy + 22 + (k * 17) % 40, HETERO))
            for yy, col in ((cy - 6, NUC[2]), (cy + 6, NUC[2])):
                N.add('<path d="M%d,%d H%d M%d,%d H%d" stroke="%s" stroke-width="3"/>' % (x + 14, yy, cx - 22, cx + 22, yy, x + 330, col))
            N.add('<path d="M%d,%d H%d" stroke="%s" stroke-width="3"/>' % (x + 14, cy - 34, x + 120, RER[2]))
            N.add('<path d="M%d,%d C%d,%d %d,%d %d,%d" fill="none" stroke="%s" stroke-width="3"/>' % (x + 120, cy - 34, x + 140, cy - 34, x + 140, cy - 6, x + 120, cy - 6, RER[2]))
            for k in range(8):
                N.add('<circle cx="%d" cy="%d" r="2.4" fill="%s"/>' % (x + 22 + k * 13, cy - 40, RIBO))
            for s in (-1, 1):
                N.add('<rect x="%d" y="%d" width="12" height="26" rx="4" fill="#b9a3d6" stroke="#5a4a8a" stroke-width="1"/>' % (cx + s * 22 - 6, cy - 13))
            N.add('<path d="M%d,%d l10,22 l-20,0 z" fill="none" stroke="#5a4a8a" stroke-width="1" opacity="0.7"/>' % (cx, cy + 12))
            N.add('<path d="M%d,%d C%d,%d %d,%d %d,%d" fill="none" stroke="#d9475d" stroke-width="2.2" stroke-linecap="round"/>' % (cx - 6, cy + 30, cx, cy + 10, cx + 4, cy - 20, cx + 30, cy - 46))
            b += [T(x + 14, y + 44, 'cytoplasm', 11.5, 400, 'muted'), T(x + 14, y + 196, 'nucleus', 11.5, 400, 'muted')]
            b.append(L(cx + 30, cy - 46, x + 260, y + 50, 'ink', 0.9))
            b.append(T(x + 262, y + 48, 'mRNA out', 11.5, 600))
            b.append(L(cx + 22, cy, x + 268, cy + 2, 'ink', 0.9))
            b.append(T(x + 272, cy + 6, 'pore', 11.5, 600))
            b.append(L(x + 130, cy - 22, x + 150, y + 54, 'ink', 0.9))
            b.append(T(x + 152, y + 56, 'rough ER', 11.5, 600))
        else:
            for k in range(6):
                xx = x + 120 + k * 18
                h = 76 - abs(k - 2.5) * 8
                N.add(N.tube('M%d,%.1f Q%.1f,%d %d,%.1f' % (xx, cy - h, xx + 36, cy, xx, cy + h), GOLGI[2], GOLGI[1], 13, 9))
            for (vx, vy, rr) in ((x + 92, cy - 30, 7), (x + 80, cy + 10, 6), (x + 96, cy + 44, 6.5), (x + 262, cy - 46, 8), (x + 272, cy - 6, 7), (x + 286, cy + 36, 8), (x + 306, cy + 70, 6)):
                N.add(N.ball(vx, vy, rr, cols=VESICLE, stroke=VESICLE[2], sw=1.2, shadow=0.12, gloss=0.5))
            b.append(P('M%d %d H%d' % (x + 30, cy, x + 70), 'edge', 1.5))
            b.append('<path d="M%d %.1f L%d %d L%d %.1f Z" fill="var(--edge)"/>' % (x + 70, cy - 3.5, x + 76, cy, x + 70, cy + 3.5))
            b.append(P('M%d %d H%d' % (x + 296, cy - 10, x + 330), 'edge', 1.5))
            b.append('<path d="M%d %.1f L%d %d L%d %.1f Z" fill="var(--edge)"/>' % (x + 330, cy - 13.5, x + 336, cy - 10, x + 330, cy - 6.5))
            b += [T(x + 18, cy - 12, 'from ER', 11.5, 600), T(x + 120, y + 44, 'cis', 11.5, 600), T(x + 214, y + 44, 'trans', 11.5, 600), T(x + 334, cy - 22, 'to membrane', 11.5, 600, 'ink', 'end')]
    b.insert(0, N.group(0, 0, 1))
    return svg(560, title, 'Four close-ups. Plasma membrane: a lipid bilayer about 7 nm thick, heads outside, tails inside, with a channel protein letting a molecule through. Mitochondrion: outer membrane, inner membrane folded into cristae, matrix with its own DNA ring. Nuclear pore: the double nuclear envelope, continuous with the rough ER, with a pore through which mRNA leaves. Golgi apparatus: vesicles from the ER enter at the cis face and leave from the trans face toward the membrane.', b, N.defs())


# ---------------------------------------------------------------- size scale
SIZES = [('Cell', 20e-6, '~20 µm'), ('Nucleus', 6e-6, '~6 µm'), ('Mitochondrion', 1e-6, '~1 µm wide'), ('Lysosome', 0.5e-6, '~0.5 µm'),
         ('Nuclear pore', 120e-9, '~120 nm'), ('Ribosome', 25e-9, '~25 nm'), ('Membrane', 7e-9, '~7 nm thick')]


def scale():
    title = 'From the cell to a ribosome, almost a thousand times smaller'
    X = lambda m: 170 + (math.log10(m) + 9) / 5 * 540
    b = [T(24, 62, 'SIZE, LOG SCALE: EACH STEP IS ×10', 11.5, 600, 'muted')]
    for i, (n, m, lab) in enumerate(SIZES):
        y = 88 + i * 30
        b.append(T(24, y + 4, n, 13, 600))
        b.append(L(X(1e-9), y, X(m), y, 'focus', 2))
        b.append(dot(X(m), y, 5, 'focus'))
        b.append(T(X(m) + 10, y + 4, lab, 11.5, 600))
    yb = 88 + len(SIZES) * 30
    b.append(L(X(1e-9), yb, X(1e-4), yb, 'edge', 1))
    for e, lab in ((-9, '1 nm'), (-8, '10 nm'), (-7, '100 nm'), (-6, '1 µm'), (-5, '10 µm'), (-4, '100 µm')):
        b.append(T(X(10 ** e), yb + 18, lab, 11.5, 400, 'muted', 'middle' if e < -4 else 'end'))
    b.append(T(24, yb + 50, 'typical values; cells and organelles vary widely in size', 11.5, 400, 'muted'))
    return svg(yb + 60, title, 'Typical sizes: cell about 20 micrometres, nucleus 6 µm, mitochondrion about 1 µm wide, lysosome 0.5 µm, nuclear pore 120 nm, ribosome 25 nm, membrane 7 nm thick.', b)
