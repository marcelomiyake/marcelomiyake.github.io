#!/usr/bin/env bash
# Run serially so concurrent Chrome instances do not skew performance scores.
set -euo pipefail

base_url="${1:-http://127.0.0.1:4174}"
report_dir="${2:-/tmp/chirpy-lighthouse}"
mkdir -p "$report_dir"

for profile in mobile desktop; do
  args=()
  if [[ "$profile" == desktop ]]; then args+=(--preset=desktop); fi
  for post in _posts/*.markdown; do
    slug="$(basename "$post" .markdown)"
    slug="${slug:11}"
    npx --yes lighthouse@13.5.0 "$base_url/posts/$slug/" \
      --chrome-flags="--headless --no-sandbox" \
      --output=json --output=html \
      --output-path="$report_dir/$profile-$slug" \
      "${args[@]}" --quiet
  done
done

python3 - "$report_dir" <<'PY'
import json
import pathlib
import sys
failed = False
for path in sorted(pathlib.Path(sys.argv[1]).glob('*.report.json')):
    report = json.loads(path.read_text())
    scores = {key: round(value['score'] * 100) for key, value in report['categories'].items()}
    print(path.stem, scores)
    failed |= any(value != 100 for value in scores.values())
sys.exit(1 if failed else 0)
PY
