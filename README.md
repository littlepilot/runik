# ᚱ Runik

A visual answer language for Claude Code. Instead of long text, answers are drawn as rule-based visuals on a live board beside the chat.

Runik installs once as a **global Claude Code skill** (`~/.claude/skills/runik`) and works in every project.

- Site: https://runik.littleman.workers.dev
- Install: `bash public/install.sh` from this repo, or `curl -fsSL https://runik.littleman.workers.dev/install.sh | bash`, or paste the prompt from the site into Claude Code.

## Layout

| Path | What |
|---|---|
| `public/` | Static site, deployed as-is to Cloudflare Workers |
| `public/skill/runik/` | The skill, **single source**: `SKILL.md`, `rules.md` (drawing rules), `runik-lint.js`, `runik_object.py`, `board.html`, `version.json` |
| `public/skill/runik/output-style.md` | Optional output style, installed to `~/.claude/output-styles/runik.md` |
| `public/install.sh` | Installer: copies the skill to `~/.claude/skills/runik` |
| `public/install.txt`, `public/install.md` | The prompt users paste and the steps Claude follows |
| `scripts/` | Page generator (drawings + template → index.html) and checks |

## What gets installed

- `~/.claude/skills/runik/`: the skill. Reinstalling overwrites it.
- `~/.claude/output-styles/runik.md`: optional output style (`/output-style`).
- `~/.claude/runik/config.json`: the board link, written by Claude the first time the skill runs. Reinstalling keeps it, so every project draws on the same board.

## Changing the rules

1. Edit `public/skill/runik/rules.md` (or `SKILL.md`).
2. Bump `version` in `public/skill/runik/version.json` and add a line to `notes`. If the board changed, bump `board`.
3. `npm run page && npm run check`
4. `git push` → checks + deploy. Rerun `bash public/install.sh` to update the global skill; the next session republishes the board if `board` went up.

## Local

    npm ci
    npm run dev        # wrangler dev
    npm run deploy     # wrangler deploy (manual)

For automatic deploys add `CLOUDFLARE_API_TOKEN` (Workers Scripts: Edit) and `CLOUDFLARE_ACCOUNT_ID` to the repo secrets; without them CI only runs the checks.
