---
name: runik
description: Runik visual answers. Explanations, comparisons, plans, architecture, processes and results are drawn as rule-based SVG drawings (or charts, tables, cards) on the Runik Board, a live artifact kept open beside the chat, instead of long text. Use before every reply that explains something, compares options, reports results or answers a question a picture could carry. Skip it for one-line confirmations and for replies that are only code, commands or file paths.
---

# Runik

Runik replaces long text with drawings. Answers go to the **Runik Board** (one live artifact shared by all projects) as cards; the chat gets at most one line pointing at the card.

Everything Runik needs ships in this skill's folder (the folder holding this file, normally `~/.claude/skills/runik`):

| File | What |
|---|---|
| `rules.md` | Drawing rules: canvas, type, color, components, patterns. Read before drawing. |
| `runik-lint.js` | Checks drawings before delivery (needs Playwright). |
| `purify.min.js` | DOMPurify, used by the lint exactly as the board uses it. |
| `runik_object.py` | Helpers for shaded, natural-color drawings of real objects (§4b of the rules). |
| `example_object.py`, `example_geo.json` | A full object drawing example and its map data. |
| `board.html` | The Runik Board artifact page. |
| `version.json` | Skill version and board version. |
| `update.sh` | Self-update: checks, compares, installs and reports. Run at the start of every session. |

## Output language

This skill is written in English, but **everything it produces is in the user's language**: card titles, topics, notes, every visible text inside drawings, chart and table labels, card summaries and items, and the one line in the chat. The user's language is the language of their messages (or the language they asked for); if unclear, follow the project's instructions or the language of the conversation so far. Number formats follow the same locale (rules §2). Only technical identifiers (field names like `type` or `data_json`, token names, code, file paths) stay as they are. The examples in this skill are in English only as examples; translate them, never copy them as-is.

## 1. Update and find the board (start of every session)

Run the update script and act only on its output. Don't compare versions, download or install anything yourself; the script does all of that and checks the network at most once a day.

```bash
bash ~/.claude/skills/runik/update.sh
```

(Use this skill's folder if it is installed somewhere else.) Lines starting with `runik:` are status; don't repeat them to the user. Lines starting with `ACTION:` are what you must do, in order. No `ACTION:` line means nothing to do. Typical output:

```
runik: 0.5.2, up to date
runik: board https://claude.ai/...
```

The actions it can ask for:

- **`re-read SKILL.md and rules.md`**: the skill was just updated; read both files again before going on.
- **`republish … board.html to <url>`**: publish `board.html` to that `url` with the Artifact tool, passing no `capabilities` (the existing database is kept), then write the new `board_version` it names into `~/.claude/runik/config.json`.
- **`create the board`** (no board yet): if project memory has a `runik.md` with a board link (ephemeral environments, see below), use that link instead. Otherwise publish `board.html` as a new artifact with the Artifact tool:
  - title: `Runik Board`
  - icon: `board`
  - capabilities: `{"db": {}}`
  - description: `Live side board where Runik answers are drawn.`

  Then write `~/.claude/runik/config.json` (the folder exists):

  ```json
  { "board_url": "<link>", "board_version": <board from version.json>, "created": "<today>" }
  ```

  Tell the user once, in one line and in their language, to keep the board open beside the chat, and offer once to pin it (Artifact `pin` only if they say yes).

The board link for the rest of the session is the one in the `runik: board …` line (or the one you just created).

- **Ephemeral environment** (a cloud session where `~/.claude` does not persist): also keep the board link in project memory as `runik.md` so the next session finds it.
- **No Artifact or ArtifactData tool in this session**: Runik can't draw here. Answer normally, short, and don't mention it again this session.

## 2. Read the rules (once per session)

Read `rules.md` from start to end and apply it to every drawing. The hard rule (§0): text is the last resort.

## 3. Write the answer to the board

Write answers, explanations and results as cards: ArtifactData `set` on the board's `cards` collection.

- doc_id: `k-YYYYMMDD-HHMMSS-short-name`
- `type`: `drawing` (default for explanations) | `chart` | `table` | `card` | `diagram` | `markdown`
- `title`: short, the answer itself
- `topic`: the project or thread name
- `time`: ISO, UTC
- `data_json`: the data as a JSON string
  - drawing: an array of SVG strings following the rules, `["<svg…>", …]`. For a long answer, `set` the first SVG, then add parts with `update`; keep `status: "writing"` until done, then remove it.
  - chart: a Vega-Lite spec
  - table: `{"columns": [], "rows": [[]]}`
  - card: `{"summary": "", "status": "ok|warn|error|info", "items": [], "numbers": {}}`
  - diagram: Mermaid source (only when a hand-drawn SVG would add nothing)
  - markdown: a short note
- `note`: optional

All visible text on the board is in the user's language (see "Output language").

Colors only through board tokens: `var(--ink)`, `var(--muted)`, `var(--edge)`, `var(--line)`, `var(--good)`, `var(--warn)`, `var(--bad)`, `var(--focus)`, `var(--k2)`, `var(--tint)`, `var(--surface)`. A real object's body is the exception: it is drawn in natural colors with shading (rules §4b); meaning colors only go on the marks on top of it.

## 4. Check before delivery

```bash
node <skill folder>/runik-lint.js card.json
```

`card.json` is the card document (with `data_json`) or a plain array of SVG strings. Fix everything it reports. It needs Playwright (local or global, `npm i -g playwright && npx playwright install chromium`); if it is missing, check the drawing by eye and tell the user once that the lint could not run.

## 5. The chat

Write at most one line in the chat, in the user's language: `→ <"on the board" in the user's language>: <title>` (Turkish: `→ panoda: <başlık>`). Things that must be exact (code, commands, links, file paths) stay in the chat. If a decision is needed, ask the question in the chat in one line and show the options on the board.

## Updating

Updates are automatic: `update.sh` (step 1) installs new versions at most a day after they are published. To update right away: `bash ~/.claude/skills/runik/update.sh --force`. The board link in `~/.claude/runik/config.json` is always kept.
