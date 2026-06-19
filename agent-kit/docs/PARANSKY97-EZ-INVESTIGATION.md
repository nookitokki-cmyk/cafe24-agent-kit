# paransky97 EZ 제거 심층 조사 — WHY / HOW

> **조사일:** 2026-06-19  
> **몰:** [https://paransky97.cafe24.com/](https://paransky97.cafe24.com/)  
> **작업 skin_code:** `skin14` (API `skin_no=16`, 이름 「아키테이블」, `editor_type=E`)  
> **SFTP:** `ecimg-ftp-c01.cafe24img.com:8008` · 루트 `/{skin_code}` (`/sde_design` 없음)  
> **관련:** [`EZ-STRATEGY.md`](EZ-STRATEGY.md) · [`WORK-GUIDE.md` §0·§15·§18](WORK-GUIDE.md) · [`VERIFICATION-EVIDENCE.md`](VERIFICATION-EVIDENCE.md)

---

## 0. 경영 요약 (Executive Summary)

paransky97에서 EZ(스마트디자인 Easy)를 걷어낸 이유는 **「IDIO(skin2)와 같은 독립 템플릿」을 만들기 위해서**다. skin14는 카페24 **아키테이블 EZ 테마**와 동일 계열(`layout.css:1` `아키테이블_style` 주석)이지만, `data-ez-*`·EZST·`body max-width` 같은 EZ 잔재가 남으면 **HTML을 자유롭게 고칠 수 없고**, 에이전트·grep·CSS 오버라이드가 모두 불리해진다.

실제 작업은 2026년 6월 초 **skin10(EZ 원본) → skin14(작업 베이스)** 로 이어지는 재판매 템플릿 빌드의 일환으로 수행됐다. 방법론은 키트 Phase C 기본안과 **동일 계열**:

1. **`strip_ez.py` 자동 제거** — 핵심 HTML에서 `data-ez-*`·`<ez-prop>` 제거  
2. **layout 런타임 제거** — `EZST` 초기화·`@js(/ez/init.js)`·ez-favicon 마커 삭제  
3. **`_nk/` 독립 레이어** — 헤더·푸터·메인 섹션을 `/_nk/inc/`로 재작성, `Layout_category` GNB로 전환  
4. **CSS 2단계 정리** — `body#nk-skin14 { max-width:none }` + base/module CSS 토큰화(§18-6)

**목표 대비 현황:** layout·index·product 등 **코어 HTML은 strip 완료**(API 실측 `data-ez` 0). 다만 **`_nk/inc/` 3파일에 `data-ez` 12건 잔존**(주로 `user-defined` 인라인 스크립트 래퍼) — IDIO(skin2) 수준의 **완전 0건**과는 미세 차이. 라이브 홈·PDP HTML에서도 `data-ez-*` 12건·`data-ez-module` 4건 확인(2026-06-19).

---

## 1. WHY — EZ를 제거한 이유 (증거 기반)

### 1.1 전략적 목표: IDIO 패턴 재현

| 근거 | 내용 |
|------|------|
| [`WORK-GUIDE.md` §0 결론 2·4](WORK-GUIDE.md) | IDIO(skin2) = 아키테이블 EZ 출신 → EZ 전부 걷고 `_idio/` 독립 레이어. skin14도 **같은 계열** → IDIO 수준까지 걷어야 skin2와 동급 |
| [`CAFE24-SMARTDESIGN-AGENT.md`](CAFE24-SMARTDESIGN-AGENT.md) | `data-ez-*`는 EZ 전용. 장기 커스텀은 `module="..."` + `_nk/` HTML이 표준 |
| [`EZ-STRATEGY.md` §1](EZ-STRATEGY.md) | strip 후 HTML-clean DOM → 에이전트·FTP 직접 편집, F27·detail.css 전쟁 감소 |

### 1.2 기술적·유지보수 이유 (실작업에서 드러난 함정)

| 문제 | EZ 잔존 시 | strip + `_nk` 후 |
|------|-----------|------------------|
| **body 좌측 쏠림** | EZ `body{max-width:1480px}` (`layout.css` 실측) | `custom.css` `body#nk-skin14{max-width:none!important}` ([`WORK-GUIDE` §15·§18](WORK-GUIDE.md)) |
| **GNB 문법 분기** | `data-ez-module="menu-main/1"` — 카테고리 미출력 위험 | `_nk/inc/menu.html` → `module="Layout_category"` ([API 실측](clients/paransky97/.workflow.md)) |
| **에이전트 컨텍스트 오염** | base `index.html`: `data-ez-` 95건·`ez-prop` 5건 (skin_no=1) | skin14 `index.html`: `data-ez` 0, `_nk` import 15건 |
| **CSS override 전쟁** | EZ 테마 `sub_theme`·`add_theme*` 늦은 로드 | `#nk-skin14` ID 스코프 + base CSS 직접 토큰화(§18-6) |
| **관리자 EZ GUI 의존** | 스마트배너·GNB 옵션 패널에 묶임 | `_nk/inc/` HTML·Swiper 직접 제어 (tradeoff: GUI 편집 포기) |

### 1.3 F35 회피 — Easy 타입 등록은 하지 않음

- `editor_type=E`는 **관리자 메타**일 뿐, SFTP `/skin14` 편집 가능 ([`VERIFICATION-EVIDENCE.md` §3](VERIFICATION-EVIDENCE.md)).
- 키트 canonical: **HTML 타입 skin 복사 + EZ FTP overlay + 코드 strip** — 관리자에 Easy 타입 신규 등록 후 FTP 대량 수정(**F35**)은 하지 않음 ([`07` Phase 0-D](../workflows/07-ez-on-legacy-setup.md)).

### 1.4 ecudemo400786와의 대비 (왜 paransky만 strip인가)

| | ecudemo400786 | paransky97 |
|--|---------------|------------|
| 목적 | 레퍼런스 1:1 **속도** 파일럿 | **재판매 템플릿** 표준 방향 |
| Phase C | **스킵** — `data-ez` 유지 + `_ref` CSS | **strip** — HTML-clean + `_nk/` |
| 근거 | 9/9 score 100 달성 후 키트가 **예외**로 격리 | [`EZ-STRATEGY.md` §4](EZ-STRATEGY.md) |

---

## 2. HOW — skin14에서 실제로 한 일 (단계별 재구성)

> 출처: [`WORK-GUIDE.md` §15·§17·§18](WORK-GUIDE.md), [`CAFE24-SMARTDESIGN-AGENT.md`](CAFE24-SMARTDESIGN-AGENT.md), 2026-06-19 API·라이브 실측.  
> 원본 상세 로그: `web/cafe24/clients/template-02/src/skin10/_nk/WORK-GUIDE.md` (워크스페이스 밖 — **미동기화**).

### Phase 0 — 베이스 선정

| 단계 | 내용 |
|------|------|
| 스킨 계보 | skin10 = 공식 EZ(아키테이블), **skin14 = EZ 걷어낸 작업 베이스** ([`WORK-GUIDE` §0](WORK-GUIDE.md)) |
| 부적합 제외 | skin15 = 구형 XHTML·고정폭 — IDIO와 다른 종 |
| 몰 매핑 | paransky97 `skin_no=16` → SFTP `/skin14` ([`VERIFICATION-EVIDENCE.md` §2](VERIFICATION-EVIDENCE.md)) |

### Phase C-1 — `strip_ez.py` 자동 strip (핵심 HTML)

**도구:** `strip_ez.py` — 원본 경로 `web/cafe24/clients/template-02/strip_ez.py`, 워크스페이스 복제본 `mcp/work/scripts/strip_ez.py`.

**절차** ([`WORK-GUIDE` §15](WORK-GUIDE.md)):

```
1. _ez-backup/ 에 원본 복사
2. python3 strip_ez.py <file>          # 미리보기·통계
3. python3 strip_ez.py <file> --write  # 적용
4. data-ez 잔여 0 + module=" 코어 생존 확인
```

**대상 파일 (문서·nookitokki002 Phase C manifest와 동일 패턴):**

- `index.html`
- `layout/basic/{layout,main,header,footer,sidebar}.html`
- `product/{detail,list}.html`
- (선택) smart-banner·supply HTML

**제거 규칙:** `<ez-prop>` 블록, `text/ez-prop` script, 모든 `data-ez-*` / `data-ez="..."` 속성.  
**유지:** `module="..."`, `@import`/`@css`/`@js`, `ez-align-*` **CSS 클래스**.

> ⚠️ paransky97용 `STRIP-MANIFEST.txt`·로컬 백업 스냅샷은 **워크스페이스에 없음** (nookitokki002만 2026-06-19 기록 존재). strip 시점·실행 로그는 **WORK-GUIDE §18 타임라인**으로 역추적.

### Phase C-2 — EZ 런타임(head) 제거

[`WORK-GUIDE` §15 EZST 절](WORK-GUIDE.md) 4종:

| 항목 | skin14 layout (API) | base layout (API) |
|------|---------------------|-------------------|
| `EZST` 초기화 script | **0** | 1 |
| `@js(/ez/init.js)` | **0** | 1 |
| `<ez-prop>` | **0** | 1 |
| `data-ez-*` | **0** | 1+ |

**의존성 처리:** `layout/basic/js/main.js` 79행 `EZST.register` **잔존**, 5행 `new Swiper` **앞** — layout에서 EZST stub 제거해도 슬라이더는 이미 초기화된 뒤라 라이브에서 `EZST` 0건·슬라이더 정상 ([§15 안전 절차](WORK-GUIDE.md)).

**삭제하지 않은 것:** `ez/` 폴더·`ez-settings.json`·`ez-module.html` (IDIO도 죽은 껍데기로 유지).

### Phase C-3 — `_nk/` 독립 레이어 (strip만으로 끝나지 않음)

strip 후 **구조 마이그레이션**이 핵심 후속 작업 ([`WORK-GUIDE` §18-9](WORK-GUIDE.md)):

| 항목 | 전 (EZ/base) | 후 (skin14) |
|------|--------------|-------------|
| 헤더 import | `@import(/layout/basic/header.html)` | `@import(/_nk/inc/header.html)` |
| 푸터 import | base footer | `@import(/_nk/inc/footer.html)` |
| GNB | `data-ez-module="menu-main"` (skin10) | `_nk/inc/menu.html` → `module="Layout_category"` |
| body ID | — | `body id="nk-skin14"` |
| 메인 | EZ `data-ez-module="product-list/N"` | `index.html` → `@import(/_nk/inc/*.html)` 섹션 조각 |
| 백업 | — | `_nk/_backup_header_layoutbasic.html` 등 |

`layout/basic/header.html`은 **strip된 레거시 사본**으로 SFTP에 남아 있으나, **layout.html·main.html은 `_nk`만 import** — 라이브는 `nk-hd` 커스텀 헤더 사용.

### Phase C-4 — EZ CSS 잔재 무력화 (HTML strip 외)

| 작업 | 근거 |
|------|------|
| `body#nk-skin14 { max-width:none!important }` | `layout.css`에 `max-width:1480px` **파일 자체는 미삭제**, CSS로 해제 |
| `html/body { overflow-x:clip }` | sticky PDP 실패 방지 (§18-7) |
| `find css/module layout/basic/css` perl 토큰화 | 골드·흰박스 박멸 (§18-6) |
| toparea 제거·헤더 80px·드로어 z-index | §18-8~10 |

### Phase D — 검증 (문서화된 QA)

- 2026-06-03~04: PC 1440 / MO 390 전 페이지 QA — 치명 버그 0 ([`WORK-GUIDE` §18-10 (A)](WORK-GUIDE.md))
- 키트 `verify-loop` 9종 score 100: **paransky URL용 스크립트화는 미완** ([`REMAINING-WORK-CHECKLIST.md`](REMAINING-WORK-CHECKLIST.md) §C)

---

## 3. Before / After — 실측 마커

### 3.1 API 소스 비교 (2026-06-19)

| 파일 | skin14 (16) | base (1) | skin2 IDIO (4) |
|------|-------------|----------|----------------|
| `layout/basic/layout.html` `data-ez-*` | **0** | 1+ | 0 |
| `layout/basic/layout.html` `EZST` / `ez/init.js` | **0** | 각 1 | 0 |
| `index.html` `data-ez-module` | **0** | 7 | 0 |
| `index.html` `ez-prop` | **0** | 5 | 0 |
| `_nk/inc/header.html` `data-ez-*` | **3** | — | — |
| `_nk/inc/footer.html` `data-ez-*` | **6** | — | — |
| `_nk/inc/topBnr.html` `data-ez-*` | **3** | — | — |
| `layout/basic/css/layout.css` `body max-width` | 1480px (파일内) | 1760px | **없음** |
| `layout.css` 주석 | `아키테이블_style` | `오우이_style` | `아키테이블_style` |

### 3.2 라이브 HTML (2026-06-19 fetch)

| 마커 | 홈 | PDP |
|------|-----|-----|
| `data-ez-module` | 4 | 4 |
| `data-ez-` (총) | 12 | 12 |
| `ez-prop` | 0 | 0 |
| `EZST` / `/ez/init.js` | 0 | 0 |
| `CAFE24.MOBILE_WEB` | `false` | `false` |
| `body id` | `nk-skin14` | `nk-skin14` |
| `_nk/` 참조 | 35 | 0 (경로 상대) |
| `menu-main` | 0 | 0 |
| `Layout_category` | 2 | 2 |

**잔존 `data-ez` 위치 (라이브 홈):** `_nk/inc/header.html`·`topBnr`·`footer`의 `data-ez="module-…"` 및 `data-ez-module="user-defined/1"` (카페24 optimizer가 감싼 인라인 `<script>`), `aside`·`.bottom-nav`·`footer_margin` 등. **코어 상품·layout EZ 모듈은 제거됨.**

### 3.3 SFTP 구조 (루트 list, 2026-06-19)

```
/skin14/_nk/          ← 커스텀 레이어 (존재 확인)
/skin14/_class-demo/
/skin14/ez/           ← 폴더 유지 (삭제 안 함)
/skin14/layout/
/skin14/index.html    (1,113b — 섹션 import만)
```

---

## 4. 키트 Phase C 3옵션 대비 — 실제 선택

| 옵션 | 설명 | paransky97 |
|------|------|------------|
| **A. strip_ez.py 자동** | §15 정규식 일괄 | ✅ **코어 HTML에 적용** (layout·index·product 등 0건 달성) |
| **B. 수동 속성 제거** | 파일별 grep·삭제 | △ `_nk` 신규 작성 시 일부 `user-defined` EZ 래퍼 **의도적/잔존** |
| **C. `_nk` 레이어 대체** | header/footer/메인 재작성 | ✅ **주력** — strip 후 §18-9 마이그레이션 |
| **header/footer만 data-ez 유지** | ecudemo 스킵 패턴 | ❌ — paransky는 strip + `_nk` |
| **EZST 4종 head 제거** | layout/main | ✅ layout·main에서 **제거 확인** |
| **ez/ 폴더 삭제** | — | ❌ 유지 (IDIO 동일) |

**스코프 요약:**

| 영역 | strip 범위 |
|------|-----------|
| `layout/basic/layout.html`·`main.html` | ✅ data-ez 0, EZST 0, `_nk` import |
| `index.html`·`product/*.html` | ✅ data-ez 0 |
| `layout/basic/header.html`·`footer.html` | ✅ strip됐으나 **미사용**(레거시) |
| `_nk/inc/*.html` | ⚠️ **부분 잔존** (user-defined script 래퍼) |
| `layout/basic/js/main.js` | `EZST.register` 1행 잔존 (무해) |
| `css/module/**` | HTML 아님 — perl **토큰화**로 색상 EZ 잔재 제거 |

---

## 5. 키트 기본 전략에 대한 교훈 (`EZ-STRATEGY.md` 보강용)

1. **strip ≠ 끝** — paransky는 strip 직후 **`_nk/inc` 마이그레이션 + base CSS 토큰화**가 본체. Phase C를 「속성 제거」만으로 정의하면 과소평가.
2. **완전 0건 목표는 `_nk`까지** — layout 0이어도 `_nk/inc`에 `user-defined` EZ 래퍼가 남을 수 있음. IDIO급 목표면 **2차 strip** 또는 수동 정리 체크리스트 필요.
3. **`editor_type=E`는 strip 판정에 쓰지 말 것** — skin14는 E이나 FTP·HTML-clean 작업본.
4. **body max-width는 layout.css 파일 수정 없이** `body#nk-skin14` 오버라이드로 해결한 실증 사례 — IDIO는 원래 없음, EZ 출신만 해당.
5. **백업·manifest 습관** — nookitokki002는 `STRIP-MANIFEST.txt` 있음. paransky는 문서(§18)만 있어 **재현성 격차** → 향후 파일럿은 manifest 필수.
6. **라이브 프리뷰** — `?skin_no=skin14` 없이도 현재 대표가 skin14면 `nk-skin14` body 확인 가능.

---

## 6. 검증하지 못한 것 / 갭

| 갭 | 설명 |
|----|------|
| **strip 실행 로그·백업** | `_ez-backup/`·`mcp/backups/paransky97/` **워크스페이스 미발견**. 실행일·변경 파일 목록은 §18 타임라인으로만 추정 |
| **template-02 원본** | `strip_ez.py`·`IDIO-ANALYSIS.md`·skin10 `_nk/WORK-GUIDE.md` — OneDrive 경로, **이 repo에 없음** |
| **SFTP 하위 경로 list** | 루트 list 성공, `/skin14/_nk`·`/skin14/layout/basic` depth list **0건 반환**(세션 reset·경로 이슈 의심). API `read_page`로 대체 검증 |
| **`_nk/inc` 잔존 EZ** | 라이브 12건 — 2차 strip 필요 여부 **미결정**(기능 무관·optimizer 래퍼 가능성) |
| **대표 skin API 플래그** | `list_themes`에 usage만 표시, 라이브는 `nk-skin14`로 skin14 적용 추정 |
| **verify-loop 9/9** | paransky 전용 score 스크립트·기록 **키트 미완** |
| **워크플로 08 formal 게이트** | Phase A/B/C 사용자 「예」기록 없음 — 작업은 **WORK-GUIDE 시대에 선행 완료** |

---

## 7. 관련 문서·다음 작업

| 문서 | 용도 |
|------|------|
| [`clients/paransky97/.workflow.md`](../clients/paransky97/.workflow.md) | 몰별 Phase·실측 스켈레톤 |
| [`08-ez-three-step-pingpong.md`](../workflows/08-ez-three-step-pingpong.md) | 신규 몰 formal Phase C 절차 |
| [`REMAINING-WORK-CHECKLIST.md`](REMAINING-WORK-CHECKLIST.md) §C | paransky end-to-end 파일럿 잔여 |

**권장 후속 (조사 범위 외):**

- `_nk/inc/{header,footer,topBnr}.html` 2차 strip → 라이브 `data-ez` 0건
- `clients/paransky97` verify-loop 9/9 paransky URL 파라미터화
- strip 시 `STRIP-MANIFEST.txt` + SFTP 백업 표준화

---

## 부록 — SFTP 설정

- `mcp/config/sftp_paransky97.json` — **port 8008** (2026-06-19 확인, 수정 불필요)
- `write_allowed`: `/skin14`, `/skin16`, `/mobile`
- 비밀번호는 설정 파일·git에 **커밋하지 않음**. 채팅에 노출된 임시 비밀번호는 **만료 전 로테이션** 권장.
