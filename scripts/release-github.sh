#!/usr/bin/env bash
# Build dist zip, tag, and GitHub Release (run from repo root)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

VER="$(head -1 VERSION | tr -d '\r')"
TAG="$VER"
ZIP="dist/cafe24-agent-kit-${TAG}.zip"

echo "== build $TAG =="
bash scripts/build-dist-kit.sh
(cd dist && rm -f "$ZIP" && powershell.exe -NoProfile -Command "Compress-Archive -Path 'cafe24-agent-kit' -DestinationPath '$(basename "$ZIP")' -Force" 2>/dev/null || \
  (cd cafe24-agent-kit && zip -r "../$(basename "$ZIP")" .))

echo "== tag $TAG =="
git tag -a "$TAG" -m "Cafe24 Agent Kit $TAG" 2>/dev/null || echo "tag exists, skipping"
git push origin main
git push origin "$TAG" 2>/dev/null || git push origin "$TAG" --force

echo "== release $TAG =="
gh release create "$TAG" "$ZIP" \
  --title "Cafe24 Agent Kit $TAG" \
  --notes-file CHANGELOG.md

echo "Done: https://github.com/nookitokki-cmyk/cafe24-agent-kit/releases/tag/$TAG"
