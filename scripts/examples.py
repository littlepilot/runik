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

# =========================================================== 3. cell division: mitosis and meiosis (researched, multi-page)
import ex_cell
EX.append(ex_cell.example())

# =========================================================== 4. lithium-ion battery (researched, multi-page)
import ex_battery
EX.append(ex_battery.example())


# =========================================================== 5. eight espresso drinks (researched, multi-page)
import ex_coffee
EX.append(ex_coffee.example())


# =========================================================== build
def main():
    out = os.path.join(ROOT, 'public', 'examples')
    os.makedirs(out, exist_ok=True)
    allsvg = []
    for e in EX:
        allsvg += e['chat'] + [s for c in e['pdf']['cards'] if c['type'] == 'drawing' for s in c['data'] if s not in e['chat']]
    json.dump(allsvg, open(os.path.join(K, 'examples.svgs.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    meta = []
    for e in EX:
        d = os.path.join(out, e['slug'])
        pages = sorted(f for f in os.listdir(d) if f.startswith('page-') and f.endswith('.png')) if os.path.isdir(d) else []
        meta.append(dict(slug=e['slug'], kind=e['kind'], title=e.get('title') or e['pdf']['title'], prompt=e.get('prompt') or e['question'],
                         line=e['line'], chat=e['chat'], pdf_title=e.get('title') or e['question'], pages=pages))
    if '--no-pdf' not in sys.argv:
        for e, m in zip(EX, meta):
            d = os.path.join(out, e['slug'])
            if os.path.isdir(d):
                shutil.rmtree(d)
            os.makedirs(d)
            title = e.get('title') or e['question']
            subtitle = e['pdf'].get('subtitle') if e.get('prompt') else e['line']
            doc = dict(e['pdf'], title=title, subtitle=subtitle, lang='en', date='2026-11-20')
            src = os.path.join(d, 'doc.json')
            json.dump(doc, open(src, 'w', encoding='utf-8'), ensure_ascii=False)
            pdf = os.path.join(d, e['slug'] + '.pdf')
            subprocess.run([sys.executable, os.path.join(SK, 'runik_pdf.py'), src, '-o', pdf], check=True)
            os.remove(src)
            if shutil.which('pdftoppm'):  # page previews for the example page
                subprocess.run(['pdftoppm', '-png', '-scale-to', '900', pdf, os.path.join(d, 'page')], check=True)
            m['pages'] = sorted(f for f in os.listdir(d) if f.startswith('page-') and f.endswith('.png'))
    json.dump(meta, open(os.path.join(K, 'examples.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('examples: %d%s' % (len(EX), '' if '--no-pdf' in sys.argv else ', PDFs in public/examples/<slug>/'))


if __name__ == '__main__':
    main()
