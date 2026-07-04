# 워크플로우 08 — EZ 3단계 핑퐁 (HTML → EZ 덮기 → 선별 제거)

> **대상:** 레거시·신규 몰에서 **에이전트↔사용자 핑퐁**으로 EZ base를 빠르게 깔고, 필요 시만 EZ 잔재를 걷는 **압축 진입 경로**.  
> **상세 배경·Phase 0~4 전체:** [`07-ez-on-legacy-setup.md`](07-ez-on-legacy-setup.md) — 본 문서는 07의 **실행용 3단계 요약**이다.  
> **FTP·에이전트 canonical:** [`07` Phase 0-D](07-ez-on-legacy-setup.md#0-d-easy-타입-vs-html-타입--ftp-작업자-선택-f35) — HTML 복사 + EZ FTP overlay. **0-C(Easy 타입 추가)는 GUI 운영자 전용.**  
> **기본 전략:** Phase C **strip** (demo000 / skin14) — [`EZ-STRATEGY.md`](../../brain/docs/EZ-STRATEGY.md)  
> **파일럿 예외:** ecudemo400786 — Phase C **스킵** (레퍼런스 1:1 속도 파일럿, 템플릿 기본 아님)

---

## 타당성 판정 (솔직 요약)

| 판정 | **Partial Yes** — 조건 맞으면 빠름, 아니면 역효과 |
|------|-----------------------------------------------------|
| **빨라지는 조건** | 레거시 HTML 몰 + EZ 골격·모듈 필요 + **FTP 주력** + `_ref*/` 레이어 패턴 + Pre-flight(`06`) 선행 |
| **느려지거나 금지** | Easy **타입** 등록 후 FTP 대량 수정(**F35**) · layout만 교체(**F36-1**) · Pre-flight 생략(**F27**) · MO 사용함+반응형 혼용(**F28/F34**) |

### A) 디자인 목표에 더 빠른가? (Devil's advocate)

**Yes (조건부)**

- EZ skin16/아키테이블 등 **검증된 base**를 FTP로 올리면 `#container>#contents`·module·반응형 골격을 **처음부터 재작성하지 않아도** 됨.
- 에이전트 핑퐁으로 관리자 설정(MO·대표 skin)·FTP 업로드를 **게이트마다 분리**하면 ecudemo류 실수(92% width, paginate, `/m/` 분리)를 초기에 차단.
- Phase C **strip** 후 HTML-clean DOM이면 에이전트·FTP 편집·F27 회피에 유리 — **키트 기본** ([`EZ-STRATEGY.md`](../../brain/docs/EZ-STRATEGY.md)).

**NOT faster (언제 역효과)**

| 상황 | 이유 |
|------|------|
| 관리자 Easy GUI만으로 색·문구 수준 변경 | `01-quick-fix`가 더 빠름 — 3단계 오버킬 |
| 순수 레거시 HTML 유지·EZ 불필요 | Phase B 자체가 부담 (dual CSS·data-ez 잔재) |
| 관리자에 **Easy 타입** 추가 + FTP HTML 수정 | **F35** — GUI 메타 충돌·초기화 오류 |
| `layout.html`만 EZ로 교체 (통째 base 없음) | **F36** — module·CSS·MO 불일치 (07 전략 C) |
| strip **없이** `data-ez-*`만 유지한 채 장기 커스텀 | F27·detail.css·에이전트 markup 노이즈 — **파일럿 스킵**만 예외 ([`EZ-STRATEGY.md`](../../brain/docs/EZ-STRATEGY.md) §4) |
| 검증 루프 없이 「완료」 선언 | **F33** — score 100 미만 잔존 |
| 신규 몰·전면 커스텀 (구매템플릿급) | `02-skin-build-standard` + §15 전량 걷어내기가 최종 목표면, overlay 후 다시 strip하는 **이중 작업** |

### B) cafe24-agent-kit에서 3단계 핑퐁 가능한가?

**Yes — 이미 구성 요소 존재.** 추가 코드 없이 워크플로우·MCP·스크립트 조합으로 실행 가능.

| 필요 요소 | 키트 내 위치 |
|-----------|-------------|
| 워크플로우·함정 | `01_작업하기/workflows/07`, `06`, 본 문서 `08` |
| EZ 걷어내기 | `brain/docs/WORK-GUIDE.md` §15, `strip_ez.py` |
| MCP SFTP/API | `cafe24_sftp_*`, `cafe24_list_themes` 등 |
| 검증 | `06-verify-loop.md`, `work/scripts/ref*-score-*.py` |
| 부트스트랩 (선택) | `get_kit_guides` — `HYBRID-ARCHITECTURE-DRAFT.md` Phase 1 |

**세팅 순서 (최소)**

1. `/접속세팅` — OAuth·SFTP·`clients/{몰}/`  
2. (선택) MCP `get_kit_guides` → `workflow_id: 08-ez-three-step-pingpong`  
3. `clients/{몰}/.workflow.md` 에 Phase A/B/C 상태 기록  
4. 본 문서 Phase별 핑퐁 — **한 Phase씩** 사용자 「예」 후 FTP

---

## 3단계 ↔ 07 매핑

| 본 문서 | 사용자 말하기 | 07 대응 | 기본 (demo000) | ecudemo400786 (예외) |
|---------|--------------|---------|-------------------|----------------------|
| **Phase A** | HTML 추가 (관리자 복사) | Phase 0-C/D, Phase 1 | HTML 타입 작업 skin | HTML 타입 작업 skin |
| **Phase B** | EZ 덮기 (FTP overlay) | Phase 1-B + Phase 2 | EZ base + `_ref*/` | skin16 → `/sde_design/base/` + `_ref393674/` |
| **Phase C** | EZ strip → HTML-clean | STEP 2 / §15 — **기본** | **strip** — `data-ez` False | **스킵** — `data-ez` 유지, CSS override |

> **이름 주의:** 「Easy」= 관리자 **스마트디자인Easy 타입**(F35 위험). 본 워크플로우 Phase B는 **EZ 테마 코드**(skin16·아키테이블) FTP 이식이며, **Easy 타입 디자인 추가가 아님**. → [`07` Phase 0-D](07-ez-on-legacy-setup.md)

---

## Phase A — HTML 작업 skin 확보 (관리자 · 코드 금지)

**목표:** 대표 레거시는 건드리지 않고, **HTML 타입** 작업용 skin 복사본 확보 + MO 반응형 전제.

> **Canonical:** 본 Phase는 [`07` Phase 0-D](07-ez-on-legacy-setup.md#0-d-easy-타입-vs-html-타입--ftp-작업자-선택-f35)의 FTP 1~2단계와 동일. **Easy 타입 디자인 추가(07 Phase 0-C)는 하지 않음.**

### Agent gate (진입 조건)

- [ ] `/접속세팅` 완료
- [ ] `cafe24_list_themes` 또는 사용자 답으로 **대표 skin·editor_type** 확정
- [ ] Phase A에서 **FTP 업로드 금지** (진단·질문만)

### Agent checklist (MCP)

| 항목 | 도구/방법 |
|------|-----------|
| editor_type | API themes — H=HTML, E=Easy |
| FTP 루트 | `nlst` — `/skinN` vs `/sde_design/base` |
| 라이브 layout | `layout/basic/layout.html` 샘플 읽기 — 레거시 vs EZ 여부 |

### 사용자 핑퐁 (복붙)

```
[Phase A — HTML 작업 skin]
1. 관리자 → 디자인 보관함: 현재 PC **대표 디자인** 이름·skin 번호·타입(HTML/Easy)?
2. 쇼핑몰 설정 → 모바일 → 「모바일 전용 디자인 사용설정」 **사용안함** 으로 바꿨나요? (반응형 EZ 필수)
3. 작업용으로 **HTML 타입 skin 복사** 완료했나요? (이름 예: HTML-work-202606) — 「아직」이면 복사 후 skin 번호 알려주세요.
4. 복사 skin을 **아직 대표로 바꾸지 마세요** — 비대표 테스트로 둡니다.
```

### MCP/FTP actions (사용자 「예」 후)

- **관리자 (사용자):** MO 사용안함 저장 · HTML skin **복사** (상속 skin 작업 금지)
- **에이전트:** 복사 skin FTP 경로 확인 · `layout.html` 존재·`#contents` 유무 기록
- **금지:** Easy 타입 디자인 추가 · 대표 전환 · skin1(원본) 수정

### Verify checkpoint

| 체크 | PASS |
|------|------|
| 작업 skin `editor_type` = HTML (H) | API/관리자 일치 |
| MO 전용 = 사용안함 | 사용자 확인 + (Phase B 후) `CAFE24.MOBILE_WEB=false` |
| 복사 skin FTP 접근 가능 | `nlst` 성공 |

### F-codes

- **F34** — MO 설정 미확인
- **F35** — Easy 타입 추가 시도

### Phase A → B 게이트

표 채움 + 사용자 1~4 답변 + 작업 skin 번호 확정. MO 미확인 시 Phase B 금지.

---

## Phase B — EZ 코드 FTP overlay + `_ref*/` 레이어

**목표:** EZ base( skin16·아키테이블 등)를 작업 skin에 **선별 이식**, 커스텀은 `_ref{id}/` 만.

### Agent gate

- [ ] Phase A PASS
- [ ] EZ 소스 확정 (skin16 / 타 몰 FTP / 디자인 라이브러리 EZ 추가 후 다운로드)
- [ ] 업로드 전 **diff·파일 목록** 사용자에게 제시

### 사용자 핑퐁 (복붙)

```
[Phase B — EZ overlay]
진단: 작업 skin={번호}, FTP={경로}, EZ 소스={skin16|아키테이블|기타}.
1. EZ base를 **통째** 올릴까요, **layout+필수 module+css**만 선별할까요? (권장: 선별 — F36)
2. 커스텀 레이어 폴더명: _ref{몰ID또는작업ID} (예: _ref393674) — 동의하시면 「예」
3. layout.html 링크 추가만 하고 EZ core·skin1은 읽기 전용 — diff 확인 후 「업로드 예」 해주세요.
```

### MCP/FTP actions

| 단계 | 액션 |
|------|------|
| 1 | EZ 소스에서 `layout/basic/`, `css/ec-base-*`, 필수 `js/`, `product/`, `index.html` 등 **목록 확정** (통째 vs 선별 — 사용자 답) |
| 2 | `MSYS_NO_PATHCONV=1` 로 대상 skin 업로드 (`open_remote` / `sftp_push`) |
| 3 | `_ref{id}/` 생성 — `css/base.css` (#contents 첫 블록), `sub.css`, `sub-paginate.css`, `js/layout.js` |
| 4 | `layout.html` — head `base.css`, body 끝 `sub-paginate.css` 링크만 추가 |
| 5 | **금지:** `skin1`·`ec-base-*` 직접 수정 · `@css` core에 `?v=` (**F3/F4**) |

### Verify checkpoint (Pre-flight — Phase B 직후 필수)

[`06-verify-loop.md`](06-verify-loop.md) Phase 0 · 0.5:

```
[Phase B 검증]
- layout에 data-ez-* + #container>#contents: {있음|없음}
- C1 #contents @390px: {PASS|FAIL} (width={N}px) — FAIL이면 Phase C 금지, base.css 수정
- MOBILE_WEB: {true|false}
- paginate spot-check: {PASS|FAIL}
```

자동화 (가능 시): `python work/scripts/ref393674-score-mobile-full.py` → **C1=100** 전까지 Phase C·페이지 작업 금지.

### F-codes

- **F27** — #contents 92%
- **F28** — `/m/` 별도 스킨
- **F36** — 통째 덮기·ez-settings 무분별 삭제
- **F3** — 캐시로 FAIL 오판

### Phase B → C 게이트

Pre-flight PASS (최소 C1 PASS + MOBILE_WEB false). FAIL 시 `_ref*/base.css`·layout 링크만 수정 후 재측정.

---

## Phase C — EZ strip (HTML-clean) — **기본 경로**

**목표:** Phase B overlay 직후 `data-ez-*`·`<ez-prop>` 제거 → **HTML-clean DOM** (demo000 / skin14 패턴).  
**전략 상세·이유:** [`EZ-STRATEGY.md`](../../brain/docs/EZ-STRATEGY.md)

### 권장 절차 (단일 경로)

1. Pre-flight PASS 확인 (C1·MOBILE_WEB)
2. `_ez-backup/` 백업
3. `strip_ez.py` 미리보기 → 대상 파일 `--write` ([`WORK-GUIDE` §15](../../brain/docs/WORK-GUIDE.md))
4. FTP 업로드 — `ez/ez-module.html`·`smart-banner/init/` 등 **시스템 파일 유지**
5. `data-ez` 잔여 0 grep · `module="..."` 카페24 코어 생존 확인
6. (필요 시) EZST 4종 제거 — `main.js` EZST vs Swiper 순서 확인 후
7. [`06-verify-loop.md`](06-verify-loop.md) — score **100 only**

```bash
# 미리보기
python3 strip_ez.py src/skinNN/product/list.html
# 적용
python3 strip_ez.py src/skinNN/product/list.html --write
```

**대상 파일 (보통):** `index.html`, `layout/basic/{header,footer,layout,main,sidebar}.html`, `product/{detail,list}.html`

### Agent gate

- [ ] Phase B Pre-flight PASS
- [ ] `_ez-backup/` 백업 완료
- [ ] strip 대상 파일 목록 확정 (기본: §15 표준 세트)

### 사용자 핑퐁 (복붙)

```
[Phase C — EZ strip (기본)]
Pre-flight PASS했습니다. demo000/skin14 패턴으로 EZ 속성을 제거합니다.
1. 백업(_ez-backup/) 확인 후 strip_ez 미리보기 diff를 보내드립니다.
2. 「업로드 예」 주시면 FTP 반영 → data-ez 0건·module= 생존 검증합니다.
3. 메인 슬라이더·장바구니·결제 1회 수동 확인 부탁드립니다.

※ 빠른 파일럿으로 EZ 유지만 하려면 ecudemo400786 스킵 예외를 참고하세요 — 신규 몰 기본은 strip입니다.
   → brain/docs/EZ-STRATEGY.md §4
```

### Verify checkpoint

| 체크 | PASS |
|------|------|
| strip 파일 `data-ez` / `<ez-prop>` 0 | grep 0건 |
| `module="product_listnormal"` 등 카페24 코어 | 생존 |
| EZST 제거 시 | Console 에러 없음 · 슬라이더·장바구니 동작 |
| verify-loop | 전 스크립트 **100** |

### F-codes

- **F36** — 무분별 ez-settings/EZST 삭제 · 통째 덮기
- **F8** — GNB (strip 후 `Layout_category` 또는 `_nk` 헤더로 대체)
- WORK-GUIDE §15 — EZST 제거 후 슬라이더 깨짐

### 파일럿 예외 — ecudemo400786 (스킵)

> **템플릿 기본이 아님.** 레퍼런스 1:1 **속도 파일럿**에서만 Phase C를 생략했다.  
> `data-ez-*` 유지 + `_ref393674/` CSS override → 9/9 score 100.  
> → `clients/ecudemo400786/.workflow.md` · [`EZ-STRATEGY.md` §4](../../brain/docs/EZ-STRATEGY.md)

### Phase C → 다음 워크플로우

| 다음 | 조건 |
|------|------|
| `05-reference-intake` | 레퍼런스 URL 있음 |
| `06-verify-loop` | 구현 중 자기검증 |
| `03-reference-renewal` | 1:1 구현 |
| `02-skin-build-standard` | 전량 제거 후 대규모 빌드 |

---

## 에이전트 핑퐁 프롬프트 템플릿

### 진입 (한 방)

```
/카페24-워크플로우
워크플로우: 08-ez-three-step-pingpong
몰ID: {mall_id}
레퍼런스: {url 또는 없음}
Phase A부터. 코드·FTP 수정 금지, 진단표+질문만.
```

### Phase 단위

```
08-ez-three-step-pingpong Phase {A|B|C}만 실행.
게이트 체크리스트 채우고 사용자 질문 블록 복붙 형태로 보내줘.
{B|C}에서 FTP는 내 「업로드 예」 전까지 diff만.
```

### ecudemo postmortem (파일럿 예외)

```
ecudemo400786: Phase C 스킵은 파일럿 예외 — 신규 몰 기본은 strip (EZ-STRATEGY.md).
지금 증상이 F27/F28/F36 중 뭔지 매핑. 한 Phase만 수정 파일 경로 제안.
```

---

## 관련 워크플로우

| 문서 | 관계 |
|------|------|
| [`07-ez-on-legacy-setup.md`](07-ez-on-legacy-setup.md) | 전체 Phase 0~4·판정 근거·0-D F35 |
| [`06-verify-loop.md`](06-verify-loop.md) | Phase B 이후 필수 검증 |
| [`05-reference-intake.md`](05-reference-intake.md) | 레퍼런스 있을 때 Phase C 다음 |
| [`02-skin-build-standard.md`](02-skin-build-standard.md) | Phase C 전량(구매템플릿) 후 |

---

## 진입 명령

```
/카페24-워크플로우 시작
워크플로우: 08-ez-three-step-pingpong
```

또는:

```
레거시 몰 EZ 3단계 핑퐁 — HTML skin 복사 → EZ FTP overlay → strip (기본).
08 문서 Phase A부터. 레퍼런스: https://demo000.cafe24.com/
```
