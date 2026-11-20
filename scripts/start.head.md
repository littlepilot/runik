# Runik: start here

You are reading this because the user pasted the Runik line into a conversation with you. Runik is a visual answer language: instead of long text, answers are drawn as rule-based SVG drawings (and short cards and tables). Read this file to the end once, then do **one** of the two paths below. Don't report progress; one short message at the end is enough.

Everything Runik produces (drawings, cards, titles, the message to the user, PDFs) is in **the user's language**: the language of their messages. This file is in English only so every agent can read it.

Sources (the first one that opens is used):
- SITE = __SITE__
- GITHUB = __GH__

## Which path?

- **Path A, install**: you can run shell commands on the user's machine and `~/.claude` exists or can be created (Claude Code: CLI, desktop app, IDE, cloud session). Runik becomes a permanent global skill with a live board.
- **Path B, use it now**: everything else (claude.ai or the Claude apps without a shell, ChatGPT, Gemini, Copilot, other chat agents, or Claude Code where installing fails). Runik works for the rest of this conversation from this file alone.

If unsure, try Path A; if its installer cannot run, fall back to Path B.

## Path A: install (Claude Code)

Download the install steps and follow them in order:

```bash
curl -fsSL __SITE__/install.md || curl -fsSL __GH__/install.md
```

They install the skill to `~/.claude/skills/runik`, create the board and write the first card. After that, ignore the rest of this file: the installed skill carries the same rules.

## Path B: use it now (any chat agent)

From now until the end of this conversation, answer the way the rules below say. You need nothing installed.

### B1. What to draw

Before every reply that explains something, compares options, reports results or answers a question a picture could carry, draw it: follow **Runik drawing rules** (below, §0–§7) for every drawing. Skip drawing for one-line confirmations and for replies that are only code, commands or links. Things that must be exact (code, commands, links) stay as text.

The rules mention helper files "in this folder" (`runik_object.py`, `example_object.py`, `runik-lint.js`). Here they live at `__SITE__/skill/runik/<file>`: use them only if you can run code and download; otherwise apply the same rules by hand. The board (cards, ArtifactData) is a Claude Code feature: in Path B the drawing goes into the conversation as described in B2.

### B2. How to show a drawing

Drawings use color tokens (`var(--ink)`, `var(--focus)` …, rules §3). Define them once where the drawing is shown, and pick the first delivery your environment supports:

1. **The environment renders HTML or SVG** (Claude artifacts, ChatGPT canvas, Gemini canvas, any HTML preview): put the answer's drawings into one HTML page. Start it with the token style below, then each `<svg>` in order with the title as `<h2>` above it. Update the same page for follow-up answers instead of opening new ones when the environment allows.
2. **You can create files** (code execution, a sandbox): write the drawings into one `.html` file with the token style below and give it to the user; or render a PNG of it if images show inline there.
3. **Neither**: put the token style as the first child of each `<svg>` (`<style>svg{…}</style>`, the same declarations) and give the SVG in a fenced `svg` code block, one line before it saying it can be saved as `.svg` and opened in a browser.

Token style (light, with dark mode):

```html
<style>
:root{__LIGHT__}
@media (prefers-color-scheme:dark){:root{__DARK__}}
body{margin:0 auto;max-width:820px;padding:24px 16px;background:var(--bg);color:var(--ink);font:15px/1.5 Inter,system-ui,sans-serif}
h2{font-size:17px;margin:28px 0 10px} svg{width:100%;height:auto;display:block}
</style>
```

Below the drawing, the chat gets at most one or two short lines in the user's language: the answer itself, not a description of the drawing.

### B3. PDF on request

When the user asks for a PDF, follow **Runik PDF** (below). If you can run Python with network access, download the renderer and its fonts and run it:

```bash
mkdir -p runik && cd runik && for f in runik_pdf.py inter.woff2 inter-tr.woff2 sg.woff2 sg-tr.woff2; do curl -fsSLO __SITE__/skill/runik/$f || curl -fsSLO __GH__/skill/runik/$f; done
python3 runik_pdf.py doc.json -o answer.pdf
```

If you cannot download it or cannot run code, write the printable page yourself: fill the **PDF page skeleton** at the end of this file (one `<section>` per card, the drawings inside `<figure>`), deliver it as an HTML page or file, and tell the user in one line to open it and use Print › Save as PDF. If your environment has its own way to turn HTML into a PDF file, use it on that page.

### B4. Keep Runik in later conversations

At the end of your first Runik answer, add one line in the user's language: to keep Runik in every conversation, they can paste the same Runik line into the custom instructions, project instructions or memory of this assistant.

### B5. Message to the user (first time only)

One line in the user's language: Runik is on for this conversation, and they can ask for any answer as a PDF. Then answer whatever they asked, the Runik way.

---

