#!/usr/bin/env bash
# agent-kit 구조·링크·원본 무결성 검증
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
AK="$ROOT"
WS="$(cd "$ROOT/.." && pwd)"
ORIG="${ORIG:-$HOME/OneDrive/문서/개발/web/cafe24/agent-kit}"
FAIL=0
pass() { echo "PASS: $1"; }
fail() { echo "FAIL: $1"; FAIL=$((FAIL+1)); }

echo "=== verify-kit ($AK) ==="

# getting-started 00-05
for n in 00-아무것도-모를-때 01-5분-컷 02-몰ID-찾기 03-접속-웹FTP-vs-SFTP 04-자주-막히는-5가지 05-MCP-연결-개요; do
  f="$AK/getting-started/${n}.md"
  if [[ -f "$f" ]]; then pass "getting-started/${n}.md"; else fail "missing $f"; fi
done

# OMC commands
for c in 도움말 접속세팅 API발급 요소측정 디자인수정; do
  f="$AK/.claude/commands/${c}.md"
  if [[ -f "$f" ]]; then pass "command /${c}"; else fail "missing $f"; fi
done

# aliases
for c in 카페24-시작 카페24-도와줘 카페24-새작업; do
  [[ -f "$AK/.claude/commands/${c}.md" ]] && pass "alias ${c}" || fail "alias ${c}"
done

# core docs
for f in commands/COMMANDS.md docs/MCP-OAUTH-GUIDE.md docs/OFFICIAL-AUDIT.md workflows/04-measure-first.md traps/INDEX.md; do
  [[ -f "$AK/$f" ]] && pass "$f" || fail "missing $f"
done

# AUDIT sections
grep -q "## Phase 1-F" "$AK/docs/OFFICIAL-AUDIT.md" && pass "AUDIT §F" || fail "AUDIT §F"
grep -q "## Phase 1-E" "$AK/docs/OFFICIAL-AUDIT.md" && pass "AUDIT §E" || fail "AUDIT §E"

# CLAUDE links
grep -q "getting-started/00" "$AK/CLAUDE.md" && pass "CLAUDE getting-started" || fail "CLAUDE gs"
grep -q "/접속세팅" "$AK/CLAUDE.md" && pass "CLAUDE commands" || fail "CLAUDE cmd"

# MCP design_type removed
if grep -q "design_type" "$WS/mcp/backends/cafe24_api.py" 2>/dev/null; then
  fail "design_type still in cafe24_api.py"
else
  pass "MCP no design_type"
fi

# broken self-ref: README claims gs exists
grep -q "getting-started/" "$AK/README.md" && pass "README gs" || fail "README"

# original untouched
if [[ -f "$ORIG/docs/OFFICIAL-AUDIT.md" ]]; then
  fail "ORIG has OFFICIAL-AUDIT (should be copy-only)"
else
  pass "ORIG no AUDIT"
fi

grep -q "## Phase G" "$AK/docs/OFFICIAL-AUDIT.md" && pass "AUDIT §G live" || fail "AUDIT §G"
[[ -f "$AK/docs/VERIFICATION-EVIDENCE.md" ]] && pass "VERIFICATION-EVIDENCE.md" || fail "VERIFICATION-EVIDENCE"
grep -q "5/5 PASS" "$AK/docs/VERIFICATION-EVIDENCE.md" && pass "smoke 5/5 recorded" || fail "smoke record"

if [[ $FAIL -eq 0 ]]; then
  echo "=== ALL PASS ($FAIL failures) ==="
  exit 0
else
  echo "=== $FAIL FAILURE(S) ==="
  exit 1
fi
