# ᚱ Runik

Claude Code için görsel cevap dili. Cevaplar uzun metin yerine kurallı çizimlerle, yan ekrandaki bir panoda gösterilir.

- Site: https://runik.littleman.workers.dev
- Kurulum: sitedeki prompt'u kopyalayıp bir Claude Code projesine yapıştır.

## Yapı

| Yol | Ne |
|---|---|
| `public/` | Cloudflare Workers'a olduğu gibi giden statik site |
| `public/skill/runik-cizim/` | Çizim kuralları: **tek kaynak** (SKILL.md, runik-lint.js) |
| `public/skill/runik/SKILL.md` | Projelere kurulan ince yükleyici skill |
| `public/skill/surum.json` | Sürüm, pano sürümü, sürüm notları |
| `public/pano/pano.html` | Runik Pano artifact şablonu |
| `public/kur.txt`, `public/kurulum.md` | Yapıştırılan prompt ve Claude'un izlediği adımlar |
| `scripts/` | Sayfa üretici (çizimler + şablon → index.html) ve kontrol |

## Kural güncellemek

1. `public/skill/runik-cizim/SKILL.md` dosyasını düzenle.
2. `public/skill/surum.json` içinde `surum`u artır, `notlar`a bir satır ekle. Pano değiştiyse `pano`yu artır.
3. `npm run sayfa && npm run kontrol`
4. `git push` → kontrol + yayın. Kurulu her proje bir sonraki thread'de yeni kuralları çeker.

## Yerel

    npm ci
    npm run yerel      # wrangler dev
    npm run yayinla    # wrangler deploy (elle)

Otomatik yayın için repo sırlarına `CLOUDFLARE_API_TOKEN` (Workers Scripts: Edit) ve `CLOUDFLARE_ACCOUNT_ID` ekle; yoksa CI yalnız kontrol eder.
