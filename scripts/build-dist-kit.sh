#!/usr/bin/env bash
# Minimal distributable cafe24-agent-kit bundle (no secrets, no work client trees)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/dist/cafe24-agent-kit"
STAGE="$ROOT/dist/.cafe24-agent-kit-staging"
rm -rf "$STAGE"
mkdir -p "$STAGE"
BUILD_ROOT="$STAGE"

copy_tree() {
  local src="$1" dest="$2"
  mkdir -p "$dest"
  if command -v rsync >/dev/null 2>&1; then
    rsync -a --exclude '.git' --exclude '__pycache__' --exclude '*.pyc' "$src/" "$dest/"
  else
    cp -R "$src/." "$dest/"
  fi
}

# agent-kit (docs, workflows, demo000; exclude personal scaffold and real client data)
mkdir -p "$BUILD_ROOT/agent-kit"
if command -v rsync >/dev/null 2>&1; then
  rsync -a --exclude '.git' --exclude '__pycache__' --exclude '*.pyc' \
    --exclude 'clients/nookitokki002' \
    --exclude 'clients/paransky97' \
    --exclude 'brain/_evidence' \
    "$ROOT/agent-kit/" "$BUILD_ROOT/agent-kit/"
else
  copy_tree "$ROOT/agent-kit" "$BUILD_ROOT/agent-kit"
  rm -rf "$BUILD_ROOT/agent-kit/clients/nookitokki002"
  rm -rf "$BUILD_ROOT/agent-kit/clients/paransky97"
  rm -rf "$BUILD_ROOT/agent-kit/brain/_evidence"
fi

# clients: allowlist — ship ONLY _template + demo000 (drop real/test client folders e.g. ecudemo*,
# and stray runtime dirs like .omc). find (mindepth 1) catches hidden entries too; rsync/cp ignore .gitignore.
if [[ -d "$BUILD_ROOT/agent-kit/clients" ]]; then
  find "$BUILD_ROOT/agent-kit/clients" -mindepth 1 -maxdepth 1 \
    ! -name '_template' ! -name 'demo000' -exec rm -rf {} +
fi

# strip OMC runtime state anywhere under agent-kit (never distributable; e.g. clients/demo000/.omc)
find "$BUILD_ROOT/agent-kit" -type d -name '.omc' -exec rm -rf {} + 2>/dev/null || true

# MCP runtime (no config secrets) — server.py imports auth.*, backends.*, config.*
# Use cp -R for packages: cp --parents on Git Bash Windows preserves absolute paths (mcp/c/Users/...).
copy_mcp_pkg() {
  local pkg="$1"
  local src="$ROOT/mcp/$pkg" dest="$BUILD_ROOT/mcp/$pkg"
  [[ -d "$src" ]] || return 0
  rm -rf "$dest"
  mkdir -p "$dest"
  if command -v rsync >/dev/null 2>&1; then
    rsync -a --exclude '__pycache__' --exclude '*.pyc' "$src/" "$dest/"
  else
    cp -R "$src/." "$dest/"
    find "$dest" -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
    find "$dest" -name '*.pyc' -delete 2>/dev/null || true
  fi
}

mkdir -p "$BUILD_ROOT/mcp"
for f in server.py cli.py smoke_test.py kit_tools.py requirements.txt README.md; do
  [[ -f "$ROOT/mcp/$f" ]] && cp "$ROOT/mcp/$f" "$BUILD_ROOT/mcp/"
done
for pkg in auth backends; do
  copy_mcp_pkg "$pkg"
done
mkdir -p "$BUILD_ROOT/mcp/config"
[[ -f "$ROOT/mcp/config/__init__.py" ]] && cp "$ROOT/mcp/config/__init__.py" "$BUILD_ROOT/mcp/config/"
EXAMPLE_SRC="$ROOT/mcp/config/cafe24_config.example.py"
if [[ ! -f "$EXAMPLE_SRC" ]]; then
  mkdir -p "$ROOT/mcp/config"
  cat > "$EXAMPLE_SRC" <<'EOF'
# Copy to cafe24_config_{mall_id}.py — fill in your values; never commit the copy.
# Template for Cafe24 Admin API OAuth (distribution kit)

MALL_ID = "your_mall_id"

CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"

REDIRECT_URI = "https://your_mall_id.cafe24.com/oauth-callback"
SCOPE = "mall.read_design"
API_VERSION = "2026-03-01"
EOF
fi
cp "$EXAMPLE_SRC" "$BUILD_ROOT/mcp/config/"
cat > "$BUILD_ROOT/mcp/config/README.txt" <<'EOF'
카페24 MCP 설정 (배포본 — 비밀 파일은 직접 추가)

1. pip install
   cd mcp && pip install -r requirements.txt

2. OAuth 앱 설정
   cafe24_config.example.py → cafe24_config_{몰ID}.py 복사 후 CLIENT_ID/SECRET/REDIRECT_URI 입력

3. (선택) SFTP
   sftp_{몰ID}.json 을 이 폴더에 추가 (비밀 — git/배포에 넣지 마세요)

4. Cursor MCP
   ../.cursor/mcp.json.example → ../.cursor/mcp.json 복사 후 Cursor 재시작
   상세: agent-kit/00_시작하기/05b-MCP-등록.md

5. OAuth 토큰
   python cli.py auth-url --mall {몰ID}
   python cli.py code "oauth-callback?code=..." --mall {몰ID}
EOF
# Belt-and-suspenders: never ship real mall configs or tokens
find "$BUILD_ROOT/mcp/config" -type f \
  ! -name 'cafe24_config.example.py' ! -name 'README.txt' ! -name '__init__.py' -delete 2>/dev/null || true

# EZ strip utility (dev path: mcp/work/scripts — referenced by paransky97 workflow)
mkdir -p "$BUILD_ROOT/mcp/work/scripts"
if [[ -f "$ROOT/mcp/work/scripts/strip_ez.py" ]]; then
  cp "$ROOT/mcp/work/scripts/strip_ez.py" "$BUILD_ROOT/mcp/work/scripts/"
fi

# Score scripts (ecudemo pilot reference) — optional: dev work/ is excluded from the clean kit
if [[ -d "$ROOT/work/scripts" ]]; then
  copy_tree "$ROOT/work/scripts" "$BUILD_ROOT/work/scripts"
fi

# Cursor MCP registration template (user copies → .cursor/mcp.json)
mkdir -p "$BUILD_ROOT/.cursor"
for ex in "$ROOT"/.cursor/mcp.json*.example; do
  [[ -f "$ex" ]] && cp "$ex" "$BUILD_ROOT/.cursor/"
done

# Root .claude — 슬래시 스킬·에이전트 (워크스페이스 루트에서 /명령 인식). worktrees 등 런타임은 제외.
if [[ -d "$ROOT/.claude" ]]; then
  mkdir -p "$BUILD_ROOT/.claude"
  for sub in skills agents; do
    if [[ -d "$ROOT/.claude/$sub" ]]; then
      if command -v rsync >/dev/null 2>&1; then
        rsync -a --exclude '.git' --exclude '__pycache__' --exclude '*.pyc' "$ROOT/.claude/$sub" "$BUILD_ROOT/.claude/"
      else
        cp -R "$ROOT/.claude/$sub" "$BUILD_ROOT/.claude/"
      fi
    fi
  done
fi

# Root pointers
cp "$ROOT/AGENTS.md" "$BUILD_ROOT/"
[[ -f "$ROOT/README.md" ]] && cp "$ROOT/README.md" "$BUILD_ROOT/"   # 배포 진입점 = 루트 README (README-DIST 대체)
[[ -f "$ROOT/CHANGELOG.md" ]] && cp "$ROOT/CHANGELOG.md" "$BUILD_ROOT/"
[[ -f "$ROOT/설치-안내.md" ]] && cp "$ROOT/설치-안내.md" "$BUILD_ROOT/"
DIST_VERSION="$(head -1 "$ROOT/VERSION" 2>/dev/null || echo v2.3.0)"
DIST_DATE="$(date -u +%Y-%m-%d)"
cat > "$BUILD_ROOT/VERSION" <<EOF
$DIST_VERSION
$DIST_DATE
EOF
# (README-DIST.md 폐지 — 배포 진입점은 루트 README.md. 위 Root pointers에서 dist 루트로 복사됨.)

# Promote staging → dist (Windows: target dir may be locked by IDE)
if [[ -d "$OUT" ]] && ! rm -rf "$OUT" 2>/dev/null; then
  echo "WARN: $OUT busy — syncing in-place" >&2
  if command -v rsync >/dev/null 2>&1; then
    rsync -a --delete "$STAGE/" "$OUT/"
  elif command -v python >/dev/null 2>&1; then
    python - "$STAGE" "$OUT" <<'PY'
import pathlib, shutil, sys
stage, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
for src in stage.rglob("*"):
    rel = src.relative_to(stage)
    dst = out / rel
    if src.is_dir():
        dst.mkdir(parents=True, exist_ok=True)
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
stage_files = {p.relative_to(stage) for p in stage.rglob("*") if p.is_file()}
for p in list(out.rglob("*")):
    if p.is_file() and p.relative_to(out) not in stage_files:
        p.unlink(missing_ok=True)
for p in sorted(out.rglob("*"), key=lambda x: len(x.parts), reverse=True):
    if p.is_dir() and not any(p.iterdir()):
        p.rmdir()
PY
  else
    echo "dist promote failed: close handles on $OUT or install python/rsync" >&2
    exit 1
  fi
else
  mkdir -p "$(dirname "$OUT")"
  mv "$STAGE" "$OUT"
fi
rm -rf "$STAGE"

# Post-build sanity checks
REQUIRED=(
  "$OUT/agent-kit/brain/docs/LEGACY-HUNTER.md"
  "$OUT/agent-kit/connect/DISTRIBUTION-KIT.md"
  "$OUT/agent-kit/00_시작하기/05b-MCP-등록.md"
  "$OUT/agent-kit/clients/demo000/.workflow.md"
  "$OUT/.claude/skills/키트시작/SKILL.md"
  "$OUT/.claude/skills/새클라이언트/SKILL.md"
  "$OUT/.claude/skills/MCP연결/SKILL.md"
  "$OUT/mcp/server.py"
  "$OUT/mcp/kit_tools.py"
  "$OUT/mcp/requirements.txt"
  "$OUT/mcp/auth/oauth.py"
  "$OUT/mcp/auth/__init__.py"
  "$OUT/mcp/backends/cafe24_api.py"
  "$OUT/mcp/backends/cafe24_sftp.py"
  "$OUT/mcp/backends/cafe24_ftp.py"
  "$OUT/mcp/backends/__init__.py"
  "$OUT/mcp/config/__init__.py"
  "$OUT/mcp/config/cafe24_config.example.py"
  "$OUT/mcp/work/scripts/strip_ez.py"
  "$OUT/.cursor/mcp.json.example"
  "$OUT/CHANGELOG.md"
  "$OUT/README.md"
)
MISSING=0
for f in "${REQUIRED[@]}"; do
  if [[ ! -f "$f" ]]; then
    echo "MISSING: $f" >&2
    MISSING=$((MISSING + 1))
  fi
done
if [[ "$MISSING" -gt 0 ]]; then
  echo "dist build incomplete ($MISSING required file(s) missing)" >&2
  exit 1
fi

# No secrets in mcp/config (example + README + loader only)
CONFIG_EXTRA=$(find "$OUT/mcp/config" -type f \
  ! -name 'cafe24_config.example.py' ! -name 'README.txt' ! -name '__init__.py' 2>/dev/null | wc -l | tr -d ' ')
if [[ "$CONFIG_EXTRA" != "0" ]]; then
  echo "FAIL: unexpected files in mcp/config (secrets?)" >&2
  find "$OUT/mcp/config" -type f ! -name 'cafe24_config.example.py' ! -name 'README.txt' ! -name '__init__.py' >&2
  exit 1
fi
if find "$OUT/mcp/config" -name 'cafe24_config_*.py' ! -name 'cafe24_config.example.py' 2>/dev/null | grep -q .; then
  echo "FAIL: real cafe24_config_*.py leaked into dist" >&2
  exit 1
fi
# clients allowlist — only _template + demo000 may ship (catches ecudemo* and any future stray)
if [[ -d "$OUT/agent-kit/clients" ]]; then
  STRAY_CLIENTS=$(find "$OUT/agent-kit/clients" -mindepth 1 -maxdepth 1 ! -name '_template' ! -name 'demo000' 2>/dev/null)
  if [[ -n "$STRAY_CLIENTS" ]]; then
    echo "FAIL: unexpected client folder(s) in dist (only _template, demo000 allowed):" >&2
    echo "$STRAY_CLIENTS" >&2
    exit 1
  fi
fi
if [[ "$(head -1 "$OUT/VERSION")" != "$DIST_VERSION" ]]; then
  echo "FAIL: dist VERSION ($(head -1 "$OUT/VERSION")) != root VERSION ($DIST_VERSION)" >&2
  exit 1
fi

# Import smoke (no OAuth tokens required) — PYTHONDONTWRITEBYTECODE so the smoke
# import never leaves .pyc (build-machine paths) inside the shipped dist.
if command -v python >/dev/null 2>&1; then
  (cd "$OUT/mcp" && PYTHONDONTWRITEBYTECODE=1 python -c "import server") || {
    echo "FAIL: python -c 'import server' in dist/mcp" >&2
    exit 1
  }
fi
# Belt-and-suspenders: strip any bytecode caches before shipping
find "$OUT" -type d -name '__pycache__' -prune -exec rm -rf {} + 2>/dev/null || true
find "$OUT" -name '*.pyc' -delete 2>/dev/null || true

echo "dist ready: $OUT"
find "$OUT" -type f | wc -l | xargs echo "files:"
