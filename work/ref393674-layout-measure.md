# ref393674 레이아웃 실측 시트 (PC 1440px)

> Playwright `getComputedStyle` + `#container` bounding rect · 2026-06-19

## 페이지별 body / #container

| 페이지 | body class | body padding-top | body max-width | #container max-width | #container padding | #container width |
|---|---|---|---|---|---|---|
| **ref 메인** | `layout cc` | 0px | none | **100%** | **0** | 1440 |
| **ref PLP** | `layout` | 0px | none | **100%** | 50px 20px 100px | 1440 |
| **ref PDP** | `layout` | 0px | none | **100%** | 20px 20px 100px | 1440 |
| **ref About** | `layout` | 0px | none | **1200px** | 50px 20px 100px | 1200 |
| **ref Login** | `layout` | 0px | none | **1200px** | 50px 20px 100px | 1200 |
| **tgt PLP (수정 전)** | `layout ref393674-sub` | **50px** | **1480px** | **1200px** | 50px 20px 100px | 1240 |
| **tgt PLP (목표)** | `layout ref393674-sub-plp` | 0px | none | 100% | 50px 20px 100px | 1440 |

## 레퍼런스 CSS 근거 (optimizer_user PLP 번들)

```css
.layout .a-container { display:flex; flex-direction:column; max-width:100%; }
.a-container { max-width:1200px; padding:50px 20px 100px; margin:0 auto; }
```

- **상품 PLP/PDP**: `.layout .a-container`가 max-width만 100%로 올리고, padding은 `.a-container`의 50px 20px 100px 유지 → **풀폭 + 좌우 20px**
- **About/Login/게시판**: `.layout .a-container` 오버라이드 없음 → **1200px 중앙**

## 수정 지시 (격차표)

| # | 속성 | 레퍼런스 | 수정 전(tgt) | 지시 |
|---|---|---|---|---|
| L1 | body padding-top (서브) | 0px | 50px | 0px |
| L2 | body max-width | none | 1480px | none |
| L3 | PLP container max-width | 100% | 1200px | 100% |
| L4 | PLP container display | flex column | block | flex column |
| L5 | PDP container padding | 20px 20px 100px | 50px 20px 100px | 20px 20px 100px |
| L6 | About container max-width | 1200px | 1200px | 유지 |
