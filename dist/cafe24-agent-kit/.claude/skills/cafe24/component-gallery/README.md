# Component Gallery 시스템 (준비물 ②)

> 디자인 토큰(값)만으로는 부족합니다. 그 값으로 **조립한 완성 부품**을 한 페이지에 진열한 것이 컴포넌트 갤러리입니다.
> 비코더는 "이 갤러리의 `nk-btn--primary`, `nk-card`를 그대로 써"라고만 지시하면 됩니다.

---

## 왜 필요한가요?

### 기존 워크플로우의 문제
- 색·폰트 토큰만 AI에게 주면 → 버튼·카드·폼의 **모양을 매번 새로 지어냄**
- 그래서 페이지마다 버튼 모서리·간격·hover가 미묘하게 달라짐 → 몰 전체가 들쭉날쭉
- "저번 페이지 버튼이랑 왜 달라요?" 피드백 왕복 반복
- 새 페이지 만들 때마다 "우리 버튼이 어떻게 생겼더라"를 말로 다시 설명

### 컴포넌트 갤러리의 해결
- `nk-tokens.css`(값) + `nk-components.css`(부품)를 불러와 **완성된 부품을 실물로 진열**
- AI에게 "이 갤러리에 있는 `.nk-btn--primary`를 그대로 붙여"라고 지시 → 전 페이지 동일
- 새 컴포넌트가 필요하면 갤러리에 먼저 추가 → 이후 모든 페이지가 같은 부품 재사용
- 클라이언트에게도 "완성 부품 목록"을 한 장으로 보여줄 수 있음(승인용)

---

## 준비물 3종 세트 안에서의 위치

| 준비물 | 정체 | 비유 | 파일 |
|---|---|---|---|
| ① 디자인 토큰 | 색·폰트·간격의 **값** | 물감·재료 | `design-tokens/` · `nk-tokens.css` |
| ② **컴포넌트 갤러리** | 조립된 **완성 부품** | 조립된 가구 | **`component-gallery/` · `nk-components.css`** |
| ③ 브랜드 프로필 | 클라이언트별 정보 | 주문서 | `brand-profile/` |

①이 재료라면 ②는 그 재료로 미리 조립해 둔 부품입니다. **둘 다 있어야** AI가 재료로 헤매지 않고 완성 부품을 그대로 씁니다.

---

## 전체 구조

```
component-gallery/
├── README.md              ← 이 문서
├── example-gallery.html   ← 예시 갤러리 (MURMUR 샘플몰 · 6개 섹션)
└── gallery.schema.json    ← 갤러리가 갖춰야 할 항목 체크리스트
```

`example-gallery.html`이 참조하는 실물 CSS 2개는 **클라이언트 폴더**에 있습니다:
```
web/cafe24/clients/{몰ID}/src/_nk/css/
├── nk-tokens.css       ← 준비물 ① (값)
└── nk-components.css   ← 준비물 ② (부품)
```

---

## 예시 갤러리에 담긴 것 (example-gallery.html)

MURMUR 샘플몰 기준 6개 섹션입니다.

| # | 섹션 | 담긴 컴포넌트 |
|---|---|---|
| 0 | Palette | 토큰 색상 스와치 (bg·point·ink 등) |
| 1 | Buttons `.nk-btn` | primary/line/ink · sm·md·lg · block · disabled · 아이콘 |
| 2 | Form | `.nk-field`(입력·셀렉트·텍스트영역) · 체크·라디오 · `.nk-form-row`·`.nk-form-section` 조립 |
| 3 | Cards | `.nk-card`(정보) · `.nk-prd-card`(상품: 썸네일·배지·가격·아이콘) |
| 4 | Data | `.nk-dl`(정의형 목록) · `.nk-table`(표) |
| 5 | Nav / Feedback | `.nk-pagetitle` · `.nk-tabs` · `.nk-badge` · `.nk-tooltip` · `.nk-pagination` · `.nk-empty` |

---

## 사용 방법 (비코더용)

### 1) 새 클라이언트 시작 시
1. `design-tokens/` 파이프라인으로 `nk-tokens.css` 생성 (준비물 ①)
2. 토큰 기반으로 `nk-components.css` 작성 (준비물 ②)
3. `example-gallery.html`을 복제해 클라 폴더에 두고 CSS 경로만 교체
4. 브라우저로 열어 **모든 부품이 한 번에 잘 보이는지 로컬 QA**

### 2) 실제 카페24 작업 지시 시
> "이 몰의 `component-gallery`에 있는 `.nk-btn--primary`, `.nk-form-row`, `.nk-card`를
> 그대로 가져와서 [로그인/장바구니/상세] 페이지를 조립해. 새 스타일 지어내지 말고
> 갤러리에 있는 부품만 재사용해."

이렇게 지시하면 AI가 부품을 새로 만들지 않고 갤러리 부품을 그대로 재사용합니다.

---

## 규칙

- **부품 클래스는 반드시 `nk-` 접두사** (누끼토끼 표준). 갤러리 뼈대는 `gx-`로 구분.
- 폰트는 **Pretendard + Phosphor** 기본 (클라 지시 없으면 유지). 예시의 Marcellus는 MURMUR 전용 디스플레이 폰트.
- 갤러리 페이지는 **컴포넌트 스타일을 정의하지 않습니다.** 오직 `nk-tokens.css`·`nk-components.css`를 불러와 진열만 합니다.
- 목업 금지 — 갤러리는 실제 작동하는 CSS로 렌더된 실물만 담습니다.
