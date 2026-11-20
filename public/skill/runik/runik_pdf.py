#!/usr/bin/env python3
"""runik_pdf.py - turn Runik cards into a Runik-style PDF (A4) or a standalone HTML page.

    python3 runik_pdf.py doc.json -o answer.pdf      PDF (needs Chrome/Chromium, Playwright, or WeasyPrint)
    python3 runik_pdf.py doc.json -o answer.html     standalone HTML page (light/dark on screen, light when printed)
    python3 runik_pdf.py doc.json -o x.html --no-fonts   same, without the embedded fonts (small file)
    python3 runik_pdf.py doctor                      what this machine can use

doc.json is either a list of cards or {"title", "subtitle", "lang", "date", "cards": [...]}.
A card is the same document the Runik Board stores: {"type", "title", "data_json" (or "data"), "note"}.
Types: drawing (array of SVG strings), table ({"columns", "rows"}), card ({"summary", "status", "items", "numbers"}),
markdown (a short note). chart and diagram need a browser library, so draw them as SVG for a PDF.

When no PDF engine is found, the script writes the HTML next to the requested PDF and exits with code 3;
the HTML prints to the same document from any browser (Print > Save as PDF).
Only the Python standard library is required.
"""
import base64, datetime, glob, html, json, os, re, shutil, subprocess, sys, tempfile, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
LIGHT = dict(ink='#1b1f2a', muted='#5f6779', edge='#8a93a5', line='#dadfe7', good='#15803d', warn='#b45309', bad='#c81e1e',
             focus='#2f5bd8', k2='#3f8f84', tint='#eef0f4', surface='#ffffff', bg='#ffffff')
DARK = dict(ink='#e8ebf2', muted='#98a1b3', edge='#636c80', line='#2c3240', good='#4ade80', warn='#fbbf24', bad='#f87171',
            focus='#7d9cf5', k2='#7cc6bc', tint='#1d2230', surface='#191d26', bg='#101319')
ICON = dict(ok='✓', warn='!', error='✗', info='i')
WORDS = dict(tr=dict(page='Sayfa', months='Ocak Şubat Mart Nisan Mayıs Haziran Temmuz Ağustos Eylül Ekim Kasım Aralık'),
             en=dict(page='Page', months='January February March April May June July August September October November December'))
FONTS = [('Inter', 'inter.woff2', '100 900', 'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD'),
         ('Inter', 'inter-tr.woff2', '100 900', 'U+011E-011F,U+0130-0131,U+015E-015F'),
         ('Space Grotesk', 'sg.woff2', '300 700', 'U+0000-00FF,U+0131,U+2000-206F,U+2212'),
         ('Space Grotesk', 'sg-tr.woff2', '300 700', 'U+011E-011F,U+0130-0131,U+015E-015F')]
E = html.escape
NO_FONTS = False


# ------------------------------------------------------------------ input
def load(path):
    raw = json.loads(Path(path).read_text(encoding='utf-8'))
    doc = {'cards': raw} if isinstance(raw, list) else dict(raw)
    cards = []
    for i, c in enumerate(doc.get('cards') or []):
        c = dict(c)
        if 'data' not in c:
            d = c.get('data_json')
            try:
                c['data'] = json.loads(d) if isinstance(d, str) else d
            except ValueError:
                c['data'] = d  # markdown/diagram may be a plain string
        if c.get('type', 'drawing') in ('chart', 'diagram'):
            sys.exit('runik_pdf: card %d (%s) is a %s; a PDF needs it drawn as SVG (type drawing).' % (i + 1, c.get('title', ''), c['type']))
        cards.append(c)
    if not cards:
        sys.exit('runik_pdf: no cards in %s' % path)
    doc['cards'] = cards
    doc.setdefault('title', cards[0].get('title', 'Runik'))
    return doc


def clean_svg(s):
    '''The drawings are the agent's own, but a PDF must never run code or fetch anything.'''
    s = re.sub(r'<script\b.*?</script\s*>', '', s, flags=re.S | re.I)
    s = re.sub(r'<foreignObject\b.*?</foreignObject\s*>', '', s, flags=re.S | re.I)
    s = re.sub(r'\son[a-z]+\s*=\s*("[^"]*"|\'[^\']*\'|[^\s>]+)', '', s, flags=re.I)
    s = re.sub(r'\s(?:xlink:)?href\s*=\s*("(?!#)[^"]*"|\'(?!#)[^\']*\')', '', s, flags=re.I)
    return s


def inline_md(t):
    t = E(t)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<i>\1</i>', t)
    return t


def markdown(src):
    out, para, lst = [], [], None
    def flush():
        nonlocal para, lst
        if para: out.append('<p>%s</p>' % inline_md(' '.join(para))); para = []
        if lst: out.append('<%s>%s</%s>' % (lst[0], ''.join('<li>%s</li>' % inline_md(x) for x in lst[1]), lst[0])); lst = None
    for line in str(src).splitlines():
        s = line.strip()
        m_ul, m_ol, m_h = re.match(r'[-*•]\s+(.*)', s), re.match(r'\d+[.)]\s+(.*)', s), re.match(r'(#{1,4})\s+(.*)', s)
        if not s: flush()
        elif m_h: flush(); out.append('<h4>%s</h4>' % inline_md(m_h.group(2)))
        elif m_ul or m_ol:
            kind = 'ul' if m_ul else 'ol'
            if para or (lst and lst[0] != kind): flush()
            lst = lst or (kind, [])
            lst[1].append((m_ul or m_ol).group(1))
        else:
            if lst: flush()
            para.append(s)
    flush()
    return ''.join(out)


def num(v, lang):
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return E(str(v))
    s = '{:,}'.format(v) if isinstance(v, int) else '{:,.2f}'.format(v).rstrip('0').rstrip('.')
    return s.replace(',', '\x00').replace('.', ',').replace('\x00', '.') if lang == 'tr' else s


def render_card(c, lang):
    t, d = c.get('type', 'drawing'), c.get('data')
    body = ''
    if t == 'drawing':
        svgs = d if isinstance(d, list) else [d]
        body = ''.join('<figure>%s</figure>' % clean_svg(str(s)) for s in svgs if s)
    elif t == 'table':
        cols, rows = d.get('columns', []), d.get('rows', [])
        isnum = [bool(rows) and all(isinstance(r[i], (int, float)) or re.fullmatch(r'[-+~%€$₺\d.,\s]+', str(r[i]) or 'x')
                                    for r in rows if i < len(r)) for i in range(len(cols))]
        head = ''.join('<th%s>%s</th>' % (' class="num"' if isnum[i] else '', E(str(h))) for i, h in enumerate(cols))
        trs = ''.join('<tr>%s</tr>' % ''.join('<td%s>%s</td>' % (' class="num"' if i < len(isnum) and isnum[i] else '', num(v, lang))
                                              for i, v in enumerate(r)) for r in rows)
        body = '<table><thead><tr>%s</tr></thead><tbody>%s</tbody></table>' % (head, trs)
    elif t == 'card':
        st = d.get('status', 'info')
        body = '<div class="kcard %s"><div class="summary"><span class="badge">%s</span><span>%s</span></div>' % (
            E(st), ICON.get(st, 'i'), inline_md(d.get('summary', '')))
        if d.get('numbers'):
            body += '<div class="numbers">%s</div>' % ''.join('<div><b>%s</b><span>%s</span></div>' % (num(v, lang), E(str(k)))
                                                          for k, v in d['numbers'].items())
        if d.get('items'):
            body += '<ul class="items">%s</ul>' % ''.join('<li>%s</li>' % inline_md(str(x)) for x in d['items'])
        body += '</div>'
    elif t == 'markdown':
        body = '<div class="md">%s</div>' % markdown(d if isinstance(d, str) else c.get('data_json', ''))
    else:
        sys.exit('runik_pdf: unknown card type %r' % t)
    title = c.get('title', '')
    note = '<p class="note">%s</p>' % inline_md(c['note']) if c.get('note') else ''
    return '<section class="c-%s">%s%s%s</section>' % (t, '<h2>%s</h2>' % E(title) if title else '', body, note)


# ------------------------------------------------------------------ page
def font_css():
    out = []
    if NO_FONTS:
        return ''
    for fam, f, w, rng in FONTS:
        p = HERE / f
        if p.exists():
            out.append('@font-face{font-family:"%s";src:url(data:font/woff2;base64,%s) format("woff2");font-weight:%s;unicode-range:%s}'
                       % (fam, base64.b64encode(p.read_bytes()).decode(), w, rng))
    return ''.join(out)


def tokens(t):
    return ';'.join('--%s:%s' % kv for kv in t.items())


def date_text(doc, lang):
    d = doc.get('date') or datetime.date.today().isoformat()
    try:
        y, m, dd = (int(x) for x in d[:10].split('-'))
        w = WORDS.get(lang)
        return '%d %s %d' % (dd, w['months'].split()[m - 1], y) if w and lang == 'tr' else \
            ('%s %d, %d' % (w['months'].split()[m - 1], dd, y) if w else d)
    except ValueError:
        return d


def page(doc):
    lang = (doc.get('lang') or 'en').split('-')[0].lower()
    w = WORDS.get(lang, WORDS['en'])
    title = doc['title']
    sub = doc.get('subtitle', '')
    cards = ''.join(render_card(c, lang) for c in doc['cards'])
    css = '''
%(fonts)s
:root{%(light)s;color-scheme:light}
@media screen and (prefers-color-scheme:dark){:root{%(dark)s;color-scheme:dark}}
@page{size:A4;margin:16mm 16mm 18mm 16mm;
  @bottom-left{content:"ᚱ Runik · %(ftitle)s";font:500 7.5pt "Space Grotesk",system-ui,sans-serif;color:#5f6779}
  @bottom-right{content:"%(pw)s " counter(page) " / " counter(pages);font:7.5pt Inter,system-ui,sans-serif;color:#5f6779}}
*{box-sizing:border-box}
html{background:var(--bg)}
body{margin:0 auto;max-width:820px;padding:32px 24px 48px;color:var(--ink);background:var(--bg);font:10.5pt/1.5 Inter,system-ui,sans-serif;
  -webkit-print-color-adjust:exact;print-color-adjust:exact}
header{border-bottom:1.5px solid var(--line);padding-bottom:14px;margin-bottom:20px}
.brand{font:600 9pt "Space Grotesk",system-ui,sans-serif;color:var(--muted);letter-spacing:.04em;display:flex;gap:6px;align-items:center}
.brand b{color:#c2410c;font-size:12pt}
h1{font:700 22pt/1.2 "Space Grotesk",system-ui,sans-serif;margin:10px 0 4px;text-wrap:balance}
.sub{color:var(--muted);margin:0}
.date{color:var(--muted);font-size:9pt;margin-top:6px}
section{margin:0 0 22px}
.c-table,.c-card,.c-markdown{break-inside:avoid}
h2{font:600 13.5pt/1.3 "Space Grotesk",system-ui,sans-serif;margin:0 0 10px;break-after:avoid;text-wrap:balance}
figure{margin:0 0 14px;break-inside:avoid}
figure svg{width:100%%;height:auto;display:block}
figure svg text{font-family:Inter,system-ui,sans-serif;font-variant-ligatures:none;font-feature-settings:"calt" 0}
.note{color:var(--muted);font-size:9pt;margin:6px 0 0}
table{border-collapse:collapse;width:100%%;font-size:9.5pt;font-variant-numeric:tabular-nums;break-inside:auto}
tr{break-inside:avoid}
th{text-align:left;font-weight:600;color:var(--muted);font-size:8pt;letter-spacing:.05em;text-transform:uppercase;border-bottom:2px solid var(--line);padding:6px 8px}
td{border-bottom:1px solid var(--line);padding:6px 8px;vertical-align:top}
.num{text-align:right}
.kcard{display:grid;gap:12px;break-inside:avoid}
.summary{font-size:13pt;font-weight:600;display:flex;gap:10px;align-items:center}
.badge{flex:none;width:28px;height:28px;border-radius:50%%;display:grid;place-items:center;font-size:12pt;border:1.5px solid var(--focus);color:var(--focus)}
.ok .badge{border-color:var(--good);color:var(--good)} .warn .badge{border-color:var(--warn);color:var(--warn)} .error .badge{border-color:var(--bad);color:var(--bad)}
.numbers{display:flex;flex-wrap:wrap;gap:10px}
.numbers div{border:1px solid var(--line);border-radius:8px;padding:8px 12px;min-width:96px}
.numbers b{display:block;font:700 17pt "Space Grotesk",system-ui,sans-serif;font-variant-numeric:tabular-nums}
.numbers span{font-size:8.5pt;color:var(--muted)}
.items{margin:0;padding:0;list-style:none;display:grid;gap:4px}
.items li{padding-left:16px;position:relative}
.items li::before{content:"";position:absolute;left:3px;top:.6em;width:6px;height:6px;border-radius:2px;background:var(--focus)}
.md p{margin:0 0 8px} .md h4{font-size:10.5pt;margin:10px 0 4px} .md ul,.md ol{margin:0 0 8px;padding-left:20px}
code{font:9pt ui-monospace,"SF Mono",Menlo,monospace;background:var(--tint);padding:1px 4px;border-radius:4px}
@media print{html,body{background:#fff}body{max-width:none;padding:0}}
''' % dict(fonts=font_css(), light=tokens(LIGHT), dark=tokens(DARK), pw=w['page'],
           ftitle=title.replace('\\', '').replace('"', "'")[:80])
    csp = "default-src 'none'; style-src 'unsafe-inline'; font-src data:; img-src data:"
    return ('<!doctype html><html lang="%s"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta http-equiv="Content-Security-Policy" content="%s"><title>%s</title><style>%s</style></head><body>'
            '<header><div class="brand"><b>ᚱ</b> Runik</div><h1>%s</h1>%s<div class="date">%s</div></header>%s</body></html>') % (
        E(lang), csp, E(title), css, E(title), '<p class="sub">%s</p>' % inline_md(sub) if sub else '', E(date_text(doc, lang)), cards)


# ------------------------------------------------------------------ engines
def find_chrome():
    '''Headless shells first (built for printing), then installed browsers, then Playwright's full Chromium.'''
    home = str(Path.home())
    roots = [r for r in (os.environ.get('PLAYWRIGHT_BROWSERS_PATH'), '/opt/pw-browsers', home + '/.cache/ms-playwright',
                         home + '/Library/Caches/ms-playwright', home + '/AppData/Local/ms-playwright') if r]
    c = [os.environ.get('RUNIK_CHROME'), shutil.which('chrome-headless-shell')]
    for r in roots:
        c += sorted(glob.glob('%s/chromium_headless_shell-*/*/chrome-headless-shell*' % r), reverse=True)
    c += [shutil.which(n) for n in ('google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser', 'chrome', 'microsoft-edge', 'msedge')]
    for a in ('Google Chrome', 'Chromium', 'Microsoft Edge', 'Brave Browser'):
        c += ['%s/Applications/%s.app/Contents/MacOS/%s' % (h, a, a) for h in ('', home)]
    c += ['C:/Program Files/Google/Chrome/Application/chrome.exe', 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe']
    for r in roots:
        for n in ('chrome', 'chrome.exe', '*.app/Contents/MacOS/*'):
            c += sorted(glob.glob('%s/chromium-*/chrome-*/%s' % (r, n)), reverse=True)
    return next((p for p in c if p and os.path.isfile(p) and os.access(p, os.X_OK)), None)


def with_chrome(src, out):
    '''Print with Chrome. Some builds write the PDF and then linger, so wait for the file and stop the process.'''
    ch = find_chrome()
    if not ch:
        return False
    prof = tempfile.mkdtemp(prefix='runik-')
    args = [ch] + ([] if 'headless-shell' in ch else ['--headless=new']) + [
        '--no-sandbox', '--disable-gpu', '--no-first-run', '--user-data-dir=' + prof,
        '--no-pdf-header-footer', '--print-to-pdf=' + str(out), src.as_uri()]
    try:
        proc = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except OSError:
        return False
    try:
        size, deadline = -1, time.time() + 120
        while time.time() < deadline:
            if proc.poll() is not None and not out.exists():
                return False
            if out.exists():
                s = out.stat().st_size
                if s > 0 and s == size:
                    break
                size = s
            time.sleep(0.5)
    finally:
        if proc.poll() is None:
            proc.kill()
        proc.wait()
        shutil.rmtree(prof, ignore_errors=True)
    return out.exists() and out.stat().st_size > 0


def with_playwright(src, out):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return False
    try:
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page()
            pg.goto(src.as_uri())
            pg.pdf(path=str(out), prefer_css_page_size=True, print_background=True)
            b.close()
    except Exception:
        return False
    return out.exists()


def with_weasyprint(src, out):
    try:
        import weasyprint
    except ImportError:
        return False
    try:
        weasyprint.HTML(filename=str(src)).write_pdf(str(out))
    except Exception:
        return False
    return out.exists()


def pages(pdf):
    b = pdf.read_bytes()
    return len(re.findall(rb'/Type\s*/Page(?!s)', b)) or '?'


def doctor():
    ch = find_chrome()
    print('chrome:', ch or 'not found (set RUNIK_CHROME=/path/to/chrome)')
    for mod in ('playwright', 'weasyprint'):
        try:
            __import__(mod); print(mod + ': yes')
        except ImportError:
            print(mod + ': no')
    print('fonts:', ', '.join(f for _, f, _, _ in FONTS if (HERE / f).exists()) or 'none (system sans-serif is used)')


def main(argv):
    if argv[:1] == ['doctor']:
        return doctor()
    global NO_FONTS
    NO_FONTS = '--no-fonts' in argv
    argv = [a for a in argv if a != '--no-fonts']
    if not argv or argv[0] in ('-h', '--help'):
        print(__doc__); return
    src = Path(argv[0])
    out = Path(argv[argv.index('-o') + 1]) if '-o' in argv else src.with_suffix('.pdf')
    doc = load(src)
    page_html = page(doc)
    if out.suffix.lower() in ('.html', '.htm'):
        out.write_text(page_html, encoding='utf-8')
        print('runik_pdf: %s (%d cards)' % (out, len(doc['cards'])))
        return
    tmp = Path(tempfile.mkdtemp(prefix='runik-')) / 'doc.html'
    tmp.write_text(page_html, encoding='utf-8')
    out = out.resolve()
    out.exists() and out.unlink()
    for name, fn in (('chrome', with_chrome), ('playwright', with_playwright), ('weasyprint', with_weasyprint)):
        if fn(tmp, out):
            print('runik_pdf: %s (%s pages, %d cards, %s)' % (out, pages(out), len(doc['cards']), name))
            shutil.rmtree(tmp.parent, ignore_errors=True)
            return
    fallback = out.with_suffix('.html')
    shutil.move(str(tmp), str(fallback))
    print('runik_pdf: no PDF engine (Chrome, Playwright or WeasyPrint) found; wrote %s instead. '
          'Open it in a browser and use Print > Save as PDF.' % fallback)
    sys.exit(3)


if __name__ == '__main__':
    main(sys.argv[1:])
