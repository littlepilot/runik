# Runik kurulumu

Bu dosyayı, kullanıcı Runik kurulum prompt'unu bir Claude Code projesine yapıştırdığı için okuyorsun. Runik, cevapların uzun metin yerine kurallı çizimlerle yan ekrandaki bir panoda gösterilmesidir. Aşağıdaki adımları sırayla uygula. Kullanıcıya ara rapor verme; sonda tek mesaj yeter.

Kaynaklar (ilk açılan kullanılır):
- SITE = https://runik.littleman.workers.dev
- YEDEK = https://raw.githubusercontent.com/littlepilot/runik/main/public

## 1. Dosyaları indir

```bash
mkdir -p /tmp/runik && cd /tmp/runik
for u in "https://runik.littleman.workers.dev" "https://raw.githubusercontent.com/littlepilot/runik/main/public"; do
  curl -fsSL "$u/skill/surum.json" -o surum.json \
  && curl -fsSL "$u/skill/runik/SKILL.md" -o yukleyici.md \
  && curl -fsSL "$u/skill/runik-cizim/SKILL.md" -o SKILL.md \
  && curl -fsSL "$u/pano/pano.html" -o pano.html \
  && echo "kaynak: $u" && break
done
```

İkisi de açılmazsa WebFetch ile dene. O da olmazsa dur ve kullanıcıya tek satırla, ortamın ağ ayarlarında bu alan adlarına izin vermesi gerektiğini söyle.

## 2. Panoyu kur

Önce proje hafızasında `runik.md` var mı bak. Varsa içindeki pano bağlantısını kullan ve 3. adıma geç.

Yoksa `/tmp/runik/pano.html` dosyasını Artifact aracıyla yeni bir artifact olarak yayınla:
- başlık: `Runik Pano`
- icon: `board`
- capabilities: `{"db": {}}`
- description: `Runik cevaplarının canlı gösterildiği yan ekran panosu.`

Dönen bağlantıyı not et.

## 3. Skill'i öner

`propose_skills` aracıyla tek bir skill öner:
- name: `runik`
- kind: hesabında `runik` adlı skill zaten varsa `improvement` (target: `runik`), yoksa `new`
- description: `yukleyici.md` frontmatter'ındaki description
- skillMd: `yukleyici.md` dosyasının tamamı + şu ek:

```
---

# Yedek kopya (runik-cizim, sürüm <surum.json'daki surum>)

Bu bölüm yalnızca güncel kurallar indirilemediğinde kullanılır.

<SKILL.md dosyasının frontmatter'sız tamamı>
```

## 4. Proje hafızasını yaz

Proje hafızasına `runik.md` dosyasını yaz (varsa güncelle):

```markdown
---
name: runik
description: Bu projede Runik kurulu; cevaplar Runik Pano'ya çizim olarak yazılır
metadata:
  type: project
---
Runik kurulu (sürüm <surum>, kurulum <bugünün tarihi>).
Pano: <pano bağlantısı> (pano sürümü <surum.json'daki pano>)
Her cevapta `runik` skill'ini uygula: önce güncel kuralları https://runik.littleman.workers.dev/skill/runik-cizim/SKILL.md'den çek, cevabı panoya kart olarak yaz, thread'e en fazla tek satır yaz.
```

## 5. Panoya ilk kartı yaz

ArtifactData ile panonun `kartlar` koleksiyonuna `set` yap. doc_id: `k-<YYYYMMDD-HHMMSS>-kuruldu`. Alanlar:
- tur: `kart`
- baslik: `Runik kuruldu`
- konu: `Kurulum`
- zaman: şimdiki zaman, ISO, UTC
- veri_json: `{"ozet":"Runik kuruldu","durum":"ok","maddeler":["Skill kartını kaydet","Panoyu yan ekranda açık tut"],"sayilar":{"sürüm":"<surum>"}}`

## 6. Kullanıcıya tek mesaj

En fazla üç satır:
- Pano bağlantısı ve "yan ekranda açık tut" önerisi.
- "Skill kartındaki Kaydet'e bas."
- İsteğe bağlı: proje talimatına şu satırı eklemesini öner: `Runik kurulu: her cevapta runik skill'ini kullan.`

Panoyu sabitlemeyi bir kez teklif et; kullanıcı evet derse Artifact `pin` ile sabitle.
