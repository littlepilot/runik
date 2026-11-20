"""Builds the site's examples: for each one, the chat drawing (what the agent shows in the conversation) and a
Runik PDF (the same answer as a document). Writes scripts/examples.json (used by page.py) and
public/examples/<slug>.pdf + <slug>.png (first page preview).

Usage: python3 scripts/examples.py [--no-pdf]   (part of npm run examples)"""
import json, math, os, shutil, subprocess, sys
K = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(K, '..')
SK = os.path.join(ROOT, 'public', 'skill', 'runik')
sys.path.insert(0, SK)
sys.path.insert(0, K)
from runik_object import Obj, rrect, smooth, blob
from runik_svg import T, R, L, arrow, varrow, circ, dot, P, check, cross, chev


def sv(h, title, desc, body, defs=''):
    return ('<svg viewBox="0 0 760 %d" width="100%%" font-size="13" role="img" aria-label="%s"><title>%s</title><desc>%s</desc>%s%s%s</svg>'
            % (h, title, title, desc, '<defs>%s</defs>' % defs if defs else '', T(24, 30, title, 15, 600), ''.join(body)))


def rating(x, y, n, c='focus'):
    return ''.join(circ(x + i * 14, y, 5, c, c if i < n else None, 1 if i < n else 0, 1.25) for i in range(5))


def hbar(x, y, w, c, h=14):
    return '<rect x="%.1f" y="%d" width="%.1f" height="%d" rx="3" fill="var(--%s)" fill-opacity="0.3" stroke="var(--%s)" stroke-width="1.5"/>' % (x, y, max(w, 2), h, c, c)


def legend(x, y, items):
    out = []
    for kind, c, label in items:
        if kind == 'arrow':
            out.append(arrow(x, y - 4, x + 18, c, 2))
        elif kind == 'dot':
            out.append(dot(x + 8, y - 4, 6, c))
        elif kind == 'box':
            out.append(R(x, y - 12, 16, 16, c, 1.5, c, 0.25, rx=3))
        out.append(T(x + 24, y, label, 11.5, 400, 'muted'))
        x += 24 + len(label) * 6.4 + 22
    return ''.join(out)


EX = []

# =========================================================== 1. laptop on a blanket (object drawing)
FABRIC = ('#e3e8f2', '#b9c3d6', '#7f8ba3')


def laptop_side(N, ox, oy, blanket):
    '''Side view of a laptop: base, open lid, rubber feet; on a desk or sunk into a blanket.'''
    if not blanket:
        N.add(N.slab(ox - 50, oy + 26, 380, 16, N.WOOD, r=4, depth=10, shadow=0.2))
    N.add(N.shadow(rrect(ox, oy, 260, 20, 6), 3, 4, 3, 0.2))
    N.add('<path d="M%d,%d L%d,%d L%d,%d L%d,%d Z" fill="%s" stroke="%s" stroke-width="1.5" stroke-linejoin="round"/>' % (
        ox + 244, oy + 2, ox + 300, oy - 128, ox + 309, oy - 125, ox + 256, oy + 4, N.linear(*N.METAL[1:], 0, 0, 1, 0), N.METAL[2]))
    N.add('<path d="%s" fill="%s" stroke="%s" stroke-width="1.5"/>' % (rrect(ox, oy, 260, 20, 6), N.linear(N.METAL[0], N.METAL[1]), N.METAL[2]))
    for k in range(9):
        N.add('<rect x="%d" y="%d" width="16" height="3" rx="1" fill="%s"/>' % (ox + 40 + k * 20, oy - 2, N.DARK[1]))
    for fx in (24, 220):
        N.add('<rect x="%d" y="%d" width="18" height="7" rx="3" fill="%s"/>' % (ox + fx, oy + 20, N.DARK[2]))
    for k in range(6):
        N.add('<rect x="%d" y="%d" width="3" height="10" rx="1" fill="%s"/>' % (ox + 92 + k * 9, oy + 6, N.DARK[1]))
    N.mark('intake', ox + 115, oy + 24)
    N.mark('out', ox + 262, oy + 10)
    N.mark('top', ox + 130, oy - 4)
    if blanket:
        pts = [(ox - 60, oy + 50), (ox - 50, oy + 14), (ox - 10, oy + 22), (ox + 40, oy + 12), (ox + 110, oy + 21), (ox + 170, oy + 11),
               (ox + 230, oy + 22), (ox + 290, oy + 13), (ox + 330, oy + 24), (ox + 340, oy + 50)]
        d = smooth(pts, closed=True, t=0.35)
        N.add(N.shadow(d, 2, 4, 4, 0.15))
        N.add('<path d="%s" fill="%s" stroke="%s" stroke-width="1.5"/>' % (d, N.linear(FABRIC[0], FABRIC[1]), FABRIC[2]))
        for k in range(5):
            N.add('<path d="M%d,%d q12,8 26,2" fill="none" stroke="%s" stroke-width="1.2" opacity="0.7"/>' % (ox - 20 + k * 70, oy + 34, FABRIC[2]))


def laptop_main():
    title = 'On a blanket, your laptop can’t breathe'
    b, defs = [], ''
    rows = [('desk', 'On a desk', 'feet lift it', 70, 'good', '✓ full speed', False),
            ('blanket', 'On a blanket', 'vents covered', 95, 'bad', '✗ slows down', True)]
    for i, (key, name, detail, temp, c, status, blanket) in enumerate(rows):
        y0 = 70 + i * 170
        N = Obj('k20261120-lap-' + key)
        laptop_side(N, 0, 140, blanket)
        b.append(N.group(170, y0 - 40, 0.78))
        defs += N.defs()
        b += [T(24, y0 + 54, name, 13, 600), T(24, y0 + 72, detail, 11.5, 400, 'muted')]
        ix, iy = N.at('intake')
        ox, oy = N.at('out')
        tx, ty = N.at('top')
        if blanket:
            b.append(cross(ix - 4, iy + 2))
            for k in range(3):
                b.append(P('M%.1f %.1f q5 -6 0 -12 q-5 -6 0 -12' % (tx - 30 + k * 30, ty - 8), 'bad', 2))
        else:
            b.append(P('M%.1f %.1f H%.1f' % (ix - 120, iy + 2, ix - 6), 'good', 2))
            b.append('<path d="M%.1f %.1f l-6 -3.5 v7 z" fill="var(--good)"/>' % (ix, iy + 2))
            b.append(P('M%.1f %.1f h36' % (ox + 6, oy), 'warn', 2))
            b.append('<path d="M%.1f %.1f l-6 -3.5 v7 z" fill="var(--warn)"/>' % (ox + 48, oy))
        # temperature bar: 0-100 °C over 200 px, throttle line at 95
        bx, by = 520, y0 + 44
        b.append(L(bx, by + 7, bx + 200, by + 7, 'line', 1))
        b.append(hbar(bx, by, temp * 2, c))
        b.append(T(bx, by - 8, 'CPU ~%d °C' % temp, 11.5, 600))
        b.append(T(bx, by + 34, status, 11.5, 600, c))
    b.append(L(710, 96, 710, 312, 'ink', 1.25, '3 3'))
    b.append(T(712, 88, '95 °C limit', 11.5, 600, 'ink', 'end'))
    b.append(L(24, 214, 736, 214))
    b.append(legend(24, 392, [('arrow', 'good', 'cool air in'), ('arrow', 'warn', 'warm air out'), ('arrow', 'bad', 'heat trapped')]))
    b.append(T(24, 416, 'simplified drawing · temperatures typical', 11.5, 400, 'muted'))
    return sv(426, title, 'Laptop side view. On a desk the rubber feet leave a gap: cool air enters underneath and warm air leaves at the back; CPU about 70 °C, full speed. On a blanket the fabric seals the bottom vents, heat stays inside; CPU about 95 °C, at the limit, so it slows down.', b, defs)


def laptop_fixes():
    title = 'Three fixes, all about the gap underneath'
    b = []
    cards = [('Hard surface', 'desk, tray, book', 'good'), ('Lap desk', 'a board on your knees', 'good'), ('Clean vents', 'dust blocks air too', 'focus')]
    for k, (n, d, c) in enumerate(cards):
        x = 24 + k * 244
        b.append(R(x, 52, 224, 150, 'edge', 1.25))
        b.append('<rect x="%d" y="52" width="224" height="6" rx="3" fill="var(--%s)"/>' % (x, c))
        cx = x + 112
        if k == 0:
            b += [R(cx - 60, 104, 120, 10, 'ink', 1.5, rx=3), R(cx - 70, 122, 140, 12, 'edge', 1.5, rx=3), varrow(cx - 30, 150, 126, 'good', 2), varrow(cx + 30, 150, 126, 'good', 2)]
        elif k == 1:
            b += [R(cx - 60, 98, 120, 10, 'ink', 1.5, rx=3), R(cx - 74, 116, 148, 8, 'edge', 1.5, rx=3),
                  P('M%d 130 q20 22 50 18 M%d 130 q-20 22 -50 18' % (cx - 50, cx + 50), 'edge', 1.5)]
        else:
            b += [R(cx - 50, 96, 100, 54, 'ink', 1.5, rx=4)] + [L(cx - 36 + i * 12, 106, cx - 36 + i * 12, 140, 'ink', 1.5) for i in range(7)]
            b += [dot(cx - 30, 120, 3, 'muted'), dot(cx + 12, 130, 3.5, 'muted'), dot(cx + 26, 112, 2.5, 'muted'), cross(cx + 56, 92, 'bad')]
        b += [T(x + 16, 176, n, 13, 600), T(x + 16, 194, d, 11.5, 400, 'muted')]
    b.append(R(24, 222, 712, 50, 'good', 2, 'good', 0.12))
    b += [T(40, 244, 'Keep the bottom open, the fan does the rest', 13, 600), T(40, 262, 'most laptops pull air in from below', 11.5)]
    return sv(282, title, 'Fixes: put the laptop on a hard surface, use a lap desk, clean dusty vents. Most laptops take air in from below.', b)


EX.append(dict(
    slug='laptop', kind='Object drawing', question='Why does my laptop get so hot on the bed?',
    line='It sits on its own air intake: the blanket seals the vents underneath.',
    chat=[laptop_main()],
    pdf=dict(title='On a blanket, your laptop can’t breathe', subtitle='Why laptops overheat on soft surfaces', cards=[
        dict(type='drawing', title='', data=[laptop_main()]),
        dict(type='drawing', title='', data=[laptop_fixes()]),
        dict(type='card', title='In short', data=dict(summary='Give the vents a gap and it stays at full speed', status='ok',
                                                     items=['Rubber feet lift it ~3 mm', 'Blankets and pillows close that gap', 'Hot CPUs slow down to protect themselves']))])))

# =========================================================== 2. noise-cancelling headphones (process panels)


def wave(x, y, w, amp, phase=0, c='ink', sw=2, dash=None, cycles=2.5):
    pts = ['%.1f %.1f' % (x + i * w / 60, y - amp * math.sin(phase + i / 60 * cycles * 2 * math.pi)) for i in range(61)]
    return P('M' + ' L'.join(pts), c, sw, dash)


def headphone(prefix):
    N = Obj(prefix)
    N.add(N.tube('M20,70 C20,0 120,0 120,70', N.DARK[2], N.DARK[1], 12, 6))
    N.add(N.ball(20, 82, 22, 28, cols=N.DARK, shadow=0.2, gloss=0.35))
    N.add(N.ball(120, 82, 22, 28, cols=N.DARK, shadow=0.2, gloss=0.35))
    N.add(N.ball(120, 98, 4, cols=N.METAL, shadow=0, gloss=0))
    N.mark('mic', 124, 102)
    return N


def anc_main():
    title = 'Headphones cancel noise by adding its mirror'
    b, defs = [], ''
    heads = ['1 · Noise arrives', '2 · Mirror is added', '3 · They cancel']
    for k, h in enumerate(heads):
        x = 24 + k * 244
        b.append(R(x, 52, 224, 190, 'edge', 1.25))
        b.append(T(x + 16, 76, h, 13, 600))
        if k < 2:
            b.append(chev(x + 234, 147))
    b.append(wave(40, 150, 192, 34, 0, 'ink'))
    b.append(T(40, 222, 'engine hum', 11.5, 400, 'muted'))
    b.append(wave(284, 150, 192, 34, 0, 'ink', 1.5))
    b.append(wave(284, 150, 192, 34, math.pi, 'focus', 2.5))
    N = headphone('k20261120-anc-hp')
    b.append(N.group(438, 58, 0.28))
    defs += N.defs()
    b.append(T(284, 222, 'mic hears · speaker flips', 11.5, 400, 'muted'))
    b.append(L(544, 150, 720, 150, 'good', 2.5))
    b.append(wave(544, 150, 176, 34, 0, 'line', 1, '3 3'))
    b.append(check(544, 196))
    b.append(T(562, 205, 'near silence', 11.5, 600, 'good'))
    b.append(T(544, 222, 'peak + valley = 0', 11.5, 400, 'muted'))
    b.append(legend(24, 268, [('arrow', 'ink', 'noise'), ('arrow', 'focus', 'mirror wave'), ('arrow', 'good', 'what you hear')]))
    return sv(280, title, 'Three panels. 1: a noise wave (engine hum) arrives. 2: the headphone microphone hears it and the speaker plays the same wave flipped upside down. 3: peaks meet valleys and add up to nearly zero, near silence.', b, defs)


def anc_where():
    title = 'Steady hums vanish, sudden sounds slip through'
    b = [T(24, 62, 'SOUND', 11.5, 600, 'muted'), T(300, 62, 'SHAPE', 11.5, 600, 'muted'), T(560, 62, 'HOW MUCH IS CANCELLED', 11.5, 600, 'muted')]
    rows = [('Plane engine', 'low, steady', 5, 'good', 'most'), ('Office chatter', 'mid, changing', 3, 'warn', 'some'), ('Door slam', 'sudden', 1, 'bad', 'little')]
    for i, (n, d, r, c, word) in enumerate(rows):
        y = 100 + i * 64
        b += [dot(30, y - 4, 6, c), T(46, y, n, 13, 600), T(46, y + 18, d, 11.5, 400, 'muted')]
        if i == 0:
            b.append(wave(300, y + 2, 200, 14, 0, 'ink', 1.5, cycles=3))
        elif i == 1:
            b.append(P('M300 %d ' % (y + 2) + ' '.join('L%d %d' % (300 + j * 10, y + 2 - (12 if j % 3 == 0 else -8 if j % 2 else 4)) for j in range(1, 21)), 'ink', 1.5))
        else:
            b.append(P('M300 %d H380 L386 %d L392 %d L398 %d H500' % (y + 2, y - 20, y + 22, y + 2), 'ink', 1.5))
        b.append(rating(566, y - 4, r, c))
        b.append(T(640, y, word, 11.5, 600, c))
        if i < 2:
            b.append(L(24, y + 34, 736, y + 34))
    b.append(R(24, 300, 712, 50, 'focus', 2, 'focus', 0.12))
    b += [T(40, 322, 'Best on planes, trains and fans', 13, 600), T(40, 340, 'the mirror needs a sound it can predict', 11.5)]
    b.append(legend(24, 376, [('dot', 'good', 'cancelled well'), ('dot', 'warn', 'partly'), ('dot', 'bad', 'barely')]))
    return sv(388, title, 'Plane engine: low and steady, cancelled the most (5 of 5). Office chatter: changing, partly (3 of 5). Door slam: sudden, barely (1 of 5). The mirror wave needs a predictable sound.', b)


EX.append(dict(
    slug='headphones', kind='Process panels', question='How do noise-cancelling headphones actually work?',
    line='They play the noise back upside down, so the two waves cancel out.',
    chat=[anc_main()],
    pdf=dict(title='Headphones cancel noise by adding its mirror', subtitle='How active noise cancelling works', cards=[
        dict(type='drawing', title='', data=[anc_main()]),
        dict(type='drawing', title='', data=[anc_where()]),
        dict(type='table', title='Inside the cup', data=dict(columns=['Part', 'Job'], rows=[
            ['Outer microphone', 'hears the noise before your ear does'], ['Chip', 'flips the wave in about a millisecond'], ['Speaker', 'plays music plus the mirror wave']]))])))

# =========================================================== 3. football-sized Sun (scale)
SUN_CM = 22.0
SCALE = SUN_CM / 100 / 1391000  # metres per km
PLANETS = [('Mercury', 4879, 57.9e6), ('Venus', 12104, 108.2e6), ('Earth', 12742, 149.6e6), ('Mars', 6779, 227.9e6),
           ('Jupiter', 139820, 778.5e6), ('Saturn', 116460, 1433e6), ('Uranus', 50724, 2872e6), ('Neptune', 49244, 4495e6)]
OBJECT = {'Mercury': 'poppy seed', 'Venus': 'peppercorn', 'Earth': 'peppercorn', 'Mars': 'mustard seed', 'Jupiter': 'grape',
          'Saturn': 'cherry', 'Uranus': 'pea', 'Neptune': 'pea'}


def solar_main():
    title = 'Football-sized Sun: Earth is a peppercorn 24 m away'
    b, defs = [], ''
    N = Obj('k20261120-sun')
    N.add(N.ball(80, 130, 52, cols=N.GOLD, shadow=0.18, gloss=0.4))
    N.add(N.ball(250, 134, 1.6, cols=N.WATER, shadow=0, gloss=0))
    N.add(N.ball(400, 134, 5.6, cols=('#f6e3c4', '#d9a86c', '#9c6b3a'), shadow=0, gloss=0.3))
    b.append(N.group(0, 0, 1))
    defs += N.defs()
    b += [T(80, 210, 'Sun', 13, 600, 'ink', 'middle'), T(80, 228, 'football · 22 cm', 11.5, 400, 'ink', 'middle')]
    b.append(circ(250, 134, 14, 'focus', None, 0, 1.5))
    b += [T(250, 210, 'Earth', 13, 600, 'ink', 'middle'), T(250, 228, 'peppercorn · 2 mm', 11.5, 400, 'ink', 'middle')]
    b += [T(400, 210, 'Jupiter', 13, 600, 'ink', 'middle'), T(400, 228, 'grape · 2 cm', 11.5, 400, 'ink', 'middle')]
    b.append(T(530, 120, 'true sizes,', 11.5, 400, 'muted'))
    b.append(T(530, 138, 'same scale', 11.5, 400, 'muted'))
    b.append(L(24, 252, 736, 252))
    b.append(T(24, 278, 'How far from the football?', 14, 600))
    x0, x1, maxm = 24, 736, 720.0
    X = lambda m: x0 + m / maxm * (x1 - x0)
    y = 340
    b.append(L(x0, y, x1, y, 'edge', 1.5))
    b.append(dot(x0, y, 6, 'warn'))
    for name, diam, dist in PLANETS:
        m = dist * SCALE
        named = name in ('Earth', 'Jupiter', 'Saturn', 'Neptune')
        b.append(dot(X(m), y, 4.5 if named else 3, 'focus' if name == 'Earth' else 'ink'))
        if named:
            up = name == 'Earth'
            a = None if up else 'end' if name == 'Neptune' else 'middle'
            b.append(T(X(m) + (6 if up else 0), y - 16 if up else y + 26, name, 11.5, 600, 'focus' if up else 'ink', a))
            b.append(T(X(m) + (6 if up else 0), y - 30 if up else y + 42, '%d m' % round(m), 11.5, 400, 'ink', a))
    b.append(P('M%.1f %d V%d H%.1f V%d' % (X(0), y + 64, y + 70, X(105), y + 64), 'ink', 1.25))
    b.append(T(X(0), y + 88, 'one football pitch · 105 m', 11.5, 400, 'muted'))
    b.append(R(24, 448, 712, 50, 'focus', 2, 'focus', 0.12))
    b += [T(40, 470, 'Space is almost all empty', 13, 600), T(40, 488, 'the whole family spans 7 pitches', 11.5)]
    b.append(T(24, 522, 'small dots: Mercury, Venus, Mars, Uranus · scale 1 : 6.3 billion', 11.5, 400, 'muted'))
    return sv(532, title, 'If the Sun were a 22 cm football: Earth would be a 2 mm peppercorn 24 m away, Jupiter a 2 cm grape 123 m away, Saturn 227 m, Neptune 711 m. One football pitch is 105 m.', b, defs)


def solar_star():
    title = 'The nearest star would be ~6,300 km away'
    b = []
    b.append(L(24, 120, 736, 120, 'edge', 1.5))
    b.append(dot(24, 120, 7, 'warn'))
    b += [T(24, 96, 'our football', 11.5, 600), T(36, 150, 'Neptune · 0.7 km', 11.5, 400, 'muted')]
    b.append(dot(24 + 0.7 / 6300 * 700, 120, 3, 'ink'))
    b.append(dot(724, 120, 7, 'warn'))
    b += [T(736, 96, 'Proxima Centauri', 11.5, 600, 'ink', 'end'), T(736, 150, '~6,300 km', 11.5, 600, 'ink', 'end')]
    b.append(P('M24 190 V184 H%.1f V190' % (24 + 5840 / 6300 * 700), 'ink', 1.25))
    b.append(T(24, 210, 'Paris to New York · 5,840 km', 11.5, 400, 'muted'))
    b.append(T(24, 246, 'Neptune’s whole orbit is a dot at this scale', 11.5, 400, 'muted'))
    return sv(256, title, 'At the same scale the nearest star, Proxima Centauri, would be about 6,300 km from the football, farther than Paris to New York (5,840 km). Neptune is only 0.7 km away.', b)


EX.append(dict(
    slug='solar', kind='Scale', question='How big is the solar system, really?',
    line='Shrink the Sun to a football and the planets become seeds scattered over 700 m.',
    chat=[solar_main()],
    pdf=dict(title='Football-sized Sun: Earth is a peppercorn 24 m away', subtitle='The solar system at 1 : 6.3 billion', cards=[
        dict(type='drawing', title='', data=[solar_main()]),
        dict(type='table', title='Every planet at this scale', data=dict(columns=['Planet', 'Looks like', 'Size', 'Distance'], rows=[
            [n, OBJECT[n], ('%.1f mm' % (d * SCALE * 1000)) if d * SCALE * 1000 < 10 else '%.1f cm' % (d * SCALE * 100), '%d m' % round(dist * SCALE)]
            for n, d, dist in PLANETS])),
        dict(type='drawing', title='', data=[solar_star()])])))

# =========================================================== 4. coffee brewing (comparison columns)
METHODS = [('Espresso', '~30 s', 'fine', 2.2, 5, 2, 1), ('Pour-over', '~3 min', 'medium', 4.0, 3, 2, 4), ('French press', '~4 min', 'coarse', 6.5, 4, 5, 4)]


def coffee_main():
    title = 'French press: strong coffee, almost no effort'
    b = []
    for k, (n, t, g, gr, strength, ease, cheap) in enumerate(METHODS):
        x = 24 + k * 244
        foc = n == 'French press'
        b.append(R(x, 52, 224, 150, 'focus' if foc else 'edge', 2 if foc else 1.25, 'focus' if foc else None, 0.06))
        b.append(T(x + 16, 76, n, 13, 600))
        cx = x + 160
        if k == 0:
            b += [P('M%d 100 h40 v26 a14 14 0 0 1 -14 14 h-12 a14 14 0 0 1 -14 -14 z' % (cx - 20), 'ink', 1.5), P('M%d 108 a8 8 0 0 1 0 14' % (cx + 20), 'ink', 1.5)]
        elif k == 1:
            b += [P('M%d 92 h52 l-18 34 h-16 z' % (cx - 26), 'ink', 1.5), R(cx - 18, 128, 36, 20, 'ink', 1.5, rx=4)]
        else:
            b += [R(cx - 18, 96, 36, 52, 'ink', 1.5, rx=4), L(cx, 86, cx, 116, 'ink', 1.5), L(cx - 14, 86, cx + 14, 86, 'ink', 2), L(cx - 16, 116, cx + 16, 116, 'ink', 1.5)]
        b.append(T(x + 16, 100, t, 11.5, 400))
        b.append(T(x + 16, 118, g + ' grind', 11.5, 400, 'muted'))
        for j in range(5):
            b.append(dot(x + 22 + j * (gr * 2.4 + 4), 140, gr, 'muted'))
        b.append(T(x + 16, 186, ('needs a machine', 'needs a steady pour', 'pour, wait, press')[k], 11.5, 400, 'muted'))
    b.append(L(24, 222, 736, 222))
    rows = [('Strength', 4), ('Ease', 5), ('Cheap gear', 6)]
    for i, (label, col) in enumerate(rows):
        y = 252 + i * 30
        b.append(T(24, y, label, 13, 600))
        for k, m in enumerate(METHODS):
            b.append(rating(24 + k * 244 + 150, y - 4, m[col], 'focus' if m[0] == 'French press' else 'edge'))
    b.append(R(24, 334, 712, 50, 'focus', 2, 'focus', 0.12))
    b += [T(40, 356, 'Start with a French press', 13, 600), T(40, 374, 'espresso is stronger, but needs a machine', 11.5)]
    b.append(T(24, 408, 'grind dots drawn to relative size · ratings out of 5, higher = better', 11.5, 400, 'muted'))
    return sv(418, title, 'Espresso: about 30 seconds, fine grind, strength 5, ease 2, cheap gear 1. Pour-over: about 3 minutes, medium grind, strength 3, ease 2, cheap gear 4. French press: about 4 minutes, coarse grind, strength 4, ease 5, cheap gear 4.', b)


def coffee_ratio():
    title = 'Same beans, very different amounts of water'
    b = [T(24, 62, 'WATER PER GRAM OF COFFEE', 11.5, 600, 'muted')]
    rows = [('Espresso', 2), ('French press', 15), ('Pour-over', 16)]
    for i, (n, r) in enumerate(rows):
        y = 92 + i * 40
        b.append(T(24, y + 11, n, 13, 600))
        for j in range(r):
            b.append(R(160 + j * 30, y, 24, 14, 'focus', 1.25, 'focus', 0.25, rx=3))
        b.append(T(160 + r * 30 + 4, y + 11, '%d g' % r, 11.5, 600))
    b.append(T(24, 236, 'each cell = 1 g of water · ratios typical', 11.5, 400, 'muted'))
    return sv(246, title, 'Water per gram of coffee: espresso 2 g, French press 15 g, pour-over 16 g.', b)


EX.append(dict(
    slug='coffee', kind='Comparison', question='Espresso, pour-over or French press: which should I start with?',
    line='French press: strong cup, cheap gear, no technique to learn.',
    chat=[coffee_main()],
    pdf=dict(title='French press: strong coffee, almost no effort', subtitle='Choosing a first brewing method', cards=[
        dict(type='drawing', title='', data=[coffee_main()]),
        dict(type='drawing', title='', data=[coffee_ratio()]),
        dict(type='card', title='French press in four steps', data=dict(summary='15 g coarse coffee, 250 g hot water, 4 minutes', status='info',
                                                                       items=['Water just off the boil', 'Stir once after pouring', 'Lid on, wait 4 minutes', 'Press slowly, pour at once']))])))

# =========================================================== 5. a cat's day (data: cell rows)
TABBY = ('#f9d3a2', '#e8a25a', '#a8642a')
CAT_AWAKE = {5, 6, 7, 12, 18, 19, 20, 21, 22}   # active at dawn and dusk, a short look around at noon
YOU_ASLEEP = {23, 0, 1, 2, 3, 4, 5, 6}


def cat_curled(prefix):
    '''A sleeping tabby curled into a loaf, tail wrapped around the front.'''
    N = Obj(prefix)
    body = smooth(blob(60, 62, 48, 28, n=14, jitter=0.04, seed=3))
    N.add(N.shadow(body, 3, 5, 4, 0.2))
    N.add('<path d="%s" fill="%s" stroke="%s" stroke-width="2"/>' % (body, N.radial(*TABBY), TABBY[2]))
    for k in range(4):
        N.add('<path d="M%d,%d q8,-10 16,0" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round" opacity="0.6"/>' % (34 + k * 14, 46, TABBY[2]))
    N.add('<path d="M18,74 C14,96 70,98 104,84" fill="none" stroke="%s" stroke-width="13" stroke-linecap="round"/>' % TABBY[2])
    N.add('<path d="M18,74 C14,96 70,98 104,84" fill="none" stroke="%s" stroke-width="9" stroke-linecap="round"/>' % TABBY[1])
    N.add('<path d="M88,40 L92,18 L104,34 Z M112,34 L124,18 L126,42 Z" fill="%s" stroke="%s" stroke-width="2" stroke-linejoin="round"/>' % (TABBY[1], TABBY[2]))
    N.add(N.ball(108, 52, 22, 20, cols=TABBY, stroke=TABBY[2], sw=2, shadow=0, gloss=0.25))
    N.add('<path d="M96,52 q4,4 8,0 M112,52 q4,4 8,0" fill="none" stroke="#5a3a1c" stroke-width="2" stroke-linecap="round"/>')
    N.add('<path d="M106,60 l2,2 l2,-2" fill="none" stroke="#7a4a2a" stroke-width="1.5"/>')
    return N


def cat_main():
    title = 'A cat sleeps 15 hours a day, you sleep 8'
    b, defs = [], ''
    x0, cw = 150, 23
    X = lambda h: x0 + h * (cw + 1)
    b.append('<rect x="%d" y="52" width="%d" height="150" fill="var(--tint)"/>' % (X(5) - 2, 3 * (cw + 1) + 3))
    b.append('<rect x="%d" y="52" width="%d" height="150" fill="var(--tint)"/>' % (X(18) - 2, 5 * (cw + 1) + 3))
    b += [T(X(5), 68, 'dawn', 11.5, 600, 'muted'), T(X(18), 68, 'dusk', 11.5, 600, 'muted')]
    for h in (0, 6, 12, 18, 24):
        b.append(T(X(h) - (0 if h < 24 else 1), 194, '%02d:00' % (h % 24) if h < 24 else '24:00', 11.5, 400, 'muted', 'middle' if 0 < h < 24 else ('end' if h == 24 else None)))
    for row, (name, detail, asleep, y) in enumerate([('Cat', '~15 h asleep', lambda h: h not in CAT_AWAKE, 88),
                                                    ('You', '~8 h asleep', lambda h: h in YOU_ASLEEP, 136)]):
        b += [T(24, y + 12, name, 13, 600), T(24, y + 30, detail, 11.5, 400, 'muted')]
        for h in range(24):
            on = asleep(h)
            b.append(R(X(h), y, cw, 30, 'focus' if on else 'edge', 1.25, 'focus' if on else None, 0.3, rx=4))
    N = cat_curled('k20261120-cat')
    b.append(N.group(560, 226, 0.95))
    defs += N.defs()
    b.append(L(24, 214, 736, 214))
    b += [T(24, 244, 'Built for twilight', 14, 600), T(24, 266, 'awake when mice are', 11.5, 400, 'muted')]
    b += [T(24, 300, 'Two thirds of the day', 13, 600), T(24, 318, 'mostly light naps, ears on', 11.5)]
    b.append(legend(24, 352, [('box', 'focus', 'asleep'), ('box', 'edge', 'awake'), ('box', 'line', 'dawn · dusk')]))
    b.append(T(24, 376, 'one cell = one hour · a typical adult cat', 11.5, 400, 'muted'))
    return sv(386, title, 'Hour-by-hour day: a cat sleeps about 15 of 24 hours and is awake mainly at dawn (05-08) and dusk (18-23); a person sleeps about 8 hours, 23:00-07:00. Cats are built for twilight hunting.', b, defs)


def cat_life():
    title = 'A 15-year-old cat has slept about 9 years'
    b = [T(24, 62, 'EACH CELL = ONE YEAR OF LIFE', 11.5, 600, 'muted')]
    for row, (name, years, asleep, y) in enumerate([('Cat', 15, 9.4, 84), ('You', 80, 26.7, 150)]):
        b += [T(24, y + 12, name, 13, 600), T(24, y + 30, '%d years' % years, 11.5, 400, 'muted')]
        per, cw = (15, 26) if years == 15 else (20, 12)
        for k in range(years):
            col, rr = k % per, k // per
            x, yy = 130 + col * (cw + 3), y + rr * (cw + 3)
            full = k + 1 <= asleep
            part = not full and k < asleep
            b.append(R(x, yy, cw, cw, 'focus' if full or part else 'edge', 1.25, 'focus' if full else 'focus' if part else None, 0.3 if full else 0.12, rx=3))
        b.append(T(130 + per * (cw + 3) + 6, y + 12, '~%g years asleep' % round(asleep), 11.5, 600))
    b.append(legend(24, 250, [('box', 'focus', 'asleep'), ('box', 'edge', 'awake')]))
    return sv(262, title, 'A 15-year-old cat has slept about 9 of its 15 years (15 of 24 hours a day); an 80-year-old person about 27 years (8 of 24 hours).', b)


EX.append(dict(
    slug='cat', kind='Data', question='Is it normal that my cat sleeps all day?',
    line='Yes: about 15 hours is typical, and the waking hours cluster at dawn and dusk.',
    chat=[cat_main()],
    pdf=dict(title='A cat sleeps 15 hours a day, you sleep 8', subtitle='How cats sleep', cards=[
        dict(type='drawing', title='', data=[cat_main()]),
        dict(type='drawing', title='', data=[cat_life()]),
        dict(type='card', title='When to worry', data=dict(summary='12 to 16 hours a day is normal', status='ok',
                                                           items=['Kittens and old cats sleep even more', 'Most of it is light dozing', 'A sudden change in sleep is worth a vet visit']))])))


# =========================================================== build
def main():
    out = os.path.join(ROOT, 'public', 'examples')
    os.makedirs(out, exist_ok=True)
    allsvg = []
    for e in EX:
        allsvg += e['chat'] + [s for c in e['pdf']['cards'] if c['type'] == 'drawing' for s in c['data'] if s not in e['chat']]
    json.dump(allsvg, open(os.path.join(K, 'examples.svgs.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    json.dump([dict(slug=e['slug'], kind=e['kind'], question=e['question'], line=e['line'], chat=e['chat'], title=e['pdf']['title']) for e in EX],
              open(os.path.join(K, 'examples.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    if '--no-pdf' in sys.argv:
        print('examples: %d (no PDFs)' % len(EX)); return
    for e in EX:
        doc = dict(e['pdf'], title=e['question'], subtitle=e['line'], lang='en', date='2026-11-20')
        src = os.path.join(out, e['slug'] + '.json')
        json.dump(doc, open(src, 'w', encoding='utf-8'), ensure_ascii=False)
        subprocess.run([sys.executable, os.path.join(SK, 'runik_pdf.py'), src, '-o', os.path.join(out, e['slug'] + '.pdf')], check=True)
        os.remove(src)
        if shutil.which('pdftoppm'):  # first page preview for the site
            subprocess.run(['pdftoppm', '-png', '-f', '1', '-l', '1', '-singlefile', '-scale-to', '900',
                            os.path.join(out, e['slug'] + '.pdf'), os.path.join(out, e['slug'])], check=True)
    print('examples: %d, PDFs in public/examples/' % len(EX))


if __name__ == '__main__':
    main()
