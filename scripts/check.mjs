// Before deploy: drawing rules (runik-lint), HTML validity, placeholders, light/dark + narrow/wide screenshots.
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { createServer } from 'node:http';
import { join, extname } from 'node:path';
import { chromium } from 'playwright';

const root = new URL('..', import.meta.url).pathname;
const pub = join(root, 'public');
const errors = [];
const html = readFileSync(join(pub, 'index.html'), 'utf8');

// 1. placeholders
for (const f of ['index.html', 'install.txt', 'install.md', 'install.sh', 'skill/runik/SKILL.md'])
  if (/__(SITE|GH)__/.test(readFileSync(join(pub, f), 'utf8'))) errors.push(`${f}: __SITE__/__GH__ not filled in`);

// 2. drawing rules
const svgs = html.match(/<svg viewBox="0 0 760[\s\S]*?<\/svg>/g) || [];
mkdirSync(join(root, 'screenshots'), { recursive: true });
writeFileSync(join(root, 'screenshots', 'svgs.json'), JSON.stringify(svgs));
try {
  console.log(execFileSync('node', [join(pub, 'skill/runik/runik-lint.js'), join(root, 'screenshots/svgs.json')], { encoding: 'utf8' }).trim());
} catch (e) { errors.push('runik-lint:\n' + (e.stdout || e.message)); }

// 3. HTML
try { execFileSync('npx', ['--no-install', 'html-validate', join(pub, 'index.html'), join(pub, '404.html')], { stdio: 'pipe' }); console.log('html: clean'); }
catch (e) { errors.push('html-validate:\n' + (e.stdout?.toString() || e.message)); }

// 4. screenshots
const types = { '.html': 'text/html; charset=utf-8', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.json': 'application/json', '.md': 'text/markdown', '.txt': 'text/plain' };
const server = createServer((q, r) => {
  let p = decodeURIComponent(q.url.split('?')[0]); if (p.endsWith('/')) p += 'index.html';
  try { r.writeHead(200, { 'content-type': types[extname(p)] || 'application/octet-stream' }); r.end(readFileSync(join(pub, p))); }
  catch { r.writeHead(404); r.end(); }
}).listen(0);
const port = server.address().port;
const b = await chromium.launch();
for (const [name, w, scheme] of [['wide-light', 1280, 'light'], ['wide-dark', 1280, 'dark'], ['narrow-light', 390, 'light'], ['narrow-dark', 390, 'dark']]) {
  const p = await b.newPage({ viewport: { width: w, height: 900 }, colorScheme: scheme });
  await p.goto(`http://localhost:${port}/`, { waitUntil: 'networkidle' });
  const overflow = await p.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  if (overflow > 0) errors.push(`${name}: horizontal overflow ${overflow}px`);
  const font = await p.evaluate(() => document.fonts.check('600 16px Inter') && document.fonts.check('700 40px "Space Grotesk"'));
  if (!font) errors.push(`${name}: font not loaded`);
  await p.screenshot({ path: join(root, 'screenshots', name + '.png'), fullPage: true });
  await p.close();
}
await b.close(); server.close();

if (errors.length) { console.error(errors.join('\n')); process.exit(1); }
console.log('check: clean · screenshots in screenshots/');
