#!/usr/bin/env bash
set -euo pipefail

REPO_URL="git+https://github.com/Adrovel/Spider-Rose.git"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Spider Rose needs Python 3.11+ installed."
  exit 1
fi

if ! python3 - <<'PY' >/dev/null 2>&1
import sys
raise SystemExit(0 if sys.version_info >= (3, 11) else 1)
PY
then
  echo "Spider Rose needs Python 3.11+."
  exit 1
fi

if ! command -v pipx >/dev/null 2>&1; then
  echo "pipx not found. Installing pipx for this user..."
  python3 -m pip install --user pipx
  python3 -m pipx ensurepath || true
fi

PIPX_BIN="$(command -v pipx || true)"
if [ -z "$PIPX_BIN" ]; then
  PIPX_BIN="$HOME/.local/bin/pipx"
fi

"$PIPX_BIN" install --force "$REPO_URL"

echo
echo "Spider Rose installed."
echo "Run it with:"
echo "  spiderrose"
echo
echo "If your shell cannot find spiderrose, restart the terminal or run:"
echo "  python3 -m pipx ensurepath"
