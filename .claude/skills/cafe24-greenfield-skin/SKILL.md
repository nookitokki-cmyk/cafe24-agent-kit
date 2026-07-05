---
name: cafe24-greenfield-skin
description: >
  카페24 SmartDesign HTML 스킨 greenfield 빌드·전페이지 blank-slate 재구성 오케스트레이션.
  메인 세션=지휘만 · 페이지당 하위 에이전트 1 · module 계약 보존 · design.md+component-gallery 기준.
  Use when: greenfield, blank-slate, 전 페이지 마크업 재구성, wave4, 페이지별 에이전트 배치.
disable-model-invocation: true
---

# Cafe24 Greenfield Skin (오케스트레이터)

> **역할**: 메인 세션은 **지휘·검수만**. 페이지 HTML 직접 작성 금지.  
> F1–F26·module 문법 SSOT는 링크 — 본문 COPY 금지.

## Hard Gates (시작 전)

1. 워크스페이스 = `cafe24-kit-작업본` 루트 (`mcp/` 보임)
2. MCP `get_kit_guides` → `CAFE24-SMARTDESIGN-AGENT.md` 로드
3. `/접속세팅` 완료 전 SFTP 업로드 금지
4. HTML vs EZ: `.claude/skills/cafe24/references/skin-method-detect.md`

## 에이전트 배치 (필수 순서)

```
① 페이지 목록 전수 나열 → 사용자 확인
② 페이지 1개 = 하위 에이전트 1 (Task tool) · 메인은 brief만 전달
③ 하위: 섹션 → 모듈 → 유닛 순 blank-slate 재구성
④ 전 페이지 완료 후 메인 통합 검수 (네이밍·토큰·컴포넌트 재사용)
```

상세: **`references/page-agent-orchestration.md`** (정본)

## 완료 정의 (절대 혼동 금지)

| 단계 | 조건 |
|------|------|
| 페이지 1개 | 3단 비교표 승인 → 코드 → **code-reviewer 모듈 계약 PASS** → 메인 보고 |
| 전체 | **모든 페이지** 위 조건 충족 + 메인 통합 검수 + 라이브 PC+MO — 그 전 **완료 보고 금지** |
| grep·4-tier PASS | 1차 통과일 뿐 — `references/04-html-css-parity.md` + visual 필수 |

## 디자인 참고 (아루나 등 외부 DS 사용 안 함)

| 정본 | 경로 |
|------|------|
| 토큰·무드 | `clients/{몰}/04_design/design.md` |
| 컴포넌트 패턴 | `clients/{몰}/04_design/component-gallery.html` |
| blank-slate 계약 | `clients/{몰}/04_design/blank-slate-rebuild-queue.md` §BLANK-SLATE |

## 클라이언트 산출물

`clients/{몰ID}/04_design/`

- `wave4-page-queue.md` — 페이지·모듈 인벤토리 (시작 시 사용자에게 요약 제시)
- `wave4-status.md` — 193 URL 전수
- `blank-slate-rebuild-queue.md` — 진행 상태
- `shots/audit/` · `shots/wave4/` — 스캔 리포트

템플릿: `templates/` in this skill folder.

## 하위 에이전트 brief 템플릿

`templates/page-agent-brief.md` — 메인이 **그대로 복사·치환**해 Task에 전달.

## 검증 파이프라인 (페이지 완료 후)

1. `code-reviewer` — module 계약 전용 (`references/module-contract-checklist.md`)
2. 4-tier / interaction — `clients/{몰}/04_design/shots/wave4/_stock-scan-tier.js` 등
3. parity — `references/04-html-css-parity.md`
4. UltraQA — `_ultraqa-wave4-sweep.js` (전 페이지 후 G8)

## 링크 허브

| 주제 | 정본 |
|------|------|
| 페이지 에이전트 배치 | `references/page-agent-orchestration.md` |
| 모듈 계약 체크리스트 | `references/module-contract-checklist.md` |
| Wave4 그룹 기술 오케스트레이션 | `references/wave4-group-orchestration.md` |
| HTML↔CSS parity | `references/04-html-css-parity.md` |
| 전수 감사 A–G | `references/08-full-audit-pipeline.md` |
| 6단계 빌드 | `agent-kit/01_작업하기/workflows/02-skin-build-standard.md` |
| 카페24 문법 | `.claude/skills/cafe24/SKILL.md` |

## Anti-patterns

- 메인 세션이 페이지 HTML/CSS 직접 작성
- 일부 페이지만 끝내고 "전체 완료" 보고
- 3단 비교표 승인 없이 코드 착수
- CSS overlay만 하고 module inner 미재구성 (blank-slate 위반)
- grep PASS = 완료 보고

## Read Order (에이전트 진입)

1. This SKILL.md
2. `references/page-agent-orchestration.md`
3. `clients/{몰}/04_design/design.md` + `wave4-page-queue.md`
4. `get_kit_guides` → AGENT.md
