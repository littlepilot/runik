import json, math, os
from runik_svg import *
out={}
# ===== HERO: mesafe ekseni
b=[]
b.append(T(24,62,'İŞLEMCİDEN UZAKLIK = OKUMA SÜRESİ',11.5,600,'muted'))
y0=150
b.append(L(80,y0,736,y0,'edge',1.5))
# actor CPU chip
b.append(R(24,y0-26,52,52,'ink',2,rx=6))
for k in range(4):
    b.append(L(32+k*12,y0-32,32+k*12,y0-26,'ink',1.5)); b.append(L(32+k*12,y0+26,32+k*12,y0+32,'ink',1.5))
b.append(T(50,y0+5,'CPU',11.5,600,'ink','middle'))
lv=[('L1','~1 ns','masa',1,'tamam'),('L2','~4 ns','çekmece',4,'tamam'),('L3','~15 ns','raf',15,'dikkat'),('RAM','~100 ns','oda',100,'dikkat'),('SSD','~100 µs','başka şehir',100000,'risk')]
def X(ns): return 130+math.log10(ns)/5*560
for n,lat,an,ns,c in lv:
    x=X(ns)
    b.append(circ(x,y0,13,c,c,0.18,2))
    b.append(T(x,y0-24,n,13,600,'ink','middle'))
    b.append(T(x,y0+34,lat,11.5,400,'ink','middle'))
    b.append(T(x,y0+52,an,11.5,400,'muted','middle'))
# kat göstergesi
b.append(L(24,236,736,236))
b.append(T(24,262,'SSD, L1’den kaç kat uzak?',14,600))
# hücre: 1 vs 100.000 -> log bar
b.append(f'<rect x="24" y="280" width="2" height="14" rx="1" fill="var(--tamam)"/>'); b.append(T(34,292,'L1 · 1 ×',11.5,600))
b.append(f'<rect x="24" y="306" width="712" height="14" rx="3" fill="var(--risk)" fill-opacity="0.35" stroke="var(--risk)" stroke-width="1.5"/>')
b.append(T(730,317,'SSD · 100.000 ×',11.5,600,'ink','end'))
b.append(R(24,342,712,50,'tamam',2,'tamam',0.12))
b.append(T(40,364,'Sıcak veriyi yakında tut',13,600)); b.append(T(40,382,'diziyi sırayla gez · önbellek dostu',11.5))
b.append(T(24,414,'üst eksen log · alt çubuklar doğrusal · süreler yaklaşık',11.5,400,'muted'))
out['hero']=svgw(760,424,'Veri uzaklaştıkça okuma katlanarak yavaşlar',
 'İşlemciden uzaklığa göre okuma süresi, log ölçek: L1 yaklaşık 1 ns (masa), L2 4 ns (çekmece), L3 15 ns (raf), RAM 100 ns (oda), SSD 100 µs (başka şehir). SSD L1’den 100.000 kat yavaş. Sonuç: sıcak veriyi yakında tut.',b)

# ===== NASIL: kurulum akışı (plan 1 uyarlaması)
b=[]
cols=[24,268,512]
heads=['1 · Kopyala','2 · Projeye yapıştır','3 · Claude kurar']
for x,h in zip(cols,heads):
    b.append(R(x,52,224,150)); b.append(T(x+16,76,h,13,600))
x=24
b.append(R(x+16,90,192,96,'edge',1.25,rx=6)); b.append(L(x+16,106,x+208,106,'edge',1.25))
for k in range(3): b.append(dot(x+26+k*9,98,2.5,'edge'))
b.append(R(x+28,116,168,56,'odak',1.5,'odak',0.12,rx=4))
for k,wd in enumerate([110,130,80]): b.append(L(x+38,128+k*10,x+38+wd,128+k*10,'odak',2))
b.append(R(x+170,122,14,16,'ink',1.25,rx=2)); b.append(R(x+174,126,14,16,'ink',1.25,fill='surface',op=1,rx=2))
b.append(chev(256,127))
x=268
b.append(f'<path d="M{x+20} 96 h184 a6 6 0 0 1 6 6 v62 a6 6 0 0 1 -6 6 h-150 l-12 12 v-12 h-22 a6 6 0 0 1 -6 -6 v-62 a6 6 0 0 1 6 -6 z" fill="none" stroke="var(--edge)" stroke-width="1.25"/>')
b.append(R(x+30,108,164,50,'odak',1.5,'odak',0.12,rx=4))
for k,wd in enumerate([110,130,80]): b.append(L(x+40,120+k*10,x+40+wd,120+k*10,'odak',2))
b.append(chev(500,127))
x=512
for k,(n,d) in enumerate([('skill','yükleyici'),('pano','yan ekran'),('hafıza','proje kuralı')]):
    yy=92+k*36
    b.append(R(x+16,yy,28,28,'tamam',1.5,'tamam',0.18,rx=4)); b.append(check(x+24,yy+13))
    b.append(T(x+54,yy+13,n,13,600)); b.append(T(x+54,yy+27,d,11.5,400,'muted'))
b.append(L(24,222,736,222))
b.append(T(24,248,'Her yeni thread’de',14,600))
b.append(R(24,272,132,92,'ink',2))
b.append(T(40,300,'yeni thread',13,600)); b.append(T(40,318,'skill açılır',11.5)); b.append(T(40,336,'güncelini çeker',11.5,400,'muted'))
src=[('GitHub','main dalı','birincil','odak','odak',False),('runik sitesi','workers.dev','yedek','dikkat','dikkat',False),('skill içi kopya','son kurulum','son çare','edge',None,True)]
for k,(n,d,lab,c,fill,dash) in enumerate(src):
    yy=264+k*38
    b.append(f'<path d="M156 318 C 190 318, 196 {yy+16}, 226 {yy+16}" stroke="var(--{c})" stroke-width="{2 if k==0 else 1.5}" fill="none"{" stroke-dasharray=\"5 4\"" if k else ""}/>')
    b.append(f'<path d="M226 {yy+12.5} L232 {yy+16} L226 {yy+19.5} Z" fill="var(--{c})"/>')
    b.append(R(234,yy,300,32,c,2 if k==0 else 1.5,fill,0.12,rx=6,dash='5 4' if dash else None))
    b.append(circ(252,yy+16,9,'ink' if k==0 else 'muted',sw=1.25))
    b.append(T(252,yy+20,str(k+1),11.5,600,'ink','middle'))
    b.append(T(270,yy+21,n,13,600)); b.append(T(400,yy+21,d,11.5,400,'ink' if fill else 'muted'))
    b.append(T(548,yy+21,lab,11.5,600,'ink' if k==0 else 'muted'))
b.append(T(628,285,'ilk açılan',11.5,400,'muted')); b.append(T(628,301,'kullanılır',11.5,400,'muted'))
b.append(P('M618 272 V350','edge',1.25)); b.append(f'<path d="M614.5 344 L618 350 L621.5 344 Z" fill="var(--edge)"/>')
b.append(R(24,384,712,52,'tamam',2,'tamam',0.12))
b.append(T(40,408,'Biz yayınlarız → sonraki thread’de herkeste',13,600))
b.append(T(40,425,'elle güncelleme yok',11.5))
b.append(T(24,458,'kesikli = yalnız önceki açılmazsa',11.5,400,'muted'))
out['nasil']=svgw(760,470,'Bir kez yapıştır, Runik hep güncel kalsın',
 'Kurulum prompt’u kopyalanır, Claude Code projesine yapıştırılır; Claude yükleyici skill, Runik pano ve proje hafızası kuralını kurar. Her yeni thread’de skill güncel kuralları sırayla bu siteden, GitHub’dan ya da kendi içindeki kopyadan çeker.',b)

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
        out.append(circ(620,y,11,'odak','odak',0.25,2.5)); out.append(T(620,y-20,'birleştirme',11.5,600,'ink','middle'))
    else:
        out.append(circ(410,y,9,'ink',sw=2))
        for x in [490,570,650]: out.append(circ(x,y,9,'k2','k2',0.25,2))
        out.append(P(f'M350 {y+44} H510',  'k2',1.5,'5 4'))
        for x in [350,430,510]: out.append(circ(x,y+44,9,'k2',sw=1.25,dash='3 3'))
        out.append(P(f'M520 {y+40} C 540 {y+30}, 560 {y+16}, 566 {y+12}','k2',1.5,'5 4'))
        out.append(T(350,y+72,'eski kopyalar atılır',11.5,400,'muted'))
    return out
b+=row(110,'merge','geçmiş olduğu gibi','merge')
b.append(L(24,186,736,186))
b+=row(250,'rebase','tek düz çizgi','rebase')
b.append(L(24,346,736,346))
lg=[(30,'ink',None,'ana dal'),(130,'k2','k2','senin commit’in'),(270,'odak','odak','birleştirme commit’i')]
for x,c,f,t in lg:
    b.append(circ(x+8,368,7,c,f,0.25,2)); b.append(T(x+22,372,t,11.5,400,'muted'))
b.append(T(24,400,'Paylaşılan dalda rebase yapma: herkesin geçmişi değişir',11.5,400,'muted'))
out['git']=svgw(760,412,'Merge geçmişi korur, rebase düzleştirir',
 'Merge: ana dal ve senin dalın ayrı kalır, bir birleştirme commit’iyle birleşir. Rebase: senin commit’lerin ana dalın ucuna yeniden yazılır, tek düz çizgi olur, eski kopyalar atılır. Paylaşılan dalda rebase önerilmez.',b)

# ===== G2: sorgu / index
b=[]
b.append(R(24,56,150,56,'ink',2))
b.append(T(40,80,'sorgu',13,600)); b.append(T(40,98,'user_id = 42',11.5))
b.append(arrow(174,84,214))
b.append(f'<path d="M274 54 L334 84 L274 114 L214 84 Z" fill="none" stroke="var(--ink)" stroke-width="1.5"/>')
b.append(T(274,82,'index',11.5,600,'ink','middle')); b.append(T(274,96,'var mı?',11.5,600,'ink','middle'))
# yes branch up-right, no branch down
b.append(arrow(334,84,392,'tamam',2)); b.append(T(342,76,'var',11.5,600,'ink'))
b.append(R(392,62,344,44,'tamam',1.5,'tamam',0.12,rx=6))
b.append(T(408,82,'doğrudan 1 satır',13,600)); b.append(T(408,98,'ağaçta 3 adım',11.5))
b.append(varrow(274,114,148,'risk',2)); b.append(T(282,138,'yok',11.5,600,'ink'))
b.append(T(24,170,'TAM TARAMA · 2 MİLYON SATIR',11.5,600,'muted'))
for i in range(28):
    for j in range(3):
        b.append(f'<rect x="{24+i*25.4:.1f}" y="{180+j*24}" width="20" height="18" rx="3" fill="var(--risk)" fill-opacity="0.22" stroke="var(--risk)" stroke-width="1"/>')
b.append(f'<rect x="{24+11*25.4:.1f}" y="{180+24}" width="20" height="18" rx="3" fill="var(--tamam)" fill-opacity="0.35" stroke="var(--tamam)" stroke-width="2"/>')
b.append(T(24,268,'her kare ~24.000 satır · yeşil = aranan',11.5,400,'muted'))
b.append(L(24,288,736,288))
b.append(T(24,314,'Süre',14,600))
b.append(T(24,344,'tarama',13,600)); b.append(f'<rect x="110" y="333" width="626" height="14" rx="3" fill="var(--risk)" fill-opacity="0.35" stroke="var(--risk)" stroke-width="1.5"/>'); b.append(T(728,344,'~1.200 ms',11.5,600,'ink','end'))
b.append(T(24,372,'index',13,600)); b.append(f'<rect x="110" y="361" width="3" height="14" rx="1" fill="var(--tamam)" stroke="var(--tamam)" stroke-width="1.5"/>'); b.append(T(122,372,'~3 ms',11.5,600))
b.append(R(24,396,712,52,'tamam',2,'tamam',0.12))
b.append(T(40,418,'Çözüm: orders(user_id) üzerine index',13,600)); b.append(T(40,436,'400× hızlı · tek satır migration',11.5))
out['sorgu']=svgw(760,460,'Sorgu yavaş çünkü index yok',
 'user_id = 42 sorgusu için index yoksa 2 milyon satırın hepsi taranır (yaklaşık 1.200 ms); index varsa ağaçta 3 adımda tek satıra gidilir (yaklaşık 3 ms). Çözüm: orders tablosunda user_id üzerine index, 400 kat hızlı.',b)

# ===== G3: PR risk satır tablosu
b=[]
b.append(T(24,62,'DOSYA',11.5,600,'muted')); b.append(T(330,62,'DEĞİŞEN SATIR',11.5,600,'muted')); b.append(T(620,62,'TEST',11.5,600,'muted'))
rows=[('odeme/servis.ts','para hesabı',220,'risk','yok'),('sepet/indirim.ts','kampanya kuralı',96,'dikkat','kısmi'),('api/siparis.ts','uç nokta',58,'tamam','var'),('ui/Buton.tsx','görünüm',31,'tamam','var'),('docs/README.md','belge',12,'tamam','gerekmez')]
mx=220
for k,(n,d,ln,c,t) in enumerate(rows):
    y=80+k*50
    b.append(dot(30,y+16,6,c))
    b.append(T(46,y+14,n,13,600)); b.append(T(46,y+31,d,11.5,400,'muted'))
    w=ln/mx*240
    b.append(f'<rect x="330" y="{y+8}" width="{w:.1f}" height="14" rx="3" fill="var(--edge)" fill-opacity="0.35" stroke="var(--edge)" stroke-width="1.25"/>')
    b.append(T(330+w+8,y+19,str(ln),11.5,600))
    if c=='risk': b.append(cross(624,y+11))
    elif c=='dikkat': b.append(P(f'M628 {y+9} v8 M628 {y+22} v0.5','dikkat',2.5))
    else: b.append(check(622,y+15))
    b.append(T(644,y+20,t,11.5,600 if c!='tamam' else 400,'ink'))
    if k<4: b.append(L(24,y+44,736,y+44))
b.append(R(24,342,712,52,'risk',2,'risk',0.12))
b.append(T(40,364,'Önce ödeme servisine test yaz',13,600)); b.append(T(40,382,'en çok değişen · testi yok',11.5))
for i,(c,t) in enumerate([('risk','test yok'),('dikkat','kısmi'),('tamam','var')]):
    b.append(dot(30+i*110,418,6,c)); b.append(T(42+i*110,422,t,11.5,400,'muted'))
out['pr']=svgw(760,436,'Bu PR’da risk tek dosyada: ödeme',
 'Beş dosya değişti: odeme/servis.ts 220 satır, testi yok; sepet/indirim.ts 96 satır, kısmi test; api/siparis.ts 58, ui/Buton.tsx 31 ve docs/README.md 12 satır, testli ya da gerekmez. Öneri: önce ödeme servisine test yaz.',b)
json.dump(out,open(os.path.join(os.path.dirname(__file__),'cizimler.json'),'w'),ensure_ascii=False)
print(list(out))
