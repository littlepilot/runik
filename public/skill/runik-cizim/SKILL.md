---
name: runik-cizim
description: Oğuz'a bir şeyi görsel anlatırken (açıklama, kavram, mimari, süreç, karşılaştırma) SVG çizimlerini Runik çizim temasıyla üretir; gerçek nesneleri (makine, dağ, kasa, bina) gölgeli ve doğal renkli çizer.
---

# Runik çizim teması

Felsefe: sessiz lüks. Görselle anlatılabilen metinle anlatılmaz; metin yalnızca görselin taşıyamadığı yerde ve kısa olur (bkz. §0, kesin kural). Her çizim, hiçbir şey bilmeyen birine anlatır gibi kurulur. Bu tema bir örnek koleksiyonu değil, kural setidir: her yeni çizim aşağıdaki tuval, yazı, renk, bileşen ve kalıp kurallarıyla sıfırdan çizilir.

İki çizim türü var, ilk iş hangisi olduğuna karar vermektir:
- **Kavram çizimi** (tanım, süreç, karşılaştırma, ölçü, mimari): düz, gölgesiz, renkler anlam taşır (§1–§6).
- **Nesne çizimi** (gerçek, dokunulabilir şey: devre kartı, dağ, kasa, dizüstü, kemik): gölgeli ve doğal renkli, Visual Explainer tekniğiyle (§4b). Runik anlam renkleri nesnenin gövdesine girmez, yalnız üstüne konan işarette kalır.

Bir çizimde ikisi bir arada olabilir: nesne doğal renkte çizilir, etiketler, oklar ve durum işaretleri Runik temasıyla üstüne konur.

## 0. Kesin kural: metin son çaredir

Görselle (şekil, konum, renk, sayı, ölçek, ok, simge, gruplama) anlatılabilen hiçbir şey metinle anlatılmaz. Her metin parçası tek tek sorgulanır: "Bunu çizerek gösterebilir miyim?" Cevap evetse metin silinir ve çizilir. Şüphede kalınırsa da çizilir.

Metni görsele çevirme tablosu:

| Metinde şu varsa | Bunun yerine |
|---|---|
| sayı, oran, büyüklük | ölçek çubuğu, hücre dizisi, ölçekli daire |
| sıra, aşama | soldan sağa konum + numara |
| ait olma, kapsam | kapsam sınırı, gruplama |
| karşılaştırma, tercih | yan yana çubuk, puan, iyi/kötü kutusu |
| durum (iyi/kötü/riskli) | durum rengi, onay/çarpı |
| akış, neden-sonuç | ok |
| koşul, seçim | karar elması |
| "var / yok", "yasak" | simge + üstü çizili simge |
| ad listesi (araçlar, dosyalar) | sayı + hücre ya da nokta kümesi; ad yalnız vurgulanan 1–2 öğede |
| biçim kuralı (yazım, format) | örneğin kendisi, iyi/kötü yan yana |

Metin bütçesi:
- Başlık en fazla 8 kelime, cevabın kendisi.
- Etiket en fazla 3 kelime. Cümle yasak (başlık hariç).
- Detay satırı yalnız çizilemeyen bir ad ya da değer için ve en fazla 4 kelime. Her nesneye detay satırı yazılmaz.
- Bilgi şeridi ve not: çizim başına en fazla bir tane, en fazla 8 kelime.
- Başlık hariç bir çizimde toplam en fazla ~40 kelime düzyazı. Aşıyorsa ya metin görsele çevrilir ya çizim ikiye bölünür.
- Bütçe düzyazıya uygulanır (not, açıklama, etiket cümlesi). Sorulan şey adların kendisiyse (dağ listesi, aday listesi) ad ve değer etiketleri bütçeye sayılmaz, ama yine tek satır ve kısa olur.
- Not varsa sonucu söyler ("ne yani?"), işaretin ne olduğunu değil.
- Metnin taşıdığı ayrıntı (kaynak, gerekçe, uzun liste) çizime girmez; gerekirse ayrı bir "ayrıntı" kartına gider.

## 1. Tuval

- El yapımı inline SVG. Mermaid görünümlü kutu-ok diyagramı, renksiz çok seviyeli hiyerarşi ağacı, emoji yok. Kavram çiziminde gölge, gradyan ve 3B yok; nesne çiziminde bunlar zorunlu (§4b). Anlam taşıyan oklu zincir (§5.5) serbesttir.
- `viewBox="0 0 760 H"`, H içeriğe göre (genelde 320–610). `width="100%"`.
- Kenar boşluğu 24: içerik x=24 ile x=736 arasında.
- Sütun ızgarası:
  - 2 sütun: x=24 ve x=392, genişlik 344, aralık 24.
  - 3 sütun: x=24, 268, 512, genişlik 224, aralık 20.
  - Tam genişlik kutu: x=24, genişlik 712.
- Bölümler arası tam genişlik ince ayırıcı: `<line x1=24 x2=736 stroke=grid>`.
- Etiketler sol hizalı. Ortalama yalnızca bir şeklin içindeki ad ve altındaki değer için.
- Metin genişliği üretim anında tahmin edilir: karakter × boyut × 0.56 (400 ağırlık), 0.60 (600), BÜYÜK HARF 0.68. Kapsayan şekle her yanda ≥10 pay. Çubuk sonundaki değer 736'yı aşacaksa çubuğun içine `text-anchor="end"` ile alınır.
- Her etiket kutusu diğer metin ve şekillerden ≥4 birim uzakta. İşaretinden 12 birimden uzak etikete kılavuz çizgi çekilir.
- Yazı boyutu ekranda görünen boyuttur: panel genişliği × boyut / 760 ≥ 9 px. Dar panel (< 600 px) için dikey yığılabilen içerik `viewBox="0 0 400 H"` tek sütun çizilir.

SVG teknik kuralları (pano SVG'yi DOMPurify svg profiliyle temizler):
- Kök: `role="img"`, `aria-label` = başlık cümlesi. İçine `<title>` (başlık) ve `<desc>` (çizimin taşıdığı tüm değerler, ≤60 kelime) konur; `<desc>` görünür bütçeye sayılmaz.
- Öznitelikler yalnız kebab-case: `font-size`, `fill-opacity`, `stroke-width`. JSX yazımı (`fontSize`) silinir.
- `<marker>`, `<use>`, `<foreignObject>`, `<animate>`, `on*`, dış `href` yok. Ok ucu yol sonuna elle çizilen üçgendir.
- Kaçınılmaz id'ler (clipPath) çizime özgü önek alır: `k20261111-dag-clip`. Aynı sayfada tekrar eden id yok.

## 2. Yazı

Kök `fontSize='13'`. Yalnızca şu boyutlar:

| Rol | Boyut / ağırlık | Renk | Not |
|---|---|---|---|
| Başlık | 15 / 600 | ink | x=24, y≈30. Her zaman ana fikri söyleyen tek cümle. |
| Bölüm sorusu | 14 / 600 | ink | "Neden …?", "Üç kaldıraç" gibi. Ayırıcıdan sonra. |
| Öğe adı | 13 / 600 | ink | Her nesnenin adı. |
| Asıl detay | 11.5 / 400 | ink | Adın altında 16–20 px. |
| Ek detay, örnek | 11.5 / 400 | quiet | En alt satır: "örnek: …". |
| Sütun başlığı | 11.5 / 600 | quiet | BÜYÜK HARF: NE?, BENZETME. |
| Not | 11.5 / 400 | quiet | En altta: "süreler yaklaşık", "kare sayıları temsili". |

- Detay satırında parçalar orta nokta ile ayrılır: `çekirdeğin içinde · ~64 KB`, `hit · ~1 ns`.
- Yaklaşık değerler `~` ile yazılır. Ölçek log ise başlıkta söylenir.
- Hiçbir yazı 10.5 birimin altına inmez. Etiket en fazla bir kısa satır.
- Sayılar Türkçe biçimde ve tek tip: binlik nokta (3.000, 5.137), ondalık virgül (%95,7, r = 0,68). Eksen etiketleri de aynı biçimde.

## 3. Renk

Renkler süs değil, anlam taşır. Bu bölüm kavram çizimleri ve nesnenin üstüne konan işaretler içindir; nesnenin gövdesi doğal renginde çizilir (§4b). Her kavram çizimi yalnızca şu rolleri kullanır:

| Rol | Ne için | Runik açık | Runik koyu | Claude Docs token |
|---|---|---|---|---|
| ink | metin, aktör çerçevesi | #1b1f2a | #e8ebf2 | --cds-text-primary |
| quiet | ikincil metin, ara oklar (›) | #5f6779 | #98a1b3 | --cds-text-secondary |
| edge | nötr çerçeve, nötr ok (≥3:1) | #8a93a5 | #636c80 | --cds-chart-axis |
| grid | yalnız süs ayırıcı çizgi | #dadfe7 | #2c3240 | --cds-chart-grid |
| good | hızlı, doğru, hit, çözüm | #15803d | #4ade80 | --cds-chart-status-good |
| warn | orta, dikkat, kirli | #b45309 | #fbbf24 | --cds-chart-status-warning |
| bad | yavaş, hata, miss, risk | #c81e1e | #f87171 | --cds-chart-status-critical |
| acc | odak, senin eylemin, ana nesne | #2f5bd8 | #7d9cf5 | --cds-chart-categorical-1 |
| tint | nötr bilgi şeridi zemini | #eef0f4 | #1d2230 | --cds-chart-reference-tint |

- Renkler pano tokenlarıyla yazılır, başka `var(--…)` kullanılmaz: ink→`--ink`, quiet→`--muted`, edge→`--edge`, grid→`--line`, good→`--tamam`, warn→`--dikkat`, bad→`--risk`, acc→`--odak`, ikinci kategori→`--k2`, tint→`--tint`, zemin→`--surface`. Claude Docs'ta aynı roller sağ sütundaki tokenlara eşlenir.
- Durum hiçbir zaman yalnız renkle verilmez: her durum rengine ikinci bir kanal eşlik eder (✓ / ! / ✗, dolu / yarım / boş ya da 1 kelimelik etiket). Yeşil-kırmızı renk körlüğünde karışır.
- Durum rengi yalnızca çizimde yazılı bir eşik ya da yargı varsa kullanılır; yoksa değer nötr (acc ya da ink) kalır. Başlık "yanıltıcı" diyorsa o değer yeşil olamaz.
- Aynı varlık bir çizimde ve bir cevabın tüm çizimlerinde aynı renkte kalır.
- Dolgu daima kendi konturuyla birlikte: büyük kutuda `fill-opacity 0.12`, küçük hücrede `0.18–0.35`, kontur aynı renkte `1.5–2.5`.
- Renkli dolgu ya da tint içindeki metin ink rengindedir; quiet yalnız saf zemin üstünde. Koyu temada 0.3'ten yoğun dolgunun üstüne metin yazılmaz.
- Durum renkleri sıralıdır: good → warn → bad. Bir ölçekte üçü birden kullanılabilir (L1/L2 good, L3/RAM warn, SSD bad).
- Kategori ayırmak gerekiyorsa (iki çekirdek) acc ve ikinci kategorik renk kullanılır; durum renkleri asla kategori için kullanılmaz.

## 4. Bileşenler

Her çizim bu parçalardan kurulur. Ölçüler sabittir.

- **Nötr nesne**: `rect rx=6–8, fill=none, stroke=edge, 1.25–1.5`. Çoğu şey budur.
- **Aktör**: konuyu başlatan şey (CPU, "senin kodun"). `stroke=ink, 2`, dolgu yok.
- **Vurgulu nesne**: durum ya da odak rengi, saydam dolgu + aynı renk kontur.
- **Kart**: `rx=8, stroke=edge 1.25`. İçerik x+16'dan: ad (y+24), asıl detay, ek detay. Kategori/durum gerekiyorsa üst kenarda 6 px renkli bant.
- **Sonuç / çözüm kutusu**: tam genişlik, `rx=8`, renk `0.12` dolgu + 2 px kontur. Bir kalın cümle + bir detay satırı. Çizimin sonunda.
- **İyi / kötü kural kutuları**: iki sütun, sol good, sağ bad, aynı yapı.
- **Bilgi şeridi**: tam genişlik, `fill=tint, stroke=edge`. Kural veya istisna için.
- **Hücre dizisi**: veri birimini gösteren 20–26 px kareler, `rx=3–4`, 4–6 px aralık. Dolu = renk dolgu, boş = edge kontur.
- **Kapsama parantezi**: bir grup hücrenin üstünde `M x1 y-6 V y-12 H x2 V y-6`, renk = anlam.
- **Durum noktası**: `r=6` daire, durum rengi, satırın solunda.
- **Ölçek çubuğu**: `height=14, rx=3`, uzunluk değerle orantılı ve daima 0'dan başlar. Dar bir aralığı göstermek gerekiyorsa çubuk değil ortak eksende nokta kullanılır. Önce/sonra ya da A/B çubukları aynı x tabanından alt alta başlar; uç uca dizme yalnız toplam anlamlıysa.
- **Ölçekli daire**: tek eksende uzaklık = maliyet; dairenin alanı kapasiteyle orantılı (yarıçap ∝ √değer, 0 tabanlı).
- **Puan**: 5 küçük daire `r=5`, dolu olan sayısı = değer.
- **Karar**: elmas, `stroke=ink 1.5`, içinde 11.5/600 soru; sonucu altta kısa kutu.
- **Oklar**: küçük dolu üçgen uç (6×6). Nötr akış `edge 1.5`. Anlamlı akış 2–3 px, rengi anlamı taşır. Kesikli = dolaylı, sonra, kopya. Panel geçişi: ince `›` (quiet, 2 px).
- **Kapsam sınırı**: bir şeyin içinde olmayı gösteren kesikli dış çerçeve (`6 4`, edge) ve sol üstte küçük BÜYÜK HARF etiket (İŞLEMCİ ÇİPİ).
- **Mini kavram simgesi**: 24–32 px, ince ink çizgi, geometrik (belge, büyüteç, göz, yol, kilit, saat, onay/çarpı). Emoji asla. Bir kavramı etiketsiz taşıyabiliyorsa etiket yazılmaz; yazılırsa tek kelime.
- **Nesne simgesi (harita, konum)**: gerçek bir nesneyi (dağ, bina, gemi) temsil eden işaret soyut geometri olamaz (üçgen, daire yetmez). Nesnenin tanınır silüeti §4b tekniğiyle, doğal renkte çizilir: dağ için `N.peak()` (girintili sırt, ikincil tepe, gölgeli yüz, kar). Boyut bir değeri taşıyorsa silüetin alanı değerle orantılıdır (boy ∝ √değer, 0 tabanlı). En büyük değer en küçüğün 2 katından azsa boyut yerine 3 sınıf kullanılır ve sınıf eşikleri lejantta yazar. Birbirine binen simgeler kaydırılıp kılavuz çizgiyle bağlanır.
- **Lejant**: satır içinde, en altta: 16×16 örnek + metin. Ayrı kutu yok.

## 4b. Nesne çizimi (Visual Explainer tekniği)

Gerçek bir nesne kutu-çubukla ya da düz renkli şekille çizilmez; tanınır, gölgeli bir resim olarak çizilir. Yardımcılar bu klasörde: `runik_nesne.py` (Visual Explainer'ın `vxart.py` tekniğinden uyarlandı, id'leri çizime özgü önekli).

```python
from runik_nesne import Nesne, pol, blob, smooth, rrect, capsule
N = Nesne("k20261118-kart")                 # önek: çizime özgü
N.add(N.slab(50, 90, 900, 700, N.PCB, r=18, depth=14))
N.add(N.grain(rrect(50, 90, 900, 700, 18), 0.35))
N.mark("cpu", 270, 222)                     # etiketlenecek nokta
svg_defs, g = N.defs(), N.group(24, 52, 0.42)   # Runik 760 tuvaline yerleştir
x, y = N.at("cpu")                          # etiket ve kılavuz çizgi buradan çıkar
```

Tam örnek: `ornek_nesne.py` (anakart + Runik etiketleri, gerçek dağ silüetli harita; panoda "Nesne çizimi: yeni tema örneği" kartı).

Yapı taşları: `slab` (kart, çip, kasa, levha), `layers` (katman kesiti), `ball` (yuvarlak gövde), `tube` (boru, kablo, damar), `peak` (dağ), `laptop`, `chip`, `shadow`, `grain`; şekil için `blob` + `smooth` (organik), `rrect`, `capsule`; dolgu için `N.linear`, `N.radial`, `N.clip`.

Kurallar:
- **Renk doğal**: devre kartı yeşil, metal gri, dağ kahve ve kar beyazı, kağıt krem. Hazır paletler: `N.PCB, METAL, DARK, PAPER, ROCK, STONE, GOLD, WOOD, GLASS, SKIN, LEAF, WATER, SAND`. Her palet (açık, orta, koyu).
- **Runik renkleri gövdeye girmez**: `var(--tamam/--dikkat/--risk/--odak)` nesneyi boyamaz. Anlam nesnenin üstüne konan işaretle verilir: kılavuz çizgi + etiket, durum yazısı (✓ hızlı), vurgu halkası, ok.
- **Işık sol üstten**: her gövdede açık tepe, koyu yan; yere değen her şeye yumuşak gölge (`shadow`, `slab` ve `ball` kendisi koyar).
- **Kontur dolgunun koyu tonu**, asla siyah. Canlılar düzensiz kontur (`smooth(blob(...))`), yapılmış şeyler düz kenar, yuvarlak köşe ve görünür kalınlık.
- **Derinlik**: arkadan öne çiz, parçalar biraz örtüşsün, içerik gövdeye kırpılsın (`N.clip`).
- **Doku**: büyük düz dolguya `grain`; tekrar eden küçük parçalar (çip, pim, vida) döngüyle.
- **Oran ve sayı gerçeğe uyar**: yanlış çizim yanlış öğretir. Sadeleştirildiyse notta söylenir ("çizim sadeleştirilmiş").
- **Nesnenin içine yazı yok**. Adlar Runik etiketleri olarak yanına yazılır (13/600 ad, 11.5 detay), kılavuz çizgi nesnenin üstünden geçmez; gerekirse önce dik çıkar, sonra yatay gider. Numaralı pin + ayrı lejant kullanılmaz.
- **Taban sessiz kalır**: harita tabanı, ülke sınırı, arka plan Runik tint/line tonlarında; doğal renk yalnız nesnenin kendisinde.
- Koyu temada da okunur: nesne kendi rengini korur, etiketler token rengindedir.

## 5. Kalıplar

Konuya göre birini seç, gerekirse ikisini alt alta birleştir (aralarında ayırıcı + bölüm sorusu):

1. **Mesafe ekseni**: tek yatay çizgi, aktör solda, öğeler maliyete göre uzaklaşır, boyut kapasiteyi gösterir. Altına "uzaklık = …, daire = …" notu.
2. **Satır tablosu**: sütunlar NE? · BENZETME · ÖLÇEK. Her satır: durum noktası, ad + detay, gündelik benzetme, ölçek çubuğu.
3. **Fiziksel harita**: şeyin gerçek yerleşimi (çip, bina, vücut). Kesikli kapsam sınırı, paylaşılan parça vurgulu, dışarıdakiler nötr.
4. **Karşılaştırma sütunları**: 2–3 eş kart, altında puan matrisi, en altta "neden hiçbiri hepsini vermiyor" notu ve sonuç kutusu.
5. **Zincir / arama**: aktör → karar elmasları → sonuç; başarısız dallar kısa renkli kelimeyle (miss), dönüş kesikli okla.
6. **Senaryo satırları**: aynı aktör dizisi her satırda tekrar eder, değişen tek şey ok deseni ve rengi. Satır başında ad + "yaygın/nadir".
7. **Süreç panelleri**: 2–3 numaralı panel (`1 · CPU tek bir sayı ister`), aralarında `›`, her panelde aynı hücre dizisinin değişen hali.
8. **Kim karar verir + kaldıraçlar**: üstte aktör → sistem şeridi, ortada kural şeridi, altta 3 kaldıraç kartı (renkli üst bant).

Her çizimin akışı: başlık cümlesi → ana görsel → (ayırıcı → bölüm sorusu → açıklayıcı parça) → sonuç kutusu veya not.

## 5b. Harita

- Taban gerçek veriden üretilir (Natural Earth vb. açık vektör), elle çizilmez. Konformal projeksiyon kullanılır (Türkiye için Lambert konformal konik); düz enlem-boylam kullanılmaz. Kaynak nota yazılır.
- Taban coğrafyası (sınır, kıyı, göl) gri ve sessiz; lejant gerektirmez. Ülke tint dolgulu, komşular yalnız ince grid kontur.
- Harita kendi başına okunur: en önemli 3–5 öğe adıyla doğrudan etiketlenir, gerisi etiketsiz işarettir. Başka çizime numarayla gönderme yapılmaz.
- Etiket sırasıyla sağ üst, sol üst, sağ alt, sol alt denenir; işaretin, başka etiketin ya da su alanının üstüne yazılmaz.
- Başlıktaki bölge iddiası haritada sayıyla ya da bölgeyle kodlanır (ör. "doğu 14 · batı 6" hücre dizisi).

## 6. Bilgi yoğunluğu

- Görsel seyrek olmaz: her parçanın ne olduğu, ne işe yaradığı ve neye bağlı olduğu üstünde okunur.
- Soyut bir şey varsa gündelik bir benzetmesi yanına yazılır (not kağıdı, masa, raf, depo, arşiv).
- Bir çizim tek fikir taşır. Fazlası ikinci çizime.
- Gerçek dünya nesnesi (vücut, makine, dağ) §4b ile doğal renkte çizilir; harita ve ekran görüntüsü gibi tabanlar gerçek veriden gelir ve sessiz tona indirilir. Üstüne konan işaretler bu temayla çizilir.

## 6b. Okunabilirlik: her işaret tek anlam

Konuyu bilmeyen bir okurun yanlış anladığı yerler hep işaretlerdi, fikir değil. Bu yüzden:

- Çizimdeki her işaret (renk, nokta, kesikli çizgi, ✓/✗, dolgu) çizim içindeki bir lejantta tanımlı olur. Tanımsız işaret yok.
- Bir işaret bir anlam taşır. ✗ "uydurur", "atlar", "yok" gibi farklı anlamlara gelecekse ✗ yerine 1 kelimelik kırmızı etiket yaz.
- Kesikli çizgi bir çizimde tek anlamda kullanılır (ör. "bilgi yok"). Gruplar ince düz gri çerçeveyle ayrılır.
- Eksen metriği ve birimi söyler, yönü belirtir ("yüksek = iyi"). Eksen 0'dan başlamıyorsa yazar.
- Farklı birimler aynı ölçeğe çizilmez (ör. hız katsayısı ile kalite puanı ayrı çubuk çiftleri olur).
- Durum renkleri (yeşil/turuncu/kırmızı) yalnızca durumu anlatır. Nötr vurgu (fark parantezi, ölçü çizgisi) mürekkep rengindedir.
- Noktalar ve çubuklar etiketsiz kalmaz. Kalabalıksa önemli 2–3 tanesi kılavuz çizgiyle adlandırılır.
- Kısaltma ya açılır ya kullanılmaz.
- Eksik veri kendi işaretiyle gösterilir (boş kesikli hücre ya da "—"), hiçbir değer kategorisiyle birleştirilmez, lejantta ayrı satırdır.
- Bir cevaptaki çizimler tek lejant sözlüğü kullanır: bir işaret ilk çizimde hangi anlamı aldıysa seri boyunca o anlamda kalır.
- Bir nesne en fazla iki görsel kanal taşır (ör. dolgu + kontur). Okurun araması beklenen durum kalın kontur (≥2.5) ya da simgeyle verilir.
- Başlığın iddiası ana görselde ön-dikkat kanalıyla kodlanır (vurgu rengi, bölge, sayım). Vurgu rengini yalnız iddiayı taşıyan öğe alır.
- Nicel öğeler değere göre azalan dizilir; matris satırları kapsama puanına göre. Alfabetik sıra yalnız bir öğe aranacaksa.
- Farklı nicelikler (yüzde ile korelasyon) aynı çubuk ölçeğine çizilmez; korelasyon ve aralıklı tahmin nokta + hata çizgisiyle gösterilir.

## 7. Teslimden önce

1. Kelime say: başlık hariç ~40 kelimeyi aşan düzyazı teslim edilmez (§0). Her metni bir kez daha "çizilebilir mi?" diye sorgula.
2. Otomatik denetim: `node runik-lint.js kart.json` (bu klasörde). Tanımsız token, camelCase öznitelik, DOMPurify'ın sildiği öğe, tekrar eden id, kenara taşan ya da çakışan yazı, eksik role/aria-label varsa düzelt.
3. Ekran görüntüsünü al ve bak: yazılar ve işaretler çakışmıyor, kesilmiyor; oklar doğru nesneye gidiyor.
4. Yalnızca tablodaki yazı boyutları ve renk rolleri var. Nesne çiziminde gövde doğal renkte, anlam renkleri yalnız işaretlerde; id'ler çizime özgü önekli.
5. 3 saniye testi: başlık ve ana görsel, etiketler okunmadan fikri veriyor.
6. Açık ve koyu temada okunuyor (renkler token).
Bilmeyen göz testi (konuyu bilmeyen bir agent'a ekran görüntülerini okutup geri anlatma ve soru cevaplama) teslim adımı değildir; yalnızca Oğuz isterse yapılır, çünkü süreci uzatır. Hızlı denetim için madde 2'deki betik yeterlidir.
