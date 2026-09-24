#!/usr/bin/env bash
# Matheux — lanceur local (backend en mémoire, rien ne part en prod)
#   ./matheux.sh          lance le serveur http://localhost:8787 et ouvre le navigateur
#   ./matheux.sh reset    remet la base de dev à l'état initial (comptes de test, référentiel)
#   ./matheux.sh test     lance les tests (smoke test API + test navigateur)
set -euo pipefail
DIR="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
cd "$DIR"
DENO="${DENO:-$(command -v deno || echo "$HOME/.deno/bin/deno")}"
PORT="${DEV_PORT:-8787}"
URL="http://localhost:$PORT"
[ -x "$DENO" ] || { echo "Deno introuvable (attendu : $HOME/.deno/bin/deno). Installer : curl -fsSL https://deno.land/install.sh | sh"; exit 1; }
FLAGS=(--allow-net --allow-read --allow-write --allow-env --allow-run=python3,google-chrome,/usr/bin/google-chrome --allow-sys --no-prompt)

en_route() { curl -fs -o /dev/null "$URL/dev/health" 2>/dev/null; }

case "${1:-}" in
  reset)
    if en_route; then
      curl -fs -X POST "$URL/dev/reset" && echo && echo "Base réinitialisée (serveur en cours)."
    else
      "$DENO" run "${FLAGS[@]}" dev/server.ts reset
    fi ;;
  test)
    "$DENO" run -A dev/smoke_test.ts
    "$DENO" run -A dev/browser_test.ts ;;
  ""|serve)
    if en_route; then echo "Déjà lancé sur $URL"; xdg-open "$URL" >/dev/null 2>&1 || true; exit 0; fi
    ( for i in $(seq 1 60); do en_route && { xdg-open "$URL" >/dev/null 2>&1 || true; break; }; sleep 0.5; done ) &
    exec "$DENO" run "${FLAGS[@]}" dev/server.ts serve --port "$PORT" ;;
  *) echo "Usage : $0 [reset|test]"; exit 1 ;;
esac
