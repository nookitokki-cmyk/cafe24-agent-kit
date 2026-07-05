# HTML ↔ CSS 정합 (parity)

> grep·4-tier PASS여도 **라이브 computed style**로 재확인.

## 검사

1. HTML `nk-*` 클래스 추출
2. 해당 `@css` 파일에서 셀렉터 grep
3. stock-only 셀렉터만 있으면 **FAIL** → 병행 셀렉터 추가

## 자주 놓치는 패턴

| 증상 | 처방 |
|------|------|
| `#footer a:hover`가 소셜 아이콘 덮음 | `:not(.nk-ft__social-link)` + Phosphor `i::before` |
| 타이틀 자간 불일치 | `--nk-ls-page-title` 토큰 통일 |
| NK 탭 + 패널 내 `ul.menu` 이중 | `.nk-tabs__panel > ul.menu { display:none }` |
| `.nk-empty` + `p` 이중 border | 내부 `p { border:0 }` |
| qty DOM `input→up→down` | flex `order` 보정 |

**완료 ≠ grep PASS**
