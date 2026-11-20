import json, math, os
from runik_svg import *
out={}
# ===== HERO: distance axis
b=[]
b.append(T(24,62,'DISTANCE FROM CPU = READ TIME',11.5,600,'muted'))
y0=150
b.append(L(80,y0,736,y0,'edge',1.5))
# actor CPU chip
b.append(R(24,y0-26,52,52,'ink',2,rx=6))
for k in range(4):
    b.append(L(32+k*12,y0-32,32+k*12,y0-26,'ink',1.5)); b.append(L(32+k*12,y0+26,32+k*12,y0+32,'ink',1.5))
b.append(T(50,y0+5,'CPU',11.5,600,'ink','middle'))
lv=[('L1','~1 ns','desk',1,'good'),('L2','~4 ns','drawer',4,'good'),('L3','~15 ns','shelf',15,'warn'),('RAM','~100 ns','room',100,'warn'),('SSD','~100 µs','another city',100000,'bad')]
def X(ns): return 130+math.log10(ns)/5*560
for n,lat,an,ns,c in lv:
    x=X(ns)
    b.append(circ(x,y0,13,c,c,0.18,2))
    b.append(T(x,y0-24,n,13,600,'ink','middle'))
    b.append(T(x,y0+34,lat,11.5,400,'ink','middle'))
    b.append(T(x,y0+52,an,11.5,400,'muted','middle'))
# how many times further
b.append(L(24,236,736,236))
b.append(T(24,262,'How much further is SSD than L1?',14,600))
# bars: 1 vs 100,000 (linear)
b.append(f'<rect x="24" y="280" width="2" height="14" rx="1" fill="var(--good)"/>'); b.append(T(34,292,'L1 · 1 ×',11.5,600))
b.append(f'<rect x="24" y="306" width="712" height="14" rx="3" fill="var(--bad)" fill-opacity="0.35" stroke="var(--bad)" stroke-width="1.5"/>')
b.append(T(730,317,'SSD · 100,000 ×',11.5,600,'ink','end'))
b.append(R(24,342,712,50,'good',2,'good',0.12))
b.append(T(40,364,'Keep hot data close',13,600)); b.append(T(40,382,'walk arrays in order · cache friendly',11.5))
b.append(T(24,414,'top axis log · bars below linear · times approximate',11.5,400,'muted'))
out['hero']=svgw(760,424,'Reads slow down sharply as data moves away',
 'Read time by distance from the CPU, log scale: L1 about 1 ns (desk), L2 4 ns (drawer), L3 15 ns (shelf), RAM 100 ns (room), SSD 100 µs (another city). SSD is 100,000 times slower than L1. Takeaway: keep hot data close.',b)

# ===== HOW: install flow (global skill)
b=[]
cols=[24,268,512]
heads=['1 · Copy','2 · Paste into Claude Code','3 · Claude installs']
for x,h in zip(cols,heads):
    b.append(R(x,52,224,150)); b.append(T(x+16,76,h,13,600))
x=24
b.append(R(x+16,90,192,96,'edge',1.25,rx=6)); b.append(L(x+16,106,x+208,106,'edge',1.25))
for k in range(3): b.append(dot(x+26+k*9,98,2.5,'edge'))
b.append(R(x+28,116,168,56,'focus',1.5,'focus',0.12,rx=4))
for k,wd in enumerate([110,130,80]): b.append(L(x+38,128+k*10,x+38+wd,128+k*10,'focus',2))
b.append(R(x+170,122,14,16,'ink',1.25,rx=2)); b.append(R(x+174,126,14,16,'ink',1.25,fill='surface',op=1,rx=2))
b.append(chev(256,127))
x=268
b.append(f'<path d="M{x+20} 96 h184 a6 6 0 0 1 6 6 v62 a6 6 0 0 1 -6 6 h-150 l-12 12 v-12 h-22 a6 6 0 0 1 -6 -6 v-62 a6 6 0 0 1 6 -6 z" fill="none" stroke="var(--edge)" stroke-width="1.25"/>')
b.append(R(x+30,108,164,50,'focus',1.5,'focus',0.12,rx=4))
for k,wd in enumerate([110,130,80]): b.append(L(x+40,120+k*10,x+40+wd,120+k*10,'focus',2))
b.append(chev(500,127))
x=512
for k,(n,d) in enumerate([('skill','global, ~/.claude'),('board','beside the chat'),('first card','installed ✓')]):
    yy=92+k*36
    b.append(R(x+16,yy,28,28,'good',1.5,'good',0.18,rx=4)); b.append(check(x+24,yy+13))
    b.append(T(x+54,yy+13,n,13,600)); b.append(T(x+54,yy+27,d,11.5,400,'muted'))
b.append(L(24,222,736,222))
b.append(T(24,248,'In every project',14,600))
b.append(R(24,272,132,92,'ink',2))
b.append(T(40,300,'any project',13,600)); b.append(T(40,318,'skill opens',11.5)); b.append(T(40,336,'no setup',11.5,400,'muted'))
src=[('rules','inside the skill','read once'),('one board','shared by all','same link'),('your language','every output','auto')]
for k,(n,d,lab) in enumerate(src):
    yy=264+k*38
    b.append(f'<path d="M156 318 C 190 318, 196 {yy+16}, 226 {yy+16}" stroke="var(--focus)" stroke-width="1.5" fill="none"/>')
    b.append(f'<path d="M226 {yy+12.5} L232 {yy+16} L226 {yy+19.5} Z" fill="var(--focus)"/>')
    b.append(R(234,yy,300,32,'focus',1.5,'focus',0.12,rx=6))
    b.append(T(250,yy+21,n,13,600)); b.append(T(390,yy+21,d,11.5,400,'ink'))
    b.append(T(548,yy+21,lab,11.5,600,'muted'))
b.append(R(24,384,712,52,'good',2,'good',0.12))
b.append(T(40,408,'Update: rerun install.sh → board kept',13,600))
b.append(T(40,425,'one command · same board',11.5))
out['nasil']=svgw(760,450,'Paste once, Runik works in every project',
 'Copy the install prompt and paste it into Claude Code; Claude installs the global runik skill in ~/.claude/skills, creates the board beside the chat and writes the first card. In every project the skill opens with its rules inside, draws on the same board and writes in your language. To update, rerun install.sh; the board is kept.',b)

# ===== G1: merge vs rebase
b=[]
def row(y,label,sub,kind):
    out=[T(24,y-30,label,13,600),T(24,y-14,sub,11.5,400,'muted')]
    out.append(L(150,y,720,y,'edge',2))
    mains=[170,250,330]
    for x in mains: out.append(circ(x,y,9,'ink',sw=2))
    if kind=='merge':
        out.append(P(f'M250 {y} C 280 {y}, 280 {y+44}, 310 {y+44} H560 C 590 {y+44}, 590 {y}, 620 {y}','k2',2))
        for x in [330,410,490]: pass
        for x in [350,430,510]: out.append(circ(x,y+44,9,'k2','k2',0.25,2))
        out.append(circ(410,y,9,'ink',sw=2))
        out.append(circ(620,y,11,'focus','focus',0.25,2.5)); out.append(T(620,y-20,'merge commit',11.5,600,'ink','middle'))
    else:
        out.append(circ(410,y,9,'ink',sw=2))
        for x in [490,570,650]: out.append(circ(x,y,9,'k2','k2',0.25,2))
        out.append(P(f'M350 {y+44} H510',  'k2',1.5,'5 4'))
        for x in [350,430,510]: out.append(circ(x,y+44,9,'k2',sw=1.25,dash='3 3'))
        out.append(P(f'M520 {y+40} C 540 {y+30}, 560 {y+16}, 566 {y+12}','k2',1.5,'5 4'))
        out.append(T(350,y+72,'old copies discarded',11.5,400,'muted'))
    return out
b+=row(110,'merge','history as it was','merge')
b.append(L(24,186,736,186))
b+=row(250,'rebase','one straight line','rebase')
b.append(L(24,346,736,346))
lg=[(30,'ink',None,'main branch'),(130,'k2','k2','your commit'),(270,'focus','focus','merge commit')]
for x,c,f,t in lg:
    b.append(circ(x+8,368,7,c,f,0.25,2)); b.append(T(x+22,372,t,11.5,400,'muted'))
b.append(T(24,400,'Never rebase a shared branch: everyone’s history changes',11.5,400,'muted'))
out['git']=svgw(760,412,'Merge keeps history, rebase flattens it',
 'Merge: the main branch and your branch stay separate and join with a merge commit. Rebase: your commits are rewritten onto the tip of main, giving one straight line; the old copies are discarded. Do not rebase a shared branch.',b)

# ===== G2: query / index
b=[]
b.append(R(24,56,150,56,'ink',2))
b.append(T(40,80,'query',13,600)); b.append(T(40,98,'user_id = 42',11.5))
b.append(arrow(174,84,214))
b.append(f'<path d="M274 54 L334 84 L274 114 L214 84 Z" fill="none" stroke="var(--ink)" stroke-width="1.5"/>')
b.append(T(274,82,'index',11.5,600,'ink','middle')); b.append(T(274,96,'exists?',11.5,600,'ink','middle'))
# yes branch right, no branch down
b.append(arrow(334,84,392,'good',2)); b.append(T(342,76,'yes',11.5,600,'ink'))
b.append(R(392,62,344,44,'good',1.5,'good',0.12,rx=6))
b.append(T(408,82,'straight to 1 row',13,600)); b.append(T(408,98,'3 steps in the tree',11.5))
b.append(varrow(274,114,148,'bad',2)); b.append(T(282,138,'no',11.5,600,'ink'))
b.append(T(24,170,'FULL SCAN · 2 MILLION ROWS',11.5,600,'muted'))
for i in range(28):
    for j in range(3):
        b.append(f'<rect x="{24+i*25.4:.1f}" y="{180+j*24}" width="20" height="18" rx="3" fill="var(--bad)" fill-opacity="0.22" stroke="var(--bad)" stroke-width="1"/>')
b.append(f'<rect x="{24+11*25.4:.1f}" y="{180+24}" width="20" height="18" rx="3" fill="var(--good)" fill-opacity="0.35" stroke="var(--good)" stroke-width="2"/>')
b.append(T(24,268,'each square ~24,000 rows · green = target',11.5,400,'muted'))
b.append(L(24,288,736,288))
b.append(T(24,314,'Time',14,600))
b.append(T(24,344,'scan',13,600)); b.append(f'<rect x="110" y="333" width="626" height="14" rx="3" fill="var(--bad)" fill-opacity="0.35" stroke="var(--bad)" stroke-width="1.5"/>'); b.append(T(728,344,'~1,200 ms',11.5,600,'ink','end'))
b.append(T(24,372,'index',13,600)); b.append(f'<rect x="110" y="361" width="3" height="14" rx="1" fill="var(--good)" stroke="var(--good)" stroke-width="1.5"/>'); b.append(T(122,372,'~3 ms',11.5,600))
b.append(R(24,396,712,52,'good',2,'good',0.12))
b.append(T(40,418,'Fix: an index on orders(user_id)',13,600)); b.append(T(40,436,'400× faster · one-line migration',11.5))
out['sorgu']=svgw(760,460,'The query is slow because there is no index',
 'Without an index, user_id = 42 scans all 2 million rows (about 1,200 ms); with an index it reaches the row in 3 steps of the tree (about 3 ms). Fix: an index on orders.user_id, 400 times faster.',b)

# ===== G3: PR risk row table
b=[]
b.append(T(24,62,'FILE',11.5,600,'muted')); b.append(T(330,62,'CHANGED LINES',11.5,600,'muted')); b.append(T(620,62,'TEST',11.5,600,'muted'))
rows=[('payment/service.ts','money math',220,'bad','none'),('cart/discount.ts','promo rule',96,'warn','partial'),('api/order.ts','endpoint',58,'good','yes'),('ui/Button.tsx','view',31,'good','yes'),('docs/README.md','docs',12,'good','not needed')]
mx=220
for k,(n,d,ln,c,t) in enumerate(rows):
    y=80+k*50
    b.append(dot(30,y+16,6,c))
    b.append(T(46,y+14,n,13,600)); b.append(T(46,y+31,d,11.5,400,'muted'))
    w=ln/mx*240
    b.append(f'<rect x="330" y="{y+8}" width="{w:.1f}" height="14" rx="3" fill="var(--edge)" fill-opacity="0.35" stroke="var(--edge)" stroke-width="1.25"/>')
    b.append(T(330+w+8,y+19,str(ln),11.5,600))
    if c=='bad': b.append(cross(624,y+11))
    elif c=='warn': b.append(P(f'M628 {y+9} v8 M628 {y+22} v0.5','warn',2.5))
    else: b.append(check(622,y+15))
    b.append(T(644,y+20,t,11.5,600 if c!='good' else 400,'ink'))
    if k<4: b.append(L(24,y+44,736,y+44))
b.append(R(24,342,712,52,'bad',2,'bad',0.12))
b.append(T(40,364,'Test the payment service first',13,600)); b.append(T(40,382,'most changed · no tests',11.5))
for i,(c,t) in enumerate([('bad','no tests'),('warn','partial'),('good','tested')]):
    b.append(dot(30+i*110,418,6,c)); b.append(T(42+i*110,422,t,11.5,400,'muted'))
out['pr']=svgw(760,436,'The risk in this PR is one file: payments',
 'Five files changed: payment/service.ts 220 lines, no tests; cart/discount.ts 96 lines, partial tests; api/order.ts 58, ui/Button.tsx 31 and docs/README.md 12 lines, tested or not needed. Advice: test the payment service first.',b)
json.dump(out,open(os.path.join(os.path.dirname(__file__),'drawings.json'),'w'),ensure_ascii=False)
print(list(out))
