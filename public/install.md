# Installing Runik

You are reading this because the user pasted the Runik install prompt into Claude Code. Runik draws answers as rule-based visuals on a board beside the chat instead of long text. It installs once, globally, as the `runik` skill in `~/.claude/skills/runik`, and works in every project. Follow the steps in order. Don't report progress; one message at the end is enough.

Sources (the first one that opens is used):
- SITE = https://runik.littleman.workers.dev
- GITHUB = https://raw.githubusercontent.com/littlepilot/runik/main/public

## 1. Run the installer

```bash
curl -fsSL https://runik.littleman.workers.dev/install.sh -o /tmp/runik-install.sh \
  || curl -fsSL https://raw.githubusercontent.com/littlepilot/runik/main/public/install.sh -o /tmp/runik-install.sh
bash /tmp/runik-install.sh
```

The installer copies the skill to `~/.claude/skills/runik` (it tries a local checkout, the GitHub CLI, GitHub and the site, in that order) and the output style to `~/.claude/output-styles/runik.md`. If no source opens, stop and tell the user in one line that the environment's network settings must allow these domains.

If this is an ephemeral cloud environment where `~/.claude` does not persist, the skill only lasts for this session; tell the user so in the final message.

## 2. Create the board

Read `~/.claude/skills/runik/SKILL.md` and follow step 1: run `bash ~/.claude/skills/runik/update.sh` and do what its `ACTION:` lines say. On a fresh install it asks you to create the board; if a board already exists, it is kept.

## 3. Write the first card

ArtifactData `set` on the board's `cards` collection. doc_id: `k-<YYYYMMDD-HHMMSS>-installed`. Write the visible texts (title, topic, summary, items, number labels) in the user's language; the English below is only the meaning. Fields:
- type: `card`
- title: `Runik installed`
- topic: `Install`
- time: now, ISO, UTC
- data_json: `{"summary":"Runik installed","status":"ok","items":["Keep the board open beside the chat","Works in every project"],"numbers":{"version":"<version from version.json>"}}`

## 4. One message to the user

In the user's language, at most four lines:
- The board link and a suggestion to keep it open beside the chat.
- Runik now works in every project; new sessions pick up the `runik` skill automatically.
- Any answer can be asked for as a PDF ("give me this as a PDF").
- Optional: the `Runik` output style can be turned on with `/output-style` to keep chat replies short.

Offer once to pin the board; if the user says yes, pin it with Artifact `pin`.
