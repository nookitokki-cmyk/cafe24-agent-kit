---
name: 레퍼런스인입
description: 레퍼런스 URL 또는 작업자 시안 인입 — 페이지 인벤토리·타입표·실측시트 (코드/FTP 금지)
---

사용자가 `/레퍼런스인입` 을 요청했습니다.

**역할: 게이트keeper.** 「무엇을·어떤 구조로·어떤 숫자로 맞출지」 합의만 한다.  
**금지:** HTML/CSS 수정, SFTP/FTP 업로드, `cafe24_sftp_upload`, 추측 여백·max-width.

상세: `01_작업하기/workflows/05-reference-intake.md` · 시안 제출: `00_시작하기/시안-제출-체크리스트.md`  
**관리자·개발자센터 메뉴 안내 전:** `brain/rules/cafe24-admin-verify.md` (웹 검색 필수)

---

## 전제

- `/접속세팅` 완료 또는 동등 정보 (타겟 몰 ID, skin_code, editor_type, FTP/SFTP).
- `editor_type` ≠ **H** 이면 HTML 자동 작업 중단 → Easy 안내.

---

## 시안 소스 (A / B 택 1 — 둘 다 필수 아님)

| ID | 소스 | 최소 제출 |
|----|------|-----------|
| **A** | 레퍼런스 URL | `https://{몰}.cafe24.com/` + (페이지별 URL은 에이전트가 GNB·푸터·Info에서 수집) |
| **B** | 작업자 시안 | HTML/CSS/JS zip **또는** Figma 링크 + 프레임명 |

둘 다 있으면: **시안 = 디자인 스펙 우선**, URL = module·동작·데이터 참고.

---

## 질문 순서 (한 번에 하나. 답 없으면 다음 금지)

### Q1. 시안 소스
「**A) 레퍼런스 URL** 인가요, **B) 작업자 시안**(HTML/Figma)인가요, **둘 다**인가요?」

### Q2. 타겟 몰
「**어느 몰에 올릴까요?** (몰 ID / `/접속세팅` 완료 여부)」

→ 미완료면 `/접속세팅` 먼저. 업로드는 인입 완료 후.

### Q3. 범위 (기본값 제시)
「범위는 **레퍼런스(또는 시안)에서 확인 가능한 페이지 전부**로 할게요. 줄일 페이지가 있나요? (없음 / 목록 붙여넣기)」

**기본값 = 전 페이지.** 사용자가 「없음」이면 GNB·푸터·Info·`/pages/*`·board 링크 전부 인벤토리.

### Q4. 완료 기준
「**PC 1440px + 모바일 390px** 둘 다 맞출까요? (예/PC만)」

→ **예**이면: **동일 base 템플릿** + `@media` (별도 mobile 스킨 아님). 검증 viewport 390은 **메인 URL** (`/m/` 아님). `brain/rules/responsive-mobile.md` 준수.

→ **즉시 안내 (MCP 불가):** 사용자에게 아래 관리자 경로를 **붙여넣어** 「모바일 전용 디자인 사용설정」**사용안함** 확인을 요청한다.

> 쇼핑몰 설정 → 사이트 설정 → 쇼핑몰 환경 설정 → **모바일** 탭 → **기본설정** → **사용설정** → **「모바일 전용 디자인 사용설정」** → **「사용안함」** → 저장  
> Help: https://support.cafe24.com/hc/ko/articles/8466336842009  
> 확인: 페이지 소스 `CAFE24.MOBILE_WEB=false`

### Q5. 데이터
「**디자인만** 맞출까요, **배너·상품 이미지·카테고리 데이터**까지 맞출까요? (디자인만 / 데이터까지)」

**이스케이프 해치:** 수치를 모르는 사용자에게는 질문만 반복하지 말고:

> 「혹시 수치를 모르시겠으면, 제가 **레퍼런스 실측 + 스크린샷** 으로 확인한 기본값(예: 본문 13px·line-height 23.4px)으로 일단 칠해서 보여드릴까요?」

**기본값 규칙 (dual-source):**
1. **엔지니어링:** Playwright `getComputedStyle` 실측 (우선)
2. **비주얼:** 레퍼런스 스크린샷에서 간격·비율 교차 확인
3. 둘 중 하나만이면 문서에 「단일 출처」 표기 — 추측 px 금지

### Q6. 마이페이지 (선택)
「로그인 후 마이페이지도 포함할까요? (포함 시 **테스트 계정** 필요 / 로그인·가입 화면만)」

---

## 에이전트 실행 (Q6 답변 후 — 여전히 코드 금지)

### 1) 페이지 인벤토리

소스 A: 레퍼런스 몰에서 수집 (Playwright·크롤·헤더 HTML)
- GNB, 푸터, Info 서브, `/pages/*`, `product/list`, `member/login`, `order/basket`, board `board_no`

소스 B: 시안 파일/Figma 프레임 목록 + 카페24 module 필요 URL 매핑

### 2) 페이지 타입 표

| # | 페이지 | URL | 타입 | container | module | 비고 |
|---|--------|-----|------|-----------|--------|------|
| | | | `hero-main` / `plp-full` / `pdp-full` / `narrow` / `board` | max-width, padding | Y/N | 배너·menupackage 등 |

타입 가이드 (`01_작업하기/workflows/05-reference-intake.md` §타입):

- `hero-main` — `/`, container 100%, padding 0
- `plp-full` — PLP, 100% + 카테고리 배너·menupackage 가능
- `pdp-full` — PDP, 100%, padding 보통 20px 20px 100px
- `narrow` — About, Login, 장바구니, 게시판 등 1200px 중앙
- `board` — narrow + 게시판 테이블

### 3) 실측 시트 (타입별 대표 1페이지 + 공통)

Playwright `getComputedStyle` 또는 시안 CSS / Figma MCP.

| 항목 | 값 |
|------|-----|
| font-family / font-size | |
| container max-width / padding | |
| PLP item width (4열) | |
| header height | |
| 색상 primary / text / bg (hex) | |

형용사 금지. 숫자·hex만.

### 4) HTML 구조 격차 (소스 A일 때 필수)

EZ skin16 vs 레퍼런스: `#contents` 유무, `titleArea` 노출, `sortby` vs `select`, `list.html` 교체 필요 Y/N.

---

## 완료 출력

```markdown
## 레퍼런스 인입 완료 (승인 대기)

- 소스: A / B / A+B
- 타겟 몰: ...
- 범위: N 페이지
- 데이터: 디자인만 / 데이터까지
- PC+MO: ...

### 페이지 인벤토리
(표)

### 페이지 타입 표
(표)

### 실측 시트
(표)

### HTML 구조 격차 (해당 시)
(표)

---
**이 표 기준으로 진행할까요? (예 / 수정할 줄 번호)**
```

**사용자 「예」 전:** `/디자인수정` · FTP · list.html 수정 **금지**.

**사용자 「예」 후:** `clients/{몰}/reference-intake.md` 저장 권장 → `/디자인수정` 또는 `01_작업하기/workflows/03-reference-renewal.md` 3단계부터 → Phase별 `01_작업하기/workflows/06-verify-loop.md`.

**PC+MO 동일 템플릿(Q4=예)인 경우:** 구현·배포 전에도 §Q4 관리자 경로를 다시 안내하고 `CAFE24.MOBILE_WEB=false` 확인을 요청한다 (미설정 시 MO verify-loop 무의미).

---

## 금지 (반복)

- 실측·인벤토리 없이 「1200px」「풀폭」 추측
- CSS 한 겹 더하기
- 인입표 승인 전 maeve/ORDINARY skin 통째 복사
