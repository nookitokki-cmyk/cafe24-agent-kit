# 카페24 수정자(modifier) · 제어 문법 레퍼런스

> 변수 출력값을 가공하는 **수정자 13종** + 조건/반복 제어 문법.
> 형식: `{$변수|수정자:파라미터}` — `module="..."` 안에서만 동작(밖이면 치환 안 됨).

---

## 수정자 13종

| # | 수정자 | 하는 일 | 문법 | 예시 |
|---|--------|---------|------|------|
| 1 | `cut` | 글자 자르기(+말줄임) | `{$v\|cut:길이,접미}` | `{$product_name\|cut:20,...}` |
| 2 | `numberformat` | 천 단위 콤마 | `{$v\|numberformat}` | `{$product_price\|numberformat}` |
| 3 | `date` | 날짜 포맷 | `{$v\|date:Y-m-d}` | `{$write_date\|date:Y.m.d}` |
| 4 | `display` | 값이 false면 `display:none` | `{$v\|display}` | `class="{$soldout_icon\|display}"` |
| 5 | `cover` | 앞뒤로 감싸기 | `{$v\|cover:앞,뒤}` | `{$subject\|cover:[,]}` |
| 6 | `replace` | 문자열 치환 | `{$v\|replace:찾을것,바꿀것}` | `{$notice_icon\|replace:notice,공지}` |
| 7 | `strconv` | 문자열 변환 | `{$v\|strconv:텍스트}` | `{$new_icon\|strconv:NEW}` |
| 8 | `imgconv` | 이미지 태그 변환 | `{$v\|imgconv:경로}` | `{$name_or_img_tag\|imgconv:'/img/a.png'}` |
| 9 | `nl2br` | 줄바꿈 → `<br>` | `{$v\|nl2br}` | `{$content\|nl2br}` |
| 10 | `striptag` | HTML 태그 제거 | `{$v\|striptag}` | `{$content\|striptag}` |
| 11 | `timetodate` | 타임스탬프 → 날짜 | `{$v\|timetodate:Y-m-d}` | `{$write_date\|timetodate:Y-m-d}` |
| 12 | `lower` | 소문자 | `{$v\|lower}` | `{$category_name\|lower}` |
| 13 | `upper` | 대문자 | `{$v\|upper}` | `{$category_name\|upper}` |

> 가장 자주 쓰는 3종: **`numberformat`**(가격), **`cut`**(상품명 말줄임), **`display`**(품절/NEW 뱃지 조건 표시).

---

## 조건부 출력 (if 대용)

카페24 스마트디자인엔 일반 `if`가 없고, 아래 두 방식으로 처리한다.

**① `display` 수정자** — 값이 false면 그 요소를 `display:none`
```html
<span class="{$soldout_icon|display}">SOLD OUT</span>
<th class="{$config.use_date|display}">작성일</th>
```

**② 로그인 상태 모듈** — 로그인 여부로 분기
```html
<div module="Layout_statelogon">  <!-- 로그인 했을 때만 -->
  {$name}님 환영합니다
</div>
<div module="Layout_statelogoff"> <!-- 로그아웃 상태만 -->
  <a href="/member/login.html">로그인</a>
</div>
```

---

## 반복 (loop) — 주석 옵션

상품/게시판 등 진열 모듈은 **주석 옵션**으로 반복 수를 정한다.

```html
<ul module="product_listnormal">
  <!--
  $count = 5
  $only_html = no
  -->
  <li>{$product_name}</li>
</ul>
```

| 옵션 | 설명 | 값 | 우선순위 |
|------|------|----|---------|
| `$only_html` | HTML에 쓴 아이템 개수만큼만 반복 | yes/no | **1(최우선)** |
| `$count` | 반복 횟수 | 숫자 | 2 |
| `$fixed` | 고정 위치 | top 등 | - |

- **⚠️ 주석 옵션은 반드시 줄바꿈** 해서 써야 함 (한 줄로 쓰면 안 먹음).
- `$count=5` + 아이템 1개 → 5개 생성 / 아이템 3개 + `$count=5` → 마지막 아이템이 반복돼 5개.
- ⚠️ **상품 진열은 `anchorBoxId` 블록이 2개 이상**이어야 정상(1개면 상품 1개만 출력) — `brain/docs/CAFE24-SMARTDESIGN-AGENT.md` 참조.

---

## 지시어 (파일 포함 · 리소스)

| 종류 | 카페24 문법 |
|------|-------------|
| 레이아웃 | `<!--@layout(/layout/basic/product.html)-->` |
| 파일 포함 | `<!--@import(/layout/basic/header.html)-->` |
| CSS | `<!--@css(/css/style.css)-->` |
| JS | `<!--@js(/js/script.js)-->` |

> ⚠️ **`@css`·`@js`는 `?query`를 못 받습니다** (붙이면 CSS/JS가 통째로 드롭됨). 캐시 무력화는 **페이지 URL에 `?v=N`** 으로. (우리 키트 실측 함정 — `02_막혔을때/함정-INDEX.md`)

---

## 빠른 팁
- 에디터에서 `{$` + `Ctrl+Space` → 변수 자동완성.
- `.xans-*` 클래스는 카페24 자동 생성 → 커스텀 클래스는 따로 추가(`nk-`).
- module 영역 **구조는 바꾸지 말 것**(바인딩 깨짐) — 스타일만 바꾸거나 바깥에 래퍼 추가.

---

*근거: 카페24 공식 스마트디자인 문법(공용 스펙) + `brain/_evidence/` 공식 문서 대조. 수정자 목록 정리는 오픈소스 레퍼런스(kimyoungwopo/cafe24-smart-design, MIT)도 참고.*
