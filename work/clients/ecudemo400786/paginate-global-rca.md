# 전역 페이징 RCA — ecudemo400786

> **일자:** 2026-06-19  
> **대상:** https://ecudemo400786.cafe24.com/ (전역 `.ec-base-paginate`)  
> **레퍼런스:** https://ecudemo393674.cafe24.com/ (maeve — 대부분 1페이지만 있어 페이징 DOM 없음)  
> **이전 문서:** `board-paginate-rca.md` (게시판 한정) → 본 문서로 통합·확장

---

## 1. 증상 (Before)

게시판·상품목록·검색 등 **모든** `ec-base-paginate typeList` 에서 동일 증상:

```html
<div class="xans-board-paging ec-base-paginate typeList section">
  <a href="?page=1">이전 페이지</a>
  <ol><li><a class="this">1</a></li></ol>
  <a href="?page=1">다음 페이지</a>
</div>
```

| 증상 | Playwright 실측 (수정 전) |
|------|---------------------------|
| 이전/다음 한글 노출 | `prevFontSize: 13px` (기대 `0px`) |
| 번호 박스 border | `numBorder: 1px` (EZ skin16 박스) |
| 페이징 좌우 margin 비대칭 | PC `margin: 40px 46px 0` (`.section` trap) |
| ol list-style | `list-style: decimal` 잔존 |

검증 URL:
- https://ecudemo400786.cafe24.com/board/free/list.html?board_no=1
- https://ecudemo400786.cafe24.com/product/list.html?cate_no=24 (페이징 `.hide` — markup은 동일)

---

## 2. 근본 원인 (Global)

### 2-A. EZ 3층 CSS 충돌

1. **head** `ec-base-paginate.css` — `font-size:0` 숨김 + `li a` 40×40 border 박스
2. **head** `_ref393674/sub.css` — `.typeList a { font-size:13px }` 가 `> a`까지 매칭 → 숨김 무력화
3. **body 끝** `sub_style.css` → `sub_theme.css` → `add_layout.css` — PNG 화살표·font-size 14px·`.section` 92% width

**head만 수정하면 body 끝 EZ가 이김.** `#contents` + body 끝 전용 파일이 필수.

### 2-B. `.section` margin trap

`add_layout.css`:

```css
#contents > .section { max-width:1480px; width:92%; margin-left:auto; margin-right:auto; }
```

Cafe24 모듈이 페이징 div에 `section` 클래스를 붙임 → 페이징만 좁아지고 좌우 margin 발생.

### 2-C. 게시판만 고치면 안 되는 이유

`ec-base-paginate typeList`는 Cafe24 공통 컴포넌트:

| 영역 | 모듈 예 |
|------|---------|
| 게시판 | `xans-board-paging` |
| 상품목록 | `product_normalpaging` |
| 검색 | `product_searchpaging` |
| 마이페이지 | 주문·쿠폰 목록 |
| 상세 | `typeSub` (리뷰·Q&A) |

동일 마크업·동일 클래스 → **한 파일 `sub-paginate.css`** 로 처리.

### 2-D. Cafe24에서 매번 반복되는 이유

| 패턴 | 설명 |
|------|------|
| 접근성 텍스트 + CSS 숨김 | `이전 페이지` DOM 텍스트 + `font-size:0` — 커스텀 `a{font-size}` 한 줄이 전역 파괴 |
| body 끝 theme CSS | EZ 스킨은 `sub_style`을 `</body>` 직전 로드 — “나중에 로드한 custom이 이긴다”는 가정이 **거짓** |
| 페이지 타입 분리 착각 | `sub-board.css`만 수정 → PLP·검색 누락 |
| 1페이지 QA | 글이 적으면 페이징 1칸만 보여 prev/next 버그 미발견 |
| base/mobile 비동기 | 한쪽 스킨만 배포 시 MO/PC 불일치 |

---

## 3. 수정 (After)

### 3-A. 신규 `sub-paginate.css`

- `body.layout #contents .ec-base-paginate` — `#contents`로 specificity 확보
- `typeList > a` — `font-size:0 !important`, PNG 화살표 유지
- `ol li a` — border 제거, underline `.this`
- `.section` — max-width/margin trap 해제
- `typeSub` — 리뷰·Q&A 동일 톤

### 3-B. `layout.html` / `main.html` body 끝

```html
<!--@css(/layout/basic/css/add_layout.css)-->
<!--@css(/_ref393674/css/sub-paginate.css)-->
```

### 3-C. `sub.css`에서 페이징 규칙 **제거** (중복·충돌 방지)

### 배포 경로

- `/sde_design/base/_ref393674/css/sub-paginate.css`
- `/sde_design/base/_ref393674/css/sub.css`
- `/sde_design/base/layout/basic/layout.html`
- `/sde_design/base/layout/basic/main.html`
- `/sde_design/mobile/` 동일 4파일

---

## 4. 검증

```bash
python work/scripts/ref393674-score-paginate.py
```

| 항목 | Before | After (기대) |
|------|--------|--------------|
| `> a` fontSize | 13px | **0px** |
| num border | 1px | **0px** |
| ol display | inline-flex | inline-flex |
| prev/next stacked | 가능 | **aligned** (동일 Y) |
| `.section` margin-left | ~46px | **0px** |

캐시 우회: 강력 새로고침 또는 `?v=` 타임스탬프.

---

## 5. 관련 파일

| 파일 | 역할 |
|------|------|
| `_ref393674/css/sub-paginate.css` | **전역 수정 (본번)** |
| `layout/basic/layout.html` | body 끝 링크 |
| `_ref393674/css/sub.css` | 페이징 규칙 제거 |
| `layout/basic/css/ec-base-paginate.css` | EZ base |
| `layout/basic/css/sub_style.css` | PNG 화살표 (body 끝) |
| `agent-kit/docs/common-pitfalls.md` | §전역 페이징 |
| `work/scripts/ref393674-score-paginate.py` | 회귀 채점 |
