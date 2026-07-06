# {몰ID} — 전체 페이지 재검토 합격 기준

> 정본: `04_design/design.md` · 큐: `wave4-page-queue.md`

## 1. 문제 정의

(자동 스캔 PASS 후에도 발견된 패턴 기록)

| 패턴 | HTML | CSS 타깃 | 증상 |
|------|------|----------|------|
| reset leak | `.nk-ft__social-link` | `#footer a:hover` reset | 소셜 hover 아이콘 미노출 |
| token drift | `.nk-*__head` title | `--nk-ls-page-title` | 타이틀 자간 페이지별 불일치 |
| stock menu dup | `.nk-etc-guide` panel | `ul.menu` hide | guide 이중 탭 |
| double border | `.nk-empty` + `p` | nk-order.css §4 | 빈 장바구니 border 2겹 |
| qty DOM order | `.nk-qty` | flex order up/down | +/- 버튼 위치 뒤바뀜 |

## 2. 합격 기준

### A. 전역
- [ ] `body.nk-skin` · `var(--nk-bg)`
- [ ] stock 파랑 0 · `{$` 노출 0 · overflow 0

### B. 페이지 유형별
(타입별 필수 체크)

## 3. 검증 파이프라인

① grep ② ultraqa ③ visual ④ login manual ⑤ parity

## 4. 로그인 필요 URL

-

## 5. 완료 정의

-
