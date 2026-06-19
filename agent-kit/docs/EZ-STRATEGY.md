# EZ 전략 — 기본은 strip (demo000 / skin14 패턴)

> **갱신:** 2026-06-19  
> **목적:** 워크플로우 08 Phase C에서 A/B/C 분기로 혼란이 생기지 않도록, **키트 기본 전략**과 그 **이유**를 한곳에 정리한다.  
> **레퍼런스 몰:** [https://demo000.cafe24.com/](https://demo000.cafe24.com/)  
> **실행 절차:** [`WORK-GUIDE.md` §15](WORK-GUIDE.md) · [`08-ez-three-step-pingpong.md`](../workflows/08-ez-three-step-pingpong.md) Phase C

---

## 0. 한 줄 결론

| 항목 | 내용 |
|------|------|
| **기본 전략** | Phase B(EZ FTP overlay) 직후 **Phase C strip** — `data-ez-*`·`<ez-prop>` 제거, HTML-clean DOM으로 전환 (demo000 / skin14) |
| **템플릿 방향** | IDIO(skin2)와 동일 — EZ 출신 아키테이블을 **걷어낸 뒤** `_nk/`·에이전트/FTP로 자유 편집 |
| **예외 (파일럿)** | ecudemo400786 — Phase C **스킵**, `data-ez-*` 유지 + `_ref393674/` CSS override만. **템플릿 기본이 아님** |

---

## 1. 왜 strip이 기본인가

### 1.1 HTML 타입 + clean DOM = 에이전트·FTP 작업에 맞음

- 키트 canonical은 **관리자 HTML 타입 skin 복사 + FTP overlay** ([`07` Phase 0-D](../workflows/07-ez-on-legacy-setup.md)) — Easy 타입 등록 없음 (**F35** 회피).
- overlay 후에도 `data-ez-module`·`<ez-prop>`이 남으면 마크업이 EZ 편집기 메타에 묶여, 에이전트가 HTML을 직접 읽고 수정하기 어렵다.
- strip 후에는 `module="..."` 카페24 코어만 남고, 헤더·메인·PLP를 **일반 스마트디자인**처럼 다룰 수 있다.

### 1.2 알려진 함정 회피

| 함정 | strip 없이 EZ 잔존 시 | strip 후 |
|------|----------------------|----------|
| **F27** `#contents` 92% | MO 히어로 좌우 흰 gap — `_ref` CSS만으로 반복 수정 | EZ 레이아웃 옵션·`.myshopArea` calc 잔재와 충돌 감소 |
| **detail.css late-load** | PDP·서브에서 EZ 테마 CSS가 늦게 로드되어 override 전쟁 | HTML-clean + `#nk-skinN` 스코프로 예측 가능 |
| **data-ez-module 노이즈** | grep·diff·에이전트 컨텍스트 오염, 「어느 속성이 라이브인지」 혼란 | `data-ez` 0건 목표 — `VERIFICATION-EVIDENCE.md` skin14 실측 |

### 1.3 IDIO / skin2 수준 유지보수

- IDIO는 아키테이블 EZ를 베이스로 가져온 뒤 **EZ 기능을 전부 걷어냈다** ([`WORK-GUIDE.md` §0 결론 2](WORK-GUIDE.md)).
- demo000 skin14: `layout.html` **data-ez False** (base는 True) — overlay·strip이 끝난 **목표 상태**의 실측 증거.
- 장기적으로 재판매 템플릿·클라이언트 커스텀은 이 수준의 **독립 레이어**(`_nk/`, `_ref*/`)가 표준이다.

### 1.4 F35 — Easy admin 타입은 등록하지 않는다

- **절대:** 관리자에 스마트디자인 **Easy 타입** 디자인을 추가한 뒤 FTP로 HTML 대량 수정 (**F35**).
- **허용:** HTML 타입 skin에 EZ **테마 코드**만 FTP로 올린 다음, 코드 레벨에서 strip ([`07` Phase 0-D](../workflows/07-ez-on-legacy-setup.md)).
- strip은 「GUI EZ를 포기하고 HTML로 간다」는 뜻이 아니라, **처음부터 HTML 타입으로 작업**하기 위한 정리 단계다.

---

## 2. strip 시 잃는 것 (솔직한 tradeoff)

| 잃는 것 | 완화 |
|---------|------|
| EZST 스마트배너 **관리자 GUI** 편집 | HTML/이미지 직접 제작 · `_nk/inc/` 배너 · Swiper 등 독자 JS ([`WORK-GUIDE` §15 EZST 제거](WORK-GUIDE.md)) |
| header `data-ez-module` 기반 GNB 옵션 패널 | `module="Layout_category"` 또는 커스텀 `_nk` 헤더로 대체 (IDIO 패턴) |
| EZ 테마 색·옵션 실시간 미리보기 | 디자인 토큰·`custom.css` + verify-loop score 100 |

> strip 전 **백업** (`_ez-backup/`) 필수. `ez/ez-module.html`·`smart-banner/init/` 등 시스템 파일은 삭제하지 않는다 (§15 표).

---

## 3. 워크플로우 08에서의 위치

```
Phase A  HTML 타입 작업 skin 복사 · MO 사용안함
    ↓
Phase B  EZ base FTP overlay + _ref*/ 레이어 · Pre-flight C1 PASS
    ↓
Phase C  ★ 기본: strip (§15 + strip_ez.py) · EZST 4종 제거 검토
    ↓
05-reference-intake / 03-reference-renewal / 02-skin-build-standard
```

- **도구:** `strip_ez.py` 미리보기 → `--write` → FTP 업로드 → `data-ez` 잔여 0 grep → (필요 시) EZST 4종 제거 · `main.js` EZST 의존성 확인.
- **검증:** [`06-verify-loop.md`](../workflows/06-verify-loop.md) — score **100 only**.

---

## 4. ecudemo400786 — 파일럿 예외 (스킵)

| 항목 | ecudemo400786 | demo000 (템플릿) |
|------|---------------|---------------------|
| Phase C | **스킵** — `data-ez-*` 유지 | **strip** — data-ez False 목표 |
| 목적 | 레퍼런스(ecudemo393674) **1:1 속도** 파일럿 | 신규 템플릿·운영 몰 **표준 방향** |
| 커스텀 | `_ref393674/` CSS override만 | strip + `_nk/` / `_ref*/` HTML·CSS |
| 계정 | 파트너 · `/sde_design/base/` | 일반 몰 · `/skin14` 등 |

**왜 스킵했나 (당시):** Phase A/B 완료 후 레퍼런스 갭을 CSS로 빠르게 메우는 파일럿 — strip 없이도 9/9 score 100 달성. **이 경로를 키트 기본으로 삼지 않는다.**

- 상세: `clients/ecudemo400786/.workflow.md` · [`getting-started/예시-데모몰.md`](../getting-started/예시-데모몰.md)
- ecudemo 폴더·이력은 **삭제·재작성하지 않음** — 「빠른 파일럿 예외」로만 참조.

---

## 5. 레퍼런스 몰 — demo000

| 항목 | 값 |
|------|-----|
| URL | [https://demo000.cafe24.com/](https://demo000.cafe24.com/) |
| 작업 skin | skin14 (아키테이블 EZ 출신 → strip 완료 방향) |
| SFTP | `/{skin_code}` (예: `/skin14`) — `VERIFICATION-EVIDENCE.md` |
| data-ez (layout) | skin14 **False** · base **True** (2026-06-19 실측) |
| 이전 주 레퍼런스 | ecudemo393674 — **1:1 갱신 파일럿용**. 신규 템플릿 기본 레퍼런스는 demo000 |

---

## 6. 관련 문서

| 문서 | 용도 |
|------|------|
| [`WORK-GUIDE.md` §0·§15·§18](WORK-GUIDE.md) | EZ 걷어내기·skin14 실증·우리화 지침 |
| [`08-ez-three-step-pingpong.md`](../workflows/08-ez-three-step-pingpong.md) | Phase A/B/C 실행·핑퐁 |
| [`07-ez-on-legacy-setup.md`](../workflows/07-ez-on-legacy-setup.md) | Phase 0-D F35 · 전체 배경 |
| [`common-pitfalls.md` §F35·F36](common-pitfalls.md) | Easy 타입 충돌 · strip 함정 |
| `REMAINING-WORK-CHECKLIST.md` §C | demo000 end-to-end 파일럿 |
