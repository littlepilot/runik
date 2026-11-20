"""Builds the landing page's two hand-made drawings (scripts/drawings.json):
hero = the Runik answer in "Same question · two answers"; nasil = "How it works".
The examples further down the page come from scripts/examples.py."""
import json, os, sys
K = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(K, '..', 'public', 'skill', 'runik'))
from runik_object import Obj, rrect
from runik_svg import T, R, L, arrow, varrow, circ, dot, P, check, chev


def sv(h, title, desc, body, defs=''):
    return ('<svg viewBox="0 0 760 %d" width="100%%" font-size="13" role="img" aria-label="%s"><title>%s</title><desc>%s</desc>%s%s%s</svg>'
            % (h, title, title, desc, '<defs>%s</defs>' % defs if defs else '', T(24, 30, title, 15, 600), ''.join(body)))


out = {}

# ===== HERO: why reading from RAM is slow (object drawing: motherboard)
N = Obj('k20261120-hero')
N.add(N.slab(50, 90, 900, 700, N.PCB, r=18, depth=14, shadow=0.3))
N.add(N.grain(rrect(50, 90, 900, 700, 18), 0.35))
for i in range(6):
    N.add('<path d="M420,%d H540" stroke="#d9b45a" stroke-width="3" opacity="0.8"/>' % (300 + i * 22))
for i in range(4):
    N.add('<path d="M%d,540 V%d Q%d,%d %d,%d H470" stroke="#d9b45a" stroke-width="3" opacity="0.8" fill="none"/>' % (
        240 + i * 22, 640 + i * 10, 240 + i * 22, 690 + i * 12, 300 + i * 22, 690 + i * 12))
for cx, cy in ((90, 130), (910, 130), (90, 750), (910, 750)):
    N.add(N.ball(cx, cy, 13, cols=N.METAL, shadow=0.1, gloss=0.3))
for i in range(7):
    N.add(N.ball(110 + i * 34, 590, 13, cols=('#6c7480', '#3b4048', '#1b1e22'), shadow=0.2, gloss=0.6))
N.add(N.chip(780, 640, 110, 90))
N.add(N.slab(110, 180, 320, 330, N.METAL, r=10, depth=10))
N.add(N.slab(150, 220, 240, 250, ('#fbfcfd', '#cfd5dc', '#7d8794'), r=14, depth=6, shadow=0.18))
N.mark('cpu', 270, 222)
for i in range(4):
    x = 560 + i * 82
    N.add(N.slab(x, 150, 44, 440, ('#3c4a5c', '#28323f', '#151b23'), r=5, depth=8))
    for k in range(8):
        N.add(N.chip(x + 8, 175 + k * 50, 28, 36))
    N.add('<path d="M%d,592 h44" stroke="#d9b45a" stroke-width="6"/>' % x)
N.mark('ram', 704, 152)
N.add(N.slab(470, 660, 270, 76, ('#3c4a5c', '#28323f', '#151b23'), r=6, depth=7))
for k in range(3):
    N.add(N.chip(500 + k * 72, 674, 56, 46))
N.mark('ssd', 740, 698)
b = [N.group(24, 52, 0.42)]
rows = [('cpu', 'CPU cache', '~1 ns · on your desk', 'good', '✓ fast', 92),
        ('ram', 'RAM', '~100 ns · down the hall', 'warn', '! slow', 176),
        ('ssd', 'SSD', '~100 µs · another city', 'bad', '✗ very slow', 330)]
for key, name, detail, c, status, y in rows:
    x, yy = N.at(key)
    if key == 'ssd':
        b.append(P('M%.1f %.1f L478 %d' % (x, yy, y - 4), 'edge', 1.25))
    else:
        b.append(P('M%.1f %.1f V%d H470 L478 %d' % (x, yy, 66 if key == 'cpu' else 76, y - 4), 'edge', 1.25))
    b.append(dot(x, yy, 4, 'ink'))
    b += [T(488, y, name, 13, 600), T(488, y + 18, detail, 11.5), T(488, y + 36, status, 11.5, 600, c)]
b.append(T(488, 246, '1 RAM read = 100 cache reads', 11.5, 600))
for i in range(100):
    b.append('<rect x="%d" y="%d" width="8" height="8" rx="2" fill="var(--good)" fill-opacity="0.35" stroke="var(--good)" stroke-width="1"/>' % (488 + (i % 25) * 10, 256 + (i // 25) * 10))
b.append(T(24, 412, 'simplified drawing · times approximate · one square = one cache read', 11.5, 400, 'muted'))
out['hero'] = sv(422, 'RAM sits far from the CPU: 100× slower',
                 'Motherboard: the CPU has cache inside (about 1 ns, like a note on your desk), RAM is further away (about 100 ns, down the hall), the SSD furthest (about 100 µs, another city). One RAM read takes as long as 100 cache reads.',
                 b, N.defs())

# ===== HOW: one line, any agent, PDF on request
b = []
b += [T(24, 66, '1 · COPY', 11.5, 600, 'muted'), T(260, 66, '2 · PASTE', 11.5, 600, 'muted'), T(560, 66, '3 · RUNIK IS ON', 11.5, 600, 'muted')]
b.append(R(24, 84, 196, 52, 'focus', 2, 'focus', 0.1, rx=8))
b.append(T(38, 106, 'Runik: read', 11.5, 600))
b.append(T(38, 124, '…/start.md', 11.5, 400))
b += [R(190, 98, 12, 14, 'ink', 1.25, rx=2), R(194, 102, 12, 14, 'ink', 1.25, 'surface', 1, rx=2)]
b.append(arrow(224, 110, 256, 'edge', 1.5))
b.append(P('M262 84 h132 a6 6 0 0 1 6 6 v34 a6 6 0 0 1 -6 6 h-96 l-12 12 v-12 h-24 a6 6 0 0 1 -6 -6 v-34 a6 6 0 0 1 6 -6 z', 'ink', 2))
b += [T(276, 106, 'any agent', 13, 600), T(276, 122, 'chat or terminal', 11.5, 400, 'muted')]
b.append(arrow(400, 110, 430, 'edge', 1.5))
b.append(P('M476 76 L520 110 L476 144 L432 110 Z', 'ink', 1.5))
b += [T(476, 107, 'can it', 11.5, 600, 'ink', 'middle'), T(476, 121, 'install?', 11.5, 600, 'ink', 'middle')]
b.append(P('M520 110 H554', 'good', 2))
b.append('<path d="M554 106.5 L560 110 L554 113.5 Z" fill="var(--good)"/>')
b.append(P('M476 144 V224 H554', 'focus', 2))
b.append('<path d="M554 220.5 L560 224 L554 227.5 Z" fill="var(--focus)"/>')
b += [T(536, 102, 'yes', 11.5, 600, 'good', 'middle'), T(484, 170, 'no', 11.5, 600, 'focus')]
b.append(R(560, 80, 176, 90, 'good', 2, 'good', 0.1))
b += [T(574, 102, 'Claude Code', 13, 600), T(574, 120, 'skill + live board', 11.5), T(574, 138, 'every project', 11.5), check(574, 150), T(592, 160, 'updates daily', 11.5, 600, 'good')]
b.append(R(560, 184, 176, 82, 'focus', 2, 'focus', 0.1))
b += [T(574, 206, 'Any other agent', 13, 600), T(574, 224, 'Claude, ChatGPT, Gemini', 11.5), check(574, 238, 'focus'), T(592, 248, 'draws in that chat', 11.5, 600, 'focus')]
b.append(L(24, 290, 736, 290))
b.append(T(24, 318, 'Any answer, also as a PDF', 14, 600))
b.append(P('M24 338 h196 a6 6 0 0 1 6 6 v28 a6 6 0 0 1 -6 6 h-160 l-12 12 v-12 h-24 a6 6 0 0 1 -6 -6 v-28 a6 6 0 0 1 6 -6 z', 'edge', 1.5))
b.append(T(38, 362, '“give me this as a PDF”', 11.5, 600))
b.append(arrow(240, 360, 300, 'edge', 1.5))
b.append(P('M310 328 h46 l14 14 v50 h-60 z M356 328 v14 h14', 'ink', 1.5))
b += [L(318, 352, 360, 352, 'focus', 2), R(318, 360, 22, 16, 'focus', 1.25, 'focus', 0.2, rx=2), L(344, 364, 362, 364, 'edge', 1.5), L(344, 372, 358, 372, 'edge', 1.5), L(318, 382, 360, 382, 'edge', 1.5)]
b += [T(388, 354, 'A4 pages', 13, 600), T(388, 372, 'same drawings · your language', 11.5, 400, 'muted')]
b.append(T(24, 420, 'outputs follow your language · Claude Code keeps one board for all projects', 11.5, 400, 'muted'))
out['nasil'] = sv(430, 'One line, and any agent answers in Runik',
                  'Copy one line and paste it into any agent. If it can install (Claude Code), it adds the skill and a live board to every project and updates daily; any other agent (Claude, ChatGPT, Gemini) draws Runik answers in that chat. Ask for any answer as a PDF: A4 pages with the same drawings, in your language.',
                  b)

json.dump(out, open(os.path.join(K, 'drawings.json'), 'w'), ensure_ascii=False)
print(list(out))
