"""Example: eight espresso drinks compared (researched; drawings to scale). Used by examples.py."""
import math, os, sys
K = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(K, '..', 'public', 'skill', 'runik'))
sys.path.insert(0, K)
from runik_object import Obj, rrect
from runik_svg import T, R, L, P, dot

PROMPT = ('Compare eight espresso drinks: espresso, macchiato, cortado, flat white, cappuccino, latte, americano and mocha. '
          'For each one show what is in the cup and in what proportions, how much caffeine it has, and how the milk is textured. '
          'Base it on café standards and published sources, and point out where the definitions disagree. Give it to me as a PDF.')
LINE = 'Most of them are the same double espresso; the amount of milk, foam or water on top is what changes the drink.'
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


def vessel(N, d, cx, base, S=15):
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
        sw = (rt + wall) * 1.32
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
                                                     ('Q%.1f,%.1f %.1f,%.1f' % (cx, yf - (16 if d['name'] == 'Cappuccino' else 10), cx + rr + 1, yf)) if dome else 'L%.1f,%.1f' % (cx + rr + 1, yf),
                                                     cx + rt + 2, yl + 1)
        g.append('<path d="%s" fill="%s"/>' % (fd, N.linear(*COL['f'])))
        g.append('<path d="M%.1f,%.1f H%.1f" stroke="%s" stroke-width="1" opacity="0.6"/>' % (cx - rt, yl + 1, cx + rt, lc[1]))
    N.add('<g clip-path="%s">%s</g>' % (clip, ''.join(g)))
    if foam and d.get('dome'):  # the dome rises above the rim, outside the clip
        rr = r_at(yf)
        if yf - 16 < top:
            N.add('<path d="M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f Z" fill="%s" stroke="%s" stroke-width="0.8"/>' % (
                cx - rt + 1, top + 1, cx, top - (12 if d['name'] == 'Cappuccino' else 7), cx + rt - 1, top + 1, COL['f'][0], COL['f'][1]))
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


def composition():
    title = 'A cortado is half coffee, a latte under a quarter'
    ds = sorted(DRINKS, key=lambda d: -d['share'])
    b = [T(24, 62, 'WHAT IS IN THE CUP, SHARE OF VOLUME', 11.5, 600, 'muted')]
    for i, d in enumerate(ds):
        y = 80 + i * 32
        b += [T(24, y + 14, d['name'], 13, 600)]
        b.append(comp_bar(140, y + 2, 460, d, 16))
        b.append(T(612, y + 14, '%d%% coffee' % round(d['share'] * 100), 11.5, 600))
        b.append(T(736, y + 14, '~%d ml' % d['ml'], 11.5, 400, 'muted', 'end'))
    b.append(legend(24, 348))
    b.append(T(24, 376, 'americano: the same share of coffee as a cappuccino, but diluted with water, not milk', 11.5, 400, 'muted'))
    return svg(386, title, 'Share of espresso in each drink: ' + ', '.join('%s %d%%' % (d['name'], round(d['share'] * 100)) for d in ds) + '.', b)


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


def foam():
    title = 'Foam: about 5 mm on a flat white, 20 on a cappuccino'
    ds = sorted([d for d in DRINKS if 'f' in d['r']], key=lambda d: d['foam_mm'])
    b = [T(24, 62, 'TOP 30 MM OF THE DRINK, TO SCALE', 11.5, 600, 'muted')]
    mm = 4.0
    for i, d in enumerate(ds):
        x, y0, w, hh = 24 + i * 120, 76, 104, 120
        lc = (COL['e'][0], COL['e'][1]) if d['name'] == 'Macchiato' else liquid_colour(d)
        fh = d['foam_mm'] * mm
        b.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x, y0 + 12, w, hh - 12, lc[0]))
        b.append('<rect x="%d" y="%.1f" width="%d" height="%.1f" fill="%s"/>' % (x, y0 + 12, w, fh, COL['f'][0]))
        micro = d['name'] != 'Cappuccino' and d['name'] != 'Macchiato'
        seed = i * 7 + 3
        for k in range(int(fh * (5 if micro else 1.6))):
            seed = (seed * 1103515245 + 12345) & 0x7fffffff
            bx = x + 2 + (seed % 1000) / 1000 * (w - 4)
            seed = (seed * 1103515245 + 12345) & 0x7fffffff
            by = y0 + 13 + (seed % 1000) / 1000 * max(fh - 2, 1)
            r = 0.7 if micro else 1.2 + (seed % 7) / 3
            b.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="%s" stroke-width="0.6" opacity="0.8"/>' % (bx, by, r, COL['f'][1]))
        b.append(R(x, y0, w, hh, 'edge', 1.25, rx=4))
        b.append(L(x, y0 + 12, x + w, y0 + 12, 'edge', 1, '3 3'))
        b += [T(x, y0 + hh + 22, d['name'], 13, 600), T(x, y0 + hh + 40, '~%d mm · %s' % (d['foam_mm'], 'microfoam' if micro else 'airy foam'), 11.5, 400, 'muted')]
    b.append(T(24, 266, 'dashed line = cup rim · sources give 5–15 mm for a flat white, 10–20 mm for a cappuccino', 11.5, 400, 'muted'))
    return svg(276, title, 'Foam depth to scale: ' + ', '.join('%s about %d mm' % (d['name'], d['foam_mm']) for d in ds) + '. Flat white, latte, mocha and cortado use fine microfoam; cappuccino and macchiato airy foam.', b)


def example():
    ov = overview()
    rows = [[d['name'], d['vessel'] and VESSELS[d['vessel']]['label'], str(d['shots']),
             ' · '.join('%s %d ml' % (NAME[k], v) for k, v in d['r'].items()), '~%d ml' % d['ml'], '~%d mg' % (d['shots'] * SHOT_MG)] for d in DRINKS]
    disagree = [['Macchiato', 'a spoon of foam on a single shot', 'espresso with a splash of milk, up to 2:1'],
                ['Cappuccino', 'equal thirds, ~150 ml (classic)', 'about 1:4 coffee to milk, 180 ml or more (specialty cafés)'],
                ['Flat white', 'microfoam layer under 5 mm', 'up to 15 mm; some use a 1:2 ratio, others 1:1'],
                ['Cortado', 'single shot, ~60 ml', 'double shot, 120–150 ml'],
                ['Shots per drink', 'one shot (Italy, many chains)', 'two shots (most specialty cafés, used here)']]
    sources = ('- Istituto Nazionale Espresso Italiano: certified espresso is 7 ± 0.5 g of coffee, 25 ± 2.5 ml in the cup (via the Wikipedia article *Espresso*).\n'
               '- USDA FoodData Central: about 212 mg caffeine per 100 g of espresso, ~63 mg per 30 ml shot.\n'
               '- European Food Safety Authority (2015): up to 400 mg of caffeine a day is safe for healthy adults.\n'
               '- Arla Barista, *Flat white vs latte vs cappuccino*: flat white foam 0.5–1.5 cm, lower end preferred.\n'
               '- Complete Home Barista, *Milk texture by drink*: cappuccino foam 1–2 cm, latte about 1 cm.\n'
               '- Trade Coffee, *The complete glossary of espresso and milk drinks*; Seattle Coffee Gear, *Espresso drinks guide*: cortado 1:1, macchiato definitions.')
    pdf = dict(title='Eight espresso drinks compared', subtitle='Recipes, caffeine and milk texture, from café standards and published sources', cards=[
        dict(type='drawing', title='', data=[ov]),
        dict(type='drawing', title='', data=[composition()]),
        dict(type='table', title='Recipes used on these pages', data=dict(columns=['Drink', 'Cup', 'Shots', 'In the cup', 'Total', 'Caffeine'], rows=rows)),
        dict(type='drawing', title='', data=[caffeine()]),
        dict(type='drawing', title='', data=[foam()]),
        dict(type='table', title='Where the definitions disagree', data=dict(columns=['Drink', 'One reading', 'Another reading'], rows=disagree)),
        dict(type='markdown', title='Sources', data=sources)])
    return dict(slug='coffee', kind='Comparison', title='Eight espresso drinks compared', prompt=PROMPT, question=PROMPT, line=LINE,
                chat=[ov], pdf=pdf, drawings=[ov] + [c['data'][0] for c in pdf['cards'][1:] if c['type'] == 'drawing'])
