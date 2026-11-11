import json
def T(x,y,s,sz=13,w=400,c='ink',a=None,caps=False):
    an=f' text-anchor="{a}"' if a else ''
    return f'<text x="{x}" y="{y}" font-size="{sz}" font-weight="{w}" fill="var(--{c})"{an}>{s}</text>'
def R(x,y,w,h,c='edge',sw=1.5,fill=None,op=0.12,rx=8,dash=None):
    f=f'fill="var(--{fill})" fill-opacity="{op}"' if fill else 'fill="none"'
    d=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" {f} stroke="var(--{c})" stroke-width="{sw}"{d}/>'
def L(x1,y1,x2,y2,c='line',sw=1,dash=None):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="var(--{c})" stroke-width="{sw}"{d}/>'
def arrow(x1,y,x2,c='edge',sw=1.5,dash=None):  # horizontal
    d=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<path d="M{x1} {y} H{x2-6}" stroke="var(--{c})" stroke-width="{sw}" fill="none"{d}/><path d="M{x2-6} {y-3.5} L{x2} {y} L{x2-6} {y+3.5} Z" fill="var(--{c})"/>'
def varrow(x,y1,y2,c='edge',sw=1.5,dash=None):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<path d="M{x} {y1} V{y2-6}" stroke="var(--{c})" stroke-width="{sw}" fill="none"{d}/><path d="M{x-3.5} {y2-6} L{x} {y2} L{x+3.5} {y2-6} Z" fill="var(--{c})"/>'
def chev(x,y): return f'<path d="M{x-4} {y-7} L{x+3} {y} L{x-4} {y+7}" stroke="var(--muted)" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
def svg(h,title,desc,body):
    return f'<svg viewBox="0 0 760 {h}" width="100%" font-size="13" role="img" aria-label="{title}"><title>{title}</title><desc>{desc}</desc>{T(24,30,title,15,600)}{"".join(body)}</svg>'

def circ(cx,cy,r,c='edge',fill=None,op=0.18,sw=1.5,dash=None):
    f=f'fill="var(--{fill})" fill-opacity="{op}"' if fill else 'fill="none"'
    d=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" {f} stroke="var(--{c})" stroke-width="{sw}"{d}/>'
def dot(cx,cy,r,c): return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="var(--{c})"/>'
def P(d,c='edge',sw=1.5,dash=None,fill='none'):
    dd=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<path d="{d}" stroke="var(--{c})" stroke-width="{sw}" fill="{fill}" stroke-linecap="round" stroke-linejoin="round"{dd}/>'
def check(x,y,c='tamam'): return P(f'M{x} {y} l4 4 l8 -9',c,2)
def cross(x,y,c='risk'): return P(f'M{x} {y} l9 9 M{x+9} {y} l-9 9',c,2)
def svgw(w,h,title,desc,body,id=''):
    return f'<svg viewBox="0 0 {w} {h}" width="100%" font-size="13" role="img" aria-label="{title}"><title>{title}</title><desc>{desc}</desc>{T(24,30,title,15,600)}{"".join(body)}</svg>'
