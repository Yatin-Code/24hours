#!/usr/bin/env bash
# One-line-ish installer: copies hours.py into ~/.local/bin/hours
set -euo pipefail
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/hours/hours.py"
DEST="${HOME}/.local/bin/hours"
mkdir -p "$(dirname "$DEST")"
cp "$SRC" "$DEST"
chmod +x "$DEST"
echo "installed: $DEST"
echo "try: hours +25m --focus 'the thing'"
