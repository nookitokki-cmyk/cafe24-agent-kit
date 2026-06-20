# Cafe24 Agent Kit — Changelog

## v2.3.2 (2026-06-20)

### Changed
- `설치-안내.md` 핑퐁 우선 재작성 — "채팅에 `/키트시작`" 중심(하나씩 물어봄), 수동 단계는 참고로 강등
- `/키트시작` 완료 시 `/API발급`(OAuth)로 자연스럽게 연결

---

## v2.3.1 (2026-06-20)

### Added
- 루트 `설치-안내.md` — 경로 무관 설치·사용·새 클라이언트 안내 (배포물 zip에도 포함)
- 범용 클라이언트 온보딩: "새 클라이언트" 한마디 → 몰 ID 하나만 묻고 `clients/{몰ID}/` 자동 생성·누적 (Tally·Notion 등 외부 폼 안 물음)

### Fixed
- 배포물에서 `__pycache__/*.pyc`(빌드 PC 경로·잉여 파일) 제외 — 빌드 시 `PYTHONDONTWRITEBYTECODE` + 사후 정리

---

## v2.3.0 (2026-06-20)

### Changed — 구조 재편 (Step 4b)
- **사람용/기계용 폴더 재편**: `getting-started`→`00_시작하기`, `examples`·`workflows`→`01_작업하기`, `traps/INDEX`·`common-pitfalls`·`F-상황-인덱스`→`02_막혔을때`, `rules`·지식 `docs`·`_evidence`→`brain`, 접속 `docs`·`scripts`→`connect` (git rename 이력 보존)
- 내부 마크다운 링크·MCP 코드(`server.py`·`kit_tools.py`)·셸 스크립트(`verify-kit.sh`·`build-dist-kit.sh`) 전부 새 구조로 갱신
- 중복 진입점 6→1 통합 (단일 진입점 = `agent-kit/README.md`)

### Added — 입문자료 (Step 4c)
- `00_시작하기/`: `0-이-키트가-뭔가요` · `용어집` · `첫수정-1건-성공` · `실패복구-가이드`

### Fixed — 익명화·범위 보강
- 배포 문서 잔존 실 클라이언트 식별자 제거(`SLOWAGINGS`·`paransky97`) + 깨진 링크 19곳 수리
- 문서 범위 정정: 강의/수강생 맥락 단어 제거 → 독자 = "이 키트를 쓰는 비개발자 누구나"

---

## v2.2.3 (2026-06-20)

### Fix
- `kit-update --from-github` — temp dir leak: extract under zip parent, single cleanup in `finally`
- `kit-update` — empty `CAFE24_KIT_UPDATE_SOURCE` no longer resolves to home dir
- `scaffold_client` — single `your_mall_id` replace (REDIRECT_URI derived from template)
- `kit_update` — reject source == workspace root (self-update guard)

---

## v2.2.2 (2026-06-20)

### Fix
- `kit-update --from-github` — private Release zip via API asset URL + `gh auth token` fallback
- `kit-update` no longer wipes entire `mcp/work/` (only `strip_ez.py`)

---

## v2.2.1 (2026-06-20)

### Fix
- `kit-update --from-github` — private repo Release zip via GitHub API asset URL (`application/octet-stream`)
- Auto `gh auth token` when `GITHUB_TOKEN` unset

---

## v2.2.0 (2026-06-19)

### Commands (onboarding + robustness)
- **`/키트시작`** — first install: pip, `import server`, MCP, smoke 5/9
- **`/새클라이언트`** — scaffold `clients/{mall_id}` from `_template`
- **`/MCP연결`** — Cursor + Claude Code MCP registration
- **`/검증`** — `run_preflight` ping-pong with F34 interpretation
- **`/캐시확인`** — `?v=N`, live URL vs SFTP path
- **`/EZ제거`** — Phase C strip (`strip_ez.py`) with user gate
- **`/버전확인`** — local VERSION + remote compare (v3 channel)

### MCP tools
- `get_kit_guides`: `kit_version`, `changelog_path`, `onboarding_commands`
- **`diagnose_kit_setup`** — structured install diagnostic
- **`scaffold_client(mall_id)`** — same logic as `/새클라이언트`

### CLI (`mcp/cli.py`)
- `diagnose`, `scaffold --mall`, `kit-version [--check-remote]`, `kit-update [--source] [--dry-run]`

### Docs & dist
- `05b-MCP-등록.md` — Cursor + Claude Code (replaces Cursor-only title)
- `OMC-명령어-매칭가이드.md`, `COMMANDS.md`, `/도움말` updated
- `smoke_test.py`: **no credentials → exit 0, 5/9 partial OK**
- `build-dist-kit.sh`: REQUIRED includes `05b`, `kit_tools.py`, `CHANGELOG.md`; version **v2.2.0**

### Release channel (v2.2.0+)
- GitHub: `nookitokki-cmyk/cafe24-agent-kit` — tag `v2.2.0` + zip asset
- `cli.py kit-update --from-github` — Release zip 자동 다운로드·적용
- `CAFE24_KIT_GITHUB_REPO` 기본값 · `kit-version --check-remote` via Releases API

---

## v2.0.1 (2026-06-18)

### Fix (critical dist regression)
- Bundle `mcp/auth/`, `mcp/backends/`, `mcp/config/__init__.py` — fixes `No module named auth`
- Windows Git Bash `cp --parents` → `copy_mcp_pkg()` with `cp -R`
- Dist includes `.cursor/mcp.json.example`, `cafe24_config.example.py`, `requirements.txt`
- Exclude `clients/nookitokki002` from dist; no secrets in `mcp/config/`

### Docs
- `05b-MCP-Cursor-등록.md` (later generalized in v2.2)
- Post-build gate: `python -c "import server"` from dist

---

## v2.0.0

- Initial distribution kit: agent-kit + MCP stdio server + score scripts
- 10 MCP tools, 8 workflows, OMC slash commands
