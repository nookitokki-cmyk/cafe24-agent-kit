# 카페24 스킨 빌더 에이전트 키트

> 이 문서는 **키트 본체 지도**입니다 (명령·폴더맵). 처음 진입은 루트 [`README.md`](../README.md) → `/키트시작`. 여기서는 본체 구조·명령·폴더를 안내합니다.

**카페24 + AI 작업자용 작업 키트** — 쇼핑몰·스킨을 에이전트와 함께 만들고, 레퍼런스·시안을 실제 몰에 옮깁니다. 작업자·클라이언트·에이전트가 같은 문서·명령·게이트를 공유합니다.

→ **누구를 위한 키트인지:** [**이-키트는-누구-용인가.md**](이-키트는-누구-용인가.md)

**두뇌(규칙·함정·문법) + 접속 가이드 + OMC 명령** 이 한 폴더에 있습니다.  
모노레포 손발(MCP): [`../mcp/`](../mcp/)

---

## ⚠️ 동기화 (canonical path)

**정본(canonical) 작업 경로:** 배포 키트 루트 (`cafe24-agent-kit/` 또는 monorepo `cafe24-agent-workspace/`)  
OneDrive 등에 있는 복사본은 오래될 수 있습니다. 문서·워크플로·MCP 변경은 정본에서만 반영하세요.

---

## 3분 시작

1. Cursor 또는 Claude Code에서 배포 키트 루트 열기  
2. 첫 설치 → 채팅 **`/키트시작`** (또는 [`00_시작하기/키트-시작-가이드.md`](00_시작하기/키트-시작-가이드.md))  
3. 채팅: **`/도움말`** 또는 **`/접속세팅`**  
4. 처음이면 [`00_시작하기/00-아무것도-모를-때.md`](00_시작하기/00-아무것도-모를-때.md)  
5. **막히면** → [`02_막혔을때/F-상황-인덱스.md`](02_막혔을때/F-상황-인덱스.md) (**F1~F34** 증상·Q&A·프롬프트 한곳)  
6. 복붙 프롬프트: [`00_시작하기/프롬프트-템플릿.md`](00_시작하기/프롬프트-템플릿.md) · 명령 매칭: [`00_시작하기/OMC-명령어-매칭가이드.md`](00_시작하기/OMC-명령어-매칭가이드.md)  
7. **Q&A (쉬운 말):** [`00_시작하기/QnA-쉬운말로.md`](00_시작하기/QnA-쉬운말로.md) (용어 없이 18문답)

---

## 명령어 (OMC 스타일)

| 명령 | 용도 |
|------|------|
| `/키트시작` | zip 풀고 pip·import·smoke (5/9 정상) |
| `/새클라이언트` | `clients/_template` scaffold |
| `/MCP연결` | Cursor·Claude Code MCP 등록 |
| `/도움말` | 지도·문서 (구 `/카페24-시작`) |
| `/레퍼런스인입` | URL **또는** 시안 → 페이지표·실측 (코드 전) |
| `/접속세팅` | 파트너 vs 일반, 몰 ID, SFTP, skin 표 |
| `/API발급` | 개발자센터 OAuth · `mall.read_design` |
| `/요소측정` | 수정 전 폰트·여백 px |
| `/디자인수정` | 실측 후 코드 (구 `/카페24-새작업`) |
| `/프롬프트참고` | 상황별 복붙 프롬프트 문서 링크 |
| `/카페24-자동화` 🧪 | 토큰빌드 → HTML → 리뷰 → QA → SFTP 원클릭 (v2.4.0 실험적) |

전체 14개(온보딩 3 + 작업 7 + 검증·운영 4): [`commands/COMMANDS.md`](commands/COMMANDS.md) · 매칭 가이드: [`00_시작하기/OMC-명령어-매칭가이드.md`](00_시작하기/OMC-명령어-매칭가이드.md)

> 🧪 = **실험적 (v2.4.0 신규)**. 실 클라이언트 검증 후 안정화 예정. 검증된 명령(`/디자인수정` 등)부터 우선 사용 권장.

---

## 폴더 맵

| 경로 | 내용 |
|------|------|
| `CLAUDE.md` | 에이전트 헌법·게이트 |
| **`00_시작하기/`** | **처음이면 여기부터 순서대로** — 온보딩 00~05 · **키트-시작-가이드** · **프롬프트 템플릿** · **OMC 명령 매칭** |
| `01_작업하기/` | 워크플로 (인입·실측·verify-loop) |
| `02_막혔을때/` | F1~F34 함정·인덱스·postmortem |
| `brain/` | 두뇌 — 규칙(`rules/`)·문서(`docs/`)·스니펫. 공식 대조: `brain/docs/OFFICIAL-AUDIT.md` |
| `connect/` | 접속·API 발급 — `connect/MCP-OAUTH-GUIDE.md` · `connect/scripts/verify-kit.sh` |
| **`02_막혔을때/F-상황-인덱스.md`** | **F1~F34 허브** (증상·Q&A·프롬프트·postmortem) |
| `00_시작하기/QnA-쉬운말로.md` | **[F?]** 태그 Q&A 18개 |
| `00_시작하기/실측-격차-설명가이드.md` | 실측 격차 이유·대응 |
| `00_시작하기/프롬프트-템플릿.md` | F코드 붙은 복붙 프롬프트 12종 |
| `02_막혔을때/함정-INDEX.md` | F1~F34 한 줄 인덱스 |
| `01_작업하기/workflows/` | 01~06 (인입·실측·verify-loop 포함) |
| `02_막혔을때/common-pitfalls.md` | narrow·**EZ #contents 92%** postmortem |
| `brain/docs/snippets/ez-contents-override.css` | `#container #contents` paste-ready |
| `brain/rules/cafe24-admin-verify.md` | 관리자 안내 전 웹 검증 |
| `brain/rules/responsive-mobile.md` | MO 단일 base 스킨 — **관리자 mobile OFF 필수** |
| `brain/rules/ez-contents-width.md` | **필수** EZ MO 92% width override (`#container #contents`) |
| `.claude/skills/` | 슬래시 대본 |
| `.claude/skills/cafe24/references/` | 변수·모디파이어·**troubleshooting** 사전 (v2.4.0 확장) |
| `.claude/skills/cafe24/snippets/` | HTML 컴포넌트 + CSS + JS (검증된 `nk-` 조각) |
| `.claude/skills/cafe24/design-tokens/` 🧪 | Figma → CSS 토큰 자동 파이프라인 (v2.4.0 실험적) |
| `.claude/skills/cafe24/brand-profile/` 🧪 | 클라이언트 통합 프로필 JSON (v2.4.0 실험적) |
| `.claude/skills/cafe24/workflows/` 🧪 | `/카페24-자동화` 워크플로우 (v2.4.0 실험적) |
| `.claude/skills/cafe24/module-browser.html` ✅ | **19개 모듈 시각 카탈로그** (v2.4.0 신규, 브라우저 더블클릭) |

> **처음이면** → [`00_시작하기/`](00_시작하기/) 의 README(순서표)부터 00~05 순서대로 읽으세요.

---

## 🆕 v2.4.0 신규 자료 (2026-06-21)

cafe24 skill 대폭 확장 — **45개 신규 + 6개 갱신**.

### ✅ 즉시 사용 권장 (검증·안정)
- **`references/troubleshooting.md`** — 비코더 막히는 5대 에러 + 해법 (21KB)
- **`references/variables.md`** — 6.4KB → 13.6KB 마스터 사전 (15개 섹션, 250+ 변수)
- **`references/modifiers.md`** — 13개 모디파이어 + Foreach·If 문법 확장
- **`module-browser.html`** — 브라우저로 열면 19개 모듈 그림으로 미리보기 (검색·다크모드)

> ⚠️ **v2.7.0 정리**: `recipes/`·`templates/`는 비-카페24 출처(APapeIsName)에서 가짜 변수가 유입돼 **제거**됨. 카페24 변수 단일 기준 = `references/variables.md`.

### 🧪 실험적 (실 클라이언트 작업 검증 후 안정화)
- `snippets/components/` — HTML 컴포넌트 (header·card·slider·footer·breadcrumb·quick-view)
- `snippets/css/` — 시스템 8개 (button·form·modal·toast 등)
- `snippets/js/` — Vanilla 모듈 6개 (scroll-anim·modal·tabs·form-validator 등)
- `design-tokens/` — Figma → JSON → CSS 토큰 파이프라인
- `brand-profile/` — 클라이언트별 통합 프로필 JSON 시스템
- `workflows/cafe24-automation.md` + `/카페24-자동화` 명령 — 6단계 원클릭 파이프라인
- `agents/qa-checker.md` + `skills/qa-loop/` — 비주얼 검증 자동 루프

**실험적 자료 주의:** 카페24 라이브 환경에서 충분히 검증되지 않았습니다. 사용 전 백업 + 소규모 테스트 권장. 안정 자료(✅)부터 도입하시고, 실험적 자료(🧪)는 검증 가능한 작업에서 차근차근 적용해보세요.

상세: [`CHANGELOG.md`](../CHANGELOG.md) v2.4.0 항목

---

## 검증

```bash
bash connect/scripts/verify-kit.sh
```

---

_배포본: 키트 루트에서 `/키트시작` · `CHANGELOG.md` 참고_
