#!/usr/bin/env bash
# Installs Runik as a global Claude Code skill (~/.claude/skills/runik) and its output style
# (~/.claude/output-styles/runik.md). Safe to rerun: it updates the skill and keeps the board link
# in ~/.claude/runik/config.json.
#
#   bash public/install.sh                                          # from a checkout of the repo
#   curl -fsSL https://runik.littleman.workers.dev/install.sh | bash   # from anywhere
set -euo pipefail

CLAUDE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
SKILL_DIR="$CLAUDE_DIR/skills/runik"
FILES="SKILL.md rules.md board.html version.json runik-lint.js purify.min.js runik_object.py example_object.py example_geo.json output-style.md"
REPO="littlepilot/runik"
SOURCES="https://raw.githubusercontent.com/$REPO/main/public https://runik.littleman.workers.dev"

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

# 1. Local checkout (this script sits in public/ next to skill/runik/)
here=""
if [ -n "${BASH_SOURCE[0]:-}" ] && [ -f "${BASH_SOURCE[0]}" ]; then
  here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fi

fetch_all() {  # $1 = command that writes file $2 to stdout
  for f in $FILES; do "$1" "$f" > "$tmp/$f" || return 1; done
}
from_local() { cat "$here/skill/runik/$1"; }
from_gh() { gh api -H "Accept: application/vnd.github.raw" "repos/$REPO/contents/public/skill/runik/$1"; }
from_url() { curl -fsSL "$base/skill/runik/$1"; }

source=""
if [ -n "$here" ] && [ -f "$here/skill/runik/SKILL.md" ] && fetch_all from_local; then
  source="$here"
elif command -v gh > /dev/null && gh auth status > /dev/null 2>&1 && fetch_all from_gh; then
  source="github.com/$REPO (gh)"
else
  for base in $SOURCES; do
    if fetch_all from_url; then source="$base"; break; fi
  done
fi
[ -n "$source" ] || { echo "runik: could not download the skill from any source" >&2; exit 1; }

mkdir -p "$SKILL_DIR" "$CLAUDE_DIR/output-styles" "$CLAUDE_DIR/runik"
for f in $FILES; do cp "$tmp/$f" "$SKILL_DIR/$f"; done
mv "$SKILL_DIR/output-style.md" "$CLAUDE_DIR/output-styles/runik.md"

version="$(sed -n 's/.*"version": *"\([^"]*\)".*/\1/p' "$SKILL_DIR/version.json" | head -1)"
echo "runik $version installed: $SKILL_DIR (source: $source)"
echo "output style: $CLAUDE_DIR/output-styles/runik.md (optional, pick it with /output-style)"
if [ -f "$CLAUDE_DIR/runik/config.json" ]; then
  echo "board: kept ($CLAUDE_DIR/runik/config.json)"
else
  echo "board: created by Claude the first time the skill runs"
fi
node -e "require('playwright')" 2> /dev/null || [ -d "$(npm root -g 2> /dev/null)/playwright" ] \
  || echo "note: runik-lint needs Playwright: npm i -g playwright && npx playwright install chromium"
