"""Example: eight espresso drinks compared (researched; drawings to scale). Used by examples.py."""
import json, math, os, sys
K = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(K, '..', 'public', 'skill', 'runik'))
sys.path.insert(0, K)
from runik_object import Obj, rrect
from runik_svg import T, R, L, P, dot, circ

SHOT_MG = 63  # USDA: ~212 mg caffeine per 100 g of espresso, ~63 mg per 30 ml shot

# recipe in ml: e = espresso, m = steamed milk, f = foam, w = hot water, c = chocolate sauce
DRINKS = [
    dict(name='Espresso', vessel='demitasse', shots=1, r=dict(e=30)),
    dict(name='Macchiato', vessel='demitasse', shots=1, r=dict(e=30, f=15), dome=True),
    dict(name='Cortado', vessel='gibraltar', shots=2, r=dict(e=60, m=55, f=5)),
    dict(name='Flat white', vessel='fwcup', shots=2, r=dict(e=60, m=100, f=10), foam_mm=5),
    dict(name='Cappuccino', vessel='tulip', shots=2, r=dict(e=60, m=60, f=60), dome=True, foam_mm=20),
    dict(name='Latte', vessel='latteglass', shots=2, r=dict(e=60, m=180, f=15), foam_mm=10),
    dict(name='Americano', vessel='mug', shots=2, r=dict(e=60, w=120)),
    dict(name='Mocha', vessel='latteglass', shots=2, r=dict(c=20, e=60, m=140, f=20), foam_mm=10),
]
for d in DRINKS:
    d['ml'] = sum(d['r'].values())
    d['share'] = d['r']['e'] / d['ml']
DRINKS[1]['foam_mm'], DRINKS[2]['foam_mm'] = 10, 2

# vessel geometry in cm: inner bottom radius, inner top radius, inner height, wall, base thickness
VESSELS = dict(
    demitasse=dict(kind='ceramic', rb=2.0, rt=2.8, h=4.2, wall=0.45, base=0.5, saucer=True, handle=True, label='demitasse · ~75 ml'),
    gibraltar=dict(kind='glass', rb=2.7, rt=3.4, h=4.4, wall=0.3, base=1.5, label='Gibraltar glass · ~130 ml'),
    fwcup=dict(kind='ceramic', rb=2.6, rt=4.2, h=4.8, wall=0.45, base=0.5, saucer=True, handle=True, label='cup · ~175 ml'),
    tulip=dict(kind='ceramic', rb=2.4, rt=4.4, h=5.2, wall=0.45, base=0.5, saucer=True, handle=True, label='tulip cup · ~195 ml'),
    latteglass=dict(kind='glass', rb=3.2, rt=3.8, h=7.6, wall=0.3, base=0.9, label='glass · ~290 ml'),
    mug=dict(kind='ceramic', rb=3.6, rt=4.0, h=5.8, wall=0.5, base=0.6, handle=True, label='mug · ~260 ml'),
)
COL = dict(e=('#6b3d22', '#3e2213'), m=('#f7ecdb', '#dccbb0'), f=('#fffdf8', '#e8dfd2'), w=('#a8703f', '#7a4a26'), c=('#5a321f', '#3a1e11'))
NAME = dict(e='espresso', m='steamed milk', f='foam', w='hot water', c='chocolate')
CERAMIC = ('#ffffff', '#dde1e7', '#98a0ab')
CREMA = ('#d9a465', '#b07a3e')


def lerp(a, b, t):
    pa, pb = [int(a[i:i + 2], 16) for i in (1, 3, 5)], [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return '#%02x%02x%02x' % tuple(round(x + (y - x) * t) for x, y in zip(pa, pb))


def liquid_colour(d):
    '''What the mixed drink actually looks like: espresso darkens the milk far more than its share.'''
    if 'w' in d['r']:
        return ('#7c4a27', '#55311a')
    t = 1 - (d['r']['e'] / (d['r']['e'] + d['r'].get('m', 0))) ** 0.8
    base = lerp('#4a2915', '#f0dcbc', t * 0.95)
    if 'c' in d['r']:
        base = lerp(base, '#4a2616', 0.35)
    return (lerp(base, '#ffffff', 0.1), lerp(base, '#3a2010', 0.15))


def level(V, rb, rt, h):
    '''Height (cm) a volume V (ml = cm³) fills in a frustum with bottom radius rb, top rt, height h.'''
    lo, hi = 0.0, h * 1.6
    for _ in range(40):
        y = (lo + hi) / 2
        r = rb + (rt - rb) * y / h
        v = math.pi * y / 3 * (rb * rb + rb * r + r * r)
        lo, hi = (y, hi) if v < V else (lo, y)
    return lo


def vessel(N, d, cx, base, S=15, saucer_k=1.32):
    v = VESSELS[d['vessel']]
    rb, rt, h, wall, bt = v['rb'] * S, v['rt'] * S, v['h'] * S, v['wall'] * S, v['base'] * S
    ib = base - bt                       # inner bottom (canvas y)
    top = ib - h
    r_at = lambda y: rb + (rt - rb) * (ib - y) / h
    outer = 'M%.1f,%.1f L%.1f,%.1f Q%.1f,%.1f %.1f,%.1f H%.1f Q%.1f,%.1f %.1f,%.1f L%.1f,%.1f Z' % (
        cx - rt - wall, top, cx - rb - wall, base - 5, cx - rb - wall, base, cx - rb - wall + 5, base,
        cx + rb + wall - 5, cx + rb + wall, base, cx + rb + wall, base - 5, cx + rt + wall, top)
    cavity = 'M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f Q%.1f,%.1f %.1f,%.1f H%.1f Q%.1f,%.1f %.1f,%.1f L%.1f,%.1f L%.1f,%.1f Z' % (
        cx - rt, top - 40, cx - rt, top, cx - rb, ib - 3, cx - rb, ib, cx - rb + 4, ib, cx + rb - 4, cx + rb, ib, cx + rb, ib - 3,
        cx + rt, top, cx + rt, top - 40)
    glass = v['kind'] == 'glass'
    if v.get('saucer'):
        sw = (rt + wall) * saucer_k
        N.add(N.shadow(rrect(cx - sw, base - 2, sw * 2, 7, 3), 2, 4, 3, 0.18))
        N.add('<path d="M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f Q%.1f,%.1f %.1f,%.1f Z" fill="%s" stroke="%s" stroke-width="1.2"/>' % (
            cx - sw, base - 1, cx, base - 6, cx + sw, base - 1, cx, base + 8, cx - sw, base - 1, N.linear(CERAMIC[0], CERAMIC[1]), CERAMIC[2]))
    elif v['kind'] == 'ceramic' or v['kind'] == 'glass':
        N.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="3" fill="#2b1c0e" opacity="0.18" filter="%s"/>' % (cx + 3, base + 1, rb + wall + 4, N.blur(3)))
    if v.get('handle'):
        hy = top + h * 0.28
        ex = cx + r_at(hy) + wall - 2
        hs = 0.22 * h + 8
        hd = 'M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f' % (ex, hy, ex + hs, hy - 6, ex + hs + 2, hy + hs * 1.3, ex - 4, hy + hs * 1.25)
        N.add(N.tube(hd, CERAMIC[2], CERAMIC[0], wall * 1.25 + 2, wall * 1.25 - 1))
    if glass:
        N.add('<path d="%s" fill="%s" fill-opacity="0.55" stroke="%s" stroke-width="1.4" stroke-linejoin="round"/>' % (outer, N.GLASS[0], N.GLASS[2]))
    else:
        N.add('<path d="%s" fill="%s" stroke="%s" stroke-width="1.4" stroke-linejoin="round"/>' % (outer, N.linear(CERAMIC[0], CERAMIC[1], 0, 0, 1, 0), CERAMIC[2]))
    clip = N.clip(cavity)
    # contents: the mixed drink, then its foam or crema; heights from real volumes
    foam = d['r'].get('f', 0)
    liquid = d['ml'] - foam
    yl = ib - level(liquid, v['rb'], v['rt'], v['h']) * S
    yf = ib - level(d['ml'], v['rb'], v['rt'], v['h']) * S
    lc = (COL['e'][0], COL['e'][1]) if d['name'] in ('Espresso', 'Macchiato') else liquid_colour(d)
    inner = '' if glass else '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>' % (cx - rt - 2, top - 2, 2 * rt + 4, ib - top + 4, N.linear('#f4f5f7', '#d5d9df', 0, 0, 1, 0))
    g = [inner, '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>' % (cx - rt - 2, yl, 2 * rt + 4, ib - yl + 2, N.linear(lc[0], lc[1]))]
    if 'c' in d['r']:
        yc = ib - level(d['r']['c'], v['rb'], v['rt'], v['h']) * S
        g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>' % (cx - rt - 2, yc, 2 * rt + 4, ib - yc + 2, N.linear(*COL['c'])))
        g.append('<path d="M%.1f,%.1f q%.1f,-5 %.1f,0 t%.1f,0" fill="none" stroke="%s" stroke-width="2" opacity="0.6"/>' % (cx - rt, yc, rt / 2, rt, rt, COL['c'][0]))
    if d['name'] in ('Espresso', 'Macchiato', 'Americano'):
        g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="4" fill="%s"/>' % (cx - rt - 2, yl - (0 if foam else 0), 2 * rt + 4, N.linear(*CREMA)))
    if foam:
        dome = d.get('dome')
        rr = r_at(yf)
        fd = 'M%.1f,%.1f L%.1f,%.1f %s L%.1f,%.1f Z' % (cx - rt - 2, yl + 1, cx - rr - 1, yf,
                                                     ('Q%.1f,%.1f %.1f,%.1f' % (cx, yf - (16 if d['name'] == 'Cappuccino' else 10) * S / 15, cx + rr + 1, yf)) if dome else 'L%.1f,%.1f' % (cx + rr + 1, yf),
                                                     cx + rt + 2, yl + 1)
        g.append('<path d="%s" fill="%s"/>' % (fd, N.linear(*COL['f'])))
        g.append('<path d="M%.1f,%.1f H%.1f" stroke="%s" stroke-width="1" opacity="0.6"/>' % (cx - rt, yl + 1, cx + rt, lc[1]))
    N.add('<g clip-path="%s">%s</g>' % (clip, ''.join(g)))
    if foam and d.get('dome'):  # the dome rises above the rim, outside the clip
        rr = r_at(yf)
        if yf - 16 < top:
            N.add('<path d="M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f Z" fill="%s" stroke="%s" stroke-width="0.8"/>' % (
                cx - rt + 1, top + 1, cx, top - (12 if d['name'] == 'Cappuccino' else 7) * S / 15, cx + rt - 1, top + 1, COL['f'][0], COL['f'][1]))
    if glass:
        N.add('<path d="M%.1f,%.1f L%.1f,%.1f" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity="0.75"/>' % (cx - rt + 5, top + 6, cx - rb + 4, base - 8))
        N.add('<path d="%s" fill="none" stroke="%s" stroke-width="1.4" stroke-linejoin="round"/>' % (outer, N.GLASS[2]))
    else:  # rim and cut edge
        N.add('<path d="M%.1f,%.1f H%.1f M%.1f,%.1f H%.1f" stroke="%s" stroke-width="1.6"/>' % (cx - rt - wall, top, cx - rt, cx + rt, top, cx + rt + wall, CERAMIC[2]))
        N.add('<path d="M%.1f,%.1f L%.1f,%.1f M%.1f,%.1f L%.1f,%.1f" stroke="%s" stroke-width="1"/>' % (cx - rt, top, cx - rb, ib, cx + rt, top, cx + rb, ib, CERAMIC[2]))
    return top


def svg(h, title, desc, body, defs=''):
    return ('<svg viewBox="0 0 760 %d" width="100%%" font-size="13" role="img" aria-label="%s"><title>%s</title><desc>%s</desc>%s%s%s</svg>'
            % (h, title, title, desc, '<defs>%s</defs>' % defs if defs else '', T(24, 30, title, 15, 600), ''.join(body)))


def comp_bar(x, y, w, d, hgt=10):
    out, xx = [], x
    for k in ('c', 'e', 'm', 'f', 'w'):
        if k in d['r']:
            ww = w * d['r'][k] / d['ml']
            out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%d" fill="%s" stroke="%s" stroke-width="0.8"/>' % (xx, y, ww, hgt, COL[k][0], COL[k][1]))
            xx += ww
    return ''.join(out)


def legend(x, y):
    out = []
    for k in ('e', 'm', 'f', 'w', 'c'):
        out.append('<rect x="%d" y="%d" width="16" height="16" rx="3" fill="%s" stroke="%s" stroke-width="1"/>' % (x, y - 12, COL[k][0], COL[k][1]))
        out.append(T(x + 22, y, NAME[k], 11.5, 400, 'muted'))
        x += 22 + len(NAME[k]) * 6.4 + 22
    return ''.join(out)


def overview():
    title = 'Eight espresso drinks, told apart by milk and water'
    N = Obj('k20261120-cof8')
    b = []
    for i, d in enumerate(DRINKS):
        col, row = i % 4, i // 4
        cx, base = 113 + col * 178, 200 + row * 250
        vessel(N, d, cx, base)
        b += [T(cx, base + 30, d['name'], 13, 600, 'ink', 'middle'),
              T(cx, base + 48, '~%d ml · %s' % (d['ml'], '1 shot' if d['shots'] == 1 else '2 shots'), 11.5, 400, 'ink', 'middle')]
        b.append(comp_bar(cx - 60, base + 58, 120, d))
    b.insert(0, N.group(0, 0, 1))
    b.append(legend(24, 540))
    b.append(P('M600 530 V536 H675 V530', 'ink', 1.25))
    b.append(T(682, 536, '5 cm', 11.5, 400, 'muted'))
    b.append(T(24, 568, 'cups and contents drawn to scale · bar = what is in the cup · common café recipes', 11.5, 400, 'muted'))
    return svg(578, title, 'Eight drinks drawn to scale in their usual cups, cut open to show the contents, each with a bar of its ingredients: ' +
               '; '.join('%s %d ml, %s' % (d['name'], d['ml'], ', '.join('%s %d' % (NAME[k], v) for k, v in d['r'].items())) for d in DRINKS), b, N.defs())


def caffeine():
    title = 'Six of the eight carry two shots, ~126 mg each'
    b = [T(24, 62, 'CAFFEINE PER DRINK, MG · BARS FROM 0', 11.5, 600, 'muted')]
    X = lambda mg: 180 + mg / 400 * 520
    ds = sorted(DRINKS, key=lambda d: (-d['shots'], DRINKS.index(d)))
    for i, d in enumerate(ds):
        y = 80 + i * 30
        mg = d['shots'] * SHOT_MG
        b.append(T(24, y + 12, d['name'], 13, 600))
        for s in range(d['shots']):
            b.append('<circle cx="%d" cy="%d" r="6" fill="%s" stroke="%s" stroke-width="1"/>' % (138 + s * 16, y + 8, COL['e'][0], COL['e'][1]))
        b.append('<rect x="180" y="%d" width="%.1f" height="16" rx="3" fill="var(--focus)" fill-opacity="0.3" stroke="var(--focus)" stroke-width="1.5"/>' % (y, X(mg) - 180))
        b.append(T(X(mg) + 8, y + 13, '~%d mg%s' % (mg, ' + a little from cocoa' if 'c' in d['r'] else ''), 11.5, 600))
    yb = 80 + 8 * 30
    b.append(L(X(400), 72, X(400), yb, 'ink', 1.25, '4 3'))
    b.append(T(X(400), 66, '400 mg a day', 11.5, 600, 'ink', 'end'))
    b.append(L(X(0), yb + 4, X(400), yb + 4, 'edge', 1))
    for mg in (0, 100, 200, 300, 400):
        b.append(T(X(mg), yb + 20, str(mg), 11.5, 400, 'muted', 'middle'))
    b.append('<circle cx="30" cy="%d" r="6" fill="%s" stroke="%s" stroke-width="1"/>' % (yb + 48, COL['e'][0], COL['e'][1]))
    b.append(T(42, yb + 52, 'one shot ≈ 63 mg', 11.5, 400, 'muted'))
    b.append(T(24, yb + 78, 'three double-shot drinks ≈ 380 mg · single-shot recipes halve these numbers', 11.5, 400, 'muted'))
    return svg(yb + 88, title, 'Caffeine: espresso and macchiato one shot, about 63 mg; cortado, flat white, cappuccino, latte, americano and mocha two shots, about 126 mg. The daily limit considered safe for adults is 400 mg.', b)




# ---------------------------------------------------------------- 1. side by side, cups to scale
def extent(d, S, k):
    v = VESSELS[d['vessel']]
    body = (v['rt'] + v['wall']) * S
    left = max(body, body * k if v.get('saucer') else 0)
    right = max(left, body + (0.22 * v['h'] * S + 8 + v['wall'] * S if v.get('handle') else 0))
    return left, right


def side_by_side():
    title = 'From a 30 ml espresso to a 255 ml latte'
    k = 1.12
    for S in [x / 4 for x in range(48, 30, -1)]:
        ws = [extent(d, S, k) for d in DRINKS]
        total = sum(l + r for l, r in ws) + 6 * (len(DRINKS) - 1)
        if total <= 712:
            break
    N = Obj('k20261120-cofrow')
    b = []
    x = 24 + (712 - total) / 2
    base = 176
    for d, (l, r) in zip(DRINKS, ws):
        cx = x + l
        vessel(N, d, cx, base, S, k)
        b += [T(cx, base + 26, d['name'], 12.5 if len(d['name']) > 9 else 13, 600, 'ink', 'middle'), T(cx, base + 43, '~%d ml' % d['ml'], 11.5, 400, 'ink', 'middle')]
        b.append(comp_bar(cx - 30, base + 51, 60, d, 8))
        x += l + r + 6
    b.insert(0, N.group(0, 0, 1))
    b.append(legend(24, 268))
    b.append(P('M%.1f 258 V264 H%.1f V258' % (736 - 5 * S, 736), 'ink', 1.25))
    b.append(T(736 - 5 * S - 6, 264, '5 cm', 11.5, 400, 'muted', 'end'))
    b.append(T(24, 294, 'cups and contents to scale, cut open · bar = what is in the cup', 11.5, 400, 'muted'))
    return svg(304, title, 'The eight drinks side by side in their usual cups, drawn to scale and cut open: ' +
               '; '.join('%s about %d ml in a %s' % (d['name'], d['ml'], VESSELS[d['vessel']]['label']) for d in DRINKS) + '.', b, N.defs())


# ---------------------------------------------------------------- 2. timeline
EVENTS = [  # (drink, [(year or (from, to), label, documented)], note)
    ('Espresso', [(1884, 'patent, Turin', True), (1906, 'by the cup, Milan fair', True)]),
    ('Cortado', [((1900, 1930), 'early 1900s, Spain', False)]),
    ('Mocha', [(1920, 'coffee + cocoa recipe', True)]),
    ('Americano', [(1928, 'in print', True), (1944, 'GI story', False)]),
    ('Cappuccino', [((1930, 1939), 'espresso version, Italy', True)]),
    ('Latte', [(1959, 'claimed, Berkeley', False)]),
    ('Macchiato', [((1980, 1989), 'named as a drink, Italy', False)]),
    ('Flat white', [(1983, 'in print, Sydney', True), (1989, 'Wellington claim', False)]),
]


def timeline():
    title = 'Espresso came first, the flat white last'
    X = lambda yr: 150 + (yr - 1880) / 120 * 576
    b = []
    y0 = 84
    yb = y0 + len(EVENTS) * 36
    b.append(L(X(1948), 58, X(1948), yb - 8, 'ink', 1.25, '4 3'))
    b.append(T(X(1948) + 6, 66, '1948 · lever machine: crema and firmer foam', 11.5, 600))
    for i, (name, evs) in enumerate(EVENTS):
        y = y0 + i * 36
        b.append(T(24, y + 4, name, 13, 600))
        b.append(L(150, y, 726, y, 'line', 1))
        if name == 'Cappuccino':
            b.append(P('M%.1f %d H156' % (X(1898), y), 'edge', 1.5, '3 3'))
            b.append('<path d="M156 %.1f L150 %d L156 %.1f Z" fill="var(--edge)"/>' % (y - 3.5, y, y + 3.5))
            b.append(T(164, y - 8, 'Kapuziner, Vienna, 1700s', 11.5, 400, 'muted'))
        if name == 'Mocha':
            b.append(T(164, y - 8, 'name: port of Mocha, Yemen', 11.5, 400, 'muted'))
        if name == 'Espresso':
            b.append(L(X(1884), y, X(1906), y, 'focus', 2))
        for yr, label, doc in evs:
            if isinstance(yr, tuple):
                b.append('<rect x="%.1f" y="%d" width="%.1f" height="10" rx="5" fill="var(--focus)" fill-opacity="0.25" stroke="var(--focus)" stroke-width="1.5"%s/>' % (
                    X(yr[0]), y - 5, X(yr[1]) - X(yr[0]), '' if doc else ' stroke-dasharray="3 2"'))
                lx = X(yr[1]) + 8
            else:
                b.append('<circle cx="%.1f" cy="%d" r="5.5" fill="%s" stroke="var(--focus)" stroke-width="2"/>' % (X(yr), y, 'var(--focus)' if doc else 'var(--surface)'))
                lx = X(yr) + 9
            right = lx + len(label) * 6.4 > 736
            tx = (X(yr[0]) if isinstance(yr, tuple) else X(yr)) - 9 if right else lx
            ty = y + 18 if name in ('Espresso', 'Americano') else y + 4
            if name == 'Flat white':
                tx, ty, right = (X(yr) - 9, y + 4, True) if yr == 1983 else (X(yr) + 6, y + 19, True)
            b.append(T(tx, ty, label, 11.5, 400, 'ink', 'end' if right else None))
    for yr in range(1880, 2001, 20):
        b.append(T(X(yr) + (6 if yr == 2000 else 0), yb + 4, str(yr), 11.5, 400, 'muted', 'end' if yr == 2000 else 'middle'))
    b.append('<circle cx="30" cy="%d" r="5.5" fill="var(--focus)" stroke="var(--focus)" stroke-width="2"/>' % (yb + 34))
    b.append(T(42, yb + 38, 'documented', 11.5, 400, 'muted'))
    b.append('<circle cx="140" cy="%d" r="5.5" fill="var(--surface)" stroke="var(--focus)" stroke-width="2"/>' % (yb + 34))
    b.append(T(152, yb + 38, 'claim or legend', 11.5, 400, 'muted'))
    b.append('<rect x="268" y="%d" width="26" height="10" rx="5" fill="var(--focus)" fill-opacity="0.25" stroke="var(--focus)" stroke-width="1.5"/>' % (yb + 29))
    b.append(T(300, yb + 38, 'only the period is known', 11.5, 400, 'muted'))
    return svg(yb + 54, title, 'First known appearances: espresso machine patent 1884 and espresso by the cup at the 1906 Milan fair; cortado in Spain in the early 1900s; a coffee and cocoa mocha recipe in 1920; americano in print in 1928 (the World War II story is a legend); the espresso cappuccino in Italy in the 1930s, after the Viennese Kapuziner; latte claimed in Berkeley in 1959; macchiato as a named drink in 1980s Italy; flat white in print in Sydney in 1983. Gaggia\'s 1948 lever machine brought crema and firmer foam.', b)


STORY = '''**Espresso, 1884–1906.** Angelo Moriondo patented a steam coffee machine in Turin in 1884, but never sold one. Luigi Bezzera and Desiderio Pavoni made a machine that brewed a single cup in seconds and showed it at the 1906 Milan fair: espresso, coffee made "expressly" for you. In 1948 Achille Gaggia's spring lever pushed water through at about 9 bar and gave espresso its crema.

**Cortado, early 1900s.** Spain, most likely the Basque Country. *Cortar* means "to cut": a little warm milk cuts the bitterness of the shot. It reached the US around 2000.

**Mocha, 1920.** The name comes from the Yemeni port of Mocha, from which Europe bought its coffee in the 1600s and 1700s. A recipe joining coffee, cocoa and milk under that name was printed in 1920; the espresso version with chocolate sauce is later.

**Americano, 1928.** The popular story says US soldiers in Italy watered down espresso during the Second World War, but the drink appears in a Somerset Maugham story published in 1928.

**Cappuccino, 1930s.** Vienna's Kapuziner, coffee with cream named after the brown habit of Capuchin friars, came first in the 1700s. The Italian espresso-and-milk cappuccino took shape in the 1930s, and the foam we know needed the post-1948 machines.

**Latte, 1959.** Lino Meiorin of Caffe Mediterraneum in Berkeley said he invented it for customers who found cappuccino too strong. Milky coffee at home is far older; the claim is about the café drink.

**Macchiato, 1980s.** "Stained" espresso: a spot of foam marks the cup so the waiter can tell it from a plain espresso. It became a named drink in 1980s Italy, though this is thinly documented.

**Flat white, 1983–1989.** A Sydney review mentions it in 1983 and Moors Espresso Bar put it on its menu in 1985; Wellington claims 1989. Australia and New Zealand still argue about it.'''


# ---------------------------------------------------------------- 3. world map
WORLD = None
PRODUCERS = {  # 2025/26, thousand 60 kg bags (USDA FAS, July 2026): arabica, robusta
    'Brazil': (38000, 25000), 'Vietnam': (1200, 30500), 'Indonesia': (1370, 11000), 'Colombia': (12500, 0), 'Ethiopia': (11560, 0),
    'Uganda': (1120, 5975), 'India': (1730, 4700), 'Honduras': (5530, 0), 'Peru': (4764, 0), 'Mexico': (3580, 500), 'Guatemala': (3025, 130),
    'Kenya': (850, 0), 'Nicaragua': (2400, 160), 'Costa Rica': (1160, 0), 'United Republic of Tanzania': (750, 700), 'Papua New Guinea': (800, 0),
}
WORLD_TOTAL = 178830


def world_map():
    global WORLD
    WORLD = WORLD or json.load(open(os.path.join(K, 'data', 'world.json'), encoding='utf-8'))
    title = 'Brazil grows over a third of the world’s coffee'
    s = 712 / (2 * 2.7064)
    top_lat = equal_y(84)
    X = lambda x: 24 + (x + 2.7064) * s
    Y = lambda y: 56 + (top_lat - y) * s
    b = []
    for name, c in WORLD['countries'].items():
        prod = name in PRODUCERS
        d = ' '.join('M' + ' L'.join('%.1f %.1f' % (X(px), Y(py)) for px, py in ring) + 'Z' for ring in c['rings'])
        b.append('<path d="%s" fill="var(--%s)" fill-opacity="%s" stroke="var(--edge)" stroke-width="0.5"/>' % (d, 'edge' if prod else 'tint', '0.35' if prod else '1'))
    for lat, lab in ((23.44, 'Tropic of Cancer'), (-23.44, 'Tropic of Capricorn')):
        yy = Y(equal_y(lat))
        b.append(L(24, yy, 736, yy, 'muted', 1, '5 4'))
        b.append(T(30, yy - 5, lab, 11.5, 400, 'muted'))
    hmap = Y(equal_y(-56))
    named = {'Brazil': (0, 1), 'Vietnam': (1, 0), 'Colombia': (-1, 0), 'Indonesia': (0, 1), 'Ethiopia': (1, 0), 'Uganda': (-1, 0), 'India': (-1, 0)}
    for name in sorted(PRODUCERS, key=lambda n: -sum(PRODUCERS[n])):
        a, r = PRODUCERS[name]
        tot = a + r
        cx, cy = WORLD['countries'][name]['label']
        cx, cy = X(cx), Y(cy)
        rad = 3.2 * math.sqrt(tot / 1000)
        b.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="var(--focus)" fill-opacity="0.55" stroke="var(--surface)" stroke-width="1.2"/>' % (cx, cy, rad))
        if r:
            f = r / tot
            if f > 0.999:
                b.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="var(--k2)" fill-opacity="0.75"/>' % (cx, cy, rad))
            else:
                ang = 2 * math.pi * f
                x1, y1 = cx, cy - rad
                x2, y2 = cx + rad * math.sin(ang), cy - rad * math.cos(ang)
                b.append('<path d="M%.1f %.1f L%.1f %.1f A%.1f %.1f 0 %d 1 %.1f %.1f Z" fill="var(--k2)" fill-opacity="0.75"/>' % (cx, cy, x1, y1, rad, rad, 1 if f > 0.5 else 0, x2, y2))
        b.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="var(--ink)" stroke-width="1"/>' % (cx, cy, rad))
        if name in named:
            dx, dy = named[name]
            share = '%d%%' % round(tot / WORLD_TOTAL * 100)
            if dy:
                b += [T(cx, cy + rad + 14, name, 11.5, 600, 'ink', 'middle'), T(cx, cy + rad + 28, share, 11.5, 400, 'ink', 'middle')]
            else:
                ax = cx + dx * (rad + 5)
                b += [T(ax, cy - 2, name, 11.5, 600, 'ink', 'end' if dx < 0 else None), T(ax, cy + 12, share, 11.5, 400, 'ink', 'end' if dx < 0 else None)]
    yx, yy = WORLD['countries']['Yemen']['label']
    b.append('<path d="M%.1f %.1f l4 -7 l4 7 z" fill="var(--ink)"/>' % (X(yx) - 4, Y(yy) + 3))
    b.append(T(X(yx) - 8, Y(yy) - 8, 'Mocha port', 11.5, 400, 'ink', 'end'))
    # world share bar
    yb = hmap + 30
    b.append(T(24, yb - 8, 'SHARE OF WORLD PRODUCTION, 2025/26', 11.5, 600, 'muted'))
    x = 24.0
    top5 = sorted(PRODUCERS, key=lambda n: -sum(PRODUCERS[n]))[:5]
    for name in top5 + ['Rest']:
        v = sum(PRODUCERS[name]) if name != 'Rest' else WORLD_TOTAL - sum(sum(PRODUCERS[n]) for n in top5)
        w = 712 * v / WORLD_TOTAL
        b.append('<rect x="%.1f" y="%.1f" width="%.1f" height="18" fill="var(--%s)" fill-opacity="%s" stroke="var(--surface)" stroke-width="1.5"/>' % (
            x, yb, w, 'focus' if name == 'Brazil' else 'edge', '0.45' if name == 'Brazil' else '0.25'))
        if w > 60:
            b.append(T(x + 6, yb + 13, '%s %d%%' % (name, round(v / WORLD_TOTAL * 100)), 11.5, 600))
        x += w
    yl = yb + 46
    b.append('<circle cx="32" cy="%.1f" r="7" fill="var(--focus)" fill-opacity="0.55" stroke="var(--ink)" stroke-width="1"/>' % (yl - 4))
    b.append(T(46, yl, 'arabica', 11.5, 400, 'muted'))
    b.append('<circle cx="122" cy="%.1f" r="7" fill="var(--k2)" fill-opacity="0.75" stroke="var(--ink)" stroke-width="1"/>' % (yl - 4))
    b.append(T(136, yl, 'robusta', 11.5, 400, 'muted'))
    b.append(T(206, yl, 'circle area = harvest · grey countries grow coffee', 11.5, 400, 'muted'))
    b.append(T(24, yl + 24, 'USDA FAS, July 2026 · Natural Earth, Equal Earth projection', 11.5, 400, 'muted'))
    return svg(yl + 34, title, 'World map of coffee-growing countries between the tropics, with circles sized by the 2025/26 harvest and split into arabica and robusta. Brazil 63.0 million 60 kg bags (35% of the world, both species), Vietnam 31.7 (18%, almost all robusta), Colombia 12.5 (7%, arabica), Indonesia 12.4 (7%, mostly robusta), Ethiopia 11.6 (6%, arabica), Uganda 7.1, India 6.4. Coffee was shipped to Europe from the port of Mocha in Yemen.', b)


def equal_y(lat):
    p = math.radians(lat)
    t = math.asin(math.sqrt(3) / 2 * math.sin(p))
    t2, t6 = t * t, t ** 6
    return t * (1.340264 - 0.081106 * t2 + t6 * (0.000893 + 0.003796 * t2))


# ---------------------------------------------------------------- 4. which beans go into which drink
ORIGINS = [('Brazil', 'arabica + robusta', 'nutty, chocolate, low acidity', (2, 2, 0, 2)),
           ('Colombia', 'arabica', 'balanced, caramel', (2, 2, 2, 0)),
           ('Guatemala', 'arabica', 'chocolate, spice', (2, 2, 0, 2)),
           ('Sumatra (Indonesia)', 'arabica', 'earthy, heavy body', (0, 2, 0, 2)),
           ('Vietnam', 'robusta', 'bitter, strong, thick crema', (2, 0, 0, 0)),
           ('Ethiopia', 'arabica', 'floral, fruity', (1, 0, 2, 0)),
           ('Kenya', 'arabica', 'bright, blackcurrant', (1, 0, 2, 0))]


def origins():
    title = 'Chocolatey beans carry milk, bright ones suit an americano'
    cols = [('ESPRESSO,', 'MACCHIATO'), ('MILK', 'DRINKS'), ('AMERICANO', ''), ('MOCHA', '')]
    xs = [452, 542, 632, 712]
    b = [T(24, 62, 'ORIGIN', 11.5, 600, 'muted'), T(210, 62, 'IN THE CUP', 11.5, 600, 'muted')]
    for (a, c), x in zip(cols, xs):
        b.append(T(x, 62, a, 11.5, 600, 'muted', 'middle'))
        if c:
            b.append(T(x, 76, c, 11.5, 600, 'muted', 'middle'))
    for i, (name, sp, flavor, use) in enumerate(ORIGINS):
        y = 106 + i * 42
        b += [T(24, y, name, 13, 600), T(24, y + 17, sp, 11.5, 400, 'muted'), T(210, y + 6, flavor, 11.5, 400)]
        for u, x in zip(use, xs):
            if u == 2:
                b.append(dot(x, y + 2, 7, 'focus'))
            elif u == 1:
                b.append(circ(x, y + 2, 6, 'focus', None, 0, 2))
        b.append(L(24, y + 26, 736, y + 26))
    yl = 106 + len(ORIGINS) * 42 + 8
    b.append(dot(30, yl - 4, 7, 'focus'))
    b.append(T(44, yl, 'common choice', 11.5, 400, 'muted'))
    b.append(circ(160, yl - 4, 6, 'focus', None, 0, 2))
    b.append(T(174, yl, 'as a single-origin shot', 11.5, 400, 'muted'))
    b.append(T(24, yl + 26, 'milk drinks: cortado, flat white, cappuccino, latte · usual café practice, not a rule', 11.5, 400, 'muted'))
    return svg(yl + 36, title, 'Origins and their usual drinks. Brazil (nutty, chocolate, low acidity): espresso, milk drinks, mocha. Colombia (balanced, caramel): espresso, milk drinks, americano. Guatemala (chocolate, spice): espresso, milk drinks, mocha. Sumatra (earthy, heavy body): milk drinks, mocha. Vietnam robusta (bitter, strong, crema): espresso blends. Ethiopia (floral, fruity) and Kenya (bright, blackcurrant): americano, and single-origin espresso.', b)


# ---------------------------------------------------------------- 5. arabica vs robusta
ROAST = ('#c99567', '#8a5631', '#4e2d16')


def bean(N, cx, cy, rx, ry, s_curve):
    N.add(N.ball(cx, cy, rx, ry, cols=ROAST, stroke=ROAST[2], sw=1.5, shadow=0.22, gloss=0.35))
    if s_curve:
        d = 'M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f' % (cx - rx * 0.75, cy + ry * 0.15, cx - rx * 0.2, cy - ry * 0.6, cx + rx * 0.2, cy + ry * 0.6, cx + rx * 0.75, cy - ry * 0.15)
    else:
        d = 'M%.1f,%.1f L%.1f,%.1f' % (cx - rx * 0.78, cy, cx + rx * 0.78, cy)
    N.add('<path d="%s" fill="none" stroke="%s" stroke-width="%.1f" stroke-linecap="round"/>' % (d, ROAST[2], ry * 0.16))


def species():
    title = 'Robusta has almost twice the caffeine of arabica'
    N = Obj('k20261120-beans')
    b = []
    cards = [('Arabica', 'Coffea arabica', 'sweeter, more acidity', 'focus', True), ('Robusta', 'Coffea canephora', 'bitter, earthy, more crema', 'k2', False)]
    for i, (n, latin, taste, c, s_curve) in enumerate(cards):
        x = 24 + i * 368
        b.append(R(x, 52, 344, 110, c, 2, c, 0.08))
        bean(N, x + 62, 104, 34 if s_curve else 30, 22 if s_curve else 25, s_curve)
        b += [T(x + 118, 88, n, 13, 600), T(x + 118, 106, latin, 11.5, 400, 'muted'), T(x + 118, 132, taste, 11.5)]
    b.insert(0, N.group(0, 0, 1))
    rows = [('Caffeine', '% of bean weight', 3.0, [(1.2, 1.5), (2.2, 2.7)], lambda v: '%g%%' % v),
            ('Altitude', 'metres', 2200, [(600, 2000), (0, 800)], lambda v: '{:,}'.format(int(v)))]
    for j, (name, unit, mx, rngs, fmt) in enumerate(rows):
        y = 200 + j * 74
        b += [T(24, y, name, 13, 600), T(24, y + 18, unit, 11.5, 400, 'muted')]
        X = lambda v: 170 + v / mx * 540
        b.append(L(X(0), y + 34, X(mx), y + 34, 'edge', 1))
        for v in (0, mx / 2, mx):
            b.append(T(X(v), y + 50, fmt(v), 11.5, 400, 'muted', 'middle'))
        for (lo, hi), c, dy in zip(rngs, ('focus', 'k2'), (8, 24)):
            b.append('<rect x="%.1f" y="%d" width="%.1f" height="10" rx="5" fill="var(--%s)" fill-opacity="0.35" stroke="var(--%s)" stroke-width="1.5"/>' % (X(lo), y + dy - 10, X(hi) - X(lo), c, c))
            b.append(T(X(hi) + 8, y + dy - 1, '%s–%s' % (fmt(lo), fmt(hi)), 11.5, 600))
    y = 360
    b += [T(24, y, 'World harvest', 13, 600), T(24, y + 18, '2025/26', 11.5, 400, 'muted')]
    fa = 94440 / WORLD_TOTAL
    b.append('<rect x="170" y="%d" width="%.1f" height="18" fill="var(--focus)" fill-opacity="0.35" stroke="var(--focus)" stroke-width="1.5"/>' % (y - 8, 540 * fa))
    b.append('<rect x="%.1f" y="%d" width="%.1f" height="18" fill="var(--k2)" fill-opacity="0.35" stroke="var(--k2)" stroke-width="1.5"/>' % (170 + 540 * fa, y - 8, 540 * (1 - fa)))
    b += [T(178, y + 6, 'arabica %d%%' % round(fa * 100), 11.5, 600), T(170 + 540 * fa + 8, y + 6, 'robusta %d%%' % round(100 - fa * 100), 11.5, 600)]
    b.append(T(24, 404, 'arabica: S-shaped crease, oval · robusta: straight crease, round · ranges from published tables', 11.5, 400, 'muted'))
    return svg(414, title, 'Arabica: sweeter with more acidity, 1.2 to 1.5% caffeine, grown at 600 to 2,000 m, 53% of the 2025/26 world harvest. Robusta: bitter and earthy with more crema, 2.2 to 2.7% caffeine, grown at 0 to 800 m, 47% of the harvest.', b, N.defs())


# ---------------------------------------------------------------- the example
PROMPT = ('Coffee. First, a side-by-side visual comparison of espresso, macchiato, cortado, flat white, cappuccino, latte, americano and mocha, '
          'showing what is in each one and the shape and size of its cup. Then a chronological story, starting with espresso: when each of the eight was first made. '
          'Then where coffee beans are grown, on a world map: what each origin is like, and which drink it is used in. '
          'Research all of this and more, then build the document.')
LINE = 'Espresso came first in 1906 and the flat white last in the 1980s; Brazil grows over a third of the beans.'


def example():
    sbs = side_by_side()
    rows = [[d['name'], VESSELS[d['vessel']]['label'], str(d['shots']),
             ' · '.join('%s %d ml' % (NAME[k], v) for k, v in d['r'].items()), '~%d ml' % d['ml']] for d in DRINKS]
    disagree = [['Macchiato', 'a spoon of foam on a single shot', 'espresso with a splash of milk, up to 2:1'],
                ['Cappuccino size', 'equal thirds, ~150 ml (classic)', 'about 1:4 coffee to milk, 180 ml or more (specialty cafés)'],
                ['Shots per drink', 'one shot (Italy, many chains)', 'two shots (most specialty cafés, used here)'],
                ['Americano', 'US soldiers in WWII Italy', 'already in print in 1928 (Maugham)'],
                ['Latte', 'invented in Berkeley, 1959', 'milky coffee is far older; only the café drink is claimed'],
                ['Flat white', 'Sydney, 1983–85', 'Wellington, 1989'],
                ['Arabica share', '53% of the 2025/26 harvest (USDA)', '60–70% (often quoted)']]
    sources = ('- Smithsonian Magazine, *The long history of the espresso machine*: Moriondo 1884, Bezzera and Pavoni, 1906 Milan fair, Gaggia 1948.\n'
               '- Britannica and Wikipedia, *Cappuccino*: the Viennese Kapuziner in the 18th century.\n'
               '- Barista Magazine, *Tiny drink, big influence: the history of the cortado*.\n'
               '- Wikipedia, *Caffè mocha*: 1920 recipe; Smithsonian, *Your mocha is named after the birthplace of the coffee trade*.\n'
               '- The Irish Times, *What\'s so American about an americano?*: the 1928 Maugham reference.\n'
               '- Caffe Mediterraneum and Wikipedia, *Latte*: Lino Meiorin\'s 1959 claim.\n'
               '- Wikipedia, *Caffè macchiato*.\n'
               '- University of Newcastle and Wikipedia, *Flat white*: 1983 review, Moors Espresso Bar 1985, Wellington 1989.\n'
               '- USDA Foreign Agricultural Service, *Coffee: World Markets and Trade*, July 2026: production by country and species, 2025/26.\n'
               '- Compound Interest, *Arabica vs robusta* (2023); Lavazza: caffeine and altitude ranges.\n'
               '- Breville, Seattle Coffee Gear, Complete Home Barista: origin flavour profiles and their use in espresso and milk drinks.\n'
               '- Istituto Nazionale Espresso Italiano (via Wikipedia, *Espresso*); USDA FoodData Central: ~63 mg caffeine per shot; EFSA (2015): 400 mg a day.\n'
               '- Natural Earth 1:110m countries (public domain).')
    pdf = dict(title='Coffee: eight drinks, their history and their beans', subtitle='A researched comparison of espresso drinks, when each appeared, and where the beans come from', cards=[
        dict(type='drawing', title='', data=[sbs]),
        dict(type='table', title='Recipes and cups', data=dict(columns=['Drink', 'Cup', 'Shots', 'In the cup', 'Total'], rows=rows)),
        dict(type='drawing', title='', data=[timeline()]),
        dict(type='markdown', title='The story, in order', data=STORY),
        dict(type='drawing', title='', data=[world_map()]),
        dict(type='drawing', title='', data=[origins()]),
        dict(type='drawing', title='', data=[species()]),
        dict(type='drawing', title='', data=[caffeine()]),
        dict(type='table', title='Where the sources disagree', data=dict(columns=['Topic', 'One reading', 'Another reading'], rows=disagree)),
        dict(type='markdown', title='Sources', data=sources)])
    return dict(slug='coffee', kind='Research', title='Coffee: eight drinks, their history and their beans', prompt=PROMPT, question=PROMPT, line=LINE,
                chat=[sbs], pdf=pdf, drawings=[c['data'][0] for c in pdf['cards'] if c['type'] == 'drawing'])
