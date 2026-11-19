import sys, json
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from runik_nesne import Nesne, rrect
def t(x, y, s, fs=13, fw=400, fill='var(--ink)', anchor=None):
    s = s.replace('&', '&amp;').replace('<', '&lt;')
    return '<text x="%.1f" y="%.1f" font-size="%g" font-weight="%d" fill="%s"%s>%s</text>' % (x, y, fs, fw, fill, ' text-anchor="%s"' % anchor if anchor else '', s)
def svg(h, title, desc, defs, body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="100%%" viewBox="0 0 760 %d" font-size="13" role="img" aria-label="%s"><title>%s</title><desc>%s</desc><defs>%s</defs>%s</svg>' % (h, title, title, desc, defs, body))

# ---- 1. anakart (gerçek nesne: doğal renk) + Runik etiketleri
N = Nesne('k20261118-kart')
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
b = [t(24, 30, 'Veri işlemciden uzaklaştıkça yavaşlar', 15, 600)]
b.append(g)
rows0 = None
rows = [('cpu', 'İşlemci', 'içinde L1–L3 önbellek', '~1–20 ns', 'var(--tamam)', '✓ hızlı'),
        ('ram', 'RAM', 'çalışan programın verisi', '~100 ns', 'var(--dikkat)', '! orta'),
        ('ssd', 'SSD', 'kalıcı dosyalar', '~100 µs', 'var(--risk)', '✗ yavaş')]
for i, (k, ad, det, sure, col, durum) in enumerate(rows):
    y = (96, 196, 320)[i]
    x, yy = N.at(k)
    if k == 'ssd': b.append('<path d="M%.1f %.1f L478 %d" fill="none" stroke="var(--edge)" stroke-width="1.25"/>' % (x, yy, y - 4))
    else:
        ty = 66 if k == 'cpu' else 76
        b.append('<path d="M%.1f %.1f V%d H470 L478 %d" fill="none" stroke="var(--edge)" stroke-width="1.25"/>' % (x, yy, ty, y - 4))
    b.append('<circle cx="%.1f" cy="%.1f" r="4" fill="var(--ink)"/>' % (x, yy))
    b += [t(488, y, ad, 13, 600), t(488, y + 18, det, 11.5), t(488, y + 36, sure, 11.5, 600, col), t(560, y + 36, durum, 11.5, 400, col)]
b.append(t(24, 414, 'çizim sadeleştirilmiş · süreler yaklaşık', 11.5, 400, 'var(--muted)'))
S1 = svg(424, 'Veri işlemciden uzaklaştıkça yavaşlar', 'Anakart üzerinde işlemci (L1-L3 önbellek, ~1-20 ns), RAM (~100 ns) ve SSD (~100 µs).', N.defs(), ''.join(b))

# ---- 2. dağ haritası: gerçek dağ silüetleri, taban sessiz
G = json.load(open(__import__('os').path.join(__import__('os').path.dirname(__file__), 'ornek_geo.json')))
D = Nesne('k20261118-dag')
b = [t(24, 30, '3.000 m üstü 20 dağın 14’ü doğuda', 15, 600)]
b.append('<g clip-path="url(#k20261118-dag-clip)">' + ''.join('<path d="%s" fill="none" stroke="var(--line)" stroke-width="1"/>' % d for d in G['nb']) + '</g>')
b.append('<path d="%s" fill="var(--tint)" stroke="var(--edge)" stroke-width="1.25" stroke-linejoin="round"/>' % G['tur'][0])
b.append('<g clip-path="url(#k20261118-dag-clip)">' + ''.join('<path d="%s" fill="var(--line)" stroke="var(--edge)" stroke-width="0.8"/>' % d for d in G['lakes']) + '</g>')
b.append('<path d="M467.8 66.1 L477.7 367.8" stroke="var(--muted)" stroke-width="1" stroke-dasharray="4 4"/>')
b += [t(458, 70, 'batı · 6', 13, 600, 'var(--ink)', 'end'), t(486, 70, 'doğu · 14', 13, 600, 'var(--odak)')]
size = lambda h: 14 if h < 3500 else 20 if h < 4000 else 28
for n, h, (x, y, _) in sorted(G['M'], key=lambda m: m[2][1]):
    D.add(D.peak(x, y + size(h) * 0.33, size(h), snow=h >= 3500))
b.append(D.group(0, 0, 1))
named = {'Ağrı': (-6, -22, 'end'), 'Cilo-Sat': (-14, 8, 'end'), 'Süphan': (-18, -2, 'end'), 'Kaçkar': (14, -6, None), 'Erciyes': (14, 2, None)}
for n, h, (x, y, _) in G['M']:
    if n in named:
        dx, dy, an = named[n]
        b.append(t(x + dx, y + dy, '%s %s' % (n, '{:,}'.format(h).replace(',', '.')), 11.5, 600, 'var(--ink)', an))
D2 = Nesne('k20261118-dagl')
lx = 24
for H, lab in ((14, '3.000–3.499 m'), (20, '3.500–3.999 m'), (28, '≥ 4.000 m')):
    D2.add(D2.peak(lx + 14, 404, H, snow=H > 14)); b_lab = (lx + 34, 404, lab); lx += 170
    b.append(t(*b_lab, fs=11.5, fill='var(--muted)'))
b.append(D2.group(0, 0, 1))
b.append(t(lx + 6, 404, 'Natural Earth · Lambert konik', 11.5, 400, 'var(--muted)'))
S2 = svg(416, '3.000 m üstü 20 dağın 14’ü doğuda', 'Doğuda 14, batıda 6 dağ. En yüksekler: Ağrı 5.137, Cilo-Sat 4.134, Süphan 4.058, Kaçkar 3.932, Erciyes 3.916 m.', '<clipPath id="k20261118-dag-clip"><rect x="24" y="56" width="712" height="322"/></clipPath>' + D.defs() + D2.defs(), ''.join(b))
json.dump([S1, S2], open('ornek.json', 'w'), ensure_ascii=False)
