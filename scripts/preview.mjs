// node scripts/preview.mjs svgs.json out-prefix [width]: renders each SVG (light and dark) to PNG for a visual check.
import { readFileSync } from 'node:fs';
import { chromium } from 'playwright';

const [, , file, prefix, width = '760'] = process.argv;
const svgs = JSON.parse(readFileSync(file, 'utf8'));
const THEMES = {
  light: '--ink:#1b1f2a;--muted:#5f6779;--edge:#8a93a5;--line:#dadfe7;--good:#15803d;--warn:#b45309;--bad:#c81e1e;--focus:#2f5bd8;--k2:#3f8f84;--tint:#eef0f4;--surface:#fff;--bg:#fff',
  dark: '--ink:#e8ebf2;--muted:#98a1b3;--edge:#636c80;--line:#2c3240;--good:#4ade80;--warn:#fbbf24;--bad:#f87171;--focus:#7d9cf5;--k2:#7cc6bc;--tint:#1d2230;--surface:#191d26;--bg:#191d26',
};
const browser = await chromium.launch();
for (const [mode, tokens] of Object.entries(THEMES)) {
  const page = await browser.newPage({ viewport: { width: Number(width) + 40, height: 600 } });
  const body = svgs.map((s) => `<div style="width:${width}px">${s}</div>`).join('');
  await page.setContent(`<html><head><style>:root{${tokens}}body{margin:0;padding:20px;background:var(--bg);font-family:Inter,system-ui,sans-serif}div{margin-bottom:20px}svg{display:block}svg text{font-variant-ligatures:none}</style></head><body>${body}</body></html>`);
  const els = await page.$$('body > div');
  for (let i = 0; i < els.length; i++) await els[i].screenshot({ path: `${prefix}-${i + 1}-${mode}.png` });
  await page.close();
}
await browser.close();
console.log(`preview: ${svgs.length} drawing(s)`);
