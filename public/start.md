# Runik: start here

You are reading this because the user pasted the Runik line into a conversation with you. Runik is a visual answer language: instead of long text, answers are drawn as rule-based SVG drawings (and short cards and tables). Read this file to the end once, then do **one** of the two paths below. Don't report progress; one short message at the end is enough.

Everything Runik produces (drawings, cards, titles, the message to the user, PDFs) is in **the user's language**: the language of their messages. This file is in English only so every agent can read it.

Sources (the first one that opens is used):
- SITE = https://runik.littleman.workers.dev
- GITHUB = https://raw.githubusercontent.com/littlepilot/runik/main/public

## Which path?

- **Path A, install**: you can run shell commands on the user's machine and `~/.claude` exists or can be created (Claude Code: CLI, desktop app, IDE, cloud session). Runik becomes a permanent global skill with a live board.
- **Path B, use it now**: everything else (claude.ai or the Claude apps without a shell, ChatGPT, Gemini, Copilot, other chat agents, or Claude Code where installing fails). Runik works for the rest of this conversation from this file alone.

If unsure, try Path A; if its installer cannot run, fall back to Path B.

## Path A: install (Claude Code)

Download the install steps and follow them in order:

```bash
curl -fsSL https://runik.littleman.workers.dev/install.md || curl -fsSL https://raw.githubusercontent.com/littlepilot/runik/main/public/install.md
```

They install the skill to `~/.claude/skills/runik`, create the board and write the first card. After that, ignore the rest of this file: the installed skill carries the same rules.

## Path B: use it now (any chat agent)

From now until the end of this conversation, answer the way the rules below say. You need nothing installed.

### B1. What to draw

Before every reply that explains something, compares options, reports results or answers a question a picture could carry, draw it: follow **Runik drawing rules** (below, §0–§7) for every drawing. Skip drawing for one-line confirmations and for replies that are only code, commands or links. Things that must be exact (code, commands, links) stay as text.

The rules mention helper files "in this folder" (`runik_object.py`, `example_object.py`, `runik-lint.js`). Here they live at `https://runik.littleman.workers.dev/skill/runik/<file>`: use them only if you can run code and download; otherwise apply the same rules by hand. The board (cards, ArtifactData) is a Claude Code feature: in Path B the drawing goes into the conversation as described in B2.

### B2. How to show a drawing

Drawings use color tokens (`var(--ink)`, `var(--focus)` …, rules §3). Define them once where the drawing is shown, and pick the first delivery your environment supports:

1. **The environment renders HTML or SVG** (Claude artifacts, ChatGPT canvas, Gemini canvas, any HTML preview): put the answer's drawings into one HTML page. Start it with the token style below, then each `<svg>` in order with the title as `<h2>` above it. Update the same page for follow-up answers instead of opening new ones when the environment allows.
2. **You can create files** (code execution, a sandbox): write the drawings into one `.html` file with the token style below and give it to the user; or render a PNG of it if images show inline there.
3. **Neither**: put the token style as the first child of each `<svg>` (`<style>svg{…}</style>`, the same declarations) and give the SVG in a fenced `svg` code block, one line before it saying it can be saved as `.svg` and opened in a browser.

Token style (light, with dark mode):

```html
<style>
:root{--ink:#1b1f2a;--muted:#5f6779;--edge:#8a93a5;--line:#dadfe7;--good:#15803d;--warn:#b45309;--bad:#c81e1e;--focus:#2f5bd8;--k2:#3f8f84;--tint:#eef0f4;--surface:#ffffff;--bg:#ffffff}
@media (prefers-color-scheme:dark){:root{--ink:#e8ebf2;--muted:#98a1b3;--edge:#636c80;--line:#2c3240;--good:#4ade80;--warn:#fbbf24;--bad:#f87171;--focus:#7d9cf5;--k2:#7cc6bc;--tint:#1d2230;--surface:#191d26;--bg:#101319}}
body{margin:0 auto;max-width:820px;padding:24px 16px;background:var(--bg);color:var(--ink);font:15px/1.5 Inter,system-ui,sans-serif}
h2{font-size:17px;margin:28px 0 10px} svg{width:100%;height:auto;display:block}
</style>
```

Below the drawing, the chat gets at most one or two short lines in the user's language: the answer itself, not a description of the drawing.

### B3. PDF on request

When the user asks for a PDF, follow **Runik PDF** (below). If you can run Python with network access, download the renderer and its fonts and run it:

```bash
mkdir -p runik && cd runik && for f in runik_pdf.py inter.woff2 inter-tr.woff2 sg.woff2 sg-tr.woff2; do curl -fsSLO https://runik.littleman.workers.dev/skill/runik/$f || curl -fsSLO https://raw.githubusercontent.com/littlepilot/runik/main/public/skill/runik/$f; done
python3 runik_pdf.py doc.json -o answer.pdf
```

If you cannot download it or cannot run code, write the printable page yourself: fill the **PDF page skeleton** at the end of this file (one `<section>` per card, the drawings inside `<figure>`), deliver it as an HTML page or file, and tell the user in one line to open it and use Print › Save as PDF. If your environment has its own way to turn HTML into a PDF file, use it on that page.

### B4. Keep Runik in later conversations

At the end of your first Runik answer, add one line in the user's language: to keep Runik in every conversation, they can paste the same Runik line into the custom instructions, project instructions or memory of this assistant.

### B5. Message to the user (first time only)

One line in the user's language: Runik is on for this conversation, and they can ask for any answer as a PDF. Then answer whatever they asked, the Runik way.

---

# Runik drawing rules

Read by the `runik` skill before drawing. These are rules, not a gallery of examples: every new drawing is built from scratch with the canvas, type, color, component and pattern rules below.

Philosophy: quiet luxury. Whatever can be shown is not told; text appears only where the picture cannot carry it, and stays short (see §0, a hard rule). Every drawing is built as if explaining to someone who knows nothing about the topic.

There are two kinds of drawing. The first job is deciding which one this is:
- **Concept drawing** (definition, process, comparison, measurement, architecture): flat, no shadows, colors carry meaning (§1–§6).
- **Object drawing** (a real, touchable thing: circuit board, mountain, safe, laptop, bone): shaded and in natural colors, using the Visual Explainer technique (§4b). Runik meaning colors never paint the object's body; they stay in the marks placed on top of it.

One drawing may combine both: the object is drawn in natural color, and labels, arrows and status marks are placed on top in the Runik theme.

All visible text (titles, labels, notes, legends, `<title>` and `<desc>`) is in the user's language, never English by default. The English words in this file ("times approximate", "e.g.", WHAT?, ANALOGY, CPU CHIP) are examples of the role; write their equivalent in the user's language.

## 0. Hard rule: text is the last resort

Nothing that can be shown visually (shape, position, color, number, scale, arrow, icon, grouping) is told in text. Question every piece of text: "Can I draw this instead?" If yes, delete the text and draw it. When in doubt, draw it.

Text-to-visual table:

| If the text contains | Use instead |
|---|---|
| number, ratio, size | scale bar, cell row, scaled circle |
| order, stage | left-to-right position + number |
| belonging, scope | scope boundary, grouping |
| comparison, preference | side-by-side bars, rating, good/bad boxes |
| status (good/bad/risky) | status color, check/cross |
| flow, cause and effect | arrow |
| condition, choice | decision diamond |
| "present / absent", "forbidden" | icon + struck-through icon |
| list of names (tools, files) | count + cells or a dot cluster; names only on the 1–2 highlighted items |
| formatting rule (spelling, format) | the example itself, good/bad side by side |

Text budget:
- Title at most 8 words, and it is the answer itself.
- Label at most 3 words. No sentences (except the title).
- A detail line only for a name or value that cannot be drawn, at most 4 words. Not every item gets a detail line.
- Info strip and note: at most one per drawing, at most 8 words.
- Excluding the title, at most ~40 words of prose per drawing. If it goes over, either turn text into visuals or split the drawing in two.
- The budget applies to prose (notes, explanations, label sentences). When the question is about the names themselves (a list of mountains, a list of candidates), name and value labels don't count toward the budget, but still stay on one short line.
- A note states the conclusion ("so what?"), not what a mark is.
- Detail that text would carry (sources, reasoning, long lists) does not go into the drawing; if needed it goes into a separate "details" card.

## 1. Canvas

- Hand-made inline SVG. No Mermaid-looking box-and-arrow diagrams, no colorless multi-level hierarchy trees, no emoji. Concept drawings have no shadows, gradients or 3D; object drawings require them (§4b). Meaningful arrow chains (§5.5) are fine.
- `viewBox="0 0 760 H"`, H fits the content (usually 320–610). `width="100%"`.
- Margin 24: content between x=24 and x=736.
- Column grid:
  - 2 columns: x=24 and x=392, width 344, gap 24.
  - 3 columns: x=24, 268, 512, width 224, gap 20.
  - Full-width box: x=24, width 712.
- Thin full-width divider between sections: `<line x1=24 x2=736 stroke=grid>`.
- Labels are left aligned. Center only a name inside a shape and the value under it.
- Estimate text width while generating: characters × size × 0.56 (weight 400), 0.60 (600), UPPERCASE 0.68. Leave ≥10 padding on each side inside an enclosing shape. If a value at the end of a bar would pass 736, move it inside the bar with `text-anchor="end"`.
- Every label box is ≥4 units from other text and shapes. A label more than 12 units from its mark gets a leader line.
- Font size means the size on screen: panel width × size / 760 ≥ 9 px. For narrow panels (< 600 px), content that can stack vertically is drawn as a single column with `viewBox="0 0 400 H"`.

SVG technical rules (the board sanitizes SVG with DOMPurify's svg profile):
- Root: `role="img"`, `aria-label` = the title sentence. Inside it, `<title>` (the title) and `<desc>` (every value the drawing carries, ≤60 words); `<desc>` does not count toward the visible budget.
- Attributes in kebab-case only: `font-size`, `fill-opacity`, `stroke-width`. JSX spelling (`fontSize`) gets stripped.
- No `<marker>`, `<use>`, `<foreignObject>`, `<animate>`, `on*`, or external `href`. An arrowhead is a triangle drawn by hand at the end of the path.
- Unavoidable ids (clipPath) get a drawing-specific prefix: `k20261111-mountain-clip`. No id repeats on the same page.

## 2. Type

Root `font-size="13"`. Only these sizes:

| Role | Size / weight | Color | Note |
|---|---|---|---|
| Title | 15 / 600 | ink | x=24, y≈30. Always a single sentence stating the main idea. |
| Section question | 14 / 600 | ink | "Why …?", "Three levers". After a divider. |
| Item name | 13 / 600 | ink | The name of every item. |
| Main detail | 11.5 / 400 | ink | 16–20 px below the name. |
| Extra detail, example | 11.5 / 400 | quiet | Bottom line: "e.g. …". |
| Column header | 11.5 / 600 | quiet | UPPERCASE: WHAT?, ANALOGY. |
| Note | 11.5 / 400 | quiet | At the bottom: "times approximate", "square counts illustrative". |

- Parts of a detail line are separated by a middle dot: `inside the core · ~64 KB`, `hit · ~1 ns`.
- Approximate values are written with `~`. If a scale is logarithmic, the title says so.
- No text goes below 10.5 units. A label is at most one short line.
- Numbers use the user's locale, consistently, axis labels included. Turkish: thousands dot, decimal comma (3.000, 5.137, %95,7, r = 0,68). English: 3,000, 95.7%, r = 0.68.

## 3. Color

Colors carry meaning, not decoration. This section covers concept drawings and the marks placed on objects; an object's body is drawn in its natural color (§4b). Every concept drawing uses only these roles:

| Role | For | Runik light | Runik dark | Claude Docs token |
|---|---|---|---|---|
| ink | text, actor frame | #1b1f2a | #e8ebf2 | --cds-text-primary |
| quiet | secondary text, in-between arrows (›) | #5f6779 | #98a1b3 | --cds-text-secondary |
| edge | neutral frame, neutral arrow (≥3:1) | #8a93a5 | #636c80 | --cds-chart-axis |
| grid | decorative divider only | #dadfe7 | #2c3240 | --cds-chart-grid |
| good | fast, correct, hit, solution | #15803d | #4ade80 | --cds-chart-status-good |
| warn | medium, caution, dirty | #b45309 | #fbbf24 | --cds-chart-status-warning |
| bad | slow, error, miss, risk | #c81e1e | #f87171 | --cds-chart-status-critical |
| focus | focus, your action, main item | #2f5bd8 | #7d9cf5 | --cds-chart-categorical-1 |
| tint | neutral info strip background | #eef0f4 | #1d2230 | --cds-chart-reference-tint |

- Colors are written with board tokens and no other `var(--…)`: ink→`--ink`, quiet→`--muted`, edge→`--edge`, grid→`--line`, good→`--good`, warn→`--warn`, bad→`--bad`, focus→`--focus`, second category→`--k2`, tint→`--tint`, background→`--surface`. In Claude Docs the same roles map to the tokens in the right column.
- Status is never given by color alone: every status color comes with a second channel (✓ / ! / ✗, full / half / empty, or a one-word label). Green and red blur together for color-blind readers.
- A status color is used only when the drawing states a threshold or a judgment; otherwise the value stays neutral (focus or ink). If the title says "misleading", that value cannot be green.
- The same entity keeps the same color within a drawing and across all drawings of one answer.
- A fill always comes with its own stroke: `fill-opacity 0.12` on a large box, `0.18–0.35` on a small cell, stroke in the same color at `1.5–2.5`.
- Text inside a colored fill or tint is ink; quiet only on the plain background. In dark theme, never put text on a fill denser than 0.3.
- Status colors are ordered: good → warn → bad. All three can appear on one scale (L1/L2 good, L3/RAM warn, SSD bad).
- To separate categories (two cores), use focus and the second categorical color; status colors are never used for categories.

## 4. Components

Every drawing is built from these parts. The measurements are fixed.

- **Neutral item**: `rect rx=6–8, fill=none, stroke=edge, 1.25–1.5`. Most things are this.
- **Actor**: what starts the story (CPU, "your code"). `stroke=ink, 2`, no fill.
- **Highlighted item**: status or focus color, translucent fill + stroke in the same color.
- **Card**: `rx=8, stroke=edge 1.25`. Content starts at x+16: name (y+24), main detail, extra detail. If a category/status is needed, a 6 px colored band on the top edge.
- **Result / solution box**: full width, `rx=8`, color at `0.12` fill + 2 px stroke. One bold sentence + one detail line. At the end of the drawing.
- **Good / bad rule boxes**: two columns, good on the left, bad on the right, same structure.
- **Info strip**: full width, `fill=tint, stroke=edge`. For a rule or an exception.
- **Cell row**: 20–26 px squares showing data units, `rx=3–4`, 4–6 px gaps. Filled = colored fill, empty = edge stroke.
- **Coverage bracket**: above a group of cells, `M x1 y-6 V y-12 H x2 V y-6`, color = meaning.
- **Status dot**: `r=6` circle, status color, at the left of the row.
- **Scale bar**: `height=14, rx=3`, length proportional to the value and always starting at 0. To show a narrow range, use dots on a shared axis instead of bars. Before/after or A/B bars start one under the other from the same x base; place them end to end only if the total matters.
- **Scaled circle**: on one axis, distance = cost; the circle's area is proportional to capacity (radius ∝ √value, zero-based).
- **Rating**: 5 small circles `r=5`, number filled = value.
- **Decision**: diamond, `stroke=ink 1.5`, an 11.5/600 question inside; the result in a short box below.
- **Arrows**: small filled triangle head (6×6). Neutral flow `edge 1.5`. Meaningful flow 2–3 px, its color carries the meaning. Dashed = indirect, later, copy. Panel transition: a thin `›` (quiet, 2 px).
- **Scope boundary**: a dashed outer frame showing containment (`6 4`, edge) with a small UPPERCASE label at top left (CPU CHIP).
- **Mini concept icon**: 24–32 px, thin ink line, geometric (document, magnifier, eye, path, lock, clock, check/cross). Never emoji. If it can carry a concept without a label, no label; if labeled, one word.
- **Object icon (map, location)**: a mark representing a real object (mountain, building, ship) cannot be abstract geometry (a triangle or circle is not enough). Draw the object's recognizable silhouette with the §4b technique, in natural color: for a mountain, `N.peak()` (jagged ridge, secondary summit, shaded face, snow). If size carries a value, the silhouette's area is proportional to it (height ∝ √value, zero-based). If the largest value is less than twice the smallest, use 3 classes instead of size and write the class thresholds in the legend. Overlapping icons are nudged apart and connected with leader lines.
- **Legend**: inline, at the bottom: 16×16 swatch + text. No separate box.

## 4b. Object drawing (Visual Explainer technique)

A real object is not drawn with boxes and bars or flat colored shapes; it is drawn as a recognizable, shaded picture. Helpers live in this folder: `runik_object.py` (adapted from Visual Explainer's `vxart.py` technique, with drawing-specific id prefixes).

```python
from runik_object import Obj, pol, blob, smooth, rrect, capsule
N = Obj("k20261118-board")                  # prefix: unique to this drawing
N.add(N.slab(50, 90, 900, 700, N.PCB, r=18, depth=14))
N.add(N.grain(rrect(50, 90, 900, 700, 18), 0.35))
N.mark("cpu", 270, 222)                     # point to label later
svg_defs, g = N.defs(), N.group(24, 52, 0.42)   # place on the Runik 760 canvas
x, y = N.at("cpu")                          # labels and leader lines start here
```

Full example: `example_object.py` (a motherboard with Runik labels, and a map with real mountain silhouettes).

Building blocks: `slab` (board, chip, case, plate), `layers` (layered cross-section), `ball` (round body), `tube` (pipe, cable, vessel), `peak` (mountain), `laptop`, `chip`, `shadow`, `grain`; shapes: `blob` + `smooth` (organic), `rrect`, `capsule`; fills: `N.linear`, `N.radial`, `N.clip`.

Rules:
- **Natural color**: circuit boards green, metal gray, mountains brown with white snow, paper cream. Ready palettes: `N.PCB, METAL, DARK, PAPER, ROCK, STONE, GOLD, WOOD, GLASS, SKIN, LEAF, WATER, SAND`. Each palette is (light, mid, dark).
- **Runik colors stay off the body**: `var(--good/--warn/--bad/--focus)` never paints the object. Meaning comes from marks placed on it: leader line + label, a status word (✓ fast), a highlight ring, an arrow.
- **Light from the top left**: every body has a light top and a dark side; everything touching the ground gets a soft shadow (`shadow`; `slab` and `ball` add their own).
- **Stroke is the dark shade of the fill**, never black. Living things get irregular outlines (`smooth(blob(...))`), made things get straight edges, rounded corners and visible thickness.
- **Depth**: draw back to front, let parts overlap slightly, clip contents to the body (`N.clip`).
- **Texture**: `grain` on large flat fills; repeated small parts (chips, pins, screws) in a loop.
- **Proportions and counts match reality**: a wrong drawing teaches the wrong thing. If simplified, say so in the note ("simplified drawing").
- **No text inside the object**. Names go beside it as Runik labels (13/600 name, 11.5 detail); leader lines never cross the object; if needed, go out perpendicular first, then horizontal. No numbered pins with a separate legend.
- **The base stays quiet**: map base, borders and background in Runik tint/line tones; natural color only on the object itself.
- Readable in dark theme too: the object keeps its own color, labels use token colors.

## 5. Patterns

Pick one for the topic; combine two vertically if needed (with a divider + section question between them):

1. **Distance axis**: one horizontal line, actor on the left, items moving away by cost, size shows capacity. Note below: "distance = …, circle = …".
2. **Row table**: columns WHAT? · ANALOGY · SCALE. Each row: status dot, name + detail, everyday analogy, scale bar.
3. **Physical map**: the thing's real layout (chip, building, body). Dashed scope boundary, shared part highlighted, outside parts neutral.
4. **Comparison columns**: 2–3 matching cards, a rating matrix below, a "why none gives you everything" note at the bottom and a result box.
5. **Chain / lookup**: actor → decision diamonds → result; failed branches with a short colored word (miss), the return path as a dashed arrow.
6. **Scenario rows**: the same actor sequence repeats on every row; the only thing that changes is the arrow pattern and color. Each row starts with a name + "common/rare".
7. **Process panels**: 2–3 numbered panels (`1 · CPU asks for one number`), `›` between them, each panel showing a changed state of the same cell row.
8. **Who decides + levers**: actor → system strip at the top, a rule strip in the middle, 3 lever cards (colored top band) at the bottom.

Every drawing flows: title sentence → main visual → (divider → section question → explaining part) → result box or note.

## 5b. Maps

- The base is generated from real data (Natural Earth or other open vectors), never drawn by hand. Use a conformal projection (Lambert conformal conic for Turkey); never plain lat-long. The source goes in the note.
- Base geography (borders, coast, lakes) is gray and quiet; it needs no legend. The country gets a tint fill, neighbors only a thin grid stroke.
- The map reads on its own: the 3–5 most important items are labeled directly by name, the rest are unlabeled marks. No references by number to other drawings.
- Try label positions in order: top right, top left, bottom right, bottom left; never on top of a mark, another label or water.
- A regional claim in the title is encoded on the map with a count or a region (e.g. an "east 14 · west 6" cell row).

## 6. Information density

- The visual is not sparse: what each part is, what it does and what it depends on is readable on it.
- Anything abstract gets an everyday analogy beside it (sticky note, desk, shelf, warehouse, archive).
- One drawing carries one idea. More goes into a second drawing.
- Real-world objects (body, machine, mountain) are drawn with §4b in natural color; bases like maps and screenshots come from real data and are toned down. Marks on top use this theme.

## 6b. Readability: one meaning per mark

The places where readers who didn't know the topic got confused were always the marks, never the idea. So:

- Every mark in a drawing (color, dot, dashed line, ✓/✗, fill) is defined in a legend inside the drawing. No undefined marks.
- One mark carries one meaning. If ✗ would mean "makes things up", "skips" and "missing", write a one-word red label instead of ✗.
- A dashed line has one meaning per drawing (e.g. "no data"). Groups are separated with a thin solid gray frame.
- An axis states its metric and unit, and its direction ("higher = better"). If the axis doesn't start at 0, it says so.
- Different units are never drawn on the same scale (e.g. a speed factor and a quality score get separate bar pairs).
- Status colors (green/orange/red) only describe status. Neutral emphasis (a difference bracket, a dimension line) is ink.
- Dots and bars are never unlabeled. If crowded, name the 2–3 important ones with leader lines.
- Abbreviations are either spelled out or not used.
- Missing data gets its own mark (an empty dashed cell or "—"), is never merged into a value category, and has its own legend row.
- All drawings in an answer share one legend vocabulary: whatever meaning a mark took in the first drawing, it keeps for the whole series.
- One item carries at most two visual channels (e.g. fill + stroke). The status the reader is expected to look for is given with a thick stroke (≥2.5) or an icon.
- The title's claim is encoded in the main visual with a pre-attentive channel (focus color, region, count). Only the item carrying the claim gets the focus color.
- Quantitative items are sorted by descending value; matrix rows by coverage score. Alphabetical order only when an item will be looked up.
- Different quantities (percentage vs. correlation) are never drawn on the same bar scale; correlations and interval estimates are shown as a dot + error bar.

## 7. Before delivery

1. Count words: prose over ~40 words, excluding the title, is not delivered (§0). Question every text once more: "can this be drawn?"
2. Automatic check: `node runik-lint.js card.json` (in this folder). Fix undefined tokens, camelCase attributes, elements DOMPurify strips, repeated ids, text running off the edge or overlapping, and missing role/aria-label.
3. Take a screenshot and look: text and marks don't collide or get cut off; arrows point at the right item.
4. Only the type sizes and color roles in the tables are used. In object drawings the body is natural color, meaning colors only on marks; ids carry a drawing-specific prefix.
5. 3-second test: the title and main visual give the idea before any label is read.
6. Readable in light and dark theme (colors are tokens).

A naive-eye test (having an agent who doesn't know the topic read the screenshots back and answer questions) is not a delivery step; do it only if the user asks, because it slows things down. The script in step 2 is enough for a quick check.

---

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
python3 runik_pdf.py doc.json -o <name>.pdf
```

The script needs only Python 3 and one of Chrome/Chromium (a Playwright Chromium is found too), the Playwright Python package, or WeasyPrint. `python3 runik_pdf.py doctor` shows what the machine has. If none is found it writes `<name>.html` instead and exits with code 3: that page prints to the same document from any browser (Print › Save as PDF); give it to the user with that one instruction.

Name the file after the title in the user's language, short, lowercase, with hyphens (`veri-yakinligi.pdf`).

## 3. Check and deliver

Open the PDF (or look at its pages) before delivering: no drawing is cut between pages, nothing overlaps, page numbers are there. Then deliver the file the way the environment allows (attach it, save it next to the user's work, or give its path) with one line in the user's language.

---

# PDF page skeleton

Used only when the renderer cannot run (Path B3). Replace the UPPERCASE placeholders; repeat `<section>` per card; tables, cards and notes use the classes in the style (`table`, `.kcard`, `.summary`, `.badge`, `.numbers`, `.items`, `.md`, `.note`).

```html
<!doctype html>
<html lang="LANG">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; font-src data:; img-src data:">
<title>TITLE</title>
<style>


:root{--ink:#1b1f2a;--muted:#5f6779;--edge:#8a93a5;--line:#dadfe7;--good:#15803d;--warn:#b45309;--bad:#c81e1e;--focus:#2f5bd8;--k2:#3f8f84;--tint:#eef0f4;--surface:#ffffff;--bg:#ffffff;color-scheme:light}
@media screen and (prefers-color-scheme:dark){:root{--ink:#e8ebf2;--muted:#98a1b3;--edge:#636c80;--line:#2c3240;--good:#4ade80;--warn:#fbbf24;--bad:#f87171;--focus:#7d9cf5;--k2:#7cc6bc;--tint:#1d2230;--surface:#191d26;--bg:#101319;color-scheme:dark}}
@page{size:A4;margin:16mm 16mm 18mm 16mm;
  @bottom-left{content:"ᚱ Runik · TITLE";font:500 7.5pt "Space Grotesk",system-ui,sans-serif;color:#5f6779}
  @bottom-right{content:"Page " counter(page) " / " counter(pages);font:7.5pt Inter,system-ui,sans-serif;color:#5f6779}}
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
figure svg{width:100%;height:auto;display:block}
figure svg text{font-family:Inter,system-ui,sans-serif;font-variant-ligatures:none;font-feature-settings:"calt" 0}
.note{color:var(--muted);font-size:9pt;margin:6px 0 0}
table{border-collapse:collapse;width:100%;font-size:9.5pt;font-variant-numeric:tabular-nums;break-inside:auto}
tr{break-inside:avoid}
th{text-align:left;font-weight:600;color:var(--muted);font-size:8pt;letter-spacing:.05em;text-transform:uppercase;border-bottom:2px solid var(--line);padding:6px 8px}
td{border-bottom:1px solid var(--line);padding:6px 8px;vertical-align:top}
.num{text-align:right}
.kcard{display:grid;gap:12px;break-inside:avoid}
.summary{font-size:13pt;font-weight:600;display:flex;gap:10px;align-items:center}
.badge{flex:none;width:28px;height:28px;border-radius:50%;display:grid;place-items:center;font-size:12pt;border:1.5px solid var(--focus);color:var(--focus)}
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
</style>
</head>
<body>
<header>
<div class="brand">
<b>ᚱ</b> Runik</div>
<h1>TITLE</h1>
<p class="sub">SUBTITLE</p>
<div class="date">DATE</div>
</header>
<section class="c-drawing">
<h2>SECTION TITLE</h2>
<figure>
<svg viewBox="0 0 760 100" width="100%">…</svg>
</figure>
<p class="note">NOTE</p>
</section>
</body>
</html>
```
