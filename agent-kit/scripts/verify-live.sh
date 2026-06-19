#!/usr/bin/env bash
# Live MCP smoke (토큰·config 필요). OneDrive 운영 mcp 권장.
set -euo pipefail
MCP_DIR="${MCP_DIR:-$HOME/OneDrive/문서/개발/web/cafe24/mcp}"
echo "=== verify-live: $MCP_DIR ==="
cd "$MCP_DIR"
OUT=$(python smoke_test.py 2>&1) || true
echo "$OUT" | tail -15
echo "$OUT" | grep -q "5/5 통과" && echo "PASS: smoke 5/5" && exit 0
echo "FAIL: smoke not 5/5 (SFTP rate-limit면 35s 후 재시도)"
exit 1
