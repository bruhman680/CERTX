#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
py=/workspace/cache_backend_venv/bin/python
cycle="$1"
"$py" freeze.py "$cycle"
mapfile -t cases < <("$py" -c 'import json,sys; print(*json.load(open(sys.argv[1]))["cases"],sep="\n")' "$cycle/CASES.json")
for case in "${cases[@]}"; do
    "$py" run_cycle.py advance "$cycle" "$case"
done
"$py" score.py "$cycle"
for case in "${cases[@]}"; do
    "$py" run_cycle.py audit "$cycle" "$case"
done
