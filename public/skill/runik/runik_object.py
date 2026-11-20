# runik_object.py - shaded SVG helpers for drawing REAL OBJECTS in Runik drawings.
# Adapted from Visual Explainer's (vxart.py) drawing technique: light from the top left, soft shadow,
# stroke in the dark shade of the fill, grain texture. Difference: every id carries a drawing-specific
# prefix (the board shows many SVGs on one page) and the output is a <defs> + <g> fragment embedded in a Runik SVG.
#
#   from runik_object import Obj, pol, blob, smooth, rrect, capsule
#   N = Obj("k20261118-board")                       # prefix: unique to this drawing, kebab-case
#   N.add(N.slab(40, 60, 300, 200, N.PCB))           # draw the object (in its own coordinates)
#   N.mark("cpu", 120, 140)                          # remember a point to label
#   defs, g = N.defs(), N.group(x=24, y=50, scale=0.7)   # embed into the Runik SVG
#   N.at("cpu")  -> (x, y) position on the Runik canvas (for labels and leader lines)
#
# Color: the object's own natural color (circuit board green, mountain brown and snow, case metal). Runik meaning
# colors (--good/--warn/--bad/--focus) never paint the object's body; only the marks placed on top of it.
import math, random

NL = chr(10)

# Natural material palettes: (light, mid, dark). Dark = stroke and shaded face.
PCB = ("#5e9f7a", "#3c7d58", "#24553a")
METAL = ("#f7f8fa", "#d3d8de", "#8d96a2")
DARK = ("#59606b", "#353a42", "#1b1e22")
PAPER = ("#ffffff", "#f3f1ea", "#b7ae98")
ROCK = ("#d9c3a0", "#a9875c", "#6e5434")
STONE = ("#f6f3ee", "#ddd6ca", "#9a8f7d")
GOLD = ("#fff1c4", "#f0b93b", "#a8730f")
WOOD = ("#f1d3a6", "#c9955a", "#8a5a2b")
GLASS = ("#f2f8fd", "#cfe3f3", "#7fa6c9")
SKIN = ("#fde3cf", "#f2b892", "#b9785a")
LEAF = ("#cfe8b8", "#7fb35a", "#3f6e2a")
WATER = ("#e4f0fa", "#bcd6ee", "#7fa6c9")
SAND = ("#f6efdd", "#e6d6b0", "#a8916a")
SHADOW = "#2b1c0e"


def pol(cx, cy, r, deg, ry=None):
    a = math.radians(deg)
    return (cx + r * math.cos(a), cy + (r if ry is None else ry) * math.sin(a))


def blob(cx, cy, rx, ry, n=14, jitter=0.05, seed=1, rot=0.0):
    rnd = random.Random(seed)
    return [(cx + rx * k * math.cos(rot + 2 * math.pi * i / n), cy + ry * k * math.sin(rot + 2 * math.pi * i / n))
            for i, k in ((i, 1 + rnd.uniform(-jitter, jitter)) for i in range(n))]


def smooth(pts, closed=True, t=0.5):
    n = len(pts)
    d = 'M%.1f,%.1f' % tuple(pts[0])
    for i in range(n if closed else n - 1):
        if closed:
            p0, p1, p2, p3 = pts[(i - 1) % n], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        else:
            p0, p1, p2, p3 = pts[max(i - 1, 0)], pts[i], pts[i + 1], pts[min(i + 2, n - 1)]
        d += ' C%.1f,%.1f %.1f,%.1f %.1f,%.1f' % (p1[0] + (p2[0] - p0[0]) * t / 3, p1[1] + (p2[1] - p0[1]) * t / 3,
                                                  p2[0] - (p3[0] - p1[0]) * t / 3, p2[1] - (p3[1] - p1[1]) * t / 3, p2[0], p2[1])
    return d + ('Z' if closed else '')


def rrect(x, y, w, h, r=8):
    r = min(r, w / 2.0, h / 2.0)
    arc = 'a%g,%g 0 0 1' % (r, r)
    return 'M%.1f,%.1f h%.1f %s %g,%g v%.1f %s %g,%g h%.1f %s %g,%g v%.1f %s %g,%g Z' % (
        x + r, y, w - 2 * r, arc, r, r, h - 2 * r, arc, -r, r, 2 * r - w, arc, -r, -r, 2 * r - h, arc, r, -r)


def capsule(L, W):
    r = W / 2.0
    return 'M%.1f,%.1f h%.1f a%.1f,%.1f 0 0 1 0,%.1f h%.1f a%.1f,%.1f 0 0 1 0,%.1f Z' % (r - L / 2.0, -r, L - W, r, r, W, W - L, r, r, -W)


class Obj:
    '''One real-object drawing. Coordinates are in the object's own units; group() places it on the Runik canvas.'''
    PCB, METAL, DARK, PAPER, ROCK, STONE, GOLD, WOOD, GLASS, SKIN, LEAF, WATER, SAND = PCB, METAL, DARK, PAPER, ROCK, STONE, GOLD, WOOD, GLASS, SKIN, LEAF, WATER, SAND

    def __init__(self, prefix):
        self.p, self._defs, self.body, self.ids, self.marks = prefix, [], [], {}, {}
        self._tf = (0, 0, 1)
        self.w = self.h = None

    def id(self, name):
        return '%s-%s' % (self.p, name)

    def _def(self, key, xml):
        if key not in self.ids:
            self.ids[key] = self.id('d%d' % len(self.ids))
            self._defs.append(xml.replace('@ID', self.ids[key]))
        return 'url(#%s)' % self.ids[key]

    def blur(self, n):
        '''n: 2, 4, 8 or 14. filter="%s" % N.blur(4)'''
        return self._def(('b', n), '<filter id="@ID" x="-30%%" y="-30%%" width="160%%" height="160%%"><feGaussianBlur stdDeviation="%d"/></filter>' % n)

    def radial(self, light, mid, dark, fx=0.36, fy=0.30, r=0.78):
        return self._def(('r', light, mid, dark, fx, fy, r),
                         '<radialGradient id="@ID" cx="50%%" cy="50%%" fx="%g%%" fy="%g%%" r="%g%%"><stop offset="0" stop-color="%s"/>'
                         '<stop offset="0.55" stop-color="%s"/><stop offset="1" stop-color="%s"/></radialGradient>' % (fx * 100, fy * 100, r * 100, light, mid, dark))

    def linear(self, c0, c1, x1=0, y1=0, x2=0, y2=1):
        return self._def(('l', c0, c1, x1, y1, x2, y2), '<linearGradient id="@ID" x1="%g" y1="%g" x2="%g" y2="%g"><stop offset="0" stop-color="%s"/>'
                         '<stop offset="1" stop-color="%s"/></linearGradient>' % (x1, y1, x2, y2, c0, c1))

    def clip(self, d):
        return self._def(('c', d), '<clipPath id="@ID"><path d="%s"/></clipPath>' % d)

    def add(self, *xml):
        self.body.extend(xml)

    def mark(self, name, x, y):
        self.marks[name] = (x, y)

    # ---- building blocks (each returns SVG text)
    def shadow(self, d, dx=4, dy=7, blur=4, opacity=0.25, w=0):
        paint = ('fill="none" stroke="%s" stroke-width="%g" stroke-linecap="round"' % (SHADOW, w)) if w else 'fill="%s"' % SHADOW
        return '<path d="%s" %s opacity="%g" filter="%s" transform="translate(%g %g)"/>' % (d, paint, opacity, self.blur(blur), dx, dy)

    def ball(self, cx, cy, rx, ry=None, cols=METAL, stroke=None, sw=2.0, shadow=0.26, gloss=0.5):
        ry = ry or rx
        o = ''
        if shadow:
            o += '<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" opacity="%g" filter="%s"/>' % (cx + rx * 0.1 + 2, cy + ry * 0.16 + 3, rx, ry, SHADOW, shadow, self.blur(4))
        o += '<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s"%s/>' % (cx, cy, rx, ry, self.radial(*cols), (' stroke="%s" stroke-width="%g"' % (stroke, sw)) if stroke else '')
        if gloss:
            o += '<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#fff" opacity="%g" filter="%s" transform="rotate(-28 %.1f %.1f)"/>' % (
                cx - rx * 0.3, cy - ry * 0.4, rx * 0.36, ry * 0.17, gloss, self.blur(2), cx - rx * 0.3, cy - ry * 0.4)
        return o

    def slab(self, x, y, w, h, cols=METAL, r=8, depth=8, shadow=0.24):
        '''Solid block seen slightly from above: board, chip, plate, case, battery.'''
        top, side = rrect(x, y, w, h, r), rrect(x, y + depth, w, h, r)
        o = '<path d="%s" fill="%s" opacity="%g" filter="%s" transform="translate(5 9)"/>' % (side, SHADOW, shadow, self.blur(8)) if shadow else ''
        o += '<path d="%s" fill="%s"/>' % (side, cols[2]) if depth else ''
        o += '<path d="%s" fill="%s" stroke="%s" stroke-width="1.5"/>' % (top, self.linear(cols[0], cols[1]), cols[2])
        return o + '<path d="M%.1f,%.1f h%.1f" stroke="#fff" stroke-width="2" stroke-linecap="round" opacity="0.65"/>' % (x + r, y + 3, w - 2 * r)

    def layers(self, x, y, w, rows, depth=70, shadow=0.24):
        '''Layered cross-section (board, battery, skin, wall, ground). rows=[(thickness, palette), ...] top to bottom.'''
        dx, dy, H, c = depth * 0.8, depth * 0.5, sum(r[0] for r in rows), rows[0][1]
        o = '<path d="M%.1f,%.1f l%.1f,%.1f h%.1f v%.1f l%.1f,%.1f h%.1f Z" fill="%s" opacity="%g" filter="%s" transform="translate(6 10)"/>' % (
            x, y, dx, -dy, w, H, -dx, dy, -w, SHADOW, shadow, self.blur(8)) if shadow else ''
        o += '<path d="M%.1f,%.1f l%.1f,%.1f h%.1f l%.1f,%.1f Z" fill="%s" stroke="%s" stroke-width="1.2"/>' % (x, y, dx, -dy, w, -dx, dy, self.linear(c[0], c[1], 0, 1, 1, 0), c[2])
        for t, c in rows:
            o += '<path d="M%.1f,%.1f h%.1f v%.1f h%.1f Z" fill="%s" stroke="%s" stroke-width="1.2"/>' % (x, y, w, t, -w, self.linear(c[0], c[1]), c[2])
            o += '<path d="M%.1f,%.1f l%.1f,%.1f v%.1f l%.1f,%.1f Z" fill="%s" stroke="%s" stroke-width="1"/>' % (x + w, y, dx, -dy, t, -dx, dy, c[2], c[2])
            y += t
        return o

    def tube(self, d, dark, light, w=14, inner=8):
        '''Pipe, cable, vessel, road.'''
        a = 'fill="none" stroke-linecap="round" stroke-linejoin="round"'
        return '<path d="%s" %s stroke="%s" stroke-width="%g"/><path d="%s" %s stroke="%s" stroke-width="%g"/>' % (d, a, dark, w, d, a, light, inner)

    def grain(self, clip_d, opacity=0.4):
        '''Takes the plastic look off a large flat fill; clip_d = the body's path.'''
        f = self._def(('g',), '<filter id="@ID" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="7" result="n"/>'
                      '<feColorMatrix in="n" type="matrix" values="0 0 0 0 0.35  0 0 0 0 0.22  0 0 0 0 0.10  0 0 0 0.55 -0.12"/></filter>')
        return '<rect x="-2000" y="-2000" width="6000" height="6000" fill="none" filter="%s" opacity="%g" clip-path="%s"/>' % (f, opacity, self.clip(clip_d))

    def chip(self, x, y, w, h):
        return self.slab(x, y, w, h, DARK, r=3, depth=3, shadow=0.15)

    def peak(self, x, y, H, wf=1.0, snow=True):
        '''Mountain: (x, y) base center, H height. Jagged ridge + secondary summit + shaded face + snow.'''
        pts = [(-0.68, 0), (-0.4, -0.5), (-0.3, -0.42), (-0.1, -0.82), (0, -1), (0.17, -0.66), (0.27, -0.74), (0.68, 0)]
        P = lambda ps: 'M' + ' L'.join('%.1f,%.1f' % (x + a * H * wf, y + b * H) for a, b in ps) + 'Z'
        body = P(pts)
        o = self.shadow(body, H * 0.04, H * 0.05, 4 if H > 60 else 2, 0.22)
        o += '<path d="%s" fill="%s" stroke="%s" stroke-width="%.1f" stroke-linejoin="round"/>' % (body, self.linear(ROCK[0], ROCK[1], 0, 0, 1, 0), ROCK[2], max(1, H * 0.012))
        o += '<path d="%s" fill="%s" opacity="0.35"/>' % (P([(0, -1), (0.17, -0.66), (0.27, -0.74), (0.68, 0), (0.05, 0)]), ROCK[2])
        if snow:
            o += '<path d="%s" fill="#fff" stroke="#c9d3de" stroke-width="%.1f" stroke-linejoin="round"/>' % (P([(-0.1, -0.82), (0, -1), (0.1, -0.84), (0.05, -0.76), (0, -0.8), (-0.05, -0.72)]), max(0.8, H * 0.008))
        return o

    def laptop(self, x, y, s=1.0):
        w, h = 150 * s, 96 * s
        o = self.slab(x, y, w, h, DARK, r=8 * s, depth=4, shadow=0.2)
        o += '<path d="%s" fill="%s"/>' % (rrect(x + 8 * s, y + 8 * s, w - 16 * s, h - 18 * s, 4), self.linear("#f5f8fc", "#dfe7f1"))
        return o + self.slab(x - 18 * s, y + h + 2, w + 36 * s, 14 * s, METAL, r=5, depth=4, shadow=0.18)

    # ---- placing into a Runik SVG
    def defs(self):
        return ''.join(self._defs)

    def group(self, x=0, y=0, scale=1.0):
        self._tf = (x, y, scale)
        return '<g transform="translate(%g %g) scale(%g)">%s</g>' % (x, y, scale, ''.join(self.body))

    def at(self, name):
        '''Position of a marked point on the Runik canvas (after group() is called).'''
        x, y = self.marks[name]
        tx, ty, s = self._tf
        return (tx + x * s, ty + y * s)
