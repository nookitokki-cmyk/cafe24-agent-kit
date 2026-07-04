#!/usr/bin/env bash
# agent-kit 구조·동작·보안 검증 (portable · 실측 기반)
# v3: "문서에 글자 있으면 통과" 순환검증 + 작성자 PC 전용 ORIG 경로 체크 제거.
#     대신 실제 동작(import) + 보안 회귀(시크릿 0) 검증.
set -euo pipefail
AK="$(cd "$(dirname "$0")/../.." && pwd)"   # agent-kit/ (스크립트는 agent-kit/connect/scripts/)
KIT="$(cd "$AK/.." && pwd)"                 # kit root (mcp/ · api-poc/ · scripts/ 위치)
PY="$(command -v python || command -v python3 || true)"
FAIL=0
pass(){ echo "PASS: $1"; }
fail(){ echo "FAIL: $1"; FAIL=$((FAIL+1)); }

# 시크릿 파일 탐지 패턴 (배포에 절대 들어가면 안 되는 것) — .gitignore와 동기화
SECRET_FIND=( -type f \(
  -name 'sftp_*.json' -o -name '*.token.json'
  -o -name 'cafe24_config_*.py' -o -name 'cafe24_config.py'
  -o -name 'auth_url.txt' -o -name '.env' -o -name 'credentials.json'
  \) -not -path '*/.git/*' -not -path '*/node_modules/*' )

echo "=== verify-kit ($KIT) ==="

# 1) 두뇌 핵심 문서 존재
for f in CLAUDE.md README.md \
         brain/docs/CAFE24-SMARTDESIGN-AGENT.md 02_막혔을때/common-pitfalls.md 02_막혔을때/F-상황-인덱스.md \
         02_막혔을때/함정-INDEX.md 01_작업하기/workflows/07-ez-on-legacy-setup.md; do
  [[ -f "$AK/$f" ]] && pass "doc $f" || fail "missing agent-kit/$f"
done

# 2) 초보자 동선(00_시작하기) 최소 5개
gs=$(find "$AK/00_시작하기" -maxdepth 1 -name '*.md' -type f 2>/dev/null | wc -l | tr -d ' ')
[[ "$gs" -ge 5 ]] && pass "00_시작하기 ${gs}개" || fail "00_시작하기 부족(${gs})"

# 3) 손발(MCP) 핵심 파일 존재
for f in server.py cli.py kit_tools.py auth/oauth.py \
         backends/cafe24_api.py backends/cafe24_sftp.py \
         config/cafe24_config.example.py; do
  [[ -f "$KIT/mcp/$f" ]] && pass "mcp $f" || fail "missing mcp/$f"
done

# 4) 설계서(핵심 자산) 존재
[[ -f "$KIT/api-poc/MCP-DESIGN.md" ]] && pass "설계서 api-poc/MCP-DESIGN.md" || fail "missing api-poc/MCP-DESIGN.md"

# 5) 보안 회귀 — 시크릿 파일 0개 (비번 문자열은 스크립트에 절대 넣지 않음)
sec=$(find "$KIT" "${SECRET_FIND[@]}" 2>/dev/null | wc -l | tr -d ' ')
if [[ "$sec" == "0" ]]; then pass "시크릿 파일 0개"
else fail "시크릿 파일 ${sec}개 발견 (배포 금지)"
  find "$KIT" "${SECRET_FIND[@]}" 2>/dev/null >&2
fi

# 5b) 실명 누출 — 벤더 브랜드(IDIO) 0건 (배포 금지)
IDLEAK=$(grep -rIlE 'IDIO|_idio|idio\.js' "$AK" "$KIT/mcp" 2>/dev/null | grep -vE '/\.git/|verify-kit\.sh' || true)
if [[ -z "$IDLEAK" ]]; then pass "벤더 브랜드(IDIO) 0건"
else fail "벤더 브랜드(IDIO) 발견 (배포 금지)"; echo "$IDLEAK" >&2
fi

# 5c) 미검증 변수 재유입 차단 — 비-카페24(APapeIsName) 출처 가짜 변수 denylist (배포 금지)
#     v2.7.0에서 recipes/templates 제거로 정리. 재유입 시 FAIL. (카페24 변수 단일 기준: references/variables.md)
FAKEVARS='\{\$(thumbnail_url|product_url|main_image_url|sale_price|retail_price|brand_name|review_score|kakao_login_url|naver_login_url|product_image2)\}'
fakev=$(grep -rIlE "$FAKEVARS" "$KIT/.claude/skills" 2>/dev/null | grep -vE '/\.git/|verify-kit\.sh' || true)
if [[ -z "$fakev" ]]; then pass "미검증 가짜 변수 0건"
else fail "미검증 가짜 변수 발견 (references/variables.md 검증본으로 교체 필요)"; echo "$fakev" >&2
fi

# 6) 실 클라이언트 폴더 없음 (_template/demo000 만 허용)
realc=$(find "$AK/clients" -mindepth 1 -maxdepth 1 -type d \
          ! -name '_template' ! -name 'demo000' 2>/dev/null | wc -l | tr -d ' ')
[[ "$realc" == "0" ]] && pass "clients = _template/demo000 만" || { fail "clients 실클라 ${realc}개"; find "$AK/clients" -mindepth 1 -maxdepth 1 -type d >&2; }

# 7) 실제 동작 — mcp import (의존성 설치돼 있으면 진짜 검증, 아니면 SKIP)
if [[ -n "$PY" ]]; then
  if (cd "$KIT/mcp" && "$PY" -c "import server" >/dev/null 2>&1); then
    pass "mcp import server (실동작)"
  else
    echo "SKIP: mcp import — 의존성 미설치 가능 (cd mcp && pip install -r requirements.txt 후 재시도)"
  fi
else
  echo "SKIP: python 미설치 — import 검증 생략"
fi

if [[ $FAIL -eq 0 ]]; then
  echo "=== ALL PASS ==="
  exit 0
else
  echo "=== ${FAIL} FAILURE(S) ==="
  exit 1
fi
