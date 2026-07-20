# 워크플로우 06 — Phase별 자기검증 루프 (verify-loop)

> **목표:** 레퍼런스 대비 구현 품질을 **페이지 타입별로** **100점만** PASS 될 때까지 자동 채점·수정 반복.  
> 선행: `/레퍼런스인입` 완료 → `03-reference-renewal` 구현 시작.

---

## 경험 있는 개발자의 권장 순서

```
1. 레퍼런스 인입 (코드 금지)
   └─ 페이지 인벤토리 → 페이지 타입 표 → 실측 시트 → 사용자 「예」
      (01_작업하기/workflows/05-reference-intake.md)

2. 레이아웃 셸 (공통)
   └─ layout.html CSS 링크 · header/footer · layout.js page-type 감지
   └─ override-ez.css 로 EZ 잔재 제거

3. 페이지 타입별 섹션 구현 + verify-loop (이 문서)
   └─ Phase 0 공통 → 1 PLP → 2 PDP → 3 장바구니 → 4 로그인 → 5 게시판 → 6 정적
   └─ 각 Phase: 구현 → FTP 업로드 → score 스크립트 → <100 이면 FAIL 항목만 수정

4. 격차 일괄 수정 (선택)
   └─ 전 Phase PASS 후 스크린샷 격차표 → 03-reference-renewal §6
```

**핵심:** 타입표·실측 없이 CSS를 얹지 않는다. PLP(풀폭)와 narrow(1200px)를 Phase 순서와 무관하게 **먼저** 표에 구분해 둔다.

---

## Phase 0 — Pre-flight (`#contents` width @390px)

**모든 Phase·FTP 업로드 전** (또는 override CSS 추가 직후):

1. Playwright viewport **390×844**, 메인 URL (`/m/` 아님).
2. **`/`** 와 **서브 1페이지**(PLP 권장)에서:
   ```javascript
   const vw = document.documentElement.clientWidth;
   const cw = document.querySelector('#contents')?.getBoundingClientRect().width;
   // PASS: cw >= vw - 4   FAIL: cw ≈ vw * 0.92 (~359 on 390)
   ```
3. **FAIL이면:** [`brain/rules/ez-contents-width.md`](../../brain/rules/ez-contents-width.md) + [`brain/docs/snippets/ez-contents-override.css`](../../brain/docs/snippets/ez-contents-override.css) 적용 후 재측정. Phase 1+ 진행 금지.

자동화: `python work/scripts/ref393674-score-mobile-full.py` → check **C1**.

---

## Phase 0.5 — Pre-flight (MO 검증 전)

MO viewport 채점·`/m/` spot-check **전에** 반드시:

1. **사용자에게 관리자 설정 확인 요청** — `brain/rules/responsive-mobile.md` §필수: 관리자 설정 경로를 붙여넣어 안내 (MCP·FTP 변경 불가)
2. **라이브 검증:** 타겟 몰 페이지 소스에서 `CAFE24.MOBILE_WEB=false`
3. **`true`이면:** MO score·verify-loop **중단** → 사용자가 「사용안함」 저장 후 재확인까지 대기

---

## 루프 절차 (매 Phase)

```
1. 구현 (해당 Phase HTML/CSS/JS만)
2. FTP 업로드 — open_remote('{몰ID}') → /sde_design/base/
3. python work/scripts/ref393674-score-{phase}.py
4. total_score < 100 → FAIL 항목만 수정 → 2번부터 반복
5. total_score = 100 → verify-loop.md 로그 → 다음 Phase
```

### 채점식

```
total_score = round((획득점수 합) / (만점 합) × 100)
PASS: total_score = 100 only (100 미만 = FAIL)
```

측정: Playwright `getComputedStyle` + `getBoundingClientRect` (PC 1440, MO 390).

### 반응형 MO (필수)

- **동일 템플릿:** MO 검증은 **메인 URL** (`https://{몰}.cafe24.com/...`) 에 viewport 390×844 — **`/m/` 별도 스킨 URL 금지** (unavoidable 전까지).
- **구현:** `@media (max-width: 1023px)` on `/sde_design/base/` — mobile 전용 HTML/CSS 신규 작성 금지 (`brain/rules/responsive-mobile.md`).
- **FTP:** 업로드 기본 `/sde_design/base/`; mobile 스킨 존재 시 동기화 또는 관리자 「모바일 전용 디자인 사용안함」 확인.
- **회귀:** 배포 후 `CAFE24.MOBILE_WEB`·`/m/` HTML에 `_ref393674` / `#header.a-header` 존재 여부 spot-check.

---

## Phase·스크립트 매핑 (ecudemo393674 → ecudemo400786)

| Phase | 페이지 | 스크립트 | 예시 PASS |
|-------|--------|----------|-----------|
| 0 | header/footer/layout | (수동 + `ref393674-score-header.py`) | — |
| 1 | PLP | `ref393674-score-plp.py` | 100 |
| 2 | PDP | `ref393674-score-pdp.py` | 100 |
| 3 | 장바구니 | `ref393674-score-basket.py` | 100 |
| 4 | 로그인 | `ref393674-score-member.py` | 100 |
| 5 | 게시판 (Notice free/1) | `ref393674-score-board.py` | 100 |
| 6 | About/Contact | `ref393674-score-page.py` | 100 |
| + | Info 드롭다운·검색 | `ref393674-score-header.py` | 100 |
| **MO** | **종합 모바일 (390×844, 5 URL)** | **`ref393674-score-mobile-full.py`** | **100 only** |

### 모바일 PASS (필수)

- **스크립트:** `work/scripts/ref393674-score-mobile-full.py`
- **조건:** `total_score = 100` — **100 미만 = FAIL** (모든 Phase 스크립트 동일)
- **viewport:** 390×844, `isMobile` + `hasTouch`, **메인 URL** (`/m/` 아님, `CAFE24.MOBILE_WEB=false` 전제)
- **대상 URL:** `/`, PLP, PDP, login, basket

로그 파일: `work/clients/{몰}/verify-loop.md`

---

## 스크립트 작성 템플릿

```python
REF = "https://{ref몰}.cafe24.com/..."
TGT = "https://{tgt몰}.cafe24.com/..."
PASS = 100

# measure(): page.goto → wait → evaluate(getComputedStyle)
# checks: 구조(class) + 레이아웃(숫자) + MO
# sys.exit(0 if pass else 1)
```

기존 `ref393674-score-plp.py` 가 PC+MO 통합 비율 채점의 참조 구현.

---

## FTP·캐시

- Windows Git Bash: `MSYS_NO_PATHCONV=1` (경로 `/sde_design/...` 깨짐 방지)
- 업로드 후 2~5분·`?v=N` 하드 리로드 전에는 FAIL을 격차로 오판하지 말 것 (`03-reference-renewal` §7)

---

## CDP 승리규칙 전수조사 (라이브 ≠ 목업/시안 진단)

> **트리거**: "라이브가 목업/시안과 다르다" · "어딘가에서 레거시 코드가 주입되는 것 같다, 전수조사해". → **추측 중단하고 CDP 실측으로 전환.**

`getComputedStyle`(값만)로는 "왜 이 값이 나오는지"를 못 짚는다. **CDP `CSS.getMatchedStylesForNode`로 각 요소의 승리 규칙(winning declaration)이 어느 파일에서 오는지 실측**한다.

### 절차
1. 문제 요소들에서 어긋난 속성(border·background·padding·font·display)의 **승리 규칙과 그 출처**를 CDP로 열거.
2. 출처가 **카페24 base**인지 **우리 과거 커스텀 CSS**(후행 로드 + `!important`)인지 판별. → **"라이브≠시안"의 진짜 범인은 대부분 카페24 base가 아니라 우리 옛 커스텀 CSS**가 나중에 로드되며 신규를 덮는 것이다.
3. 처방(클린 컷오버 우선):
   - **(a)** 특정 페이지에서만 그 레거시 파일의 `@css(...)` 로드 라인 제거 — **공유 파일은 다른 페이지를 위해 잔존**(그 페이지에서만 끊음).
   - **(b)** 레거시 소스의 해당 섹션을 삭제하고 owner를 **단일 파일로** 통일.
   - **(c)** 특이도 보강 — 컨테이너 클래스 prepend 또는 `.xans-* nk-*` 앵커로 base/generic을 로드순·`!important` 무관하게 이김.
   - **(d)** 범용 규칙이 owner를 침범하면 `!important`로 키우지 말고 **범용 쪽에 `:not(.owner클래스)`** 로 제외.
4. 제거/보강 후 **CDP 재실측** → 게이트 = **"모든 승리 규칙 = 우리 owner, base·레거시 승리 요소 0."**

### 증거 규율
- **파일명은 증거가 아니다** — optimizer가 번들 href에 원본 파일명을 안 남긴다. **번들 결합 CSS의 내용 grep + computed style + 스크린샷**이 증거.
- 헤드리스 `getComputedStyle(el,'::before').content` 빈값 quirk는 실제 렌더 정상일 수 있음 → **스크린샷으로 판정**.

### 함께 자주 나오는 원인
- **이중 owner 충돌**: 같은 셀렉터를 owner 두 파일이 다르게 이중 정의 → 선·빈칸·배경 중첩. **중복 블록 제거로 단일 owner화**(칸 단위 땜질 금지).
- **죽은 파일 편집 착시**: 어떤 HTML도 로드하지 않는 고아 CSS를 고치면 라이브가 안 바뀐다 → "고쳤는데 그대로 = 간섭" 오판. **참조 grep 0건이면 편집 원복·제외**, 실제 활성 owner만 수정.
- **optimizer 캐시 이원**: `@css`/`@js`엔 `?v=` 금지(mtime 자동버스트, 번들 2~5분 지연) / 직접 `<link>`는 `?v=` 필수 / 즉시 반영 필요 시 직접링크로 이관.

---

## 관련 문서

- 인입: `05-reference-intake.md`
- 구현: `03-reference-renewal.md`
- 함정: `02_막혔을때/common-pitfalls.md`
- **EZ #contents:** `brain/rules/ez-contents-width.md`
- 키트 로드맵: `brain/docs/kit-roadmap.md`
