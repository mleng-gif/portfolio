#!/usr/bin/env bash
set -euo pipefail

DEPLOY=false

usage() {
  echo "Usage: $0 <path-to-latest-html> [--deploy]"
}

if [[ $# -lt 1 ]]; then
  usage
  exit 1
fi

SOURCE_FILE="$1"

if [[ "${2:-}" == "--deploy" ]]; then
  DEPLOY=true
fi

if [[ ! -f "$SOURCE_FILE" ]]; then
  echo "Error: file not found: $SOURCE_FILE"
  exit 1
fi

if [[ "${SOURCE_FILE##*.}" != "html" ]]; then
  echo "Warning: source file does not end with .html"
fi

mkdir -p versions
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

if [[ -f "index.html" ]]; then
  cp "index.html" "versions/index-${TIMESTAMP}.html"
  echo "Backed up current index.html -> versions/index-${TIMESTAMP}.html"
fi

cp "$SOURCE_FILE" "index.html"
echo "Updated index.html from: $SOURCE_FILE"

echo "Done. Validate locally with: python3 -m http.server 8080"

if [[ "$DEPLOY" == "true" ]]; then
  if ! command -v vercel >/dev/null 2>&1; then
    echo "Error: vercel CLI not found. Install with: npm i -g vercel"
    exit 1
  fi

  echo "Deploying to Vercel production..."
  vercel --prod
fi
