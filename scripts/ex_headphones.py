"""Example: how noise-cancelling headphones work (researched, multi-page). Used by examples.py."""
import math, os, sys
K = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(K, '..', 'public', 'skill', 'runik'))
sys.path.insert(0, K)
from runik_object import Obj, rrect, smooth, blob
from runik_svg import T, R, L, P, dot, circ

SHELL = ('#5b616b', '#353a42', '#1b1e22')
CUSHION = ('#4a4f57', '#2c3036', '#16181b')
FOAM = ('#e9e1d3', '#cbbfa9', '#8f8470')
MAGNET = ('#b8bec7', '#7d8591', '#454b54')
DIAPH = ('#f4f1ea', '#d8d2c4', '#8f8878')
PCB = ('#5e9f7a', '#3c7d58', '#24553a')
SKIN = ('#fde3cf', '#f2b892', '#b9785a')
BATT = ('#9fb6d9', '#5d7fb5', '#2f4f80')
MIC = ('#d7dbe2', '#9aa2ae', '#5a626e')


def svg(h, title, desc, body, defs=''):
    return ('<svg viewBox="0 0 760 %d" width="100%%" font-size="13" role="img" aria-label="%s"><title>%s</title><desc>%s</desc>%s%s%s</svg>'
            % (h, title, title, desc, '<defs>%s</defs>' % defs if defs else '', T(24, 30, title, 15, 600), ''.join(body)))


def wave(x, y, w, amp, phase=0, c='ink', sw=2, dash=None, cycles=2.5):
    pts = ['%.1f %.1f' % (x + i * w / 80, y - amp * math.sin(phase + i / 80 * cycles * 2 * math.pi)) for i in range(81)]
    return P('M' + ' L'.join(pts), c, sw, dash)


def head(N, x, y):
    '''Side of a head with the ear and ear canal, cut through at the canal.'''
    d = smooth([(x - 10, y - 120), (x + 40, y - 126), (x + 70, y - 80), (x + 74, y), (x + 70, y + 80), (x + 40, y + 130), (x - 10, y + 128)], closed=False, t=0.5)
    N.add('<path d="%s L%d,%d L%d,%d Z" fill="%s" stroke="%s" stroke-width="1.5"/>' % (d, x - 30, y + 128, x - 30, y - 120, N.linear(SKIN[1], SKIN[0], 0, 0, 1, 0), SKIN[2]))
    N.add('<path d="%s" fill="%s" stroke="%s" stroke-width="1.5"/>' % (smooth(blob(x + 76, y, 14, 32, n=12, jitter=0.06, seed=4)), N.radial(*SKIN), SKIN[2]))
    N.add('<path d="M%d,%d H%d" stroke="%s" stroke-width="9" stroke-linecap="round"/>' % (x + 24, y + 2, x + 72, '#c98a6c'))
    N.add('<path d="M%d,%d H%d" stroke="#e9b29a" stroke-width="5" stroke-linecap="round"/>' % (x + 26, y + 2, x + 70))
    N.add('<ellipse cx="%d" cy="%d" rx="2" ry="6" fill="#a15c48"/>' % (x + 24, y + 2))


# ---------------------------------------------------------------- 1. cutaway of an ear cup
def cutaway():
    title = 'Inside an ear cup: two microphones, a chip and a speaker'
    N = Obj('k20261120-anc-cup')
    b = []
    hx, hy = 120, 300
    head(N, hx, hy)
    # headband over the top
    N.add(N.tube('M%d,%d C%d,%d %d,%d %d,%d' % (hx + 196, hy - 100, hx + 214, hy - 210, hx + 30, hy - 240, hx - 40, hy - 214), SHELL[2], SHELL[1], 16, 10))
    # cushion (cut): foam in a protein-leather skin, sealing round the ear
    for sy in (-1, 1):
        cy = hy + sy * 70
        N.add('<path d="%s" fill="%s" stroke="%s" stroke-width="1.5"/>' % (rrect(hx + 90, cy - 22, 44, 44, 18), N.linear(CUSHION[0], CUSHION[1]), CUSHION[2]))
        N.add('<path d="%s" fill="%s"/>' % (rrect(hx + 96, cy - 16, 32, 32, 13), N.linear(FOAM[0], FOAM[1])))
        for k in range(6):
            N.add('<circle cx="%.1f" cy="%.1f" r="1.6" fill="none" stroke="%s" stroke-width="0.6"/>' % (hx + 102 + (k * 7) % 22, cy - 9 + (k * 5) % 18, FOAM[2]))
    # cup shell (cut)
    shell = 'M%d,%d C%d,%d %d,%d %d,%d L%d,%d C%d,%d %d,%d %d,%d Z' % (hx + 132, hy - 100, hx + 210, hy - 104, hx + 250, hy - 60, hx + 252, hy, hx + 252, hy,
                                                                     hx + 250, hy + 60, hx + 210, hy + 104, hx + 132, hy + 100)
    N.add(N.shadow(shell, 4, 7, 6, 0.2))
    N.add('<path d="%s" fill="%s" stroke="%s" stroke-width="2"/>' % (shell, N.linear(SHELL[0], SHELL[1], 0, 0, 1, 0), SHELL[2]))
    inner = 'M%d,%d C%d,%d %d,%d %d,%d C%d,%d %d,%d %d,%d Z' % (hx + 134, hy - 90, hx + 200, hy - 92, hx + 238, hy - 56, hx + 240, hy,
                                                               hx + 238, hy + 56, hx + 200, hy + 92, hx + 134, hy + 90)
    N.add('<path d="%s" fill="#2a2e34"/>' % inner)
    N.add('<rect x="%d" y="%d" width="6" height="200" fill="#8a8f97" opacity="0.5"/>' % (hx + 132, hy - 100))  # acoustic mesh
    # driver: magnet, voice coil, cone-shaped diaphragm
    dx = hx + 150
    N.add('<path d="%s" fill="%s" stroke="%s" stroke-width="1.2"/>' % (rrect(dx + 22, hy - 22, 26, 44, 4), N.linear(*MAGNET[:2]), MAGNET[2]))
    N.add('<rect x="%d" y="%d" width="6" height="30" fill="#c77d3a"/>' % (dx + 16, hy - 15))
    N.add('<path d="M%d,%d L%d,%d L%d,%d L%d,%d Z" fill="%s" stroke="%s" stroke-width="1.2"/>' % (dx + 18, hy - 16, dx + 2, hy - 46, dx + 2, hy + 46, dx + 18, hy + 16, N.linear(DIAPH[0], DIAPH[1], 0, 0, 1, 0), DIAPH[2]))
    N.add('<path d="M%d,%d V%d" stroke="%s" stroke-width="3"/>' % (dx + 2, hy - 50, hy + 50, SHELL[2]))
    N.mark('driver', dx + 6, hy - 30)
    # feedback mic in front of the driver, feedforward mic on the outside of the shell
    N.add(N.ball(hx + 142, hy + 34, 5, cols=MIC, stroke=MIC[2], sw=1, shadow=0.1, gloss=0.4))
    N.mark('fbmic', hx + 142, hy + 34)
    N.add(N.ball(hx + 248, hy - 40, 5, cols=MIC, stroke=MIC[2], sw=1, shadow=0.1, gloss=0.4))
    N.mark('ffmic', hx + 250, hy - 40)
    # electronics: ANC chip on a small board, battery
    N.add(N.slab(hx + 196, hy - 70, 34, 22, PCB, r=3, depth=3, shadow=0.1))
    N.add(N.chip(hx + 204, hy - 66, 16, 12))
    N.mark('chip', hx + 212, hy - 60)
    N.add(N.slab(hx + 196, hy + 44, 32, 28, BATT, r=4, depth=3, shadow=0.1))
    N.mark('batt', hx + 212, hy + 58)
    N.mark('cushion', hx + 112, hy + 70)
    N.mark('canal', hx + 50, hy + 2)
    b.append(N.group(0, 0, 1))
    labels = [('ffmic', 'Outer microphone', 'hears noise arriving', 76), ('chip', 'ANC chip', 'flips and times the wave', 136), ('driver', 'Speaker driver', 'plays music + anti-noise', 196),
              ('fbmic', 'Inner microphone', 'checks what is left', 256), ('batt', 'Battery', 'powers the electronics', 316), ('cushion', 'Ear cushion', 'seals out high sounds', 376)]
    for key, name, what, y in labels:
        mx, my = N.at(key)
        b.append('<path d="M%.1f %.1f L520 %d H528" fill="none" stroke="var(--ink)" stroke-width="0.9"/>' % (mx, my, y - 4))
        b.append(dot(mx, my, 2.6, 'ink'))
        b += [T(532, y, name, 13, 600), T(532, y + 17, what, 11.5, 400, 'muted')]
    cx_, cy_ = N.at('canal')
    b.append('<path d="M%.1f %.1f L60 470" fill="none" stroke="var(--ink)" stroke-width="0.9"/>' % (cx_, cy_))
    b.append(dot(cx_, cy_, 2.6, 'ink'))
    b += [T(24, 488, 'Ear canal', 13, 600), T(24, 505, 'where the two waves meet', 11.5, 400, 'muted')]
    b.append(T(24, 540, 'cut through an over-ear headphone · simplified, not to scale', 11.5, 400, 'muted'))
    return svg(550, title, 'Cutaway of an over-ear noise-cancelling headphone on a head: an outer microphone on the shell hears noise arriving, an ANC chip flips and times the signal, the speaker driver plays music plus anti-noise, an inner microphone in front of the driver checks what is left, a battery powers it, and the cushion seals out high-pitched sound. The two waves meet in the ear canal.', b, N.defs())


# ---------------------------------------------------------------- 2. the cancelling loop
def loop():
    title = 'The anti-noise is the same wave, flipped and on time'
    b = []
    heads = [('1 · Noise arrives', 'engine hum, ~100 Hz'), ('2 · Chip flips it', 'same shape, upside down'), ('3 · They add up', 'peak + valley ≈ 0')]
    for k, (h, sub) in enumerate(heads):
        x = 24 + k * 244
        b.append(R(x, 52, 224, 170, 'edge', 1.25))
        b += [T(x + 16, 76, h, 13, 600), T(x + 16, 208, sub, 11.5, 400, 'muted')]
        if k < 2:
            b.append('<path d="M%d 131 l6 6 l-6 6" fill="none" stroke="var(--muted)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>' % (x + 231))
    b.append(wave(40, 140, 192, 36, 0, 'ink'))
    b.append(wave(284, 140, 192, 36, 0, 'ink', 1.2, '3 3'))
    b.append(wave(284, 140, 192, 36, math.pi, 'focus', 2.5))
    b.append(wave(528, 140, 192, 36, 0, 'line', 1, '3 3'))
    b.append(wave(528, 140, 192, 36, math.pi, 'line', 1, '3 3'))
    b.append(wave(528, 140, 192, 3, 0.6, 'good', 2.5, cycles=2.5))
    b.append(L(24, 246, 736, 246))
    b.append(T(24, 274, 'Every few microseconds, around a loop', 14, 600))
    boxes = [('Outer mic', 'samples the noise', 24), ('ANC chip', 'invert, filter, delay', 212), ('Speaker', 'adds anti-noise', 400), ('Inner mic', 'measures the rest', 588)]
    for name, what, x in boxes:
        b.append(R(x, 292, 148, 58, 'focus' if name == 'ANC chip' else 'edge', 1.5, 'focus' if name == 'ANC chip' else None, 0.08))
        b += [T(x + 14, 316, name, 13, 600), T(x + 14, 334, what, 11.5, 400, 'muted')]
    for x in (172, 360, 548):
        b.append(P('M%d 321 H%d' % (x + 2, x + 34), 'edge', 1.5))
        b.append('<path d="M%d 317.5 L%d 321 L%d 324.5 Z" fill="var(--edge)"/>' % (x + 34, x + 40, x + 34))
    b.append(P('M662 350 V376 H286 V356', 'focus', 1.5, '5 4'))
    b.append('<path d="M282.5 356 L286 350 L289.5 356 Z" fill="var(--focus)"/>')
    b.append(T(474, 392, 'correction: adjust until the ear hears silence', 11.5, 600, 'focus', 'middle'))
    b.append(legend_waves(24, 424))
    return svg(436, title, 'Three panels: a low engine hum arrives; the chip makes the same wave upside down; added together, peaks meet valleys and almost nothing is left. The loop: the outer microphone samples the noise, the chip inverts, filters and delays it, the speaker adds the anti-noise, and the inner microphone measures what is left so the chip can correct itself.', b)


def legend_waves(x, y):
    out = []
    for c, lab, dash in (('ink', 'noise', None), ('focus', 'anti-noise', None), ('good', 'what you hear', None)):
        out.append(P('M%d %d h22' % (x, y - 4), c, 2.5, dash))
        out.append(T(x + 30, y, lab, 11.5, 400, 'muted'))
        x += 30 + len(lab) * 6.4 + 26
    return ''.join(out)


# ---------------------------------------------------------------- 3. three designs
def designs():
    title = 'Where the microphone sits decides what it can fix'
    N = Obj('k20261120-anc-types')
    b = []
    cols = [('Feedforward', 'mic outside the cup', (True, False), [('hears noise early', 'good'), ('can’t hear what reaches the ear', 'warn'), ('picks up wind', 'bad')]),
            ('Feedback', 'mic inside the cup', (False, True), [('hears what you hear', 'good'), ('corrects fit and leaks', 'good'), ('can ring if pushed', 'warn')]),
            ('Hybrid', 'both microphones', (True, True), [('widest frequency range', 'good'), ('fewer artefacts', 'good'), ('costs more power', 'warn')])]
    for i, (name, sub, (ff, fb), pros) in enumerate(cols):
        x = 24 + i * 244
        foc = name == 'Hybrid'
        b.append(R(x, 52, 224, 306, 'focus' if foc else 'edge', 2 if foc else 1.25, 'focus' if foc else None, 0.06))
        b += [T(x + 16, 76, name, 13, 600), T(x + 16, 94, sub, 11.5, 400, 'muted')]
        cx, cy = x + 112, 170
        cup = 'M%d,%d C%d,%d %d,%d %d,%d C%d,%d %d,%d %d,%d Z' % (cx - 40, cy - 52, cx + 10, cy - 54, cx + 40, cy - 30, cx + 42, cy, cx + 40, cy + 30, cx + 10, cy + 54, cx - 40, cy + 52)
        N.add(N.shadow(cup, 3, 5, 4, 0.18))
        N.add('<path d="%s" fill="%s" stroke="%s" stroke-width="1.6"/>' % (cup, N.linear(SHELL[0], SHELL[1], 0, 0, 1, 0), SHELL[2]))
        N.add('<path d="%s" fill="%s" stroke="%s" stroke-width="1"/>' % (rrect(cx - 52, cy - 52, 14, 104, 6), N.linear(CUSHION[0], CUSHION[1]), CUSHION[2]))
        N.add('<path d="M%d,%d L%d,%d L%d,%d L%d,%d Z" fill="%s" stroke="%s" stroke-width="1"/>' % (cx - 10, cy - 10, cx - 24, cy - 30, cx - 24, cy + 30, cx - 10, cy + 10, DIAPH[1], DIAPH[2]))
        if ff:
            N.add(N.ball(cx + 40, cy - 22, 6, cols=MIC, stroke=MIC[2], sw=1, shadow=0.1, gloss=0.4))
            b.append(circ(cx + 40, cy - 22, 11, 'focus', None, 0, 2))
        if fb:
            N.add(N.ball(cx - 32, cy + 22, 6, cols=MIC, stroke=MIC[2], sw=1, shadow=0.1, gloss=0.4))
            b.append(circ(cx - 32, cy + 22, 11, 'focus', None, 0, 2))
        b.append(P('M%d %d h-26' % (cx + 90, cy - 22), 'ink', 1.5))
        b.append('<path d="M%d %.1f L%d %d L%d %.1f Z" fill="var(--ink)"/>' % (cx + 64, cy - 25.5, cx + 58, cy - 22, cx + 64, cy - 18.5))
        b.append(T(cx + 92, cy - 30, 'noise', 11.5, 400, 'muted', 'end'))
        for k, (txt, c) in enumerate(pros):
            y = 258 + k * 28
            b.append(dot(x + 22, y - 4, 5, c))
            b.append(T(x + 34, y, txt, 11.5, 400))
    b.insert(0, N.group(0, 0, 1))
    b.append('<circle cx="30" cy="378" r="7" fill="none" stroke="var(--focus)" stroke-width="2"/>')
    b.append(T(44, 382, 'microphone', 11.5, 400, 'muted'))
    lx = 140
    for c, lab in (('good', 'strength'), ('warn', 'limit'), ('bad', 'weakness')):
        b.append(dot(lx + 6, 378, 5, c))
        b.append(T(lx + 18, 382, lab, 11.5, 400, 'muted'))
        lx += 100
    return svg(394, title, 'Three designs. Feedforward: the microphone is outside the cup, hears noise early but cannot hear what reaches the ear and picks up wind. Feedback: the microphone is inside, hears what you hear and corrects for fit, but can ring if pushed. Hybrid: both microphones, the widest frequency range and fewer artefacts, at the cost of power.', b, N.defs())


# ---------------------------------------------------------------- 4. why low sounds cancel best
def physics():
    title = 'A tiny delay ruins cancellation at high pitch'
    delay = 50e-6
    X = lambda f: 120 + (math.log10(f) - math.log10(20)) / (math.log10(20000) - math.log10(20)) * 560
    def red(f):
        phi = 2 * math.pi * f * delay
        return -20 * math.log10(max(2 * math.sin(phi / 2), 1e-6))
    Y = lambda db: 230 - db / 40 * 150
    b = [T(24, 62, 'NOISE REMOVED IF THE ANTI-NOISE IS 50 µs LATE', 11.5, 600, 'muted')]
    for db in (0, 10, 20, 30, 40):
        b.append(L(120, Y(db), 680, Y(db), 'line', 1))
        b.append(T(112, Y(db) + 4, '%d dB' % db, 11.5, 400, 'muted', 'end'))
    pts = []
    f = 20.0
    while f <= 20000:
        d = red(f)
        if d < -2:
            break
        pts.append((X(f), Y(max(min(d, 40), -6))))
        f *= 1.05
    b.append(P('M' + ' L'.join('%.1f %.1f' % p for p in pts), 'focus', 2.5))
    fz = 1 / (6 * delay)
    b.append(L(X(fz), Y(0) - 4, X(fz), 236, 'bad', 1.25, '4 3'))
    b.append(T(X(fz) + 6, Y(0) - 8, 'above ~3.3 kHz it adds noise', 11.5, 600, 'bad'))
    for f, lab in ((20, '20 Hz'), (100, '100 Hz'), (1000, '1 kHz'), (10000, '10 kHz')):
        b.append(T(X(f), 252, lab, 11.5, 400, 'muted', 'middle'))
    for f, lab in ((100, 'engine hum'), (1000, 'voices')):
        b.append(dot(X(f), Y(red(f)), 5, 'focus'))
        b.append(T(X(f) + 8, Y(red(f)) - 8, '%s · %d dB' % (lab, round(red(f))), 11.5, 600))
    b.append(L(24, 278, 736, 278))
    b.append(T(24, 306, 'Why: the same delay is a bigger slice of a short wave', 14, 600))
    rows = [(100, 'engine hum'), (1000, 'speech'), (5000, 'a hiss')]
    for i, (f, lab) in enumerate(rows):
        y = 336 + i * 44
        per = 1000 / f
        b += [T(24, y + 4, '%s Hz' % ('{:,}'.format(f)), 13, 600), T(24, y + 20, lab, 11.5, 400, 'muted')]
        w = per / 10 * 400
        b.append('<rect x="160" y="%d" width="%.1f" height="16" rx="3" fill="var(--edge)" fill-opacity="0.2" stroke="var(--edge)" stroke-width="1.25"/>' % (y - 8, w))
        dw = 0.05 / 10 * 400
        b.append('<rect x="160" y="%d" width="%.1f" height="16" rx="2" fill="var(--bad)" fill-opacity="0.5" stroke="var(--bad)" stroke-width="1"/>' % (y - 8, max(dw, 2)))
        b.append(T(160 + w + 8, y + 5, '%g%% of the wave' % round(0.05 / per * 100, 1), 11.5, 600, 'bad'))
        b.append(T(160, y + 22, 'one wave lasts %g ms' % per, 11.5, 400, 'muted'))
    b.append(T(24, 482, 'red = 50 µs of delay · reduction = −20·log₁₀(2·sin(φ/2)), φ = phase error · physics, not a measurement', 11.5, 400, 'muted'))
    return svg(492, title, 'With a 50 microsecond timing error, cancellation removes about 30 dB at 100 Hz, about 10 dB at 1 kHz and nothing above about 3.3 kHz, where it starts adding noise. The same delay is 0.5% of a 100 Hz wave, 5% of a 1 kHz wave and 25% of a 5 kHz wave.', b)


def coverage():
    title = 'ANC takes the lows, the ear cushion the highs'
    X = lambda f: 120 + (math.log10(f) - math.log10(20)) / 3 * 560
    b = [T(24, 62, 'NOISE REDUCTION BY FREQUENCY, ILLUSTRATIVE SHAPE', 11.5, 600, 'muted')]
    base = 230
    anc = [(f, 120 * math.exp(-((math.log10(f) - 2.2) / 0.55) ** 2)) for f in [20 * 1.08 ** k for k in range(90)] if f <= 20000]
    pas = [(f, 120 / (1 + math.exp(-(math.log10(f) - 3.0) * 4))) for f in [20 * 1.08 ** k for k in range(90)] if f <= 20000]
    for pts, c in ((pas, 'k2'), (anc, 'focus')):
        d = 'M%.1f %d ' % (X(20), base) + ' '.join('L%.1f %.1f' % (X(f), base - v) for f, v in pts) + ' L%.1f %d Z' % (X(pts[-1][0]), base)
        b.append('<path d="%s" fill="var(--%s)" fill-opacity="0.25" stroke="var(--%s)" stroke-width="2"/>' % (d, c, c))
    b.append(L(120, base, 680, base, 'edge', 1))
    for f, lab in ((20, '20 Hz'), (100, '100 Hz'), (1000, '1 kHz'), (10000, '10 kHz')):
        b.append(T(X(f), base + 18, lab, 11.5, 400, 'muted', 'middle'))
    b += [T(X(160), base - 128, 'active (ANC)', 13, 600, 'focus', 'middle'), T(X(6000), base - 128, 'passive (cushion, shell)', 13, 600, 'k2', 'middle')]
    b.append(T(24, base + 46, 'measured curves vary by model; the crossover sits around 1 kHz', 11.5, 400, 'muted'))
    return svg(base + 56, title, 'Active cancellation works on low frequencies, peaking around 100 to 300 Hz and fading towards 1 kHz; the passive seal of the cushion and shell blocks more and more above about 1 kHz. Together they cover the range. Illustrative shape; measured curves vary by model.', b)


# ---------------------------------------------------------------- 5. real sounds
def sounds():
    title = 'Steady rumbles disappear, sudden and high sounds get through'
    rows = [('Plane cabin', 'steady low roar', 5, 'good'), ('Train, bus', 'rumble', 5, 'good'), ('Air conditioner', 'steady hum', 4, 'good'),
            ('Office chatter', 'mid, changing', 3, 'warn'), ('Keyboard clicks', 'sharp, high', 2, 'warn'), ('Baby crying', 'high, changing', 2, 'warn'), ('Door slam', 'sudden', 1, 'bad')]
    b = [T(24, 62, 'SOUND', 11.5, 600, 'muted'), T(500, 62, 'HOW MUCH YOU STOP HEARING', 11.5, 600, 'muted')]
    for i, (n, d, r, c) in enumerate(rows):
        y = 92 + i * 34
        b += [dot(30, y - 4, 6, c), T(46, y, n, 13, 600), T(200, y, d, 11.5, 400, 'muted')]
        for k in range(5):
            b.append(circ(506 + k * 16, y - 4, 6, c, c if k < r else None, 1 if k < r else 0, 1.25))
        b.append(L(24, y + 14, 736, y + 14))
    yl = 92 + len(rows) * 34 + 12
    lx = 24
    for c, lab in (('good', 'mostly removed'), ('warn', 'partly'), ('bad', 'barely')):
        b.append(dot(lx + 6, yl - 4, 6, c))
        b.append(T(lx + 18, yl, lab, 11.5, 400, 'muted'))
        lx += 130
    b.append(T(24, yl + 24, 'combined effect of ANC and the passive seal; ratings out of 5, a summary of the sources, not a lab test', 11.5, 400, 'muted'))
    return svg(yl + 34, title, 'Plane cabin, train and air conditioner: mostly removed. Office chatter, keyboard clicks and a baby crying: partly. A door slam: barely.', b)


# ---------------------------------------------------------------- 6. history
EVENTS = [(1934, 'Paul Lueg', 'patent: cancel sound with sound', 0), (1953, 'Olson & May', 'electronic sound absorber', 2),
          (1978, 'Amar Bose', 'idea on a noisy flight', 1), (1986, 'Voyager', 'non-stop round-the-world flight with ANC headsets', 3),
          (1989, 'First headset on sale', 'for pilots, after 10 years', 0)]


def history():
    title = 'From a 1934 patent to pilots’ headsets'
    X = lambda y: 60 + (y - 1930) / 70 * 640
    axis = 132
    levels = {0: 62, 1: 100, 2: 172, 3: 210}
    b = [L(X(1930), axis, X(2000), axis, 'edge', 1.5)]
    for yr, who, what, lv in EVENTS:
        ty = levels[lv]
        end = yr >= 1978
        b.append(L(X(yr), axis, X(yr), ty + 18 if lv < 2 else ty - 12, 'focus', 1.25))
        b.append(dot(X(yr), axis, 6, 'focus'))
        tx = X(yr) + (-8 if end else 8)
        b.append(T(tx, ty, '%d · %s' % (yr, who), 13, 600, 'ink', 'end' if end else None))
        b.append(T(tx, ty + 16, what, 11.5, 400, 'muted', 'end' if end else None))
    for yr in (1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000):
        b.append(T(X(yr), 256, str(yr), 11.5, 400, 'muted', 'middle' if yr < 2000 else 'end'))
    b.append(L(X(1930), 240, X(2000), 240, 'line', 1))
    return svg(268, title, 'History: Paul Lueg filed a patent for cancelling sound with sound in 1934 (granted in the US in 1936) but could not build it; Harry Olson and Everett May built an electronic sound absorber in 1953; Amar Bose had the idea for headphones on a noisy flight in 1978; Dick Rutan and Jeana Yeager flew non-stop around the world in 1986 wearing ANC headsets; the first commercial headset, for pilots, went on sale in 1989.', b)


# ---------------------------------------------------------------- the example
PROMPT = ('How do noise-cancelling headphones work? Show what is inside one, how the cancelling works step by step, '
          'the difference between feedforward, feedback and hybrid designs, which sounds it removes and why, and a short history. '
          'Research it, then build the document.')
LINE = 'Microphones hear the noise, a chip plays the same wave upside down, and the two cancel in your ear; it works best on low, steady sounds.'


def example():
    cut = cutaway()
    sources = ('- Wikipedia, *Active noise control*; Acoustical Society of America, *Active noise control* (147th meeting press room): Lueg\'s patent (US 2,043,416, 1936), the 1986 Voyager flight, the first commercial headset in 1989.\n'
               '- H. G. Leventhall, *Active attenuators: a historical review and some recent developments* (Institute of Acoustics): Olson and May\'s electronic sound absorber, 1953.\n'
               '- University of Alaska Fairbanks, *The history of active noise control*: Amar Bose\'s 1978 flight.\n'
               '- SoundGuys, *What is active noise cancellation*: feedforward, feedback and hybrid designs, their strengths and weaknesses.\n'
               '- Rivera, Nowak and Zölzer (2017), *Evaluation of a decoupled feedforward-feedback hybrid structure for active noise control*: hybrid ANC coverage.\n'
               '- Phase-error formula: standard result for adding two equal sine waves; the 50 µs delay is an example value.')
    pdf = dict(title='How noise-cancelling headphones work', subtitle='Inside the ear cup, the cancelling loop, the three designs, the physics and the history', cards=[
        dict(type='drawing', title='', data=[cut]),
        dict(type='drawing', title='', data=[loop()]),
        dict(type='drawing', title='', data=[designs()]),
        dict(type='drawing', title='', data=[physics()]),
        dict(type='drawing', title='', data=[coverage()]),
        dict(type='drawing', title='', data=[sounds()]),
        dict(type='drawing', title='', data=[history()]),
        dict(type='markdown', title='Sources', data=sources)])
    return dict(slug='headphones', kind='Research', title='How noise-cancelling headphones work', prompt=PROMPT, question=PROMPT, line=LINE,
                chat=[cut], pdf=pdf, drawings=[c['data'][0] for c in pdf['cards'] if c['type'] == 'drawing'])
