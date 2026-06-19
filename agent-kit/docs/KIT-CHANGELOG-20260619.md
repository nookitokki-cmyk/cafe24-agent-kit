# 키트 변경 이력 — 2026-06-19

## 10차 — 포지셔닝 (긍정 정의만) (2026-06-19)

| 경로 | 변경 |
|------|------|
| `이-키트는-누구-용인가.md` | NOT FOR·부정 변명 제거 — FOR + HOW TO USE 만 |
| `README.md` · `getting-started/README.md` · `키트-시작-가이드.md` | 「수강생 전용 아님」 등 부정 문구 제거 — Cafe24+AI **작업자** 긍정 정의 |
| `examples/01~03_*.md` | blockquote 부정 괄호 제거 |
| `.claude/agents/카페24-도우미.md` | 온보딩 멘트 긍정 정의만 |

---

## 9차 — 포지셔닝 중립화 (작업자 우선) (2026-06-19)

| 경로 | 변경 |
|------|------|
| **`이-키트는-누구-용인가.md`** | **NEW** — FOR / NOT FOR / HOW TO USE · 「수강생 전용 아님」 명시 |
| `README.md` · `getting-started/README.md` · `00-아무것도-모를-때.md` | 상단 포지셔닝 — Cafe24+AI **작업자** · 강의 전용 아님 |
| `getting-started/예시-데모몰.md` | **NEW** — Ref/Tgt URL **선택 연습용** (키트 필수 아님) |
| `getting-started/키트-시작-가이드.md` | 데모 URL → `예시-데모몰.md` 로 분리 |
| `getting-started/시안-제출-체크리스트.md` | 클라이언트·작업 의뢰 · 협업자·에이전트 용어 |
| `docs/F-상황-인덱스.md` | 수강생 → 작업자·에이전트 공용 허브 |
| `workflows/README.md` · `05-reference-intake.md` · `03-reference-renewal.md` | W5·수강생 → 레퍼런스/시안 1:1 · 작업자 |
| `.claude/commands/레퍼런스인입.md` · `.claude/agents/카페24-도우미.md` | 수강생·W3 차시 → 작업자·키트 문서 |
| `docs/MCP-OAUTH-GUIDE.md` | 파트너센터 진입 — 강의 프레이밍 제거 |

---

## 8차 — examples 강의 프레이밍 제거 (2026-06-19)

| 경로 | 변경 |
|------|------|
| `examples/01~03_*.md` | W2~W7·강의 영상·수업 전용 문구 → 범용 시나리오 중립 표현 · 상단 범용 안내 blockquote 추가 |

---

## 7차 — getting-started 대상 중립화 (2026-06-19)

| 경로 | 변경 |
|------|------|
| `getting-started/수강생-QnA-쉬운말로.md` | **→** `QnA-쉬운말로.md` — 제목·체크리스트·§10 수업 프레이밍 제거 |
| `getting-started/수강생-실측-격차-설명가이드.md` | **→** `실측-격차-설명가이드.md` — §3 강사용 멘트 → 설명할 때 쓸 말 (선택) |
| `getting-started/README.md` · `README.md` · `키트-시작-가이드.md` · `프롬프트-템플릿.md` · `OMC-명령어-매칭가이드.md` · `docs/F-상황-인덱스.md` | 파일명·링크 갱신 · §11 시안만 · W5 특강 → 레퍼런스 1:1 |

---

## 6차 — 시작 가이드 재작성 (2026-06-19)

| 경로 | 변경 |
|------|------|
| `getting-started/키트-시작-가이드.md` | **NEW** — 배포본 첫 열기용 (워크플로·F27~34·문서 맵·OMC 콤보). 강의/수업 프레이밍 제거 |
| `getting-started/강의-키트-소개-가이드.md` | **삭제** → `키트-시작-가이드.md` 로 대체 |
| `getting-started/README.md` · `README.md` · `프롬프트-템플릿.md` | 새 가이드 링크 반영 |

---

## 배경

**ecudemo393674 → ecudemo400786** 레퍼런스 갱신 프로젝트가 agent-kit 개선을 두 차례 유발했다.

| 파 | 시각(대략) | 내용 |
|----|-----------|------|
| **1차** | ~07:22 | 레퍼런스·시안 인입 워크플로, 명령·체크리스트 정비 |
| **2차** | ~13:26 (Phase 4+) | 90pt verify-loop, narrow postmortem, 관리자 검증 규칙, 로드맵 |
| **3차** | ~19:00 | 반응형 MO 단일 스킨 규칙, mobile 스킨 postmortem (ecudemo400786) |
| **4차** | ~20:00 | 관리자 「모바일 전용 디자인 사용안함」 필수 안내 — 인입·verify pre-flight |
| **5차** | ~21:00 | EZ `#contents` 92% trap — mandatory rule, snippet, score C1, verify Phase 0 |

---

## 5차 — EZ `#contents` 92% width trap (2026-06-19)

**배경:** MO full-bleed 실패가 반복 — `margin:0`만 적용, EZ `#container #contents { width:92% }` (spec 512) 미해제.

| 경로 | 변경 |
|------|------|
| `rules/ez-contents-width.md` | **NEW** — mandatory `#container #contents` override, specificity 표, copy-paste |
| `docs/snippets/ez-contents-override.css` | **NEW** — 메인·PLP·PDP·narrow paste-ready |
| `docs/common-pitfalls.md` | §EZ #contents 92% trap — 체크리스트·hero postmortem 일반화 |
| `workflows/06-verify-loop.md` | Phase 0 pre-flight — `#contents` width @390 on `/` + PLP |
| `workflows/02-skin-build-standard.md` | ③ Setup — override 첫 블록 `#container #contents` 필수 |
| `README.md` | `rules/ez-contents-width.md` · snippet 링크 |
| `work/scripts/ref393674-score-mobile-full.py` | check **C1** — `/` + PLP `#contents` width ≥ viewport−4 |

---

## 4차 — 관리자 mobile OFF 필수 (2026-06-19)

**배경:** 반응형 단일 base 스킨은 관리자 「모바일 전용 디자인 사용설정」= **사용안함** + `CAFE24.MOBILE_WEB=false` 가 전제. MCP·FTP로 변경 불가.

| 경로 | 변경 |
|------|------|
| `rules/responsive-mobile.md` | §필수: 관리자 설정 — 전체 메뉴 경로·검증·에이전트 의무 |
| `docs/common-pitfalls.md` | §모바일 예방 — 작업 전·배포 후 사용자 확인 체크 |
| `workflows/06-verify-loop.md` | Phase 0.5 pre-flight — MO 검증 전 admin OFF |
| `workflows/05-reference-intake.md` | PC+MO 인입 체크리스트 — admin OFF |
| `.claude/commands/레퍼런스인입.md` | Q4 직후·승인 후 관리자 경로 붙여넣기 의무 |
| `getting-started/시안-제출-체크리스트.md` | 강사 선택 체크 — mobile OFF 확인됨 |
| `README.md` | `rules/responsive-mobile.md` 링크 |

---

## 신규 파일 (NEW)

| 경로 | 용도 |
|------|------|
| `workflows/06-verify-loop.md` | Phase별 score 스크립트 90점 PASS 자기검증 루프 |
| `workflows/05-reference-intake.md` | 레퍼런스·시안 인입 게이트 (코드 전 합의) **(1차)** |
| `docs/common-pitfalls.md` | narrow 레이아웃 오적용 postmortem (ecudemo400786) |
| `docs/kit-roadmap.md` | score 스크립트·추가 문서 로드맵 |
| `rules/cafe24-admin-verify.md` | 관리자·개발자센터 안내 전 웹 검증 규칙 |
| `.claude/commands/레퍼런스인입.md` | `/레퍼런스인입` 슬래시 대본 **(1차 신규, 이후 수정)** |
| `getting-started/시안-제출-체크리스트.md` | 시안 제출 전 필수 항목 체크리스트 **(1차)** |
| `rules/responsive-mobile.md` | MO = base `@media` 단일 템플릿 필수 규칙 **(3차)** |
| `rules/ez-contents-width.md` | EZ MO `#contents` 92% — `#container #contents` 필수 **(5차)** |
| `docs/snippets/ez-contents-override.css` | paste-ready width override **(5차)** |

---

## 수정 파일 (MODIFIED)

| 경로 | 변경 요약 |
|------|-----------|
| `workflows/03-reference-renewal.md` | 05·06 워크플로 연계, Phase 순서·verify-loop 참조 |
| `workflows/README.md` | 05·06 워크플로 목록 추가 |
| `.claude/commands/레퍼런스인입.md` | Q5 이스케이프(dual-source 실측), 2차 보강 |
| `.claude/commands/디자인수정.md` | 인입 완료·verify-loop 선행 조건 반영 |
| `getting-started/시안-제출-체크리스트.md` | Q5 이스케이프·인입 연동 **(1차 이후 수정)** |
| `docs/common-pitfalls.md` | §모바일 별도 스킨 postmortem **(3차)** |
| `workflows/06-verify-loop.md` | 반응형 MO — 메인 URL 390px **(3차)** · Phase 0.5 admin pre-flight **(4차)** |
| `rules/responsive-mobile.md` | §필수: 관리자 설정 **(4차)** |
| `workflows/02-skin-build-standard.md` | ④ 생성: base `@media` only **(3차)** · ③ `#container #contents` **(5차)** |
| `workflows/06-verify-loop.md` | Phase 0 `#contents` pre-flight **(5차)** |
| `docs/common-pitfalls.md` | §EZ #contents 92% trap **(5차)** |
| `.claude/commands/레퍼런스인입.md` | Q4 동일 템플릿 + `@media` **(3차)** |
| `README.md`, `commands/COMMANDS.md` 등 | `/레퍼런스인입`·워크플로 05·06 반영 **(1차)** |

---

## 핵심 추가 요약

- **90pt verify-loop** — 페이지 타입별 `ref393674-score-*.py` 채점, 90 미만 FAIL 항목만 수정 반복
- **narrow 레이아웃 postmortem** — PLP/PDP에 1200px 적용 치명 오류 사례·근본 원인 4가지
- **Q5 이스케이프** — 수치 미제공 시 레퍼런스 `getComputedStyle` + 스크린샷 dual-source 실측 허용
- **cafe24 admin web verify** — 관리자 메뉴·개발자센터 경로 안내 전 공식 URL fetch 필수
- **kit roadmap** — work/ 검증 스크립트를 키트로 흡수할 항목·우선순위 정리
- **반응형 MO 단일 스킨 (3차)** — mobile 별도 FTP 경로 금지, `@media` on base, 390px 메인 URL 검증, ecudemo400786 mobile postmortem
- **관리자 mobile OFF 필수 (4차)** — 에이전트가 사용자에게 관리자 경로 안내·`CAFE24.MOBILE_WEB=false` 확인 요청; verify-loop Phase 0.5 pre-flight
- **EZ #contents 92% trap (5차)** — `#container #contents` width override 규칙·스니펫·verify Phase 0·score C1

---

## 권장 읽기 순서 (6)

1. [`workflows/05-reference-intake.md`](../workflows/05-reference-intake.md) — 인입 게이트
2. [`getting-started/시안-제출-체크리스트.md`](../getting-started/시안-제출-체크리스트.md) — 시안 제출 전
3. [`workflows/06-verify-loop.md`](../workflows/06-verify-loop.md) — 구현·검증 루프
4. [`docs/common-pitfalls.md`](common-pitfalls.md) — 레이아웃 함정
5. [`rules/ez-contents-width.md`](../rules/ez-contents-width.md) — **MO full-bleed 필수** **(5차)**
6. [`rules/cafe24-admin-verify.md`](../rules/cafe24-admin-verify.md) — 공식 경로 안내 규칙
7. [`rules/responsive-mobile.md`](../rules/responsive-mobile.md) — MO 단일 base 스킨 **(3차)**

---

## 런타임 검증 도구 (agent-kit 외, 페어링)

키트 문서와 함께 쓰는 채점 스크립트는 `cafe24-agent-workspace/work/scripts/` 에 있다 (키트에 미포함).

| 스크립트 | 대상 |
|----------|------|
| [`work/scripts/ref393674-score-plp.py`](../../work/scripts/ref393674-score-plp.py) | PLP |
| [`work/scripts/ref393674-score-pdp.py`](../../work/scripts/ref393674-score-pdp.py) | PDP |
| [`work/scripts/ref393674-score-basket.py`](../../work/scripts/ref393674-score-basket.py) | 장바구니 |
| [`work/scripts/ref393674-score-member.py`](../../work/scripts/ref393674-score-member.py) | 로그인·회원 |
| [`work/scripts/ref393674-score-board.py`](../../work/scripts/ref393674-score-board.py) | 게시판 |
| [`work/scripts/ref393674-score-header.py`](../../work/scripts/ref393674-score-header.py) | 헤더 |
| [`work/scripts/ref393674-score-page.py`](../../work/scripts/ref393674-score-page.py) | 정적·기타 |

상세: [`docs/kit-roadmap.md`](kit-roadmap.md) § work/ 검증 스크립트.
