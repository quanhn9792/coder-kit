#!/usr/bin/env bash
# Đóng gói mỗi skill thành một file zip để upload lên claude.ai / Desktop (Settings > Capabilities > Skills).
# Kết quả: dist/<skill>.zip, bên trong có thư mục <skill>/SKILL.md ở gốc.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/dist"
rm -rf "$OUT" && mkdir -p "$OUT"
for dir in "$ROOT"/plugins/*/skills/*/; do
  name="$(basename "$dir")"
  [ -f "$dir/SKILL.md" ] || { echo "skip $name (no SKILL.md)"; continue; }
  (cd "$(dirname "$dir")" && zip -qr "$OUT/$name.zip" "$name" -x '*.DS_Store')
  echo "built dist/$name.zip"
done
