"""Realistic pictures for the headphones example: a head wearing headphones, a section through ear and ear cup,
sound as air molecules, and interference. Used by ex_headphones.py."""
import math, os, sys
K = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(K, '..', 'public', 'skill', 'runik'))
sys.path.insert(0, K)
from runik_object import Obj, rrect, smooth
from runik_svg import T, R, L, P, dot

SKIN = ('#fbe0cc', '#efb796', '#b07258')
SKIN_D = '#d99a7c'
HAIR = ('#6b4a36', '#3e2a1e', '#22160f')
SHELL = ('#6a717c', '#3a4048', '#1a1d22')
METAL = ('#f2f4f7', '#c3c9d1', '#7c8590')
PAD = ('#5a5f68', '#2d3137', '#15171a')
FOAM = ('#efe7d8', '#d2c5ad', '#958a74')
MAGNET = ('#c9ced6', '#858d99', '#474d56')
DIAPH = ('#faf7f0', '#ddd6c6', '#968e7d')
COIL = ('#f1b98a', '#c77d3a', '#7f4a1c')
PCB = ('#5e9f7a', '#3c7d58', '#24553a')
BATT = ('#a6bce0', '#6286c0', '#2f4f80')
MIC = ('#e1e4e9', '#9aa2ae', '#555d68')
BONE = ('#f7f1e3', '#e3d6b8', '#a8996f')
CANAL = '#c9826a'
DRUM = ('#f6d9c8', '#e7b49a', '#a8705a')
AIR = '#7a8aa8'


def svg(h, title, desc, body, defs=''):
    return ('<svg viewBox="0 0 760 %d" width="100%%" font-size="13" role="img" aria-label="%s"><title>%s</title><desc>%s</desc>%s%s%s</svg>'
            % (h, title, title, desc, '<defs>%s</defs>' % defs if defs else '', T(24, 30, title, 15, 600), ''.join(body)))


def leader(b, N, key, x, y, name, what, side='r'):
    mx, my = N.at(key)
    if side == 'r':
        b.append('<path d="M%.1f %.1f L%d %d H%d" fill="none" stroke="var(--ink)" stroke-width="0.9"/>' % (mx, my, x - 12, y - 4, x - 4))
        b += [T(x, y, name, 13, 600), T(x, y + 17, what, 11.5, 400, 'muted')]
    else:
        b.append('<path d="M%.1f %.1f L%d %d H%d" fill="none" stroke="var(--ink)" stroke-width="0.9"/>' % (mx, my, x + 132, y - 4, x + 124))
        b += [T(x, y, name, 13, 600), T(x, y + 17, what, 11.5, 400, 'muted')]
    b.append(dot(mx, my, 2.6, 'ink'))


# ---------------------------------------------------------------- 1. a head wearing headphones
HEAD = [(176, 30), (232, 44), (272, 86), (290, 150), (286, 212), (270, 262), (248, 296), (240, 340), (244, 396), (150, 396), (146, 352),
        (132, 320), (112, 310), (98, 298), (94, 282), (100, 272), (92, 262), (96, 252), (90, 240), (94, 230), (86, 224), (70, 212), (66, 204),
        (82, 186), (90, 160), (88, 140), (96, 116), (104, 84), (128, 50)]


def exterior():
    title = 'Noise-cancelling headphones: they listen, then answer with silence'
    N = Obj('k20261120-anc-head')
    ox, oy, s = 70, 86, 1.08
    pt = lambda x, y: (ox + x * s, oy + y * s)
    head = smooth([pt(*p) for p in HEAD], closed=True, t=0.45)
    N.add(N.shadow(head, 6, 10, 10, 0.18))
    N.add('<path d="%s" fill="%s" stroke="%s" stroke-width="1.4"/>' % (head, N.linear(SKIN[0], SKIN[1], 0, 0, 1, 0.4), SKIN[2]))
    # cheek, lips, eye, brow
    N.add('<ellipse cx="%.1f" cy="%.1f" rx="22" ry="16" fill="#f3a48c" opacity="0.28"/>' % pt(130, 240))
    N.add('<path d="M%.1f,%.1f q8,-3 14,1" fill="none" stroke="%s" stroke-width="2.4" stroke-linecap="round"/>' % (*pt(98, 250), '#c96a5c'))
    N.add('<path d="M%.1f,%.1f q10,-6 22,0" fill="none" stroke="%s" stroke-width="2.6" stroke-linecap="round"/>' % (*pt(104, 152), HAIR[2]))
    N.add('<path d="M%.1f,%.1f q8,-5 16,0 q-8,5 -16,0 z" fill="#fff" stroke="%s" stroke-width="1"/>' % (*pt(104, 170), SKIN[2]))
    N.add('<circle cx="%.1f" cy="%.1f" r="3" fill="%s"/>' % (*pt(108, 170), '#4a3424'))
    N.add('<path d="M%.1f,%.1f q-6,8 -2,18" fill="none" stroke="%s" stroke-width="1.4" opacity="0.7"/>' % (*pt(84, 196), SKIN[2]))
    N.add('<path d="M%.1f,%.1f q30,30 70,28" fill="none" stroke="%s" stroke-width="1.4" opacity="0.5"/>' % (*pt(150, 330), SKIN_D))
    # hair
    hair = smooth([pt(*p) for p in ((104, 92), (126, 46), (178, 24), (236, 38), (278, 84), (296, 150), (290, 214), (272, 258), (246, 282),
                                    (238, 250), (246, 200), (232, 150), (196, 112), (150, 98), (118, 104))], closed=True, t=0.45)
    N.add('<path d="%s" fill="%s" stroke="%s" stroke-width="1.2"/>' % (hair, N.linear(HAIR[0], HAIR[1], 0, 0, 1, 1), HAIR[2]))
    for k in range(9):
        x0, y0 = pt(140 + k * 16, 60 + k * 6)
        N.add('<path d="M%.1f,%.1f q20,%d 30,%d" fill="none" stroke="%s" stroke-width="1" opacity="0.4"/>' % (x0, y0, 10 + k, 40 + k * 3, HAIR[0]))
    # headband: padded arc over the crown, metal sliders into the cup yokes
    band = 'M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f' % (*pt(206, 186), *pt(216, -40), *pt(70, -30), *pt(100, 40))
    N.add(N.tube('M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f' % (*pt(204, 120), *pt(214, -24), *pt(160, -34), *pt(136, 26)), SHELL[2], SHELL[1], 18, 12))
    N.add(N.tube('M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f' % (*pt(196, 44), *pt(194, 6), *pt(166, -4), *pt(148, 22)), PAD[2], PAD[0], 9, 4))
    N.add('<path d="M%.1f,%.1f L%.1f,%.1f" stroke="%s" stroke-width="5" stroke-linecap="round"/>' % (*pt(206, 112), *pt(208, 150), METAL[2]))
    N.add('<path d="M%.1f,%.1f L%.1f,%.1f" stroke="%s" stroke-width="2.4" stroke-linecap="round"/>' % (*pt(206, 112), *pt(208, 150), METAL[0]))
    N.mark('band', *pt(186, -8))
    N.mark('slider', *pt(207, 132))
    # ear cup seen from outside, cushion edge visible
    cx, cy = pt(212, 214)
    N.add(N.shadow('M%.1f,%.1f m-50,0 a50,64 0 1,0 100,0 a50,64 0 1,0 -100,0' % (cx, cy), 5, 8, 6, 0.25))
    N.add('<ellipse cx="%.1f" cy="%.1f" rx="56" ry="70" fill="%s" stroke="%s" stroke-width="1.4"/>' % (cx - 8, cy + 2, N.linear(PAD[0], PAD[1], 0, 0, 1, 0), PAD[2]))
    N.add('<ellipse cx="%.1f" cy="%.1f" rx="50" ry="64" fill="%s" stroke="%s" stroke-width="1.6"/>' % (cx, cy, N.radial(SHELL[0], SHELL[1], SHELL[2], 0.35, 0.3, 0.9), SHELL[2]))
    N.add('<ellipse cx="%.1f" cy="%.1f" rx="38" ry="50" fill="none" stroke="%s" stroke-width="1.2" opacity="0.6"/>' % (cx, cy, METAL[1]))
    N.add('<path d="M%.1f,%.1f a38,50 0 0,1 30,-36" fill="none" stroke="#fff" stroke-width="3" opacity="0.35" stroke-linecap="round"/>' % (cx - 34, cy - 10))
    for k in range(5):  # microphone grille holes on the outside of the cup
        N.add('<circle cx="%.1f" cy="%.1f" r="1.3" fill="#111"/>' % (cx + 26 + (k % 3) * 4, cy - 40 + (k // 3) * 4))
    N.mark('mic', cx + 30, cy - 38)
    N.mark('cup', cx - 20, cy + 30)
    N.mark('pad', cx - 58, cy + 30)
    b = [N.group(0, 0, 1)]
    leader(b, N, 'band', 470, 92, 'Headband', 'padded, adjusts with metal sliders')
    leader(b, N, 'mic', 470, 200, 'Outer microphones', 'hear the noise before your ear does')
    leader(b, N, 'cup', 470, 278, 'Ear cup', 'holds driver, chip, battery, inner mic')
    leader(b, N, 'pad', 470, 356, 'Cushion', 'memory foam seals around the ear')
    b.append(R(470, 412, 266, 60, 'focus', 2, 'focus', 0.08))
    b += [T(486, 436, 'They measure the noise and play', 13, 600), T(486, 454, 'its mirror image, many times a second', 11.5)]
    b.append(T(24, 540, 'over-ear design; earbuds use the same parts, much smaller', 11.5, 400, 'muted'))
    return svg(550, title, 'A person in profile wearing over-ear noise-cancelling headphones: a padded headband with metal sliders, an ear cup with outer microphones behind a small grille, and a memory-foam cushion that seals around the ear. The headphones measure the noise and play its mirror image many times a second.', b, N.defs())


# ---------------------------------------------------------------- 2. section through ear and ear cup
def section():
    title = 'Cut through: the noise is cancelled right at the ear canal'
    N = Obj('k20261120-anc-sect')
    # head tissue, skull and the ear canal leading to the eardrum
    N.add('<path d="M24,70 H250 C262,140 262,420 250,470 H24 Z" fill="%s"/>' % N.linear(SKIN[1], SKIN[0], 0, 0, 1, 0))
    N.add('<path d="M24,70 H168 C176,150 176,390 168,470 H24 Z" fill="%s" opacity="0.9"/>' % N.linear(BONE[1], BONE[0], 0, 0, 1, 0))
    for k in range(14):
        N.add('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-width="0.8" opacity="0.6"/>' % (40 + (k * 37) % 120, 90 + (k * 53) % 360, 2 + k % 3, BONE[2]))
    N.add('<path d="M168,246 C190,240 230,238 262,246 L262,290 C230,298 190,296 168,290 Z" fill="%s"/>' % N.linear('#f5c3ac', CANAL, 0, 0, 0, 1))
    N.add('<path d="M168,246 C190,240 230,238 262,246 M168,290 C190,296 230,298 262,290" fill="none" stroke="%s" stroke-width="1.5"/>' % SKIN[2])
    N.add('<path d="M168,244 C160,256 160,280 168,292" fill="%s" stroke="%s" stroke-width="2"/>' % (DRUM[1], DRUM[2]))
    N.mark('drum', 164, 268)
    N.mark('canal', 214, 268)
    # outer ear (pinna) folded inside the cup
    N.add('<path d="%s" fill="%s" stroke="%s" stroke-width="1.5"/>' % (smooth([(258, 150), (300, 160), (318, 220), (316, 300), (300, 370), (262, 392), (262, 300), (276, 268), (262, 240)], closed=True, t=0.45),
                                                                       N.linear(SKIN[0], SKIN[1], 0, 0, 1, 0), SKIN[2]))
    N.add('<path d="M282,186 C304,210 304,320 286,352" fill="none" stroke="%s" stroke-width="2" opacity="0.6"/>' % SKIN[2])
    N.mark('pinna', 304, 300)
    # cushion (cut), pressed against the head
    for y0 in (110, 400):
        N.add('<path d="%s" fill="%s" stroke="%s" stroke-width="1.5"/>' % (rrect(256, y0, 56, 52, 22), N.linear(PAD[0], PAD[1]), PAD[2]))
        N.add('<path d="%s" fill="%s"/>' % (rrect(262, y0 + 6, 44, 40, 17), N.linear(FOAM[0], FOAM[1])))
        for k in range(10):
            N.add('<circle cx="%d" cy="%d" r="%.1f" fill="none" stroke="%s" stroke-width="0.6"/>' % (268 + (k * 11) % 34, y0 + 12 + (k * 7) % 28, 1.2 + (k % 3) * 0.5, FOAM[2]))
    N.mark('pad', 284, 426)
    # cup shell, baffle with mesh
    shell = 'M312,96 C420,92 486,150 492,270 C486,390 420,448 312,444 L312,430 C410,430 470,378 474,270 C470,162 410,110 312,110 Z'
    N.add(N.shadow(shell, 4, 7, 6, 0.2))
    N.add('<path d="M312,110 C410,110 470,162 474,270 C470,378 410,430 312,430 Z" fill="#23272d"/>')
    N.add('<path d="%s" fill="%s" stroke="%s" stroke-width="1.6"/>' % (shell, N.linear(SHELL[0], SHELL[1], 0, 0, 1, 0), SHELL[2]))
    N.add('<rect x="312" y="96" width="8" height="348" fill="%s" stroke="%s" stroke-width="1"/>' % (N.linear(METAL[1], METAL[2], 0, 0, 1, 0), METAL[2]))
    for k in range(40):
        N.add('<circle cx="316" cy="%d" r="1.1" fill="#2a2d33"/>' % (180 + k * 4.5))
    N.mark('shell', 482, 330)
    # driver: frame, ferrite magnet with pole piece, voice coil in the gap, cone and surround
    N.add('<path d="M326,186 L382,226 L382,314 L326,354 Z" fill="none" stroke="%s" stroke-width="3"/>' % METAL[2])
    N.add('<path d="%s" fill="%s" stroke="%s" stroke-width="1.2"/>' % (rrect(382, 230, 36, 80, 4), N.linear(MAGNET[0], MAGNET[1], 0, 0, 1, 0), MAGNET[2]))
    N.add('<rect x="374" y="248" width="10" height="44" fill="%s"/>' % N.linear(METAL[0], METAL[2], 0, 0, 1, 0))
    N.add('<rect x="368" y="244" width="5" height="52" rx="1" fill="%s" stroke="%s" stroke-width="0.8"/>' % (N.linear(COIL[0], COIL[1]), COIL[2]))
    for k in range(10):
        N.add('<path d="M368,%d h5" stroke="%s" stroke-width="0.8"/>' % (246 + k * 5, COIL[2]))
    N.add('<path d="M368,246 L330,196 L330,344 L368,294 Z" fill="%s" stroke="%s" stroke-width="1.2"/>' % (N.linear(DIAPH[0], DIAPH[1], 0, 0, 1, 0), DIAPH[2]))
    N.add('<path d="M330,196 q-6,-6 -4,-12 M330,344 q-6,6 -4,12" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % PAD[1])
    N.add('<path d="M370,248 q4,-12 14,-14 M370,292 q4,12 14,14" fill="none" stroke="#c8a96a" stroke-width="2"/>')  # spider
    N.mark('magnet', 400, 240)
    N.mark('coil', 370, 262)
    N.mark('cone', 344, 210)
    # microphones: feedback in front of the driver, feedforward in the shell wall
    N.add(N.ball(334, 372, 6, cols=MIC, stroke=MIC[2], sw=1, shadow=0.1, gloss=0.4))
    N.mark('fbmic', 334, 372)
    N.add(N.ball(470, 168, 6, cols=MIC, stroke=MIC[2], sw=1, shadow=0.1, gloss=0.4))
    for k in range(3):
        N.add('<circle cx="%d" cy="%d" r="1" fill="#111"/>' % (480 + k * 3, 160 + k * 3))
    N.mark('ffmic', 472, 166)
    # electronics
    N.add(N.slab(420, 150, 42, 26, PCB, r=3, depth=3, shadow=0.1))
    N.add(N.chip(428, 154, 18, 14))
    N.add('<path d="M430,180 C420,200 400,214 390,228" fill="none" stroke="#c77d3a" stroke-width="1.2"/>')
    N.mark('chip', 437, 160)
    N.add(N.slab(420, 340, 42, 46, BATT, r=4, depth=3, shadow=0.1))
    N.mark('batt', 441, 362)
    b = [N.group(0, 0, 1)]
    leader(b, N, 'ffmic', 560, 84, 'Outer microphone', 'feedforward: hears noise early')
    leader(b, N, 'chip', 560, 140, 'ANC chip', 'inverts and times the signal')
    leader(b, N, 'magnet', 560, 196, 'Magnet', 'fixed field for the coil')
    leader(b, N, 'coil', 560, 252, 'Voice coil', 'moves with the signal')
    leader(b, N, 'cone', 560, 308, 'Diaphragm', 'pushes the air')
    leader(b, N, 'batt', 560, 364, 'Battery', 'powers mics, chip, amplifier')
    leader(b, N, 'shell', 560, 420, 'Shell', 'blocks and damps sound')
    for k, (key, name, what) in enumerate((('drum', 'Eardrum', 'hears the result'), ('canal', 'Ear canal', '~2.5 cm long'), ('pad', 'Cushion', 'foam seal, passive'),
                                           ('pinna', 'Outer ear', 'sits inside the cup'), ('fbmic', 'Inner microphone', 'hears what you hear'))):
        x = 24 + k * 144
        mx, my = N.at(key)
        b.append('<path d="M%.1f %.1f L%d 490" fill="none" stroke="var(--ink)" stroke-width="0.9"/>' % (mx, my, x + 20))
        b.append(dot(mx, my, 2.6, 'ink'))
        b += [T(x, 508, name, 13, 600), T(x, 525, what, 11.5, 400, 'muted')]
    b.append(T(24, 560, 'horizontal section · cushion, cup and driver simplified · ear canal ~2.5 cm, cup ~9 cm', 11.5, 400, 'muted'))
    return svg(570, title, 'Horizontal section through the head, ear and ear cup. The ear canal, about 2.5 cm long, leads to the eardrum; the outer ear sits inside the cup, sealed by a foam cushion. The cup holds an outer feedforward microphone, an ANC chip, a battery, and a dynamic driver: a magnet, a voice coil that moves with the signal, and a diaphragm that pushes the air. An inner feedback microphone in front of the driver hears what reaches the ear.', b, N.defs())


# ---------------------------------------------------------------- 3. what sound is
def sound():
    title = 'Sound is air pushed together and pulled apart'
    b = []
    import random
    rng = random.Random(4)
    x0, x1, y0, y1 = 120, 736, 64, 168
    period = 150
    for k in range(900):
        u = rng.random()
        x = x0 + u * (x1 - x0)
        dens = 1 + 0.85 * math.cos(2 * math.pi * (x - x0) / period)
        if rng.random() * 1.85 < dens:
            b.append('<circle cx="%.1f" cy="%.1f" r="1.6" fill="%s" opacity="0.75"/>' % (x, y0 + rng.random() * (y1 - y0), AIR))
    b.append(R(x0, y0 - 4, x1 - x0, y1 - y0 + 8, 'edge', 1, rx=4))
    N = Obj('k20261120-anc-spk')
    N.add('<path d="M40,78 L84,92 L84,140 L40,154 Z" fill="%s" stroke="%s" stroke-width="1.2"/>' % (N.linear(DIAPH[0], DIAPH[1], 0, 0, 1, 0), DIAPH[2]))
    N.add('<path d="%s" fill="%s" stroke="%s" stroke-width="1"/>' % (rrect(84, 100, 22, 32, 3), N.linear(MAGNET[0], MAGNET[1]), MAGNET[2]))
    b.insert(0, N.group(0, 0, 1))
    b.append(T(24, 176, 'speaker cone', 11.5, 400, 'muted'))
    for k in range(4):
        xc = x0 + k * period
        if xc < x1:
            b.append(T(xc + 4, 60, 'squeezed', 11.5, 600, 'ink'))
    yw = 230
    b.append(L(x0, yw, x1, yw, 'line', 1))
    b.append(P('M' + ' L'.join('%.1f %.1f' % (x, yw - 34 * math.cos(2 * math.pi * (x - x0) / period)) for x in range(x0, x1 + 1, 3)), 'ink', 2))
    b.append(T(24, yw - 26, 'more pressure', 11.5, 400, 'muted'))
    b.append(T(24, yw + 34, 'less pressure', 11.5, 400, 'muted'))
    b.append(P('M%d %d V%d H%d V%d' % (x0, yw - 46, yw - 52, x0 + period, yw - 46), 'ink', 1.25))
    b.append(T(x0 + period / 2, yw - 58, 'one wavelength', 11.5, 600, 'ink', 'middle'))
    b.append(L(24, 290, 736, 290))
    b.append(T(24, 318, 'Low notes are long waves, high notes short ones', 14, 600))
    rows = [(100, 'engine hum'), (1000, 'speech'), (5000, 'a hiss')]
    Xl = lambda m: 170 + m / 3.43 * 470
    for i, (f, lab) in enumerate(rows):
        y = 350 + i * 40
        lam = 343 / f
        b += [T(24, y + 4, '{:,} Hz'.format(f), 13, 600), T(24, y + 20, lab, 11.5, 400, 'muted')]
        b.append('<rect x="170" y="%d" width="%.1f" height="14" rx="3" fill="var(--focus)" fill-opacity="0.3" stroke="var(--focus)" stroke-width="1.5"/>' % (y - 7, max(Xl(lam) - 170, 3)))
        b.append(T(max(Xl(lam), 173) + 8, y + 5, ('%.1f m' % lam) if lam >= 1 else ('%d cm' % round(lam * 100)), 11.5, 600))
    hw = Xl(0.15) - 170
    b.append('<rect x="170" y="472" width="%.1f" height="14" rx="3" fill="var(--edge)" fill-opacity="0.25" stroke="var(--edge)" stroke-width="1.25"/>' % hw)
    b += [T(24, 484, 'your head', 13, 600), T(170 + hw + 8, 484, '~15 cm', 11.5, 600)]
    b.append(T(24, 514, 'speed of sound 343 m/s · wavelength = speed ÷ frequency · dots = air molecules, density exaggerated', 11.5, 400, 'muted'))
    return svg(524, title, 'A speaker cone pushes air molecules together (higher pressure) and pulls them apart (lower pressure), and the pattern travels as a wave. Wavelength is the speed of sound, 343 m/s, divided by frequency: 3.4 m for a 100 Hz hum, 34 cm for 1 kHz speech, 7 cm for a 5 kHz hiss; a head is about 15 cm wide.', b, N.defs())


# ---------------------------------------------------------------- 4. interference at the molecule level
def interference():
    title = 'Where squeezed air meets stretched air, the air stays still'
    import random
    b = []
    period = 160
    rows = [('Noise', 0, 'ink'), ('Anti-noise', math.pi, 'focus'), ('Together', None, 'good')]
    for i, (name, ph, c) in enumerate(rows):
        y0 = 60 + i * 120
        rng = random.Random(10 + i)
        b.append(T(24, y0 + 44, name, 13, 600, c if c != 'ink' else 'ink'))
        for k in range(560):
            x = 150 + rng.random() * 586
            dens = 1 if ph is None else 1 + 0.85 * math.cos(2 * math.pi * (x - 150) / period + ph)
            if rng.random() * 1.85 < dens:
                b.append('<circle cx="%.1f" cy="%.1f" r="1.5" fill="%s" opacity="0.7"/>' % (x, y0 + 8 + rng.random() * 56, AIR))
        b.append(R(150, y0 + 4, 586, 64, 'edge', 1, rx=4))
        amp = 0 if ph is None else 26
        b.append(P('M' + ' L'.join('%.1f %.1f' % (x, y0 + 98 - amp * math.cos(2 * math.pi * (x - 150) / period + (ph or 0))) for x in range(150, 737, 3)),
                   c, 2.5 if ph is None else 2))
    b += [T(24, 120, 'pressure', 11.5, 400, 'muted'), T(24, 360, 'flat: silence', 11.5, 600, 'good')]
    b.append(T(24, 418, 'dots = air molecules, density exaggerated · the two waves are the same size and exactly opposite', 11.5, 400, 'muted'))
    return svg(428, title, 'Three strips of air molecules. The noise squeezes and stretches the air; the anti-noise does exactly the opposite at the same moment; together the air molecules stay evenly spread and the pressure line is flat, which you hear as silence.', b)
