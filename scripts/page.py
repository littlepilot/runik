"""Builds public/index.html: template + drawings + install prompt + release notes.
Usage: python3 scripts/drawings.py && python3 scripts/page.py"""
import json, os, html
K = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(K, '..', 'public')
t = open(os.path.join(K, 'page.template.html'), encoding='utf-8').read()
for k, v in json.load(open(os.path.join(K, 'drawings.json'), encoding='utf-8')).items():
    t = t.replace('{{%s}}' % k, v)
ex = json.load(open(os.path.join(K, 'examples.json'), encoding='utf-8'))
t = t.replace('{{examples}}', '\n'.join(
    f'''    <a class="panel excard" href="/examples/{e['slug']}/"><span class="kind">{html.escape(e['kind'])}</span><b>{html.escape(e['title'])}</b><span class="more">Prompt, answer and {len(e['pages'])}-page PDF →</span></a>''' for e in ex))
t = t.replace('{{prompt}}', html.escape(open(os.path.join(P, 'install.txt'), encoding='utf-8').read().strip()))
s = json.load(open(os.path.join(P, 'skill', 'runik', 'version.json'), encoding='utf-8'))
li = lambda n: f'    <li><code>{n["version"]}</code><time datetime="{n["date"]}">{n["date"]}</time><span>{html.escape(n["summary"])}</span></li>'
ul = lambda ns: '  <ul class="notes">\n%s\n  </ul>' % '\n'.join(li(n) for n in ns)
notes = ul(s['notes'][:3])
if len(s['notes']) > 3:
    notes += '\n  <details class="more"><summary>Earlier releases · %d</summary>\n%s\n  </details>' % (len(s['notes']) - 3, ul(s['notes'][3:]))
t = t.replace('{{notes}}', notes).replace('__VERSION__', s['version'])
assert '{{' not in t, 'unfilled placeholder'
open(os.path.join(P, 'index.html'), 'w', encoding='utf-8').write(t)
print('public/index.html written')

# one page per example: the prompt, the drawn answer, the PDF
style = t[t.index('<style>') + 7:t.index('</style>')]
et = open(os.path.join(K, 'example.template.html'), encoding='utf-8').read()
for e in ex:
    pages = '\n'.join(f'''    <a href="/examples/{e['slug']}/{e['slug']}.pdf#page={i + 1}"><img src="/examples/{e['slug']}/{pg}" alt="Page {i + 1} of the PDF" width="637" height="900" loading="lazy"></a>'''
                      for i, pg in enumerate(e['pages']))
    n = len(e['pages'])
    page = (et.replace('{{style}}', style).replace('{{title}}', html.escape(e['title'])).replace('{{kind}}', html.escape(e['kind']))
            .replace('{{prompt}}', html.escape(e['prompt'])).replace('{{line}}', html.escape(e['line'])).replace('{{chat}}', ''.join(e['chat']))
            .replace('{{pdf}}', f"/examples/{e['slug']}/{e['slug']}.pdf").replace('{{npages}}', '%d page%s' % (n, '' if n == 1 else 's'))
            .replace('{{pages}}', pages).replace('{{version}}', s['version']))
    assert '{{' not in page, 'unfilled placeholder in example page'
    open(os.path.join(P, 'examples', e['slug'], 'index.html'), 'w', encoding='utf-8').write(page)
print('example pages: %d' % len(ex))
