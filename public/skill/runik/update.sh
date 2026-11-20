#!/usr/bin/env bash
# Runik self-update. Claude runs this at the start of every session and only reads its output.
# It checks at most once a day, compares the installed version with the published one, reinstalls
# when a newer version exists, and tells Claude whether the board needs republishing.
#
#   bash ~/.claude/skills/runik/update.sh           # normal run (once a day)
#   bash ~/.claude/skills/runik/update.sh --force   # check now
#
# Output: "runik: ..." lines are status; "ACTION: ..." lines are what Claude must do. No ACTION = nothing to do.
# Always exits 0 so a failed check never blocks the session.
set -uo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
STATE_DIR="$CLAUDE_DIR/runik"
STAMP="$STATE_DIR/last-check"
CONFIG="$STATE_DIR/config.json"
SOURCES="${RUNIK_SOURCES:-https://raw.githubusercontent.com/littlepilot/runik/main/public https://runik.littleman.workers.dev}"
FORCE=0; [ "${1:-}" = "--force" ] && FORCE=1

json_get() {  # $1 = key, $2 = file; first match of "key": "value" or "key": number
  [ -f "$2" ] || return 0
  sed -n "s/.*\"$1\": *\"\{0,1\}\([^\",}]*\)\"\{0,1\}.*/\1/p" "$2" | head -1
}
newer() {  # true when version $1 > $2
  awk -v a="$1" -v b="$2" 'BEGIN { n = split(a, x, "."); split(b, y, ".");
    for (i = 1; i <= n || i <= 3; i++) { if (x[i] + 0 > y[i] + 0) exit 0; if (x[i] + 0 < y[i] + 0) exit 1 } exit 1 }'
}

mkdir -p "$STATE_DIR"
local_version="$(json_get version "$SKILL_DIR/version.json")"
today="$(date +%Y-%m-%d)"

if [ "$FORCE" = 0 ] && [ "$(cat "$STAMP" 2> /dev/null)" = "$today" ]; then
  echo "runik: $local_version, already checked today"
else
  remote="" ; src=""
  for base in $SOURCES; do
    if remote="$(curl -fsSL --max-time 8 "$base/skill/runik/version.json" 2> /dev/null)" && [ -n "$remote" ]; then src="$base"; break; fi
  done
  if [ -z "$src" ]; then
    echo "runik: $local_version, update check failed (no network); using the installed version"
  else
    echo "$today" > "$STAMP"
    remote_version="$(printf '%s' "$remote" | sed -n 's/.*"version": *"\([^"]*\)".*/\1/p' | head -1)"
    if [ -n "$remote_version" ] && newer "$remote_version" "$local_version"; then
      if curl -fsSL --max-time 20 "$src/install.sh" 2> /dev/null | bash > "$STATE_DIR/update.log" 2>&1; then
        installed="$(json_get version "$SKILL_DIR/version.json")"   # may be newer than a cached remote file
        echo "runik: updated $local_version → ${installed:-$remote_version}"
        echo "ACTION: re-read SKILL.md and rules.md before drawing (they changed)"
      else
        echo "runik: $local_version, update to $remote_version failed (see $STATE_DIR/update.log); using the installed version"
      fi
    else
      echo "runik: $local_version, up to date"
    fi
  fi
fi

# Board: compare the installed board version with the one the user's board was published with.
board_installed="$(json_get board "$SKILL_DIR/version.json")"
board_url="$(json_get board_url "$CONFIG")"
board_published="$(json_get board_version "$CONFIG")"
if [ -z "$board_url" ]; then
  echo "ACTION: create the board (see SKILL.md step 1)"
elif [ "${board_published:-0}" -lt "${board_installed:-0}" ] 2> /dev/null; then
  echo "runik: board $board_url"
  echo "ACTION: republish $SKILL_DIR/board.html to $board_url (no capabilities), then set board_version to $board_installed in $CONFIG"
else
  echo "runik: board $board_url"
fi
exit 0
