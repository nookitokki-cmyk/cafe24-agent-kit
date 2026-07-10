# 검증 템플릿 uplift 가이드 — ecudemo402307 → `_verified-template`

> 작성: 2026-07-10  
> 근거: `C:\nookitokki\cafe24-agent-kit\.omc\plans\cafe24-agent-kit-skin-safety-ralplan.md` Domain A / P4·P5·P8  
> 대상: `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\src`  
> 원본 후보: `C:\nookitokki\cafe24-kit-작업본\agent-kit\clients\ecudemo402307`

---

## 0. 한 줄 원칙

**ecudemo402307을 통째로 복사하지 않는다.**  
이미 검증된 파일 중 초보자 starter에 안전한 A/B 후보만 골라, 기존 `_verified-template/src` 파일을 **제자리에서(in-place) 수정**한다.

이 가이드는 에이전트가 `_verified-template`을 보강할 때 다음 사고를 막기 위한 작업 지침이다.

- 실클라이언트/데모몰 파일을 대량 복사해서 브랜드·몰ID·내부경로가 공개 kit에 섞이는 사고
- 카페24 SmartDesign의 `<!--@layout-->`, `<!--@css-->`, `{$변수}`, `module="..."`, `xans-*`, `ec-base-*`를 깨뜨리는 사고
- 주문/결제/PG 파일을 “완성형처럼 보이게” 고치다가 실제 결제 흐름을 망가뜨리는 사고
- 새 client 폴더를 만들어 build allowlist·kit-update 전달 경로를 깨뜨리는 사고

---

## 1. 작업 경계

### 1-1. 허용되는 작업

| 구분 | 허용 내용 |
|---|---|
| 원본 조사 | `C:\nookitokki\cafe24-kit-작업본\agent-kit\clients\ecudemo402307`의 검증 산출물 읽기 |
| 대상 수정 | `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\src` 내부의 기존 파일 **in-place 수정** |
| 문서 갱신 | `_verified-template` 사용법·rollback·검증 설명 갱신 |
| 검증 | `verify-kit.sh` + skin-safety evaluator의 targeted verification |

### 1-2. 금지되는 작업

| 금지 | 이유 |
|---|---|
| `ecudemo402307/src` 또는 `src-skin1` 전체 복사 | 브랜드·몰ID·내부경로·검증 외 파일이 함께 들어올 수 있음 |
| `_verified-template/src`를 삭제 후 교체 | 기존 starter의 설치 경로·README 설명·검증 기준이 한 번에 무너짐 |
| `agent-kit/clients/ecudemo402307` 같은 새 client 폴더 생성 | ralplan P4 규칙 위반. build allowlist·gitignore·kit-update 전달 경로가 추가로 필요해짐 |
| `_verified-template/src/order/orderform.html`, `order/order_result.html`, `order/pg_success.html` 신규 편입 | 주문·결제·PG는 결제사/몰 설정/카페24 시스템 파일 의존도가 높아 초보자 starter 기본값으로 위험 |
| SFTP upload, Cafe24 API write, OAuth 연결, live mall 변경 | Domain B. 자동 실행 금지, 대표님 승인 전 HALT |
| git push, release, deploy | Domain B. 별도 승인 전 금지 |

---

## 2. 소스와 대상

### 2-1. source of truth

작업 원본은 아래 한 곳으로 고정한다.

```text
C:\nookitokki\cafe24-kit-작업본\agent-kit\clients\ecudemo402307
```

이 원본은 402307 데모몰에서 wave4·ultraqa를 거친 검증 산출물이다. 다만 **그 자체가 공개 템플릿은 아니다.** 원본에는 특정 데모몰·브랜드·작업 로그·내부 경로가 섞여 있을 수 있으므로, 공개 kit에는 선별·중립화된 결과만 반영한다.

### 2-2. uplift 대상

수정 대상은 아래 기존 템플릿만이다.

```text
C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\src
```

작업 방식은 “파일 복사”가 아니라 “기존 템플릿을 안전하게 보강”이다.

```text
좋은 방식:
원본 파일 읽기 → module/변수/구조 비교 → 필요한 블록만 이식 → 브랜드 중립화 → evaluator 확인

나쁜 방식:
원본 폴더 복사 → 이름만 바꾸기 → grep 몇 번 하고 완료 처리
```

---

## 3. A/B/C 그룹 분류

### 3-1. A그룹 — 우선 uplift 후보

A그룹은 초보자 starter의 “빈 곳”을 채우되, 결제·PG처럼 사고 위험이 큰 영역을 건드리지 않는 페이지다. 아래 후보는 ralplan P4의 우선 후보다.

```text
product/search.html
shopinfo/company.html
shopinfo/guide.html
coupon/coupon_zone.html
board/free/read.html
board/free/write.html
board/product/list.html
member/join_result.html
member/id/find_id.html
member/passwd/find_passwd_info.html
myshop/wish_list.html
myshop/coupon/coupon.html
```

A그룹을 다룰 때의 원칙:

1. 대상 파일이 `_verified-template/src`에 이미 있으면 **그 파일을 in-place 수정**한다.
2. 대상 파일이 없으면 먼저 “정말 starter 기본에 필요한가?”를 판단한다.
3. 추가가 필요하더라도 원본을 그대로 복사하지 말고 다음을 보존·중립화한다.
   - `<!--@layout(...)-->`
   - `<!--@css(...)-->`
   - `{$...}` 카페24 변수
   - `module="..."`
   - `xans-*`, `ec-base-*`
   - `anchorBoxId_{$product_no}` 반복 구조
4. 브랜드 문구·색·이미지·몰ID는 반드시 중립값으로 교체한다.

### 3-2. B그룹 — 선별 uplift 후보

B그룹은 기능상 유용하지만, starter 기본 파일로 넣으면 유지 면적이 커지는 페이지다. 기본 원칙은 “CSS 전량·공통 레이아웃으로 커버하고, HTML 셸은 최소화”다.

예시:

| 유형 | 기본 처리 |
|---|---|
| 부속 member 페이지 | `nk-member.css`로 커버. HTML 셸은 선별 |
| 부속 myshop 페이지 | `nk-myshop.css`·`nk-order.css`로 커버. 주문내역/프린트류는 제외 우선 |
| 부속 board 페이지 | `nk-board.css`로 커버. 대표 셸 외 전량 복사 금지 |
| popup·fragment | `layout/basic/popup.html` + `nk-popup.css`로 커버. 각 팝업 HTML 전량 복사 금지 |
| etc 페이지 | `nk-etc.css`로 커버. 실제 초보자 starter에 필요한 페이지만 선별 |

B그룹 판단 질문:

1. 이 파일이 없어도 카페24 기본 HTML + `_nk/css/*`로 안전하게 동작하는가?
2. 이 파일을 넣으면 브랜드·몰ID·내부경로 grep 면적이 늘어나는가?
3. 초보자가 수정할 가능성이 높은가, 아니면 시스템 보조 화면인가?
4. 주문·정산·PG·프린트·AJAX 조각과 연결되어 있지는 않은가?

4번이 “예”이면 C그룹으로 내려서 기본 제외한다.

### 3-3. C그룹 — 기본 제외, 선택형 고급 recipe

C그룹은 starter 기본값에 넣지 않는다. 필요하면 “고급 선택 recipe”로만 안내한다.

```text
order/orderform.html
order/order_result.html
order/pg_success.html
order/gift_select.html
myshop/order/*
myshop/order/print/*
product/image_zoom.html
product/stocklayer.html
coupon/coupon_productdetail.html
board/*/secret.html
board/*/comment_all.html
calendar/*
poll/*
link/*
```

#### 왜 주문/결제/PG는 제외하나?

비개발자 수강생에게 가장 중요한 설명은 이것이다.

> 주문서·결제·PG 화면은 “디자인 페이지”가 아니라 **실제 돈이 오가는 시스템 화면**이다.  
> 카페24, 결제대행사(PG), 배송/쿠폰/적립금/세금계산서 설정이 함께 얽혀 있어서 HTML을 예쁘게 바꾸는 순간 결제 버튼·리다이렉트·주문완료 처리·가상 파일 의존성이 깨질 수 있다.

따라서 starter 기본값은 다음 전략을 쓴다.

| 영역 | 기본 전략 | 이유 |
|---|---|---|
| `order/orderform.html` | 카페24 기본 HTML 유지 | 결제 form, PG 이동, 주문 후 이동값이 몰 설정과 연결됨 |
| `order/order_result.html` | 기본 제외 | 주문완료/결제결과는 PG 응답·주문상태와 연결됨 |
| `order/pg_success.html` | 기본 제외 | PG 성공 콜백 성격. 디자인 starter가 건드릴 영역 아님 |
| `myshop/order/*` | 기본 제외 또는 CSS 커버 | 주문내역·교환·반품·프린트는 상태별 분기가 많음 |
| `myshop/order/print/*` | 기본 제외 | 인쇄 전용. 레이아웃·브라우저 인쇄 설정 영향 큼 |

초보자에게는 “빠진 파일”이 아니라 “사고를 막기 위해 의도적으로 카페24 기본값을 쓰는 영역”이라고 설명한다.

#### C그룹 optional recipe 기본형

C그룹을 꼭 다뤄야 하는 경우에도 starter 파일로 편입하지 않고 아래 recipe로 분리한다.

```markdown
## 고급 recipe: C그룹 페이지 톤만 맞추기

1. 운영 스킨이 아닌 복사 스킨에서만 진행한다.
2. 해당 파일을 수정하기 전 원본을 백업한다.
3. HTML 구조와 `module="..."`, `{$...}` 변수는 바꾸지 않는다.
4. 새 HTML을 만들지 말고 CSS만 추가한다.
5. 결제 버튼, form action, hidden input, PG redirect 관련 코드는 절대 수정하지 않는다.
6. 적용 후 주문서 진입까지만 smoke test한다. 실결제 자동 테스트는 하지 않는다.
7. 이상하면 즉시 백업본으로 되돌린다.
```

---

## 4. in-place edit 규칙

### 4-1. 새 client 폴더 금지

이번 uplift에서 새 폴더를 만들지 않는다.

```text
금지:
C:\nookitokki\cafe24-agent-kit\agent-kit\clients\ecudemo402307
C:\nookitokki\cafe24-agent-kit\agent-kit\clients\verified-template-v2
C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template-next
```

허용 대상은 기존 폴더 하나뿐이다.

```text
C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template
```

새 client 폴더를 만들면 `.gitignore`, build allowlist, dist 사후 하드페일, `kit_tools.py` 자동업데이트 전달 경로를 모두 동기화해야 한다. Domain A의 이번 문서·uplift 작업은 그 범위가 아니다.

### 4-2. 파일별 수정 순서

각 파일은 아래 순서로 다룬다.

1. `_verified-template/src`의 현재 파일을 먼저 읽는다.
2. 402307 원본에서 대응 파일을 읽는다.
3. 다음 요소를 표로 비교한다.
   - SmartDesign 지시어
   - `module="..."`
   - `{$...}` 변수
   - `xans-*`, `ec-base-*`
   - import/css/js 경로
4. 필요한 구조만 옮긴다.
5. 브랜드·몰ID·내부경로를 제거한다.
6. 파일 하나 단위로 skin-safety evaluator를 돌린다.
7. 여러 파일을 한 번에 대량 변경하지 않는다.

### 4-3. 보존해야 하는 카페24 구조

아래는 “예쁘게 정리”한다는 이유로 지우면 안 된다.

```html
<!--@layout(/layout/basic/layout.html)-->
<!--@css(/_nk/css/nk-etc.css)-->
<!--@import(/_nk/inc/nk-header.html)-->
<div module="product_listnormal">
  {$product_name}
</div>
<li id="anchorBoxId_{$product_no}">
```

쉬운 설명:

- `<!--@layout-->`: 이 페이지가 어떤 공통 레이아웃을 입을지 알려주는 연결선
- `<!--@css-->`: 카페24가 CSS 파일을 불러오게 하는 연결선
- `<!--@import-->`: 헤더·푸터 같은 조각을 끼워 넣는 연결선
- `module="..."`: 카페24가 상품·회원·장바구니 데이터를 넣는 자리
- `{$...}`: 카페24가 실제 값으로 바꿔 주는 변수
- `anchorBoxId_{$product_no}`: 상품 반복을 카페24 엔진이 알아보는 구조

---

## 5. 브랜드 sanitization 체크리스트

uplift한 파일은 공개 kit에 들어갈 수 있으므로, 다음 흔적은 0건이어야 한다.

### 5-1. 금지 문자열

```text
MURMUR
ecudemo402307
ecudemo401788
ecudemo
401788
402307
reference-intake
03_references
ref-401788
mcp/backups
sftp_
cafe24_config_
higgsfield
test1111
#cc785c
#a9583e
#181715
벤더 브랜드명/전용 폴더명/전용 스크립트명
```

주의: `ecudemo`는 예시몰 설명 문서에서는 등장할 수 있지만, `_verified-template/src`의 배포 파일 안에는 들어가지 않는 것이 원칙이다.

### 5-2. 교체 기준

| 원본 흔적 | 교체 방식 |
|---|---|
| 브랜드명 | 가능한 곳은 `{$mall_name}`. module 밖이면 `YOUR BRAND`·`SHOP` 같은 중립 문구 |
| 브랜드 컬러 | `var(--nk-*)` 토큰으로 연결. 직접 hex 반복 금지 |
| 브랜드 이미지 | 중립 그라디언트 placeholder 또는 설치자가 교체할 주석 |
| 작업 경로 주석 | 공개 설명 주석으로 재작성. 로컬 절대경로 제거 |
| 데모몰 ID | 템플릿 파일에서는 제거. 케이스 스터디 문서에서만 설명 |
| 테스트 계정 | 제거. 로그인 테스트 안내 문서에도 실제 계정 노출 금지 |

### 5-3. sanitization 후 확인

대상은 `_verified-template/src`로 좁힌다.

```bash
# 금지 브랜드/내부경로 흔적 확인
grep -RInE 'MURMUR|ecudemo|401788|402307|reference-intake|03_references|ref-401788|mcp/backups|sftp_|cafe24_config_|higgsfield|test1111|#cc785c|#a9583e|#181715' \
  C:/nookitokki/cafe24-agent-kit/agent-kit/clients/_verified-template/src
```

PASS 기준: 출력 0건.  
단, 검증 도구가 Windows Git Bash에서 실행될 수 있으므로 실제 자동 검증은 Main이 환경에 맞춰 실행한다.

---

## 6. rollback 규칙

### 6-1. 로컬 git-tracked 파일 rollback

이번 Domain A 작업은 로컬 파일만 다룬다. 문제가 생기면 파일 단위로 되돌린다.

```bash
# 특정 파일 되돌리기
git checkout -- agent-kit/clients/_verified-template/src/상대경로.html

# 문서 파일 되돌리기
git checkout -- agent-kit/brain/docs/VERIFIED-TEMPLATE-UPLIFT.md
```

### 6-2. 여러 파일을 수정한 경우

여러 파일을 만졌다면 “한 번에 전체 되돌림”보다 아래 순서가 안전하다.

1. 실패한 evaluator evidence에서 문제 파일을 확인한다.
2. 해당 파일만 rollback한다.
3. 다시 `verify-kit.sh`와 skin-safety evaluator를 실행한다.
4. PASS count가 회복되는지 확인한다.

### 6-3. `.omc` scratch rollback

skin-safety evaluator 실행 로그나 autoresearch scratch가 문제를 만들었으면 해당 local scratch만 삭제한다.

```text
C:\nookitokki\cafe24-agent-kit\.omc\autoresearch\cafe24-agent-kit-skin-safety\
```

단, `.omc` 삭제는 작업 로그 손실이 있을 수 있으므로 Main이 최종 판단한다.

---

## 7. targeted verification

프로젝트 전체 formatter, project-wide lint, 전체 테스트는 이 작업 범위가 아니다. 아래 두 검증만 targeted로 수행한다.

### 7-1. verify-kit gate

위치:

```text
C:\nookitokki\cafe24-agent-kit\agent-kit\connect\scripts\verify-kit.sh
```

실행:

```bash
cd C:/nookitokki/cafe24-agent-kit
bash agent-kit/connect/scripts/verify-kit.sh
```

PASS:

```text
=== ALL PASS ===
exit 0
```

이 검증은 kit 배포 대상에 벤더 브랜드·가짜 변수·필수 파일 누락이 없는지 확인하는 기본 gate다. ralplan P0 hotfix 이후 `_verified-template` 때문에 gate가 영구 실패하지 않아야 한다.

### 7-2. skin-safety evaluator

skin-safety evaluator는 `_verified-template` uplift 전후로 아래 8개 기준을 검사해야 한다.

| 기준 | PASS 의미 |
|---|---|
| `smartdesign_directives_preserved` | `<!--@layout-->`, `<!--@css-->`, `<!--@import-->` 같은 지시어가 보존됨 |
| `cafe24_variables_preserved` | `{$...}` 변수가 삭제·하드코딩되지 않음 |
| `modules_preserved` | `module="..."` 구조가 보존됨 |
| `xans_ecbase_preserved` | `xans-*`, `ec-base-*` 기반 카페24 구조가 보존됨 |
| `order_payment_pg_excluded` | 주문/결제/PG C그룹이 기본 편입되지 않음 |
| `backup_and_rollback_defined` | 되돌릴 방법이 문서·작업 로그에 남음 |
| `brand_traces_removed` | 브랜드·몰ID·내부경로 흔적이 0건 |
| `non_developer_safe` | 비개발자도 왜 안전한지 이해할 수 있는 설명이 있음 |

권장 출력 형식:

```json
{
  "pass": false,
  "score": 0,
  "criteria": {
    "smartdesign_directives_preserved": false,
    "cafe24_variables_preserved": false,
    "modules_preserved": false,
    "xans_ecbase_preserved": false,
    "order_payment_pg_excluded": false,
    "backup_and_rollback_defined": false,
    "brand_traces_removed": false,
    "non_developer_safe": false
  },
  "blockers": [],
  "evidence": []
}
```

실행 원칙:

1. evaluator command는 `C:\nookitokki\cafe24-agent-kit\.omc\autoresearch\cafe24-agent-kit-skin-safety\evaluator.json`에 고정된 명령을 따른다.
2. evaluator가 아직 고정되지 않은 상태라면 uplift를 시작하지 않는다. ralplan 원칙은 **evaluator-first**다.
3. 파일을 여러 개 수정했다면 “전체 src”와 “수정 파일 목록”을 모두 evidence에 남긴다.
4. C그룹 파일이 편입됐거나 주문/결제/PG 구조가 바뀐 흔적이 있으면 FAIL 처리한다.

### 7-3. 증거 로그에 반드시 남길 것

```text
- 어떤 파일을 uplift했는지
- 원본 후보 파일은 무엇이었는지
- A/B/C 중 어떤 그룹으로 판단했는지
- SmartDesign 지시어·변수·module 보존 evidence
- 브랜드 sanitization grep 결과
- C그룹/order/payment/PG 제외 evidence
- rollback 경로
- verify-kit 결과
- skin-safety evaluator 결과
```

---

## 8. 작업자용 빠른 체크리스트

작업 전:

- [ ] source가 `C:\nookitokki\cafe24-kit-작업본\agent-kit\clients\ecudemo402307`인지 확인
- [ ] target이 `C:\nookitokki\cafe24-agent-kit\agent-kit\clients\_verified-template\src`인지 확인
- [ ] 새 client 폴더를 만들지 않는지 확인
- [ ] evaluator 기준 8개를 먼저 확인

파일 수정 중:

- [ ] 대량 복사 대신 in-place edit만 수행
- [ ] `<!--@layout-->`, `<!--@css-->`, `<!--@import-->` 보존
- [ ] `{$...}` 변수 보존
- [ ] `module="..."` 보존
- [ ] `xans-*`, `ec-base-*` 보존
- [ ] 주문/결제/PG 파일은 기본 제외
- [ ] 브랜드·몰ID·내부경로 제거

검증:

- [ ] `bash agent-kit/connect/scripts/verify-kit.sh` 결과 `=== ALL PASS ===`
- [ ] skin-safety evaluator 8개 criteria PASS
- [ ] C그룹 제외 evidence 있음
- [ ] rollback 경로 기록됨

---

## 9. 초보자에게 설명할 때의 문장

아래 문장을 README나 강의 안내에서 그대로 써도 된다.

> `_verified-template`은 완성 스킨을 통째로 복사한 것이 아니라, 실제 데모몰에서 검증된 구조 중 초보자가 안전하게 시작할 수 있는 부분만 골라 만든 starter입니다.  
> 주문서·결제·PG 화면은 일부러 기본값을 유지합니다. 이 영역은 디자인보다 결제 안정성이 더 중요하고, 몰 설정·PG사·카페24 시스템 파일과 연결되어 있어 초보자가 HTML을 바꾸면 실제 주문 흐름이 깨질 수 있기 때문입니다.  
> 대신 헤더·푸터·폰트·버튼·표·탭 같은 공통 톤은 `_nk/css/*` 토큰 레이어로 맞춰, 주문 흐름은 안전하게 두면서도 쇼핑몰 전체 분위기는 템플릿과 자연스럽게 이어지게 합니다.

---

## 10. 최종 판정 기준

이 guide를 따르는 uplift는 아래 조건을 모두 만족해야 완료로 본다.

1. 새 client 폴더가 없다.
2. `ecudemo402307` 전체 복사가 없다.
3. `_verified-template/src` in-place 수정만 있다.
4. A그룹은 우선, B그룹은 선별, C그룹은 기본 제외다.
5. 주문/결제/PG 제외 이유가 비개발자도 이해할 수 있게 설명되어 있다.
6. 브랜드·몰ID·내부경로 흔적이 없다.
7. rollback 경로가 있다.
8. `verify-kit.sh`와 skin-safety evaluator로 targeted verification을 통과한다.
