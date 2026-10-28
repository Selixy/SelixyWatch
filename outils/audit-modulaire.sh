#!/usr/bin/env bash
set -euo pipefail
ICI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHONDONTWRITEBYTECODE=1 exec python3 "$ICI/audit/audit.py" "$@"
