# example_object.py - two object drawings built with runik_object.py; writes example.json (an SVG array).
#   python3 example_object.py && node runik-lint.js example.json
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from runik_object import Obj, rrect


def text(x, y, s, fs=13, fw=400, fill='var(--ink)', anchor=None):
    s = s.replace('&', '&amp;').replace('<', '&lt;')
    return '<text x="%.1f" y="%.1f" font-size="%g" font-weight="%d" fill="%s"%s>%s</text>' % (x, y, fs, fw, fill, ' text-anchor="%s"' % anchor if anchor else '', s)


def svg(h, title, desc, defs, body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="100%%" viewBox="0 0 760 %d" font-size="13" role="img" aria-label="%s"><title>%s</title><desc>%s</desc><defs>%s</defs>%s</svg>' % (h, title, title, desc, defs, body))


# ---- 1. motherboard (real object: natural colors) + Runik labels
N = Obj('k20261118-board')
N.add(N.slab(50, 90, 900, 700, N.PCB, r=18, depth=14, shadow=0.3))
N.add(N.grain(rrect(50, 90, 900, 700, 18), 0.35))
for i in range(6):
    N.add('<path d="M420,%d H540" stroke="#d9b45a" stroke-width="3" opacity="0.8"/>' % (300 + i * 22))
for i in range(4):
    N.add('<path d="M%d,540 V%d Q%d,%d %d,%d H470" stroke="#d9b45a" stroke-width="3" opacity="0.8" fill="none"/>' % (240 + i * 22, 640 + i * 10, 240 + i * 22, 690 + i * 12, 300 + i * 22, 690 + i * 12))
for cx, cy in ((90, 130), (910, 130), (90, 750), (910, 750)):
    N.add(N.ball(cx, cy, 13, cols=N.METAL, shadow=0.1, gloss=0.3))
for i in range(7):
    N.add(N.ball(110 + i * 34, 590, 13, cols=("#6c7480", "#3b4048", "#1b1e22"), shadow=0.2, gloss=0.6))
N.add(N.chip(780, 640, 110, 90))
N.add(N.slab(110, 180, 320, 330, N.METAL, r=10, depth=10))
N.add(N.slab(150, 220, 240, 250, ("#fbfcfd", "#cfd5dc", "#7d8794"), r=14, depth=6, shadow=0.18))
N.mark('cpu', 270, 222)
for i in range(4):
    x = 560 + i * 82
    N.add(N.slab(x, 150, 44, 440, ("#3c4a5c", "#28323f", "#151b23"), r=5, depth=8))
    for k in range(8):
        N.add(N.chip(x + 8, 175 + k * 50, 28, 36))
    N.add('<path d="M%d,592 h44" stroke="#d9b45a" stroke-width="6"/>' % x)
N.mark('ram', 704, 152)
N.add(N.slab(470, 660, 270, 76, ("#3c4a5c", "#28323f", "#151b23"), r=6, depth=7))
for k in range(3):
    N.add(N.chip(500 + k * 72, 674, 56, 46))
N.mark('ssd', 740, 698)
g = N.group(24, 52, 0.42)
b = [text(24, 30, 'Data slows down as it moves away from the CPU', 15, 600)]
b.append(g)
rows = [('cpu', 'CPU', 'L1–L3 cache inside', '~1–20 ns', 'var(--good)', '✓ fast'),
        ('ram', 'RAM', 'running program data', '~100 ns', 'var(--warn)', '! medium'),
        ('ssd', 'SSD', 'persistent files', '~100 µs', 'var(--bad)', '✗ slow')]
for i, (key, name, detail, latency, col, status) in enumerate(rows):
    y = (96, 196, 320)[i]
    x, yy = N.at(key)
    if key == 'ssd':
        b.append('<path d="M%.1f %.1f L478 %d" fill="none" stroke="var(--edge)" stroke-width="1.25"/>' % (x, yy, y - 4))
    else:
        ty = 66 if key == 'cpu' else 76
        b.append('<path d="M%.1f %.1f V%d H470 L478 %d" fill="none" stroke="var(--edge)" stroke-width="1.25"/>' % (x, yy, ty, y - 4))
    b.append('<circle cx="%.1f" cy="%.1f" r="4" fill="var(--ink)"/>' % (x, yy))
    b += [text(488, y, name, 13, 600), text(488, y + 18, detail, 11.5), text(488, y + 36, latency, 11.5, 600, col), text(560, y + 36, status, 11.5, 400, col)]
b.append(text(24, 414, 'simplified drawing · times approximate', 11.5, 400, 'var(--muted)'))
S1 = svg(424, 'Data slows down as it moves away from the CPU', 'Motherboard with the CPU (L1-L3 cache, ~1-20 ns), RAM (~100 ns) and SSD (~100 µs).', N.defs(), ''.join(b))

# ---- 2. mountain map: real mountain silhouettes, quiet base
G = json.load(open(os.path.join(HERE, 'example_geo.json'), encoding='utf-8'))
M = Obj('k20261118-mtn')
title = '14 of 20 peaks above 3,000 m are in the east'
b = [text(24, 30, title, 15, 600)]
b.append('<g clip-path="url(#k20261118-mtn-clip)">' + ''.join('<path d="%s" fill="none" stroke="var(--line)" stroke-width="1"/>' % d for d in G['neighbors']) + '</g>')
b.append('<path d="%s" fill="var(--tint)" stroke="var(--edge)" stroke-width="1.25" stroke-linejoin="round"/>' % G['turkey'][0])
b.append('<g clip-path="url(#k20261118-mtn-clip)">' + ''.join('<path d="%s" fill="var(--line)" stroke="var(--edge)" stroke-width="0.8"/>' % d for d in G['lakes']) + '</g>')
b.append('<path d="M467.8 66.1 L477.7 367.8" stroke="var(--muted)" stroke-width="1" stroke-dasharray="4 4"/>')
b += [text(458, 70, 'west · 6', 13, 600, 'var(--ink)', 'end'), text(486, 70, 'east · 14', 13, 600, 'var(--focus)')]
size = lambda h: 14 if h < 3500 else 20 if h < 4000 else 28
for name, h, (x, y, _) in sorted(G['peaks'], key=lambda m: m[2][1]):
    M.add(M.peak(x, y + size(h) * 0.33, size(h), snow=h >= 3500))
b.append(M.group(0, 0, 1))
named = {'Ağrı': (-6, -22, 'end'), 'Cilo-Sat': (-14, 8, 'end'), 'Süphan': (-18, -2, 'end'), 'Kaçkar': (14, -6, None), 'Erciyes': (14, 2, None)}
for name, h, (x, y, _) in G['peaks']:
    if name in named:
        dx, dy, anchor = named[name]
        b.append(text(x + dx, y + dy, '%s %s' % (name, '{:,}'.format(h)), 11.5, 600, 'var(--ink)', anchor))
L = Obj('k20261118-mtnl')
lx = 24
for H, label in ((14, '3,000–3,499 m'), (20, '3,500–3,999 m'), (28, '≥ 4,000 m')):
    L.add(L.peak(lx + 14, 404, H, snow=H > 14))
    b.append(text(lx + 34, 404, label, fs=11.5, fill='var(--muted)'))
    lx += 170
b.append(L.group(0, 0, 1))
b.append(text(lx + 6, 404, 'Natural Earth · Lambert conic', 11.5, 400, 'var(--muted)'))
S2 = svg(416, title, '14 peaks in the east, 6 in the west. Highest: Ağrı 5,137, Cilo-Sat 4,134, Süphan 4,058, Kaçkar 3,932, Erciyes 3,916 m.',
         '<clipPath id="k20261118-mtn-clip"><rect x="24" y="56" width="712" height="322"/></clipPath>' + M.defs() + L.defs(), ''.join(b))
json.dump([S1, S2], open('example.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('example.json written: 2 drawings')
