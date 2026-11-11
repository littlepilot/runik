---
name: runik
description: Runik görsel iletişim. Bu projede her cevap, açıklama ve sonuç uzun metin yerine Runik Pano'ya kurallı çizim olarak yazılır. Her thread'in başında ve her cevaptan önce kullan.
---

# Runik (yükleyici)

Bu skill ince bir yükleyicidir. Çizim kuralları her thread'de en güncel halden okunur; bu dosyanın sonundaki kopya yalnız son çaredir.

## 1. Güncel kuralları çek (thread başına bir kez)

```bash
mkdir -p /tmp/runik && cd /tmp/runik
for u in "https://runik.littleman.workers.dev" "https://raw.githubusercontent.com/littlepilot/runik/main/public"; do
  curl -fsSL "$u/skill/surum.json" -o surum.json \
  && curl -fsSL "$u/skill/runik-cizim/SKILL.md" -o SKILL.md \
  && curl -fsSL "$u/skill/runik-cizim/runik-lint.js" -o runik-lint.js \
  && curl -fsSL "$u/skill/runik-cizim/purify.min.js" -o purify.min.js \
  && echo "kaynak: $u" && break
done
```

Sonra `/tmp/runik/SKILL.md` dosyasını baştan sona oku ve uygula; denetim betiği `/tmp/runik/runik-lint.js`. İki kaynak da açılmazsa bu dosyanın sonundaki "Yedek kopya"yı uygula ve kullanıcıya bir kez, tek satırla, ağ ayarlarında bu alan adlarına izin verilmesi gerektiğini söyle.

## 2. Cevabı panoya yaz

Pano bağlantısı proje hafızasındaki `runik.md` dosyasındadır. Yoksa kullanıcıya https://runik.littleman.workers.dev adresindeki kurulum prompt'unu önerip dur.

Cevapları, açıklamaları ve sonuçları panoya kart olarak yaz: ArtifactData ile `kartlar` koleksiyonuna `set`.
- doc_id: `k-YYYYMMDD-HHMMSS-kisa-ad`
- tur: `cizim` (açıklamalar için varsayılan) | `grafik` | `tablo` | `kart` | `markdown`
- baslik: kısa, cevabın kendisi
- konu: thread başlığı
- zaman: ISO, UTC
- veri_json: veri JSON string olarak
  - cizim: güncel kurallara uygun SVG dizisi `["<svg…>", …]`. Uzun cevapta önce ilk SVG ile `set`, sonra parçaları `update` ile ekle; bitene kadar `durum: "yaziliyor"` ver.
  - grafik: Vega-Lite spec
  - tablo: `{"sutunlar":[],"satirlar":[[]]}`
  - kart: `{"ozet","durum":"ok|uyari|hata|bilgi","maddeler":[],"sayilar":{}}`
- not: isteğe bağlı

Renkler yalnız pano tokenlarıyla: `var(--ink)`, `var(--muted)`, `var(--edge)`, `var(--line)`, `var(--tamam)`, `var(--dikkat)`, `var(--risk)`, `var(--odak)`, `var(--k2)`, `var(--tint)`, `var(--surface)`.

Thread'e en fazla tek satır yaz: `→ panoda: <başlık>`. Kod, bağlantı ve dosya yolu gibi birebir gerekenler thread'de kalabilir. Karar gerekiyorsa karar kartını kullan.

## 3. Pano güncelliği

`/tmp/runik/surum.json` içindeki `pano` sürümü hafızadakinden büyükse `<kaynak>/pano/pano.html` dosyasını indir, aynı pano bağlantısına yeniden yayınla (capabilities verme, mevcut db korunur) ve hafızadaki pano sürümünü güncelle.
