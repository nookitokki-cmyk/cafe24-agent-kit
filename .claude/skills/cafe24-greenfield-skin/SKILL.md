---
name: cafe24-greenfield-skin
description: >
  카페24 SmartDesign HTML 스킨을 처음부터 빌드할 때의 오케스트레이션.
  Wave0 온보딩 → foundation → 페이지 Wave → Phase A–F 전수 감사(4-tier·ultraqa·visual).
  Use when: greenfield, 신규 몰, blank-slate, 처음부터 스킨, 전 페이지 재검토, wave4 audit.
disable-model-invocation: true
---

# Cafe24 Greenfield Skin (오케스트레이터)

> **이 스킬은 지식 백과가 아닙니다.** F1–F36·module 문법·6단계 YAML은 **링크만** — 본문 COPY 금지.

## Hard Gates (시작 전)

1. 워크스페이스 = `cafe24-kit-작업본` 루트 (`mcp/` 보임)
2. MCP `get_kit_guides` → `CAFE24-SMARTDESIGN-AGENT.md` 로드
3. `/접속세팅` 완료 전 SFTP 업로드 금지
4. HTML vs EZ 판별: `.claude/skills/cafe24/references/skin-method-detect.md`

## 완료 정의 (절대 혼동 금지)

- **grep·4-tier PASS ≠ 완료** — `nk-*` HTML + stock-only CSS 불일치는 parity + 라이브 스크린샷 필요
- **완료** = 라이브 PC1440 + MO390 스크린샷 + audit 파이프라인 PASS + 로그인 게이트 수동 확인

## 워크플로 DAG

```
Wave0  scaffold_client · design.md · SFTP sync · css/module 인벤토리
  → DS Adapt  사용자 DS+코드 Read → nk-tokens · 매핑표 (06-design-system-adaptation)
  → Foundation  tokens · reset · base · nk-components · component-gallery
  → Page Waves  blank-slate-rebuild-queue 순 (05-module-shell-rebuild · Layer1/2)
  → Phase A–F  references/08-full-audit-pipeline.md
  → Report  05_work-log.md · defects 0 · ?v=N URL
```

## 링크 허브 (SSOT)

| 주제 | 정본 |
|------|------|
| 6단계 빌드 | `agent-kit/01_작업하기/workflows/02-skin-build-standard.md` |
| Phase 채점 | `06-verify-loop.md` |
| 레퍼런스 인입 | `05-reference-intake.md` |
| **css/module · 모듈 껍데기** | `references/05-module-shell-rebuild.md` |
| **DS·코드 → 카페24** | `references/06-design-system-adaptation.md` |
| 함정 F번호 | `02_막혔을때/함정-INDEX.md` → `brain/docs/CAFE24-SMARTDESIGN-AGENT.md` §6 |
| 문법·모듈 | `.claude/skills/cafe24/SKILL.md` |
| blank-slate | `clients/{몰}/04_design/blank-slate-rebuild-queue.md` |
| 전수 감사 | `references/08-full-audit-pipeline.md` (이 스킬) |
| HTML↔CSS 정합 | `references/04-html-css-parity.md` |

## 클라이언트 산출물 (instances)

`clients/{몰ID}/04_design/` — `design.md` · `css-module-inventory.md` · `blank-slate-rebuild-queue.md` · `wave4-page-queue.md` · `rerun-audit-spec.md` · `shots/audit/`

`clients/{몰ID}/03_references/source/` — 사용자 제공 DS·HTML·CSS 원본

템플릿 복제: `templates/` — `blank-slate-rebuild-queue.md` · `wave4-page-queue.md` · `rerun-audit-spec.md`

## 스크립트 (실행 순서)

**SSOT**: `.claude/skills/cafe24-greenfield-skin/scripts/` — `README.md` 참조

```
scripts/
  run-audit.js              # 오케스트레이터
  stock-scan-tier.js        # 4-tier
  ultraqa-wave4-sweep.js    # 전역 sweep
  interaction/              # main · plp · pdp · auth · board
  config/batches.js         # URL 배치
  lib/resolve-config.js     # --mall-id · audit-overrides.json
```

```powershell
cd cafe24-kit-작업본
node .claude/skills/cafe24-greenfield-skin/scripts/run-audit.js --mall-id {몰ID}
node .claude/skills/cafe24-greenfield-skin/scripts/stock-scan-tier.js --mall-id {몰ID} --tier page --batch default
```

몰별 URL: `clients/{몰ID}/04_design/audit-overrides.json` (템플릿: `templates/audit-overrides.example.json`)

레거시 스냅샷: `clients/ecudemo402307/04_design/shots/wave4/_*.js` (검증본 보존)

## Human-Only Gates

- `cafe24_sftp_upload` 전 사용자 OK
- 로그인 URL: myshop/* · modify · board/product/write — sweep 제외, 수동 스크린샷
- visual-verdict / qa-checker — grep 통과 후에도 필수

## Anti-patterns (스킬 위반)

- wave4 grep PASS만 보고 완료 보고
- ecudemo402307 경로 하드코딩을 신규 몰에 복사
- F1–F36 본문을 SKILL에 중복 기록
- EZ 제거를 사용자 확인 없이

## Read Order (에이전트 진입)

1. This SKILL.md
2. `get_kit_guides`
3. `references/orchestration.md`
4. **`references/06-design-system-adaptation.md`** (사용자 DS·코드 있을 때)
5. **`references/05-module-shell-rebuild.md`** (HTML/CSS 구현 전)
6. `references/08-full-audit-pipeline.md`
7. `clients/{몰}/04_design/design.md` · `blank-slate-rebuild-queue.md`
