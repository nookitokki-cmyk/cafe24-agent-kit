# Cafe24 Agent Kit — Changelog

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
