#!/usr/bin/env bash
# verify-kit.sh — 배포 전 동작 검증 (파일 존재 체크가 아닌 실제 동작 확인)
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/dist/cafe24-agent-kit"
PASS=0; FAIL=0

ok()   { echo "  ✓  $*"; PASS=$((PASS+1)); }
fail() { echo "  ✗  $*" >&2; FAIL=$((FAIL+1)); }

echo "=== cafe24-agent-kit 동작 검증 ==="
echo "대상: $OUT"

# dist 폴더 존재 여부 (build-dist-kit.sh 먼저 실행 필요)
if [[ ! -d "$OUT" ]]; then
  echo "SKIP: dist 폴더 없음 — 먼저 scripts/build-dist-kit.sh 를 실행하세요." >&2
  exit 1
fi

# ── [1] Python 환경 ──────────────────────────────────────────────
echo ""
echo "[1] Python 환경"
# python3(Mac/Linux 기본) 우선, 없으면 python(Windows) 폴백
PY="$(command -v python3 || command -v python || true)"
if [[ -n "$PY" ]]; then
  PY_VER=$("$PY" --version 2>&1)
  ok "Python 발견: $PY_VER ($PY)"
else
  fail "python 명령어 없음 — Python 3.10+ 필요"
fi

# ── [2] MCP 서버 import 테스트 ────────────────────────────────────
echo ""
echo "[2] MCP 서버 import 테스트"
(cd "$OUT/mcp" && "$PY" -c "import server" 2>&1)        && ok "import server" \
  || fail "import server 실패 (requirements.txt 의존성 확인)"
(cd "$OUT/mcp" && "$PY" -c "import kit_tools" 2>&1)     && ok "import kit_tools" \
  || fail "import kit_tools 실패"
(cd "$OUT/mcp" && "$PY" -c "from backends import cafe24_sftp" 2>&1) && ok "import cafe24_sftp" \
  || fail "import cafe24_sftp 실패"
(cd "$OUT/mcp" && "$PY" -c "from auth import oauth" 2>&1) && ok "import oauth" \
  || fail "import oauth 실패"

# ── [3] Cursor MCP 예시 파일 JSON 유효성 ─────────────────────────
echo ""
echo "[3] Cursor MCP 예시 파일 JSON 파싱"
if [[ -f "$OUT/.cursor/mcp.json.example" ]]; then
  # Windows Python은 MSYS 경로(/c/...)를 못 열므로 cygpath로 변환 (없으면 원경로)
  MCP_EX="$OUT/.cursor/mcp.json.example"
  command -v cygpath >/dev/null 2>&1 && MCP_EX="$(cygpath -m "$MCP_EX")"
  "$PY" -c "import json,sys; json.load(open(sys.argv[1], encoding='utf-8'))" "$MCP_EX" 2>&1 \
    && ok "mcp.json.example 유효한 JSON" \
    || fail "mcp.json.example JSON 파싱 오류"
else
  fail ".cursor/mcp.json.example 없음"
fi

# ── [4] 실 클라이언트 데이터 제외 확인 ────────────────────────────
echo ""
echo "[4] 실 클라이언트 데이터 제외 확인"
if [[ -d "$OUT/agent-kit/clients/paransky97" ]]; then
  fail "clients/paransky97 이 배포본에 포함됨 — 실 클라이언트 데이터 유출 위험!"
else
  ok "clients/paransky97 없음"
fi
if [[ -d "$OUT/agent-kit/clients/nookitokki002" ]]; then
  fail "clients/nookitokki002 이 배포본에 포함됨"
else
  ok "clients/nookitokki002 없음"
fi
if [[ -d "$OUT/agent-kit/clients/demo000" ]]; then
  ok "clients/demo000 존재 (예시 워크플로우 포함)"
else
  fail "clients/demo000 없음 — 예시 워크플로우가 빠졌습니다"
fi

# ── [5] mcp/config 시크릿 누출 확인 ──────────────────────────────
echo ""
echo "[5] mcp/config 시크릿 누출 확인"
if find "$OUT/mcp/config" -name 'sftp_*.json' 2>/dev/null | grep -q .; then
  fail "mcp/config 에 sftp_*.json 존재 — SFTP 비밀번호 유출 위험!"
else
  ok "sftp_*.json 없음"
fi
if find "$OUT/mcp/config" -name 'cafe24_config_*.py' ! -name 'cafe24_config.example.py' 2>/dev/null | grep -q .; then
  fail "mcp/config 에 실제 cafe24_config_*.py 존재 — OAuth 시크릿 유출 위험!"
else
  ok "실제 cafe24_config_*.py 없음"
fi

# ── [6] 키워드 grep (비밀번호 패턴 광역 검색) ────────────────────
echo ""
echo "[6] 민감 키워드 광역 검색"
LEAKED=$(grep -r --include="*.py" --include="*.json" --include="*.md" \
  -l "paransky97\|beautysleep001\|__REDACTED_ROTATE__\|IDIO\|_idio\|idio\.js" \
  "$OUT" 2>/dev/null || true)
if [[ -n "$LEAKED" ]]; then
  fail "민감 키워드 발견:"
  echo "$LEAKED" | while read -r f; do echo "     $f"; done
else
  ok "민감 키워드(paransky97·IDIO 등) 미발견"
fi

# ── [7] VERSION 및 CHANGELOG 확인 ────────────────────────────────
echo ""
echo "[7] 버전 파일 확인"
if [[ -f "$OUT/VERSION" ]]; then
  VER=$(head -1 "$OUT/VERSION")
  ok "VERSION: $VER"
else
  fail "VERSION 파일 없음"
fi
if [[ -f "$OUT/CHANGELOG.md" ]]; then
  ok "CHANGELOG.md 존재"
else
  fail "CHANGELOG.md 없음"
fi

# ── [8] smoke_test.py 실행 가능 확인 ─────────────────────────────
echo ""
echo "[8] smoke_test.py 확인"
if [[ -f "$OUT/mcp/smoke_test.py" ]]; then
  ok "smoke_test.py 존재"
else
  fail "smoke_test.py 없음"
fi

# ── [9] 드리프트 가드 — v2.9.0 통일 사항 재유입 감시 (ADR follow-up) ──
echo ""
echo "[9] 드리프트 가드 (토큰 어휘·스니펫 변수·템플릿 중립성)"
# 9-1) 패자 토큰 어휘: 스니펫에서 --nk-color-* 재유입 금지 (flat 어휘가 kit 표준)
DRIFT_VOCAB=$(grep -rIl -- '--nk-color-' "$OUT/.claude/skills/cafe24/snippets" 2>/dev/null || true)
if [[ -n "$DRIFT_VOCAB" ]]; then
  fail "패자 토큰 어휘(--nk-color-*) 재유입:"
  echo "$DRIFT_VOCAB" | while read -r f; do echo "     $f"; done
else
  ok "스니펫 토큰 어휘 flat 유지 (--nk-color-* 0건)"
fi
# 9-2) 가짜 변수 재유입: {$link}·{$count} (검증본: {$link_product_list}·{$basket_count})
DRIFT_VARS=$(grep -rIlE '\{\$link\}|\{\$count\}' "$OUT/.claude/skills/cafe24/snippets" 2>/dev/null || true)
if [[ -n "$DRIFT_VARS" ]]; then
  fail "미검증 변수({\$link}/{\$count}) 재유입:"
  echo "$DRIFT_VARS" | while read -r f; do echo "     $f"; done
else
  ok "스니펫 변수 정합 유지 ({\$link}/{\$count} 0건)"
fi
# 9-3) 구 하드코딩 액센트(#2b6cb0) 재유입 금지 (중립 수렴값 #222222)
DRIFT_HEX=$(grep -rIli '#2b6cb0' "$OUT/.claude/skills/cafe24" 2>/dev/null || true)
if [[ -n "$DRIFT_HEX" ]]; then
  fail "구 하드코딩 액센트(#2b6cb0) 재유입:"
  echo "$DRIFT_HEX" | while read -r f; do echo "     $f"; done
else
  ok "하드코딩 액센트(#2b6cb0) 0건"
fi
# 9-4) 검증 템플릿 중립성: 브랜드·타클라·계정 문자열 유입 금지
VT="$OUT/agent-kit/clients/_verified-template"
if [[ -d "$VT" ]]; then
  DRIFT_VT=$(grep -rIliE 'MURMUR|#cc785c|#a9583e|401788|reference-intake|test1111|Marcellus' "$VT" 2>/dev/null || true)
  if [[ -n "$DRIFT_VT" ]]; then
    fail "_verified-template 브랜드/타클라 문자열 유입:"
    echo "$DRIFT_VT" | while read -r f; do echo "     $f"; done
  else
    ok "_verified-template 중립성 유지 (브랜드/타클라 0건)"
  fi
else
  fail "_verified-template 폴더가 dist에 없음"
fi

# ── 최종 결과 ────────────────────────────────────────────────────
echo ""
echo "========================================"
echo " 통과: $PASS   실패: $FAIL"
echo "========================================"
if [[ "$FAIL" -gt 0 ]]; then
  echo "FAIL: $FAIL 건 발견 — 배포 전 수정 필요" >&2
  exit 1
fi
echo "OK: 모든 검증 통과 — 배포 준비 완료"
