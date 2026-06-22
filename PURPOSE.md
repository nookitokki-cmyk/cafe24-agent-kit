# PURPOSE — 카페24 에이전트 키트 목적·구조 헌장

> 이 문서는 키트의 **목적·구조 원칙·개편 불변식**을 고정하는 단일 기준이다.
> 구조를 바꾸는 모든 작업은 §3 "자동업데이트 불변식"을 위반하지 않아야 한다.
> 작성: 2026-06-22 · 0단계 검증(critic) 반영본

---

## 1. 목적 (한 줄)
**비코더가 Cursor/Claude Code로 카페24 스킨 작업을 자동화하는 키트.**
누끼토끼 본인의 작업 두뇌이자, 외부에 배포하는 제품(둘 다).

- **타깃**: ① 누끼토끼 본인(git 클론 = git 채널) ② 외부 비코더 셀러·에이전시(GitHub Release zip = release 채널)
- **핵심 동선**: 받기 → Cursor/Claude Code로 열기 → `/키트시작` → 작업 (코드 몰라도 됨)

## 2. 3층 분리 원칙
| 층 | 누가 보나 | 무엇 | 위치 |
|---|---|---|---|
| **표면 (Surface)** | 사용자(사람) | 진입점 README, 온보딩, 슬래시 명령, 가이드 | `README.md`, `agent-kit/00_시작하기/`, `01_작업하기/`, `02_막혔을때/` |
| **두뇌 (Brain)** | 에이전트(Claude) | cafe24 스킬·지식·규칙·base CSS 지도 | `agent-kit/.claude/skills/`, `agent-kit/brain/docs/` |
| **빌드/배포 (Build)** | 개발자 | dist 빌드 도구·산출물 (자동업데이트 일부 의존) | `scripts/`, `dist/`, `mcp/work/scripts/` |
| **백스테이지 (Dev)** | 개발자(대표님)만 | 개발 이력·증거·메타 (배포·업데이트 **완전 제외**) | `_dev/`(신설) |

> ⚠️ `scripts/`·`dist/`·`mcp/work/scripts/`는 "백스테이지"가 아니다 — `mcp/work/scripts/strip_ez.py`는 UPDATE_PATHS(kit_tools.py:586)에 등재돼 **자동업데이트 대상**이다. (참고: line 593의 루트 `work/scripts`는 소스 부재로 항상 skip되는 죽은 항목.) 배포 제외 대상은 오직 `_dev/`.

## 3. ★ 자동업데이트 불변식 (구조 개편의 절대 제약)
자동 업데이트는 `mcp/kit_tools.py` 앵커 4개 + `UPDATE_PATHS` 화이트리스트에 전적으로 의존. **위반 시 기존 설치자의 자동 업데이트가 깨진다.** (줄번호는 검증 시점 실측)

### 3-1. 앵커 4개 (상대구조 고정 — kit_tools.py:17~22)
```
MCP_DIR        = mcp/                (kit_tools.py 위치)
WORKSPACE_ROOT = MCP_DIR.parent      (= 레포 루트, 깊이 정확히 1단계)
KIT_ROOT       = WORKSPACE_ROOT/agent-kit
CONFIG_DIR     = mcp/config/
```

### 3-2. 절대 이동·이름변경 금지 9
1. `mcp/kit_tools.py` 2. `mcp/` 폴더(루트 직속) 3. `mcp/server.py`(zip 검증+진단 import) 4. `agent-kit/`(KIT_ROOT) 5. `agent-kit/clients/_template/` 6. `mcp/config/` 7. 루트 `VERSION`(1행 `vX.Y.Z`) 8. release zip 이름 접두어 `cafe24-agent-kit` + zip 내부 `VERSION`+`mcp/server.py` 동거(kit_tools.py:204) 9. 루트 `.git`(채널 감지)

### 3-3. 보존 경로 (자동업데이트가 절대 안 덮음 — 옮기면 사용자 토큰·작업물 유실)
- `mcp/config/` (UPDATE_PATHS에 **부재** = 보존) · `agent-kit/clients/{몰ID}/` (clients는 `_template`·일부 reference만 갱신, 나머지 보존: kit_tools.py:642~646)

### 3-4. 폴더 재배치 시 동시 수정 의무 (4곳)
`agent-kit/` 하위 폴더를 옮기거나 **이름 바꾸면** 아래를 **모두 함께** 수정. 누락 시 구 폴더 고아 + 신 폴더 영영 미갱신:
1. `mcp/kit_tools.py` `UPDATE_PATHS`(574~598) — 자동업데이트 화이트리스트 (특히 `agent-kit/brain` 580줄 = brain 통째)
2. `scripts/build-dist-kit.sh` — dist 하드코딩 폴더 + REQUIRED 검증(197~256)
3. `agent-kit/connect/scripts/verify-kit.sh` — 소스 검증, 폴더명 하드코딩(`00_시작하기`·`01_작업하기/workflows/...`·`02_막혔을때`)
4. `scripts/verify-kit.sh` — dist 검증(별개 파일)
> kit_update의 stale 삭제는 "디렉토리 **내부**"만(kit_tools.py:626~635). 디렉토리 자체 이동/개명은 자동 정리 안 됨 → 개명 회피가 최선.

### 3-5. 안전한 격리 위치
- `_dev/`를 **레포 루트**(agent-kit 밖)에 두면: build allowlist라 dist 자동 제외 + UPDATE_PATHS 무관 → **가장 안전**.
- `.gitignore`에 `_dev/` 추가(선택, git 제외).

## 4. 목표 구조 (개편 후 — ★번호 폴더 개명 없음)
```
cafe24-agent-kit/                  (개발 레포)
├─ README.md            ← ★유일 진입점 (이게 뭐고 → /키트시작, 30초)
├─ VERSION · CHANGELOG.md          ← [불변] 자동업데이트 의존
├─ agent-kit/           ← 키트 본체 = 배포 대상 [이름 불변]
│  ├─ 00_시작하기/      ← [표면] 온보딩 (현 이름 유지)
│  ├─ 01_작업하기/      ← [표면] 작업 흐름 (★현 이름 유지 — 개명 시 UPDATE_PATHS·verify 깨짐)
│  ├─ 02_막혔을때/      ← [표면] 막혔을 때 (현 이름 유지)
│  ├─ .claude/skills/   ← [두뇌] cafe24 스킬·지식·CSS지도
│  ├─ brain/docs/       ← [두뇌] 에이전트 참조 지식 (이력·_evidence는 _dev로 물리이동)
│  ├─ connect/          ← verify·배포 문서
│  ├─ clients/_template ← [불변] scaffold 원본
│  └─ clients/{몰}/     ← [보존] 작업물
├─ mcp/                 ← [불변] 손발 전체 (kit_tools·server·cli·auth·backends·config·work/scripts)
├─ api-poc/             ← connect verify(41줄) 의존 → 유지 (또는 단계1에서 _dev 결정)
├─ scripts/             ← 빌드 도구 (build-dist-kit.sh)
├─ dist/                ← 배포 산출물
└─ _dev/                ← ★[백스테이지] 배포·업데이트 완전 제외
   ├─ history/          (개발 이력 화석 — 검토 후. ※WORK-GUIDE는 두뇌라 brain 유지)
   └─ meta/             (__THE-ONE·__STATUS·MANIFEST) ✅단계1 완료
   ※ agent-kit/brain/_evidence 는 brain에 **유지** — 두뇌 문서(OFFICIAL-AUDIT·admin-verify·07-ez)가
     참조하므로 이동 시 링크 깨짐. 격리는 build 제외(단계4)로. 자동업데이트는 brain 통째
     rmtree+재복사(UPDATE_PATHS:580)라 build에서 빠지면 기존 설치자에게도 사라짐(좀비 없음).
```

**핵심**: 폴더 **개명·이동은 최소화**(고위험). 개편의 실질 = ① 개발 메타 `_dev/` 격리(이동) + 개발 증거는 build 제외(비이동) ② 진입점 README 단일화 ③ 배포 빌드에 `_dev`·`_evidence` 제외. 표면 가독성(번호 폴더 직관성)은 README가 안내.

## 5. 개편 단계 (단계별 100점 게이트)
| 단계 | 작업 | 불변식 영향·주의 |
|---|---|---|
| **0** | 이 PURPOSE.md 박제 (검증 완료) | — |
| **1** ✅ | 메타(`__THE-ONE`·`__STATUS`·`MANIFEST`)만 루트 `_dev/meta`로 `git mv` + README 링크 2곳 수정. **`_evidence`는 brain 유지**(두뇌 문서 다수 참조) — 격리는 build 제외(단계4)로. | 완료 (깨진 참조 0) |
| **2** | 진입점 단일화 — README 1개로 통합, `__*` 메타·중복 진입 문서 정리(1단계서 _dev 이동) | 낮음 |
| **3** | (축소) 폴더 **개명 없이** brain/docs 내 이력만 정리, 표면 가독성은 진입점으로 | 낮음 (개명 회피로 위험 제거) |
| **4** | 배포 빌드 — `build-dist-kit.sh`에 `_dev`(루트 allowlist 자동제외 확인) + **`agent-kit/brain/_evidence` 제외** 추가, zip 루트 구조 유지, DISTRIBUTION-KIT.md 구버전 서술 정정 | 중 (§3 zip 구조 유지) |
| **5** | 온보딩 동선 검증 — 받기→/키트시작→작업 막힘 제거 + verify 2종 PASS | 낮음 |

> **단계 순서 의존**: 단계1의 brain 물리삭제가 안 되면 이후가 무의미. 1 → 2 → (3) → 4 → 5 순서 고정.

## 6. 개편 방법론 + 롤백
- 한 번에 "다 정리" 금지(195파일·경로 참조 多). **단계 하나씩, 100점 검증 후 다음.**
- 검증: `bash scripts/verify-kit.sh`(dist) + `bash agent-kit/connect/scripts/verify-kit.sh`(소스) 둘 다 PASS.
- **롤백**: git 채널(본인)은 단계별 커밋으로 안전. **release 채널(외부)** 은 잘못 배포 시 *직전 버전 zip을 latest로 재발행* 해야 회복되므로, **release 발행(단계4 이후)은 dist 검증 통과 후에만**.
