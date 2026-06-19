# 규칙 — EZ skin16 `#contents` 92% 폭 (필수)

> **MANDATORY:** full-bleed 섹션(히어로·배너·풀폭 그리드)을 만들 때 `#contents`에 **`margin`만** 건드리면 **절대 안 된다**.  
> EZ `layout.css`의 **`width:92%`** 를 반드시 **`#container #contents`** 로 덮어써야 한다.

---

## 왜 margin-only가 실패하는가

EZ skin16 `layout.css`:

```css
@media (max-width: 1024px) {
  #container #contents {
    width: 92%;
    margin: 0 auto;
  }
}
```

| 셀렉터 | ID 수 | 대략 specificity | `width` | `margin` |
|--------|-------|------------------|---------|----------|
| `#container #contents` (EZ) | **2** | **512** | 92% | 0 auto |
| `body.layout #contents { margin:0 }` | 1 | **305** | *(EZ 승)* | 0 |
| `body.ref393674-main #container #contents` | **2** | **≥512** + class | **100%** | **0** |

- **`margin`과 `width`는 별도 속성** — margin 오버라이드가 width를 바꾸지 않는다.
- specificity가 낮으면 EZ가 **`width:92%`를 그대로 유지** → 좌우 ~4% 흰 gap.
- 자식(`.main-sec1`, `.swiper`)에만 `width:100vw`를 걸어도 **부모 `#contents`가 359px**이면 gap은 남는다.

---

## MUST / NEVER

| ✅ MUST | ❌ NEVER |
|---------|----------|
| `#container #contents` (ID **2개**) + `width:100% !important` | `#contents` 단독 셀렉터로 width 해제 시도 |
| 메인·서브 **페이지 타입별** 블록을 override CSS **첫 섹션**에 배치 | 히어로/배너 자식에만 full-bleed CSS |
| DevTools 390px: `#contents` computed width = viewport | `margin:0`만 추가하고 “풀폭 완료”로 간주 |
| `docs/snippets/ez-contents-override.css` 복사 후 타입 class 맞춤 | 튜토리얼의 `body #contents { margin:0 }` 그대로 복사 |

---

## copy-paste — 메인 (`ref393674-main`)

`base.css` 또는 override 레이어 **최상단**에 넣는다:

```css
/* EZ layout.css @media #container #contents { width:92% } — spec 512, margin-only override 불가 */
body.layout.cc.ref393674-main #container #contents,
body.ref393674-main #container #contents {
  width: 100% !important;
  max-width: none !important;
  padding: 0 !important;
  margin: 0 !important;
}
```

---

## copy-paste — 서브 (PLP / PDP / narrow)

`sub.css` 타입별 — **`#container #contents`** 필수 (기존 `#contents` 단독 규칙은 MO에서 EZ에 진다):

```css
/* PLP · 풀폭 */
body.layout.ref393674-sub-plp #container #contents {
  width: 100% !important;
  max-width: none !important;
  margin: 0 !important;
  padding: 0 !important;
}

/* PDP · 풀폭 */
body.layout.ref393674-sub-pdp #container #contents {
  width: 100% !important;
  max-width: none !important;
  margin: 0 !important;
  padding: 0 !important;
}

/* narrow (About/Login/장바구니/게시판) — container 1200px, contents는 container 안 100% */
body.layout.ref393674-sub-narrow #container #contents {
  width: 100% !important;
  max-width: none !important;
  margin: 0 !important;
  padding: 0 !important;
}
```

container padding은 타입별 `#container.a-container` 규칙 유지 (`sub.css` 참고).

---

## DevTools 검증 (390px)

1. viewport **390×844**, 메인 URL (`/m/` 아님).
2. Elements → `#contents` → Computed → **width**.
3. **PASS:** width ≈ **390** (±2px). **FAIL:** ~**359** (92% of ~390).

서브 PLP URL에서도 동일. `ref393674-score-mobile-full.py` check **C1**이 자동 검사한다.

**verify-loop PASS:** `#contents` 폭 포함 **모든** score 스크립트는 **`total_score = 100` only** — 100 미만이면 Phase 미완료.

---

## 관련

- 스니펫: [`docs/snippets/ez-contents-override.css`](../docs/snippets/ez-contents-override.css)
- 함정: [`docs/common-pitfalls.md`](../docs/common-pitfalls.md) §EZ #contents 92% trap
- verify: [`workflows/06-verify-loop.md`](../workflows/06-verify-loop.md) Phase 0 pre-flight
- skin-build: [`workflows/02-skin-build-standard.md`](../workflows/02-skin-build-standard.md) ③ Setup
