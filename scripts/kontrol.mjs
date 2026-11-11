// Yayından önce: çizim kuralları (runik-lint), HTML geçerliliği, yer tutucu, açık/koyu + dar/geniş ekran görüntüsü.
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { createServer } from 'node:http';
import { join, extname } from 'node:path';
import { chromium } from 'playwright';

const kok = new URL('..', import.meta.url).pathname;
const pub = join(kok, 'public');
const hatalar = [];
const html = readFileSync(join(pub, 'index.html'), 'utf8');

// 1. yer tutucu
for (const f of ['index.html', 'kur.txt', 'kurulum.md', 'skill/runik/SKILL.md'])
  if (/__(SITE|GH)__/.test(readFileSync(join(pub, f), 'utf8'))) hatalar.push(`${f}: __SITE__/__GH__ doldurulmamış`);

// 2. çizim kuralları
const svgs = html.match(/<svg viewBox="0 0 760[\s\S]*?<\/svg>/g) || [];
mkdirSync(join(kok, 'ekran'), { recursive: true });
writeFileSync(join(kok, 'ekran', 'svgs.json'), JSON.stringify(svgs));
try {
  console.log(execFileSync('node', [join(pub, 'skill/runik-cizim/runik-lint.js'), join(kok, 'ekran/svgs.json')], { encoding: 'utf8' }).trim());
} catch (e) { hatalar.push('runik-lint:\n' + (e.stdout || e.message)); }

// 3. HTML
try { execFileSync('npx', ['--no-install', 'html-validate', join(pub, 'index.html'), join(pub, '404.html')], { stdio: 'pipe' }); console.log('html: temiz'); }
catch (e) { hatalar.push('html-validate:\n' + (e.stdout?.toString() || e.message)); }

// 4. ekran görüntüleri
const tip = { '.html': 'text/html; charset=utf-8', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.json': 'application/json', '.md': 'text/markdown', '.txt': 'text/plain' };
const sunucu = createServer((q, r) => {
  let p = decodeURIComponent(q.url.split('?')[0]); if (p.endsWith('/')) p += 'index.html';
  try { r.writeHead(200, { 'content-type': tip[extname(p)] || 'application/octet-stream' }); r.end(readFileSync(join(pub, p))); }
  catch { r.writeHead(404); r.end(); }
}).listen(0);
const port = sunucu.address().port;
const b = await chromium.launch();
for (const [ad, w, tema] of [['genis-acik', 1280, 'light'], ['genis-koyu', 1280, 'dark'], ['dar-acik', 390, 'light'], ['dar-koyu', 390, 'dark']]) {
  const p = await b.newPage({ viewport: { width: w, height: 900 }, colorScheme: tema });
  await p.goto(`http://localhost:${port}/`, { waitUntil: 'networkidle' });
  const tasma = await p.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  if (tasma > 0) hatalar.push(`${ad}: yatay taşma ${tasma}px`);
  const font = await p.evaluate(() => document.fonts.check('600 16px Inter') && document.fonts.check('700 40px "Space Grotesk"'));
  if (!font) hatalar.push(`${ad}: font yüklenmedi`);
  await p.screenshot({ path: join(kok, 'ekran', ad + '.png'), fullPage: true });
  await p.close();
}
await b.close(); sunucu.close();

if (hatalar.length) { console.error(hatalar.join('\n')); process.exit(1); }
console.log('kontrol: temiz · ekran görüntüleri ekran/ içinde');
