"""Builds public/start.md, the file the one-line Runik prompt points at: the start instructions
(scripts/start.head.md) + the drawing rules + the PDF rules + a PDF page skeleton, so any agent needs one fetch.
Usage: python3 scripts/start.py   (part of npm run page)"""
import json, os, subprocess, sys, tempfile
K = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(K, '..', 'public')
S = os.path.join(P, 'skill', 'runik')
SITE, GH = 'https://runik.littleman.workers.dev', 'https://raw.githubusercontent.com/littlepilot/runik/main/public'
sys.path.insert(0, S)
import runik_pdf as R

read = lambda p: open(p, encoding='utf-8').read().strip()
head = read(os.path.join(K, 'start.head.md'))
tok = lambda t: ';'.join('--%s:%s' % kv for kv in t.items())
head = head.replace('__SITE__', SITE).replace('__GH__', GH).replace('__LIGHT__', tok(R.LIGHT)).replace('__DARK__', tok(R.DARK))

# The skeleton is the renderer's own output for a placeholder document, without embedded fonts.
doc = {'title': 'TITLE', 'subtitle': 'SUBTITLE', 'lang': 'en', 'date': '2026-01-01',
       'cards': [{'type': 'drawing', 'title': 'SECTION TITLE', 'data': ['<svg viewBox="0 0 760 100" width="100%">…</svg>'], 'note': 'NOTE'}]}
with tempfile.TemporaryDirectory() as d:
    src, out = os.path.join(d, 'doc.json'), os.path.join(d, 'doc.html')
    json.dump(doc, open(src, 'w'))
    subprocess.run([sys.executable, os.path.join(S, 'runik_pdf.py'), src, '-o', out, '--no-fonts'], check=True, stdout=subprocess.DEVNULL)
    skel = read(out)
skel = skel.replace('><', '>\n<').replace('<style>', '<style>\n')
skel = skel.replace('lang="en"', 'lang="LANG"').replace('January 1, 2026', 'DATE')

body = [head, read(os.path.join(S, 'rules.md')), '---', read(os.path.join(S, 'pdf.md')).replace('<skill folder>/', ''),
        '---', '# PDF page skeleton\n\nUsed only when the renderer cannot run (Path B3). Replace the UPPERCASE placeholders; '
        'repeat `<section>` per card; tables, cards and notes use the classes in the style (`table`, `.kcard`, `.summary`, '
        '`.badge`, `.numbers`, `.items`, `.md`, `.note`).\n\n```html\n' + skel + '\n```']
open(os.path.join(P, 'start.md'), 'w', encoding='utf-8').write('\n\n'.join(body) + '\n')
print('public/start.md written (%d KB)' % (os.path.getsize(os.path.join(P, 'start.md')) // 1024))
