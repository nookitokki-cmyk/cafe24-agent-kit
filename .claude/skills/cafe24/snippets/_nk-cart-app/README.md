# _nk-cart-app — 카트 JS 재구축 세트

> **[프로토타입 · 검증됨 2026-07-06]** 카페24 장바구니를 표 안 뜯고 **완전 커스텀**하는 방법.
> 자세한 원리·안전규칙: [`../../references/cart-js-rebuild.md`](../../references/cart-js-rebuild.md)

## 언제 쓰나
- 장바구니·주문서처럼 **표(`<table>`)를 뜯으면 주문이 깨지는** 거래 페이지를,
- CSS 덧칠 수준이 아니라 **디자인을 100% 새로** 하고 싶을 때.

## 파일
| 파일 | 역할 |
|---|---|
| `basket-app-skeleton.html` | `order/basket.html` 대체 골격. `#nk-src`에 원본 카트를 숨겨 넣고 `#nk-cart-app`은 JS가 채움 |
| `nk-cart-app.js` | 엔진 — 숨긴 원본에서 데이터 읽어 커스텀 UI 렌더 + 버튼 배선 연결 |
| `nk-cart-app.css` | 커스텀 카트 브랜드 스타일 (색은 `:root`/`--` 토큰으로 교체) |

## 3줄 적용
1. `basket-app-skeleton.html`의 `#nk-src`에 이 몰 **원본 `basket.html` 본문**을 붙여넣기 → `order/basket.html`로 저장
2. `nk-cart-app.js` → `_nk/js/`, `nk-cart-app.css` → `_nk/css/` 업로드
3. **연습 스킨에서** 상품 담아 렌더·수량·삭제·주문 라우팅 검증 → 통과 시 반영

## ⚠️ 하드닝 필요 (아직 프로토타입)
검증됨: 단순 상품 렌더 + 전체상품주문 라우팅.
미검증: 옵션 상품 · 품절 · 배송그룹 여러 개 · 수량 동기화 정밀도 → 실무 적용 전 해당 케이스 실증.

## ★ 안 까먹을 안전규칙
- `#nk-src`는 **`left:-99999px`(화면 밖)로만** 숨긴다. `visibility:hidden`/`display:none` 쓰면 **버튼 클릭이 안 먹혀 주문이 안 됨**.
- 주문 링크는 `a[link-order]` 첫 번째가 아니라 **"전체상품주문" 텍스트로** 골라야 함(스토어픽업 링크 오선택 주의).
