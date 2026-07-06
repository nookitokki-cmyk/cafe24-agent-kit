# HTML ↔ CSS 정합 (parity)

> grep·4-tier가 **못 잡는** 가장 흔한 Wave4 잔존 버그.

## 검사 방법

1. 페이지 HTML에서 `nk-*` 클래스 목록 추출
2. 해당 페이지 `@css` 로드 파일에서 셀렉터 grep
3. HTML 클래스에 대응하는 NK 셀렉터 없고 stock만 있으면 **FAIL**

## 병행 셀렉터 패턴

```css
/* BAD — HTML이 nk-tabs 인데 stock만 */
body.nk-skin .nk-order-page .ec-base-tab .menu { ... }

/* GOOD */
body.nk-skin .nk-etc-guide .nk-tabs__panel > ul.menu,
body.nk-skin .nk-etc-guide .ec-base-tab .menu { display: none; }
```

## 도메인별 체크리스트

| 도메인 | HTML 흔적 | CSS 파일 | 병행 대상 |
|--------|-----------|----------|-----------|
| base/footer | `nk-ft__social-link` `ph-*` | nk-base.css · nk-cafe24-reset.css | `#footer a:hover` 전역 |
| board | `nk-tabsle` `nk-panel` `nk-actions` | nk-board.css §10 | ec-base-table/box/button |
| myshop | `nk-tabs` `nk-myshop__table` | nk-myshop.css §0-4a | ec-base-tab/button |
| order | `nk-empty` `nk-qty` | nk-order.css | ec-base-box, qty DOM 순서 |
| member | `nk-mbr-*` | nk-member.css | ec-base-box 5px |
| etc | `nk-etc-guide` `nk-tabs__panel` | nk-etc.css | ec-base-tab `.menu` |
| tokens | `nk-*__head` page title | nk-tokens.css + 도메인 CSS | 페이지별 하드코딩 ls |

## 완료 ≠ grep PASS

parity grep 통과 후에도 **라이브 computed style** 확인 필수 (stock 인라인·늦은 번들).

---

## 실전 패턴 (ecudemo402307 Wave4 잔존 — grep이 놓침)

### 1) Reset 전역 셀렉터가 NK 컴포넌트를 덮음

**증상**: 푸터 소셜 아이콘 hover 시 배경은 코랄인데 아이콘 색이 안 바뀜·안 보임.

**원인**: `nk-cafe24-reset.css` `#footer a:hover { color: var(--nk-point) }` 가 `.nk-ft__social-link`까지 적용. Phosphor 글리프는 `i::before`라 `color: inherit`만으로는 부족.

```css
/* reset — 예외 분기 */
body.nk-skin #footer a:hover:not(.nk-ft__social-link) {
  color: var(--nk-point);
}

/* base — hover 시 글리프까지 명시 */
body.nk-skin #footer.nk-ft .nk-ft__social-link:hover i::before {
  color: var(--nk-on-point);
}
```

**검증**: 라이브 hover → DevTools computed `color` on `i::before` · PC+MO 스크린샷.

### 2) 페이지 타이틀 자간 — 토큰 1곳, 도메인 CSS N곳

**증상**: myshop/member/board 타이틀 자간이 페이지마다 제각각.

**처방**: `nk-tokens.css`에 단일 토큰 → 각 `.nk-*__head` 타이틀에 `letter-spacing: var(--nk-ls-page-title)`.

```css
/* nk-tokens.css */
--nk-ls-page-title: -1px;

/* nk-member.css · nk-myshop.css · nk-order.css · nk-board.css · nk-etc.css · nk-components.css */
letter-spacing: var(--nk-ls-page-title);
```

**검증**: grep `letter-spacing` 하드코딩 0 · Marcellus 타이틀 라이브 3페이지 이상 샘플.

### 3) HTML은 NK 탭인데 패널 안 stock 메뉴가 그대로 노출

**증상**: `guide.html` — 상단 `nk-tabs__nav`와 패널 내부 `ul.menu` 이중 탭.

```css
body.nk-skin .nk-etc-guide .nk-tabs__panel > ul.menu,
body.nk-skin .nk-etc-guide .ec-base-tab .menu {
  display: none;
}
```

**주의**: `module` 구조·앵커 `href`는 **삭제 금지** — 시각만 숨김.

### 4) NK 래퍼 + stock 자식 이중 border

**증상**: 빈 장바구니 카드에 border가 두 겹.

**원인**: `.nk-empty`에 border + 내부 `p`에 stock border.

```css
body.nk-skin .nk-order-page .xans-order-empty p,
body.nk-skin .nk-order-page .nk-empty .nk-empty__desc {
  border: 0;
  padding: 0;
}
```

### 5) 수량 스테퍼 — DOM 순서 ≠ 시각 순서

**증상**: 장바구니 `+`/`-` 버튼 위치 뒤바뀜.

**원인**: 카페24 `{$form.quantity}` 출력 순서가 `input → up → down`. PDP형 `down | input | up`은 **flex `order`** 또는 DOM 재배치 없이 `a.up`/`a.down` order 지정.

```css
body.nk-skin .nk-cart-product .orderListArea .nk-qty a.down { order: 1; }
body.nk-skin .nk-cart-product .orderListArea .nk-qty a.up   { order: 3; }
/* input은 order:2 (flex 컨테이너 .nk-qty) */
```

**검증**: filled cart 라이브에서 qty click-test · MO390 터치 영역.

---

## Parity grep 스크립트 보완 (수동)

자동 tier가 PASS여도 아래는 **수동 sweep** 권장:

| grep 대상 | 기대 |
|-----------|------|
| `#footer a:hover` (reset) | `:not(.nk-ft__social-link)` 포함 |
| `letter-spacing:` (도메인 CSS) | `var(--nk-ls-page-title)` 또는 없음 |
| HTML `nk-ft__social` | `nk-base.css`에 hover `i::before` |
| HTML `nk-etc-guide` | `ul.menu` hide 셀렉터 존재 |
| HTML `nk-qty` | `order` 또는 PDP 동일 패턴 |
