# Page Agent Brief — {몰ID} / {페이지명}

> 메인 세션이 Task tool에 **아래 전체를 복사**해 하위 에이전트에 전달.

---

## 담당 범위

| 항목 | 값 |
|------|-----|
| 몰ID | {몰ID} |
| URL | {라이브 URL} |
| 소스 | `clients/{몰ID}/src/{경로}.html` |
| inc 포함 | {예: nk-header — 해당 시만} |
| queue § | `wave4-page-queue.md` §{N} |
| CSS writer | `src/_nk/css/nk-{type}.css` only |

## 정본 (읽기 순서)

1. `04_design/design.md`
2. `04_design/component-gallery.html`
3. `04_design/blank-slate-rebuild-queue.md` §BLANK-SLATE
4. `.claude/skills/cafe24-greenfield-skin/references/page-agent-orchestration.md` §2

## 공통 작업 규칙 (요약)

- **CSS overlay 금지** — module **안쪽** DOM을 NK 마크업으로 재구성
- **L1 KEEP**: module · {$vars} · anchorBoxId≥2 · form name/id/action · ez속성
- **L2 NEW**: nk-* 클래스 · component-gallery 패턴 · `var(--nk-*)`

## 진행 순서 (엄수)

1. **3단 비교표** (`templates/page-markup-compare.md`) — 사용자 승인 **전 코드 금지**
2. 섹션 → 모듈 → 유닛 순 재작성
3. **code-reviewer** — `module-contract-checklist.md` only
4. 결과 보고: 변경 파일 · `?v=` · PASS/FAIL

## 금지

- 다른 페이지/공유 CSS 파일 수정 (본 brief CSS writer 외)
- module 계약 훼손
- 추측 디자인 결정 (모호하면 메인→사용자 질문)

## 모듈 인벤토리 (이 페이지)

| # | module | 유닛 수 | anchorBoxId | 비고 |
|---|--------|:---:|---|---|
| 1 | | | | |
| 2 | | | | |

## 완료 보고 형식

```
페이지: {URL}
상태: PASS | FAIL
변경: {파일 목록}
module-contract: PASS | FAIL ({위반 요약})
라이브: https://{몰}.cafe24.com{path}?v={N}
남은 이슈: {있으면}
```
