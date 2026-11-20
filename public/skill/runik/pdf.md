# Runik PDF

When the user asks for an answer, a result or the whole conversation as a PDF ("give me this as a PDF", "PDF olarak ver", "export to PDF"), deliver it as a **Runik PDF**: the same drawings, cards and tables as on the board, laid out on A4 pages with the Runik type and colors. Ask nothing first: take the most recent answer (or what the user named), and say which part you used in one line.

The PDF follows the drawing rules (`rules.md`) like everything else: text is the last resort, every visible text is in the user's language.

## 1. Build the document

A Runik document is a JSON file: a title and a list of cards in exactly the board's card format.

```json
{
  "title": "<the answer itself, at most 8 words>",
  "subtitle": "<optional, one line: topic or question>",
  "lang": "<the user's language code: tr, en, ...>",
  "date": "<YYYY-MM-DD, today>",
  "cards": [
    { "type": "drawing", "title": "<section title>", "data_json": "[\"<svg …>\", \"<svg …>\"]", "note": "<optional>" },
    { "type": "card", "title": "…", "data_json": "{\"summary\":\"…\",\"status\":\"ok\",\"items\":[],\"numbers\":{}}" },
    { "type": "table", "title": "…", "data_json": "{\"columns\":[],\"rows\":[[]]}" },
    { "type": "markdown", "title": "…", "data_json": "a short note" }
  ]
}
```

- `data_json` may also be given as `data` (the object itself instead of a string).
- Cards already on the board can be copied as they are (read them with ArtifactData). Charts (Vega-Lite) and diagrams (Mermaid) need browser libraries: redraw them as SVG drawings for a PDF.
- Order the cards as a reader should meet them: the answer first, then the explanation, then details.
- A PDF can carry more than a chat reply, but the text budget per drawing (§0) still holds. Put details that text would carry into a separate `markdown` card at the end.
- Drawings use the board tokens (`var(--ink)` …); the PDF defines them.

## 2. Render it

```bash
python3 <skill folder>/runik_pdf.py doc.json -o <name>.pdf
```

The script needs only Python 3 and one of Chrome/Chromium (a Playwright Chromium is found too), the Playwright Python package, or WeasyPrint. `python3 runik_pdf.py doctor` shows what the machine has. If none is found it writes `<name>.html` instead and exits with code 3: that page prints to the same document from any browser (Print › Save as PDF); give it to the user with that one instruction.

Name the file after the title in the user's language, short, lowercase, with hyphens (`veri-yakinligi.pdf`).

## 3. Check and deliver

Open the PDF (or look at its pages) before delivering: no drawing is cut between pages, nothing overlaps, page numbers are there. Then deliver the file the way the environment allows (attach it, save it next to the user's work, or give its path) with one line in the user's language.
