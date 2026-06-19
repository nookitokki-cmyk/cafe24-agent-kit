# Distribution Kit — 배포 번들 가이드



> **갱신:** 2026-06-19  

> **산출물:** `dist/cafe24-agent-kit/` (비밀·실몰 work tree 제외)



---



## 1. 빌드 방법



```bash

cd cafe24-agent-workspace

bash scripts/build-dist-kit.sh

```



빌드 후 `dist/cafe24-agent-kit/README-DIST.md`에 UTC 타임스탬프가 기록된다.



---



## 2. 번들에 포함되는 것



| 경로 | 내용 |

|------|------|

| `agent-kit/` | docs, workflows, rules, skills, clients 템플릿·레퍼런스 (`demo000`, `ecudemo400786`, `_template` 등) |

| `mcp/` | MCP 런타임: `server.py`, `cli.py`, `smoke_test.py`, `requirements.txt`, **`auth/`**, **`backends/`**, `config/__init__.py` + `cafe24_config.example.py` |
| `.cursor/mcp.json.example` | Cursor MCP 등록 템플릿 (수신자가 `.cursor/mcp.json`으로 복사) |

| `mcp/work/scripts/strip_ez.py` | EZ strip 유틸 (Phase C) |

| `work/scripts/ref393674-score-*.py` | ecudemo 파일럿 채점 스크립트 9종 |

| `work/scripts/score_mall.py` | v2 몰 ID·베이스 URL 해석 헬퍼 (`CAFE24_MALL_ID`, `--mall-id`) |

| `AGENTS.md` | 루트 에이전트 진입점 |



---



## 3. 의도적으로 제외되는 것



| 제외 | 이유 |

|------|------|

| `mcp/config/*.token.json`, `sftp_*.json` | OAuth·SFTP 비밀 |
| `mcp/config/cafe24_config_*.py` (example·`__init__.py` 제외) | 실몰 Client ID/Secret |
| `agent-kit/clients/nookitokki002` | 개인 스캐폴드 (v2 dist 제외) |

| `work/deploy-*`, `work/clients/*/deploy/` | 실몰 FTP 미러·대용량 스킨 트리 |

| `.git`, `__pycache__`, `*.pyc` | 메타·캐시 |

| 파트너 전용 live 증거 원본 (비공개 credential 세션) | 배포 시 재생성 |



수신자는 `mcp/config/README.txt` 안내에 따라 **자기 secure store**에서 토큰·SFTP JSON을 복사한다.



---



## 4. 첫 몰 세팅 (수신자) — 4단계

**초보자용 상세:** [`getting-started/05b-MCP-등록.md`](../getting-started/05b-MCP-등록.md) · **`/키트시작`**

1. **의존성** — Cursor에서 `dist/cafe24-agent-kit` 폴더를 워크스페이스로 연다 → `cd mcp && pip install -r requirements.txt` (+ 채점용: `pip install playwright && playwright install chromium`)

2. **몰 설정** — `mcp/config/cafe24_config.example.py` → `cafe24_config_{몰ID}.py` 복사 후 `CLIENT_ID`·`CLIENT_SECRET`·`REDIRECT_URI` 입력. SFTP 사용 시 `sftp_{몰ID}.json` 추가 (`mcp/config/README.txt` 참고).

3. **Cursor MCP** — `.cursor/mcp.json.example` → `.cursor/mcp.json` 복사 (또는 Settings → MCP → Edit Config에 붙여넣기) → Cursor 재시작.

4. **OAuth** — `python cli.py auth-url --mall {몰ID}` → 브라우저 허용 → `python cli.py code "oauth-callback?code=…" --mall {몰ID}` → `python cli.py status --mall {몰ID}` 로 `access_token_valid: true` 확인.

**검증 (연결 후)** — `python -c "import server"` · `python smoke_test.py` · MCP `get_kit_guides` → `run_preflight(check="all", mall_id="…")`



**상세 OAuth/SFTP:** `agent-kit/docs/MCP-OAUTH-GUIDE.md` 또는 `/접속세팅` — OAuth 앱·`cafe24_config_{mall}.py`·토큰 발급. SFTP: `sftp_{mall}.json` 작성 (일반몰 vs 파트너 `/sde_design/` 경로 — `MCP-OAUTH-GUIDE.md` 참조).



**EZ 전략:** 기본 **strip** ([`EZ-STRATEGY.md`](EZ-STRATEGY.md)). ecudemo400786만 Phase C **스킵** 파일럿 예외.



---



## 5. v1 vs v2 로드맵



| | **v1.0.0** (배포됨) | **v2.0.0** (배포됨) |

|---|---------------------|------------------------------|

| `run_preflight` | 9 check 타입 + `check=all` batch, F34/MOBILE_WEB 힌트 | `mall_id` 파라미터 + `CAFE24_MALL_ID` env 전달; **`mall_id_applied_to_scripts: true`** |

| 대상 몰 | ecudemo400786 하드코딩 (메타데이터만 `mall_id` 기록) | **`score_mall.py` + 9 score 스크립트** (`--mall-id` / env) |

| MOBILE_WEB | `mobile_full` FAIL 시 F34 안내 문자열 | `mobile_full`이 라이브 페이지 소스에서 `CAFE24.MOBILE_WEB` **자동 프로브** ✅ |

| smoke | `valid_checks` 10종 incl. `all` · header 라이브 · `SMOKE_PREFLIGHT_ALL=1`로 9/9 batch | **토큰 있으면 `SMOKE_PREFLIGHT_ALL` 기본 1** → 9/9 라이브 batch; `=0`으로 빠른 smoke; `valid_checks` **10/10** incl. `all` |

| dist | `dist/cafe24-agent-kit/VERSION` = `v1.0.0` | 동일 번들 경로, **`v2.0.0`** → **`v2.0.1`** (auth/backends 패키지 포함 수정) |



**v2.1+ (미완):** `run_preflight(mall_id=demo000)` 실채점·demo000 workflow 08 end-to-end (다른 몰 baseline·셀렉터 검증).



**v1 배포 경로:** `dist/cafe24-agent-kit/` (폴더 그대로 또는 zip 압축 후 전달)



**v2 배포 방법 (수신자):**



1. `dist/cafe24-agent-kit` 폴더를 Cursor 워크스페이스로 연다 (또는 zip 해제).

2. `cd mcp && pip install -r requirements.txt` (+ Playwright: `playwright install chromium`)

3. `mcp/config/`에 OAuth 토큰·SFTP JSON 복사 + `.cursor/mcp.json.example` → `.cursor/mcp.json`

4. `python -c "import server"` 로 import 확인 후 MCP `get_kit_guides` → `run_preflight(check="all", mall_id="…")`

5. 검증: `python smoke_test.py` (토큰 있으면 9/9 batch 기본, ~15분). 빠른 smoke: `SMOKE_PREFLIGHT_ALL=0 python smoke_test.py`.



---



## 6. 관련 문서



- [`LEGACY-HUNTER.md`](LEGACY-HUNTER.md) — strip 전후 스킨 감사

- `TEMPLATE-PILOT-ACCEPTANCE.md` — 파일럿 합격 기준

- `REMAINING-WORK-CHECKLIST.md` — 열린 MVP 항목

---

## 7. GitHub Release · kit-update

**저장소:** [github.com/nookitokki-cmyk/cafe24-agent-kit](https://github.com/nookitokki-cmyk/cafe24-agent-kit) (private)

| 방법 | 명령 |
|------|------|
| zip 수동 | Releases → `cafe24-agent-kit-v2.2.0.zip` 다운로드 |
| 버전 확인 | `cd mcp && python cli.py kit-version --check-remote` |
| 자동 업데이트 | `python cli.py kit-update --from-github` |
| 특정 태그 | `python cli.py kit-update --from-github --tag v2.2.0` |
| 미리보기 | `python cli.py kit-update --from-github --dry-run` |

**환경변수 (선택)**

| 변수 | 기본값 | 용도 |
|------|--------|------|
| `CAFE24_KIT_GITHUB_REPO` | `nookitokki-cmyk/cafe24-agent-kit` | Releases API |
| `CAFE24_KIT_RELEASE_URL` | (없음) | raw `VERSION` URL — 설정 시 API 대신 사용 |
| `GITHUB_TOKEN` | (없음) | private repo — `gh auth login` 또는 PAT (`repo` scope) |

**보존:** `mcp/config/*`, `agent-kit/clients/{본인몰}/` — update 후에도 덮어쓰지 않음.

슬래시: **`/버전확인`** · **`/키트시작`**

