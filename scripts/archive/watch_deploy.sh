#!/bin/bash
# AlgèbreBoost — surveille backend.js et clasp push automatique dès modification
# Usage : ./watch_deploy.sh  (lancer dans un terminal séparé, Ctrl+C pour arrêter)

DIR="$(dirname "$0")"
FILE="$DIR/backend.js"
LAST=""

echo "👀 Surveillance de backend.js... (Ctrl+C pour arrêter)"

while true; do
  CURRENT=$(stat -c %Y "$FILE" 2>/dev/null)
  if [ "$CURRENT" != "$LAST" ] && [ -n "$LAST" ]; then
    echo ""
    echo "🔄 $(date '+%H:%M:%S') — Modification détectée → clasp push"
    cd "$DIR" && clasp push --force && echo "✅ Push OK"
  fi
  LAST="$CURRENT"
  sleep 2
done
