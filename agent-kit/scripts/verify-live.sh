#!/usr/bin/env bash
# Live MCP smoke — 실제 stdio MCP 왕복 검증. 토큰 없으면 partial(정상).
# v3: 작성자 PC 경로 하드코딩 제거(키트 자체 mcp 기본) + 깨진 "5/5 통과" grep 대신
#     smoke_test.py 의 종료코드로 판정(자기증명 문자열 의존 제거).
set -euo pipefail
MCP_DIR="${MCP_DIR:-$(cd "$(dirname "$0")/../../mcp" && pwd)}"
echo "=== verify-live: $MCP_DIR ==="
cd "$MCP_DIR"
if python smoke_test.py; then
  echo "PASS: smoke (exit 0 — OK/partial 정상)"
  exit 0
fi
echo "FAIL: smoke 비정상 종료 — SFTP rate-limit면 35s 후 재시도, 또는 OAuth/SFTP 설정 확인"
exit 1
