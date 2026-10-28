#!/usr/bin/env bash
set -euo pipefail
NOM=selixy-watch-banc-bdd
PORT=${BANC_BDD_PORT:-55432}

case "${1:-}" in
  demarrer)
    podman rm -f "$NOM" >/dev/null 2>&1 || true
    podman run -d --name "$NOM" -e POSTGRES_PASSWORD=banc -e POSTGRES_DB=banc -p "127.0.0.1:$PORT:5432" docker.io/library/postgres:17-alpine >/dev/null
    until podman exec "$NOM" pg_isready -U postgres -d banc >/dev/null 2>&1; do sleep 1; done
    echo "postgresql://postgres:banc@127.0.0.1:$PORT/banc"
    ;;
  arreter)
    podman rm -f "$NOM" >/dev/null
    ;;
  *)
    echo "usage : $0 demarrer|arreter" >&2
    exit 2
    ;;
esac
