# F1~F26 함정 인덱스 (traps)

> **읽는 법:** 에이전트는 문제 생기면 **여기서 번호 찾고** → `brain/docs/CAFE24-SMARTDESIGN-AGENT.md` §6에서 상세 읽기.  
> **출처 등급:** 🟢 공식 문서 | 🟡 실무(프로젝트 검증) | ⚪ 미대조(공식 문장 없음)

| ID | 한 줄 요약 | 등급 |
|----|------------|------|
| **C** | module 밖 `{$변수}` 금지 · EZ/data-ez 건드리지 않기 · base 직접 수정 금지(원칙) | 🟢 변수·모듈 / 🟡 EZ·base·Easy경계(§AUDIT D) |
| F1 | `<section>` 120px margin → 상단 빈 공간 | 🟡 |
| F2 | `overflow-x:hidden`이 sticky 깨짐 → `clip` | 🟡 |
| F3 | 업로드 후 2~5분 캐시·optimizer 지연 | 🟡 |
| F4 | `@css`에 `?v=` 붙이면 파일 깨짐 | 🟡 |
| F5 | `find` 결과를 한 변수에 몰아 perl → 조용히 실패 | 🟡 |
| F6 | `.inner` 이중 패딩 (container + section) | 🟡 |
| F7 | logotop.css가 로고 가운데 강제 | 🟡 |
| F8 | GNB 가운데 — absolute + translate | 🟡 |
| F9 | css/module 두 번째 base 레이어 놓침 | 🟡 |
| F10 | EZ `body max-width` → 좌측 쏠림 | 🟡 |
| F11 | `{$product_name}`을 alt 등 속성에 넣지 말 것 | 🟡 |
| F12 | Swiper v4/5 클래스·breakpoints | 🟡 |
| F13 | Grid + product_list `width:25%` 축소 | 🟡 |
| F14 | category.css `#category` margin | 🟡 |
| F15 | 데이터 0건인데 빈 셸만 남음 | 🟡 |
| F16 | `.detail_guide` 2열 flex 어긋남 | 🟡 |
| F17 | PDP `max-width` 캡 → 양옆 빈공간 | 🟡 |
| F18 | `.infoArea margin-left:100px` grid 잘림 | 🟡 |
| F19 | 페이징 박스·화살표 base 스타일 | 🟡 |
| F20 | select padding 대칭 → caret 겹침 | 🟡 |
| F21 | 인라인 script `/` 문자열 → skin prefix 이중 | 🟡 |
| F22 | @css/@js 없는 파일 → base fallback 로드 | 🟡 |
| F23 | SFTP 유령 스텁 (목록만 있고 읽기 실패) | 🟡 |
| F24 | 팝업 레이아웃은 custom.css 안 탐 | 🟡 |
| F25 | `@layout`/`@import` 경로 오타 → 영역 증발 | 🟢 @layout 공식 / 🟡 오타 결과 |
| F26 | `@layout` 안 부르는 layout 파일 = 고아 | 🟢 @layout / 🟡 고아 개념 |
| **F27** | EZ MO `#container #contents` **92%** → 히어로·배너 좌우 흰 gap | 🟡 |
| **F28** | PC `base/`만 배포 → 실제 `/m/` 은 별도 mobile 스킨 | 🟡 |
| **F29** | 서브페이지 전부 **1200px narrow** 오판 (PLP·PDP는 풀폭) | 🟡 |
| **F30** | PLP HTML 구조 격차 — CSS만으로 menupackage·sortby 미해결 | 🟡 |
| **F31** | MO 장바구니 가격·수량 **줄바꿈** (card 레이아웃) | 🟡 |
| **F32** | PLP 상품카드 description **행간 넓음** | 🟡 |
| **F33** | score **100점 미만**인데 「완료」 보고 (검증 루프 생략) | 🟡 |
| **F34** | 관리자 **「모바일 전용 디자인」** ON — MCP로 못 끔 | 🟡 |

> **F27~F34** 상세: [`02_막혔을때/common-pitfalls.md`](common-pitfalls.md) · 학생용 허브: [`02_막혔을때/F-상황-인덱스.md`](F-상황-인덱스.md)

## 초보자용 5대 함정 (getting-started 04 ↔ 공식)

| 초보 문구 | 대응 | 공식 |
|-----------|------|------|
| 고쳤는데 안 바뀜 | F3 캐시 | 🟡 |
| `{$mall_name}` 그대로 보임 | C module 밖 변수 | 🟢 |
| CSS 통째로 사라짐 | F4 @css ?query | 🟡 |
| 상품 1개만 나옴 | 반복 블록 2개+ (anchorBoxId) | 🟡 (공식은 `$count` 주석변수 별도 설명) |
| 푸터 한 페이지만 바뀜 | layout vs index 파일 | 🟢 @layout |

## 공식 문서 링크 (에이전트가 인용할 때)

- 변수·모듈·반복: https://developers.cafe24.com/design/front/smart/sdsupport/basic
- module 307종 목록: https://sdsupport.cafe24.com/product/list.html?cate_no=61
- 상세 문법 전체: `brain/docs/CAFE24-SMARTDESIGN-AGENT.md` §4~§6
