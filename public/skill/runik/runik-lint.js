// runik-lint: node runik-lint.js <card.json | svgs.json> [purify.min.js]
// Takes a board card JSON (data_json field) or a plain array of SVG strings. Exits with code 1 on any violation.
// The board sanitizes with the svg + svgFilters profile (shadow and texture filters in object drawings survive).
const fs = require('fs');
const path = require('path');
// Playwright: local install first, then the global npm root.
const { chromium } = (() => {
  try { return require('playwright'); } catch {}
  try { return require(path.join(require('child_process').execSync('npm root -g', { encoding: 'utf8' }).trim(), 'playwright')); } catch {}
  console.error('runik-lint needs Playwright: npm i -g playwright && npx playwright install chromium');
  process.exit(2);
})();
const TOKENS = ['ink', 'muted', 'edge', 'line', 'good', 'warn', 'bad', 'focus', 'k2', 'tint', 'bg', 'surface'];
const ADD_ATTR = ['font-size', 'font-weight', 'text-anchor', 'stroke-dasharray', 'fill-opacity', 'stroke-linecap', 'stroke-linejoin', 'role', 'aria-label'];
(async () => {
  const inp = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const svgs = Array.isArray(inp) ? inp : JSON.parse(inp.data_json);
  const purify = fs.readFileSync(process.argv[3] || path.join(__dirname, 'purify.min.js'), 'utf8');
  const problems = [];
  const ids = {};
  svgs.forEach((s, i) => {
    for (const m of s.matchAll(/var\(--([a-z0-9-]+)\)/g)) if (!TOKENS.includes(m[1])) problems.push(`#${i + 1}: undefined token --${m[1]}`);
    for (const m of s.matchAll(/\sid="([^"]+)"/g)) (ids[m[1]] = ids[m[1]] || []).push(i + 1);
    if (/[a-z][A-Z][a-z]*=/.test(s.replace(/(viewBox|stdDeviation|baseFrequency|numOctaves|gradientUnits)=/g, ''))) problems.push(`#${i + 1}: camelCase attribute (must be kebab-case)`);
    if (/<marker|<use|<foreignObject|<animate|<set\b|\son[a-z]+=/.test(s)) problems.push(`#${i + 1}: element DOMPurify will strip`);
  });
  for (const [id, where] of Object.entries(ids)) if (where.length > 1) problems.push(`id "${id}" repeats in drawings ${where.join(', ')}`);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 800, height: 800 } });
  await p.setContent(`<html><head><style>:root{${TOKENS.map(t => `--${t}:#888`).join(';')}}body{margin:0;font-family:Inter,system-ui,sans-serif}svg text{font-variant-ligatures:none;font-feature-settings:"calt" 0}</style><script>${purify}</script></head><body><div id="w" style="width:760px"></div></body></html>`);
  const res = await p.evaluate(({ svgs, ADD_ATTR }) => {
    const out = [];
    const count = s => { const d = document.createElement('div'); d.innerHTML = s; return d.querySelectorAll('*').length; };
    svgs.forEach((s, i) => {
      const clean = DOMPurify.sanitize(s, { USE_PROFILES: { svg: true, svgFilters: true }, ADD_ATTR });
      const lost = count(s) - count(clean);
      if (lost) out.push(`#${i + 1}: DOMPurify stripped ${lost} element(s)`);
      const w = document.getElementById('w'); w.innerHTML = clean;
      const svg = w.querySelector('svg'); if (!svg) { out.push(`#${i + 1}: no svg`); return; }
      const vb = svg.viewBox.baseVal;
      if (!svg.getAttribute('role') || !svg.getAttribute('aria-label')) out.push(`#${i + 1}: missing role/aria-label`);
      const texts = [...svg.querySelectorAll('text')].map(t => ({ t: t.textContent, b: t.getBBox(), fs: parseFloat(t.getAttribute('font-size') || svg.getAttribute('font-size') || 13) }));
      for (const x of texts) {
        if (x.b.x < 20 || x.b.x + x.b.width > vb.width - 20) out.push(`#${i + 1}: runs off the side "${x.t}"`);
        if (x.b.y + x.b.height > vb.height) out.push(`#${i + 1}: runs off the bottom "${x.t}"`);
        const screen = x.fs * 600 / vb.width;
        if (screen < 9) out.push(`#${i + 1}: ${screen.toFixed(1)} px text on a 600 px panel "${x.t}"`);
      }
      for (let a = 0; a < texts.length; a++) for (let c = a + 1; c < texts.length; c++) {
        const A = texts[a].b, C = texts[c].b;
        const ox = Math.min(A.x + A.width, C.x + C.width) - Math.max(A.x, C.x);
        const oy = Math.min(A.y + A.height, C.y + C.height) - Math.max(A.y, C.y);
        if (ox > 1 && oy > 2) out.push(`#${i + 1}: overlapping text "${texts[a].t}" × "${texts[c].t}"`);
      }
    });
    return out;
  }, { svgs, ADD_ATTR });
  await b.close();
  problems.push(...res);
  if (problems.length) { console.log(problems.join('\n')); process.exit(1); }
  console.log(`clean: ${svgs.length} drawing(s)`);
})();
