#!/bin/bash
# Double-click in Finder. This opens saved results without running analysis.
set -e
COMET_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$COMET_ROOT"

if [[ -x "$COMET_ROOT/.venv/bin/python" ]]; then
    COMET_PYTHON="$COMET_ROOT/.venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
    COMET_PYTHON="$(command -v python3)"
else
    if [[ -f "$COMET_ROOT/outputs/app/index.html" ]]; then
        echo "Python is unavailable; opening the saved app directly."
        exec open "$COMET_ROOT/outputs/app/index.html"
    fi
    echo "The saved app is missing. See README.md for the complete Explorer download."
    exit 1
fi

exec "$COMET_PYTHON" "$COMET_ROOT/scripts/serve_app.py" "$@"
