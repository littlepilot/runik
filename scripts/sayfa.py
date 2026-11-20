"""public/index.html'i üretir: şablon + çizimler + kurulum prompt'u + sürüm notları.
Kullanım: python3 scripts/cizimler.py && python3 scripts/sayfa.py"""
import json, os, html
K = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(K, '..', 'public')
t = open(os.path.join(K, 'sayfa.template.html'), encoding='utf-8').read()
for k, v in json.load(open(os.path.join(K, 'cizimler.json'), encoding='utf-8')).items():
    t = t.replace('{{%s}}' % k, v)
t = t.replace('{{prompt}}', html.escape(open(os.path.join(P, 'install.txt'), encoding='utf-8').read().strip()))
s = json.load(open(os.path.join(P, 'skill', 'runik', 'version.json'), encoding='utf-8'))
notlar = '\n'.join(f'    <li><code>{n["version"]}</code><time datetime="{n["date"]}">{n["date"]}</time><span>{html.escape(n["summary"])}</span></li>' for n in s['notes'])
t = t.replace('{{notlar}}', notlar).replace('__SURUM__', s['version'])
assert '{{' not in t, 'doldurulmamış yer tutucu'
open(os.path.join(P, 'index.html'), 'w', encoding='utf-8').write(t)
print('public/index.html yazıldı')
