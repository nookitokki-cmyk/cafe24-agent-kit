# 모바일 히어로 좌우 흰 여백 — RCA (ecudemo400786)

**날짜:** 2026-06-19  
**뷰포트:** 390×844 (메인 URL, `CAFE24.MOBILE_WEB=false`)  
**타겟:** https://ecudemo400786.cafe24.com/  
**레퍼런스:** https://ecudemo393674.cafe24.com/

---

## 증상

모바일 메인 히어로(`.main-sec1`) 좌우에 흰 여백(~16px씩). 이전 `ref393674-score-mobile-full.py` 감사는 100 PASS였으나, **swiper 존재·overflow 없음만 검사**하여 이 결함을 놓침.

---

## 근본 원인 (1차 — 확정)

### EZ skin16 `layout.css` 모바일 `#contents` 92% 폭 + specificity 패배

| 항목 | 값 |
|------|-----|
| **파일** | `layout/basic/css/layout.css` |
| **셀렉터** | `@media (max-width:1024px) { #container #contents { width: 92%; margin: 0 auto; } }` |
| **specificity** | ID 2개 = **(0, 2, 0) → 512** |

타겟은 skin16 구조로 히어로가 `#container > #contents > .main-sec1` 안에 있음.  
레퍼런스(393674)는 `#contents` 래퍼 없이 `#container > .main-sec1` — 구조 자체가 다름.

기존 오버라이드:

```css
body.layout.cc.ref393674-main #contents { padding: 0; margin: 0; }
```

- specificity **(0, 1, 3) → 305** — `#container #contents`에 **패배**
- `width` 미지정 → EZ 기본 **92%** 유지
- 결과: `#contents` x=15.6px, width=358.8px → 히어로도 동일 inset

### 왜 이전 감사가 PASS였나

`ref393674-score-mobile-full.py` R1 체크가 swiper 존재 + `scrollWidth ≤ clientWidth` 만 검사.  
히어로가 92% 폭으로 **안쪽에 맞게** 들어가 있어 overflow는 없었음 → **false PASS**.

---

## 실측 (Playwright 390×844)

### Before (수정 전)

| 요소 | x | width | 비고 |
|------|---|-------|------|
| `#container` | 0 | 390 | 정상 |
| `#contents` | **15.6** | **358.8** | width=92%, margin auto |
| `.main-sec1` | **15.6** | **358.8** | 부모 상속 |
| `.main-sec1 img` | **15.6** | **358.8** | gap 가시 |

### After (수정 후)

| 요소 | x | width | 비고 |
|------|---|-------|------|
| `#contents` | 0 | 390 | full bleed |
| `.main-sec1` | 0 | 390 | **PASS** (x≤2, w≥386) |

### 레퍼런스 (393674)

| 요소 | x | width | 비고 |
|------|---|-------|------|
| `.main-sec1` | 0 | 390 | `#contents` 없음 |

---

## 수정 내용

**파일:** `_ref393674/css/base.css`, `_ref393674/css/sub.css`

```css
body.ref393674-main #container #contents,
body.layout.cc.ref393674-main #container #contents {
  width: 100% !important;
  max-width: none !important;
  padding: 0 !important;
  margin: 0 !important;
}
```

- `#container` + `#contents` ID 2개 + body class → EZ media rule과 동급 이상 + `!important`로 번들 순서 무관 확정
- `#container.ref393674-container` (미사용 클래스) → `#container.a-container` 로 정리

**배포:** FTP `base` + `mobile` 각 `/_ref393674/css/base.css`, `sub.css` (2026-06-19)

---

## Cafe24 EZ가 이렇게 하는 이유

skin16은 태블릿/모바일에서 본문을 **가독성용 92% 컬럼**으로 중앙 정렬 (`width:92%; margin:0 auto`). PC용 max-width 1480px 패턴의 모바일 축소판. 커스텀 풀블리드 히어로·배너는 **반드시 `#container #contents` 수준에서 width 100% 오버라이드** 필요.

---

## 회귀 방지

- `ref393674-score-mobile-full.py` R1: `heroFullBleed` (x≤2, width≥viewport-4) 추가
- `agent-kit/docs/common-pitfalls.md` — 「히어로 좌우 흰 여백」 섹션
