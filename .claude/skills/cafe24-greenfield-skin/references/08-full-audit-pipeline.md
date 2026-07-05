# Phase A–F — 전 페이지·전 CSS 전수 감사 파이프라인

> ecudemo402307 `rerun-audit-spec.md` + `wave4-checklist.md` 일반화.  
> **grep·stock-scan PASS였어도 실사용 URL에서 FAIL 반복** — 이 파이프라인이 필수.

## 0. 황금 규칙

```
자동 스캔 PASS = 1차 통과일 뿐.
완료 = A→F 전부 + visual + 로그인 수동.
```

## 1. 파이프라인 순서

| 단계 | 이름 | 도구/문서 | PASS 조건 |
|------|------|-----------|-----------|
| A | CSS grep preflight | `_ultraqa-wave4-sweep.js` grep 섹션 / `diagnose-overrides.js` | italic 0 · `#008bcc` 0 · hex 하드코딩 0 |
| B | HTML↔CSS parity | `04-html-css-parity.md` · 수동+grep | `nk-*` HTML에 stock-only CSS 없음 |
| C | 4-tier live scan | `_stock-scan-tier.js` module→submodule→section→page | violations=0 |
| D | Interaction/state | `_main/_plp/_pdp/_auth/_board-interaction-scan.js` | click-test · 열림 상태 |
| E | UltraQA global sweep | `_ultraqa-wave4-sweep.js` | 22+ URL PC+MO overflow 0 · `{$` 0 |
| F | Visual-verdict | qa-checker · agy/codex 교차 | 핵심 10 URL 90+ |
| G | Login-gate manual | `rerun-audit-spec` §로그인 필요 URL | 스크린샷 + 사용자 확인 |

재진입: 단계 N FAIL → N부터 반복 (이전 단계 스킵 금지).

## 2. HTML↔CSS parity (자주 놓침)

| HTML | CSS만 타깃 시 | 증상 |
|------|---------------|------|
| `nk-tabsle` | `.ec-base-table` | stock 5px border |
| `nk-panel` | `.ec-base-box` | 회색 박스 |
| `nk-actions` | `.ec-base-button` | float·회색 CTA |
| `nk-tabs__panel > ul.menu` | `.ec-base-tab .menu` | stock 탭 메뉴 노출 |
| `nk-empty` 내부 `p` | 컨테이너+`p` 둘 다 border | 이중 박스 |

처방: **CSS 병행 셀렉터** (`body.nk-skin .nk-board .nk-tabsle, body.nk-skin .nk-board .ec-base-table`).

## 3. 페이지 큐 (타입 순차)

한 타입 **끝까지** PASS 후 다음 타입 (`wave4-checklist.md`):

메인 → PLP → PDP → cart/order → member → myshop → board → etc → popup

각 행 상태: **PASS | FAIL | 미검증 | 수용** 만 허용.

## 4. blank-slate vs overlay

- **Layer 1 KEEP**: `module=""` · `{$vars}` · anchorBoxId≥2 · 설정 주석
- **Layer 2 NEW**: inner DOM `nk-*` · 타입별 `nk-{type}.css`

overlay만 할 때도 parity 규칙은 동일.

## 5. 로그인 필요 URL (sweep 제외)

- `/myshop/*` 대부분
- `/member/modify.html`
- `/board/product/write.html` (로그인+파라미터)

→ 브라우저 수동 스크린샷 목록에 문서화.

## 6. 배포·캐시

- FTP `cafe24_sftp_upload` · 사용자 OK
- 확인: `?v=N` · optimizer 2~5분
- PC + MO 동일 URL ( `/m/` 별도 스킨 금지 — `@media` )

## 7. run-audit (로컬)

```powershell
cd cafe24-kit-작업본
node .claude/skills/cafe24-greenfield-skin/scripts/run-audit.js --mall-id {몰}
node .claude/skills/cafe24-greenfield-skin/scripts/stock-scan-tier.js --mall-id {몰} --tier page --batch default
node .claude/skills/cafe24-greenfield-skin/scripts/ultraqa-wave4-sweep.js --mall-id {몰}
```

몰별 URL: `clients/{몰}/04_design/audit-overrides.json` · 상세: `scripts/README.md`

## 8. 완료 체크리스트

- [ ] `wave4-page-queue.md` 해당 타입 전행 PASS
- [ ] ultraqa defects 0 (로그인 제외 문서화)
- [ ] visual-verdict 핵심 URL
- [ ] `05_work-log.md` 갱신
- [ ] 남은 defects → `wave4-defects.md`
