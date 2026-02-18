#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <path-to-latest-html>"
  exit 1
fi

SOURCE_FILE="$1"

if [[ ! -f "$SOURCE_FILE" ]]; then
  echo "Error: file not found: $SOURCE_FILE"
  exit 1
fi

if [[ "${SOURCE_FILE##*.}" != "html" ]]; then
  echo "Warning: source file does not end with .html"
fi

TIMESTAMP=$(date +%Y%m%d-%H%M%S)

if [[ -f "index.html" ]]; then
  cp "index.html" "versions/index-${TIMESTAMP}.html"
  echo "Backed up current index.html -> versions/index-${TIMESTAMP}.html"
fi

cp "$SOURCE_FILE" "index.html"
echo "Updated index.html from: $SOURCE_FILE"

echo "Done. Validate locally with: python3 -m http.server 8080"
