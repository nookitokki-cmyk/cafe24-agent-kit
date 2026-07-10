# Cafe24 Developers 자동화 문서 맵

> **한 줄 결론:** Cafe24 Developers 문서는 이 kit가 "무엇을 확인할 수 있는지"를 알려 주는 지도다. 이 문서가 있다고 해서 실제 쇼핑몰에 자동으로 업로드하거나, 상품을 만들거나, OAuth를 연결해도 된다는 뜻은 아니다.

- 대상 독자: 카페24 스킨을 수정하려는 비개발자 수강생과 kit 작업 에이전트
- 이 문서의 역할: Cafe24 Developers 공식 문서(Admin API, Front API, OAuth, MCP, Web Components, Design)를 이 kit의 안전 규칙에 연결
- 이 문서의 금지: live mall 자동 변경, API write 자동 실행, OAuth 자동 연결, SFTP 자동 업로드를 허용하는 근거로 사용 금지

---

## 0. 먼저 알아야 할 쉬운 비유

| 용어 | 쉬운 설명 | 이 kit에서의 의미 |
|---|---|---|
| Admin API | 쇼핑몰 관리자 안쪽 정보를 보는/바꾸는 공식 통로 | 스킨 유형, 디자인 목록, 상품·주문·SEO 설정 같은 "진단 후보"를 찾는 데 도움 |
| Front API | 고객이 보는 화면 쪽 공개 정보를 조회하거나 일부 고객 행동을 처리하는 공식 통로 | 상품 진열, 카테고리, 장바구니 같은 프론트 화면 진단 후보 |
| OAuth | 앱이 쇼핑몰 관리자에게 "허락"을 받는 절차 | 토큰 발급은 실제 권한 연결이므로 Domain B hard gate |
| MCP | AI 도구가 Cafe24 작업 도구를 호출할 수 있게 하는 연결 방식 | 이 kit의 손발 도구와 연결 가능하지만, 쓰기 작업은 별도 승인 필요 |
| Web Components | 카페24가 제공하는 화면 구성 요소 계열 문서 | 후속 화면 자동화/컴포넌트 연구 색인, 현재 스킨 자동 변경 권한 아님 |
| Design / SmartDesign | 스킨 HTML, 모듈, 편집창, 화면 구조 문서 | `module="..."`, `{$변수}`, `<!--@...-->` 보존 기준의 근거 |

---

## 1. 공식 문서 → kit 사용처 매핑

| 공식 문서 영역 | 공식 URL | kit에서 보는 이유 | 자동 실행 가능 여부 |
|---|---|---|---|
| Cafe24 Developers 홈 | https://developers.cafe24.com/ | App, Design, MCP, Web Components, Data 메뉴의 출발점 | 문서 조회만 가능 |
| Admin API | https://developers.cafe24.com/docs/api/admin/ | 관리자 데이터, 디자인(Themes), 상품, 주문, 결제, SEO, 게시판, 회원 설정 등 진단 후보 확인 | **GET 조회만 Domain A 후보**. POST/PUT/DELETE는 Domain B |
| Front API | https://developers.cafe24.com/docs/api/front/?version=2021-06-01 | 고객 화면에 가까운 상품·카테고리·장바구니 등 조회 후보 확인 | **GET 조회만 Domain A 후보**. 장바구니 생성 등 POST는 Domain B |
| OAuth 전체 흐름 | https://developers.cafe24.com/app/front/app/develop/oauth/process | 앱 권한 동의 흐름 이해 | OAuth 연결 자체는 Domain B |
| Authorization Code 요청 | https://developers.cafe24.com/app/front/app/develop/oauth/oauthcode | `code=`를 받는 절차 이해 | Domain B |
| Access Token 발급 | https://developers.cafe24.com/app/front/app/develop/oauth/token | access token 교환 절차 이해 | Domain B |
| App 생성 | https://developers.cafe24.com/app/front/app/develop/createapps | 개발자센터에서 앱을 만드는 위치 확인 | 사용자가 직접 수행, 자동 생성 금지 |
| OAuth 설정 | https://developers.cafe24.com/app/front/app/develop/oauth/put | Redirect URI, Scope 설정 위치 확인 | 사용자가 직접 수행, 자동 변경 금지 |
| MCP server | https://developers.cafe24.com/mcpserver/front/mcpserver | Cafe24 공식 MCP 방향성 확인 | 연결/호출은 kit gate를 따름 |
| MCP tool reference | https://developers.cafe24.com/mcpserver/front/mcpserver/mcptools | 공식 MCP 도구 범위 확인 | 쓰기 도구는 Domain B로 분리 |
| Web Components | https://developers.cafe24.com/webcomponents/front/webcomponents | 향후 컴포넌트 기반 화면 연구 색인 | 현재 스킨 live 자동 변경 권한 아님 |
| Design Guide | https://developers.cafe24.com/design/front/design | 디자인 개발 문서 출발점 | 문서 조회만 가능 |
| SmartDesign 소개 | https://developers.cafe24.com/design/front/smart | 카페24 스킨/디자인 개발 문서 출발점 | 문서 조회만 가능 |
| SmartDesign 기본 이해 | https://developers.cafe24.com/design/front/smart/sdsupport/basic | 모듈, 변수, 주석 변수 등 스킨 문법 이해 | 스킨 코드 수정 시 보존 기준 |
| SmartDesign 편집창 | https://developers.cafe24.com/design/front/smart/sdsupport/editor | 관리자 편집창과 모듈 편집 방식 이해 | 수동 작업 안내 근거 |
| SmartDesign 모듈 목록 | https://sdsupport.cafe24.com/product/list.html?cate_no=61 | `Layout_category`, `product_listnormal` 등 모듈명 확인 | 코드 생성 전 참조 |

> **주의:** 공식 API 문서에 POST/PUT/DELETE 예시가 있어도, 이 kit가 자동으로 실제 몰을 바꿔도 된다는 뜻이 아니다. 공식 문서는 "가능한 API"를 설명하고, 이 kit의 Domain 규칙은 "지금 자동으로 해도 되는 일"을 제한한다.

---

## 2. Domain A / Domain B 경계

### Domain A — 로컬·조회·진단: 자율 실행 가능

Domain A는 실패해도 되돌릴 수 있거나, 외부 쇼핑몰에 영향을 주지 않는 범위다.

| 작업 | 허용 이유 | 예시 |
|---|---|---|
| 로컬 문서 작성/수정 | git으로 되돌릴 수 있음 | `agent-kit/brain/docs/*.md` 갱신 |
| 로컬 스킨 안전성 evaluator 작성 | live mall에 영향 없음 | `module`, `{$변수}`, `xans-*`, 주문/결제 제외 검사 |
| Cafe24 API read-only 설계 | 실제 호출 전 문서화 단계 | Admin API에서 어떤 GET이 진단에 유용한지 정리 |
| 이미 연결된 read-only 토큰의 상태 확인 | 값을 바꾸지 않음 | `cafe24_auth_status` |
| 디자인 목록 조회 | 값을 바꾸지 않음 | `cafe24_list_themes` |
| HTML 페이지 정본 읽기 | 값을 바꾸지 않음 | `cafe24_read_page` |
| SFTP list/read/download/backup | 파일을 바꾸지 않거나 백업만 생성 | `cafe24_sftp_list`, `cafe24_sftp_read`, `cafe24_sftp_download`, `cafe24_sftp_backup` |
| 로컬 smoke test | kit 설치 상태 확인 | `python smoke_test.py`, `verify-kit.sh` |

### Domain B — 외부·불가역: 자동 실행 금지

Domain B는 실제 몰, 토큰, 배포, 상품, 주문, 결제, 공개 릴리즈에 영향을 줄 수 있는 범위다. 반드시 멈추고 대표님 명시 승인을 받아야 한다.

| 작업 | 왜 위험한가 | gate |
|---|---|---|
| live Cafe24 SFTP upload | 운영 스킨 파일이 바로 바뀔 수 있음 | 승인형 SFTP write gate |
| Cafe24 API POST/PUT/DELETE | 상품·주문·설정·디자인 데이터가 바뀔 수 있음 | API write hard gate |
| OAuth 토큰 발급/연결 | 앱에 실제 쇼핑몰 권한이 부여됨 | OAuth hard gate |
| `create_product` | 실제 상품이 생성될 수 있음 | create_product hard gate |
| 주문/결제/PG 관련 API write | 고객 주문·정산·결제 흐름에 영향 | 항상 hard gate |
| live mall 설정 변경 | 관리자 설정이 바뀜 | always halt |
| git push / release / deploy | 공개 배포 또는 버전 배포 | 별도 승인 필요 |

---

## 3. 권한 매트릭스 — 이 문서의 핵심

| 구분 | 구체 작업 | HTTP/도구 기준 | Domain | 자동 실행 | 필요한 승인 |
|---|---|---|---|---|---|
| 문서 확인 | 공식 URL 읽기 | Browser/Read/Web Search | A | 가능 | 없음 |
| 로컬 문서화 | 이 파일 같은 `.md` 작성 | file write | A | 가능 | 없음 |
| API 설계 | 어떤 endpoint가 진단에 유용한지 표로 정리 | 문서 기반 | A | 가능 | 없음 |
| API 상태 확인 | 토큰 존재/만료시각 확인 | `cafe24_auth_status` | A 또는 B 직전 | 가능, 단 토큰 발급은 금지 | 기존 토큰이 있을 때만 |
| Admin API 조회 | 디자인/상품/설정 정보 읽기 | GET | A 후보 | 가능, read-only 조건 | 기존 read scope 필요 |
| Front API 조회 | 공개 상품/카테고리 정보 읽기 | GET | A 후보 | 가능, read-only 조건 | 필요한 경우 client_id/scope 확인 |
| SFTP 목록 보기 | 원격 폴더 구조 확인 | `cafe24_sftp_list` | A | 가능 | 기존 접속정보 필요 |
| SFTP 읽기 | 원격 파일 내용 확인 | `cafe24_sftp_read` | A | 가능 | 기존 접속정보 필요 |
| SFTP 다운로드 | 원격 파일을 로컬 백업/분석용으로 받기 | `cafe24_sftp_download` | A | 가능 | 기존 접속정보 필요 |
| SFTP 백업 | 업로드 전 원본 백업 생성 | `cafe24_sftp_backup` | A | 가능 | 기존 접속정보 필요 |
| SFTP 업로드 | 원격 스킨 파일 반영 | `cafe24_sftp_upload` | B | **자동 실행 금지** | 대표님 명시 승인 + whitelist + 백업 |
| OAuth 권한 연결 | authorization code/token 발급 | OAuth flow | B | **자동 실행 금지** | 대표님 명시 승인 + scope 확인 |
| API write | POST/PUT/DELETE | Admin/Front API write | B | **자동 실행 금지** | endpoint별 명시 승인 |
| 상품 생성 | `Create a product` | POST `/api/v2/admin/products` | B | **항상 금지 상태로 멈춤** | 별도 작업으로 재승인 필요 |
| 릴리즈 | git push/release/deploy | Git/배포 | B | **자동 실행 금지** | 별도 승인 |

**실무 문장으로 요약하면:**

- "조회해도 될까요?" → 기존 연결이 있고 GET/list/read라면 Domain A다.
- "바꿔도 될까요?" → 거의 항상 Domain B다.
- "올려도 될까요?" → SFTP upload이므로 Domain B다.
- "상품 만들어도 될까요?" → `create_product` hard gate다. 자동 실행 금지다.

---

## 4. Read-only 진단은 무엇까지 가능한가

Read-only 진단은 "쇼핑몰의 현재 상태를 읽어서, 스킨 수정 전에 위험을 줄이는 일"이다. 비개발자 기준으로는 병원에서 수술 전 검사표를 보는 것과 같다. 검사표를 보는 것은 가능하지만, 수술을 자동으로 하지는 않는다.

| 진단 목적 | 공식 문서에서 보는 위치 | kit에서 얻는 도움 | live 변경 여부 |
|---|---|---|---|
| 스킨 종류 확인 | Admin API `Themes` | `editor_type`으로 H(HTML SmartDesign), E(SmartDesignEasy) 등을 구분 | 없음 |
| 스킨 폴더 후보 확인 | Admin API `Themes`의 `skin_code` | SFTP 폴더 추정에 도움. 단 공식이 폴더명 동일을 보장한다고 말하지 않음 | 없음 |
| HTML 페이지 읽기 | Admin API `Themes pages` | `/layout/basic/layout.html` 같은 페이지 소스 정본 확인 | 없음 |
| 상품 진열 구조 이해 | Admin/Front API Product, Category | 상품 번호, 카테고리, 진열 상태를 스킨 변수와 대조 | 없음 |
| 장바구니/프론트 동작 후보 확인 | Front API Personal/Cart | 화면 기능이 API상 어떤 리소스인지 파악 | GET만 없음. POST는 변경 가능성이 있으므로 B |
| 주문/결제/PG 위험 분리 | Admin API Order, Payment | C그룹 기본 제외 근거 강화 | 조회만 없음. write는 절대 B |
| SEO 설정 확인 | Admin API SEO setting | 스킨 `<title>`, meta 작업과 관리자 SEO 설정의 충돌 가능성 파악 | GET만 없음 |
| 게시판 설정 확인 | Admin API Boards setting / SmartDesign board modules | 게시판 스킨 수정 전 board module 구조 확인 | GET만 없음 |

### Read-only 진단에서 지켜야 할 말하기 규칙

- "API로 확인할 수 있습니다"는 **조회 가능**이라는 뜻이다.
- "API로 수정할 수 있습니다"는 공식 기능 설명일 뿐, 이 kit에서 자동 실행 가능하다는 뜻이 아니다.
- 보고서에는 반드시 `조회`, `백업`, `업로드`, `생성`, `수정`, `삭제`를 구분해서 적는다.
- `GET`이 아닌 요청은 기본적으로 Domain B라고 본다.

---

## 5. 승인형 SFTP write gate

SFTP upload는 스킨 파일을 실제 몰에 올리는 작업이다. 카페24 스킨은 HTML 한 줄만 잘못 올라가도 헤더, 상품 목록, 주문 페이지가 깨질 수 있다. 그래서 이 kit에서는 업로드를 "자동화의 편의 기능"이 아니라 "승인형 반영 단계"로 다룬다.

### SFTP upload 전 필수 조건

| 순서 | 조건 | 이유 |
|---|---|---|
| 1 | 대표님이 "업로드 승인"을 명시 | 외부 live 변경이므로 자동 판단 금지 |
| 2 | 대상 mall_id 확인 | 엉뚱한 몰 업로드 방지 |
| 3 | 대상 remote path 확인 | `/skin14`와 `/skin16`처럼 스킨 폴더를 혼동하면 위험 |
| 4 | `write_allowed` whitelist 안인지 확인 | 원본/구매템플릿/base 보호 |
| 5 | 업로드 전 `cafe24_sftp_backup` 실행 | 되돌릴 백업 확보 |
| 6 | 업로드 파일 diff 또는 변경 요약 제시 | 비개발자가 무엇이 바뀌는지 알아야 함 |
| 7 | 업로드 후 targeted smoke check | 화면 깨짐 조기 확인 |

### 승인 문구 예시

SFTP upload를 진행하려면 승인 요청은 이렇게 분명해야 한다.

```text
아래 1개 파일을 demo000의 /skin16/_nk/css/header.css로 업로드하면 운영 스킨이 바뀝니다.
백업 경로는 mcp/backups/demo000/2026-... 입니다.
진행해도 될까요?
```

반대로 아래 표현은 충분하지 않다.

```text
수정 반영할게요.
업로드해도 될 듯합니다.
자동으로 올리겠습니다.
```

---

## 6. `create_product` hard gate

Admin API 문서에는 상품 생성 기능(`Create a product`)이 있다. 공식 문서 기준으로는 POST `/api/v2/admin/products` 계열 작업이 가능하다. 하지만 이 kit에서는 `create_product`를 **항상 Domain B hard gate**로 둔다.

### 왜 더 강하게 막는가

| 이유 | 설명 |
|---|---|
| 실제 상품이 생김 | 테스트 상품이라도 관리자 상품 목록, 검색, 진열, 재고, SEO에 남을 수 있음 |
| 삭제까지 연쇄 작업이 됨 | 만들고 지우는 과정 자체가 추가 write 작업 |
| 수강생 실수 위험이 큼 | 비개발자는 테스트몰/운영몰 구분, 상품 상태, 진열 상태를 놓치기 쉬움 |
| 스킨 수정 목표와 다름 | Domain A의 목표는 스킨 안전성·진단·문서화이지 상품 운영 자동화가 아님 |

### 처리 원칙

- `create_product` 요청이 나오면 즉시 멈춘다.
- "공식 API에 있으므로 가능"이라고 말하지 않는다.
- 별도 승인, 별도 작업 범위, 테스트몰 여부, 롤백/삭제 계획이 없으면 실행하지 않는다.
- 이 kit의 기본 자동화에 `create_product`를 연결하지 않는다.

---

## 7. API 문서가 스킨 수정에 도움이 되는 지점

스킨 수정은 대부분 HTML/CSS/JS와 SmartDesign 문법 문제다. 그래도 API 문서는 "화면에 들어오는 데이터의 정체"를 이해하는 데 도움이 된다.

| 스킨 수정 상황 | 도움이 되는 공식 문서 | 어떻게 쓰나 | 주의 |
|---|---|---|---|
| 어떤 스킨을 수정해야 하는지 모름 | Admin API `Themes` | 디자인 목록, `skin_no`, `skin_code`, `editor_type` 확인 | SFTP 폴더 매핑은 실측 확인 필요 |
| HTML 스킨인지 Easy인지 헷갈림 | Admin API `Themes` + Design Guide | `editor_type`으로 1차 분류, 실제 파일의 `data-ez-*`로 2차 확인 | `E`라고 해서 무조건 SFTP 불가라고 단정 금지 |
| `{$product_name}` 같은 변수가 어디서 오는지 궁금함 | SmartDesign 기본 이해 + Product API | 상품 리소스와 스킨 변수의 의미를 대조 | API 필드명과 스킨 변수명이 항상 1:1 같지는 않음 |
| 상품 목록이 이상하게 보임 | Front API Product/Category + SmartDesign Product modules | 카테고리/상품 진열 상태와 module 구조를 함께 확인 | CSS 문제와 데이터 문제를 분리 |
| 게시판 페이지를 고침 | Admin API Boards setting + SmartDesign board modules | 게시판 설정과 module 번호/구조를 확인 | 게시글 write API는 별도 Domain B |
| 주문/결제 페이지가 포함됨 | Admin API Order/Payment | 위험도를 파악하고 C그룹 기본 제외 근거로 사용 | 주문/결제/PG 파일은 기본적으로 자동 승격 제외 |
| SEO 문구가 충돌함 | Admin API SEO setting | 관리자 SEO 설정과 스킨 meta 작업을 구분 | SEO setting update는 Domain B |
| 화면 컴포넌트 연구 | Web Components / Design Guide | 후속 컴포넌트 패턴 참고 | 현재 kit 스킨을 자동 변경하는 근거 아님 |

### 스킨 작업에서 공식 Design 문서가 특히 중요한 이유

카페24 스킨은 일반 HTML 파일처럼 보이지만, 실제로는 카페24 엔진이 아래 문법을 읽고 화면을 만든다.

| 문법 | 의미 | 깨지면 생기는 문제 |
|---|---|---|
| `<!--@layout(...)-->` | 이 페이지가 어떤 레이아웃을 쓸지 알려 주는 지시어 | 페이지가 빈 화면이 되거나 레이아웃이 깨짐 |
| `<!--@import(...)-->` | 다른 HTML 조각을 불러오는 지시어 | 헤더/푸터/공통 영역 누락 |
| `<!--@css(...)-->`, `<!--@js(...)-->` | CSS/JS를 카페24 방식으로 등록 | 스타일·동작 누락 |
| `module="Layout_category"` | 카페24가 데이터를 채워 넣는 영역 | 카테고리, 로그인, 장바구니 등 기능 깨짐 |
| `{$product_name}` | 카페24가 실제 값으로 바꾸는 변수 | 상품명·가격·이미지 미노출 또는 `{...}` 그대로 노출 |
| `xans-*`, `ec-base-*` | 카페24가 자동으로 붙이는 클래스 | 기본 CSS/JS 연결 깨짐 |

따라서 API 문서를 볼 때도 최종 목적은 "API로 다 바꾸기"가 아니라, **스킨 파일에서 무엇을 절대 지우면 안 되는지 더 정확히 아는 것**이다.

---

## 8. OAuth와 Scope는 왜 조심해야 하나

OAuth는 쇼핑몰 운영자가 앱에 권한을 허락하는 절차다. 비개발자 기준으로는 "AI 도구에게 쇼핑몰 관리자 열쇠를 일부 맡기는 것"에 가깝다.

### Scope 해석 원칙

| Scope 유형 | 쉬운 의미 | kit 처리 |
|---|---|---|
| `mall.read_*` | 읽기 권한. 정보를 조회할 수 있음 | Domain A 후보. 그래도 기존 연결이 있을 때만 |
| `mall.write_*` | 쓰기 권한. 정보를 만들거나 바꿀 수 있음 | Domain B. 자동 연결/자동 호출 금지 |
| design read | 디자인 목록/페이지 읽기 | 진단 후보 |
| design write | 디자인 페이지 수정 | API write이므로 Domain B |
| product write | 상품 생성/수정/삭제 | `create_product` 포함 hard gate |
| order/payment write | 주문·결제 상태 영향 | 항상 hard gate |

### OAuth 작업에서 금지되는 말

- "한 번 연결해두면 제가 알아서 바꿔둘게요."
- "write scope까지 받아두면 편합니다."
- "테스트니까 상품 하나 만들어볼게요."
- "토큰을 채팅에 붙여주세요."

### OAuth 작업에서 허용되는 말

- "공식 문서상 이 작업에는 어떤 scope가 필요한지 확인했습니다."
- "이번 Domain A에서는 OAuth 연결을 하지 않습니다."
- "기존 read-only 연결이 없으면 실제 API 조회는 생략하고 문서 기반 설계만 합니다."
- "write scope가 필요한 순간 Domain B로 멈춥니다."

---

## 9. MCP / Web Components / Design 문서의 kit 내 위치

### MCP

Cafe24 Developers의 MCP 문서는 AI 도구와 Cafe24 기능을 연결하는 공식 방향을 보여 준다. 다만 이 repo의 `mcp/` 폴더는 이미 별도 안전장치를 가진 로컬 kit 구현이다.

| kit MCP 도구 | 안전 분류 | 설명 |
|---|---|---|
| `get_kit_guides` | Domain A | kit 문서와 workflow 안내 |
| `diagnose_kit_setup` | Domain A | 설치 상태 진단 |
| `run_preflight` | Domain A | 로컬/브라우저 기반 스킨 안전성 검사 |
| `cafe24_auth_status` | Domain A 후보 | 기존 토큰 상태 확인. 토큰 발급은 아님 |
| `cafe24_list_themes` | Domain A 후보 | 디자인 목록 조회 |
| `cafe24_read_page` | Domain A 후보 | HTML 페이지 조회 |
| `cafe24_sftp_list` | Domain A 후보 | 원격 목록 보기 |
| `cafe24_sftp_read` | Domain A 후보 | 원격 파일 읽기 |
| `cafe24_sftp_download` | Domain A 후보 | 원격 파일 다운로드 |
| `cafe24_sftp_backup` | Domain A 후보 | 업로드 전 백업 |
| `cafe24_sftp_upload` | Domain B | 운영 반영. 자동 실행 금지 |

### Web Components

Web Components 문서는 향후 카페24 화면 구성요소를 더 공식적인 컴포넌트 단위로 연구할 때 유용하다. 현재 Domain A에서는 색인과 설계만 허용한다.

- 허용: 공식 URL 정리, 컴포넌트 후보 조사, 스킨 안전성 evaluator에 참고 항목 추가
- 금지: live mall에 Web Component 삽입 자동 반영, 외부 스크립트 운영몰 자동 주입

### Design / SmartDesign

Design 문서는 이 kit의 스킨 안전성 기준과 직접 연결된다.

- `module="..."`는 카페24 기능 블록이다.
- `{$변수}`는 카페24가 실제 상품명·가격·이미지 등으로 바꾸는 값이다.
- `<!--@layout-->`, `<!--@import-->`, `<!--@css-->`, `<!--@js-->`는 카페24 엔진에게 전달하는 지시어다.
- 이 문법을 지우는 리팩터링은 "예쁜 코드 정리"가 아니라 "쇼핑몰 기능 파손"일 수 있다.

---

## 10. 작업자가 따라야 할 안전 문장 템플릿

### 진단 보고

```text
이번 단계는 Domain A read-only 진단입니다.
공식 Admin API/SmartDesign 문서를 기준으로 스킨 유형과 페이지 구조를 확인했으며,
SFTP upload, API write, OAuth 연결, live mall 설정 변경은 실행하지 않았습니다.
```

### Domain B 도달 보고

```text
여기서부터는 Domain B입니다.
이 작업은 실제 Cafe24 몰에 변경을 만들 수 있으므로 자동 실행하지 않습니다.
진행하려면 대상 mall_id, 작업 경로/API endpoint, 백업/롤백 방법을 확인한 뒤 대표님 명시 승인이 필요합니다.
```

### `create_product` 차단 보고

```text
`create_product`는 공식 Admin API에 존재하지만 실제 상품을 생성하는 POST 작업입니다.
이 kit의 Domain A 자동화 범위가 아니므로 여기서 멈춥니다.
별도 승인된 상품 운영 자동화 작업으로 분리해야 합니다.
```

---

## 11. 빠른 체크리스트

작업자가 Cafe24 Developers 문서를 보고 자동화 아이디어를 냈다면, 실행 전 아래 질문에 답해야 한다.

- [ ] 이 작업은 문서 조회인가, 실제 쇼핑몰 조회인가, 실제 쇼핑몰 변경인가?
- [ ] HTTP Method가 GET인가? POST/PUT/DELETE인가?
- [ ] OAuth 토큰 발급이나 scope 변경이 필요한가?
- [ ] SFTP upload가 포함되는가?
- [ ] 상품·주문·결제·PG·회원·쿠폰·SEO 설정을 바꾸는가?
- [ ] `create_product` 또는 상품 write가 포함되는가?
- [ ] 비개발자도 무엇이 바뀌는지 이해할 수 있게 설명했는가?
- [ ] 백업/롤백 경로가 있는가?
- [ ] Domain B라면 자동 실행을 멈추고 승인 요청으로 전환했는가?

하나라도 Domain B에 해당하면 자동 실행하지 않는다.

---

## 12. 공식 URL 모음

- Cafe24 Developers: https://developers.cafe24.com/
- Admin API: https://developers.cafe24.com/docs/api/admin/
- Front API: https://developers.cafe24.com/docs/api/front/?version=2021-06-01
- OAuth process: https://developers.cafe24.com/app/front/app/develop/oauth/process
- OAuth authorization code: https://developers.cafe24.com/app/front/app/develop/oauth/oauthcode
- OAuth access token: https://developers.cafe24.com/app/front/app/develop/oauth/token
- App creation: https://developers.cafe24.com/app/front/app/develop/createapps
- OAuth app settings: https://developers.cafe24.com/app/front/app/develop/oauth/put
- MCP server: https://developers.cafe24.com/mcpserver/front/mcpserver
- MCP tool reference: https://developers.cafe24.com/mcpserver/front/mcpserver/mcptools
- Web Components: https://developers.cafe24.com/webcomponents/front/webcomponents
- Design Guide: https://developers.cafe24.com/design/front/design
- SmartDesign: https://developers.cafe24.com/design/front/smart
- SmartDesign 기본 이해: https://developers.cafe24.com/design/front/smart/sdsupport/basic
- SmartDesign 편집창: https://developers.cafe24.com/design/front/smart/sdsupport/editor
- SmartDesign 모듈 목록: https://sdsupport.cafe24.com/product/list.html?cate_no=61

---

## 13. 최종 원칙

1. 공식 문서는 "가능한 기능"을 알려 준다.
2. 이 kit의 Domain 규칙은 "지금 자동으로 해도 되는 일"을 정한다.
3. Domain A는 조회·진단·문서화·로컬 검증이다.
4. Domain B는 업로드·쓰기·OAuth·상품 생성·주문/결제·배포다.
5. Domain B에 도달하면 자동화가 똑똑해도 멈춘다.
6. 비개발자 수강생에게는 "무엇을 읽었는지"와 "무엇을 절대 바꾸지 않았는지"를 함께 설명한다.
