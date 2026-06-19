# 템플릿 파일럿 수용 기준 (TEMPLATE-PILOT)

> **목적:** agent-kit이 “진짜로 동작한다”는 것을 **한 몰·한 템플릿**으로 end-to-end 증명하는 기준.  
> 작성: 2026-06-19

---

## 1. 파일럿 정의 (둘 중 하나)

| 경로 | 설명 | 현재 상태 |
|------|------|-----------|
| **A. 신규 템플릿** | 워크플로우 **08** (HTML skin + EZ FTP overlay + **Phase C strip**)로 **처음부터** 한 몰 완성 | 후보: [paransky97.cafe24.com](https://paransky97.cafe24.com/) |
| **B. 레퍼런스 마무리** | **ecudemo400786** — ecudemo393674 대비 verify-loop **전 페이지 100점** | **현재 파일럿 몰** — **9/9 스크립트 PASS** (2026-06-19 closeout 실측) |

> **현재 파일럿 몰:** `ecudemo400786`  
> 상세: [`getting-started/예시-데모몰.md`](../getting-started/예시-데모몰.md), [`workflows/08-ez-three-step-pingpong.md`](../workflows/08-ez-three-step-pingpong.md)

---

## 2. Done 기준 (PASS = 100만 인정)

### 2.1 자동 채점 (필수)

대상 몰 URL에 대해 `work/scripts/ref*-score-*.py` **전부** 실행:

| 스크립트 | 페이지 타입 | 필수 |
|----------|-------------|------|
| `ref393674-score-mobile-full.py` | 공통 MO preflight + 다페이지 | ✅ |
| `ref393674-score-header.py` | 헤더 (Info·검색) | ✅ |
| `ref393674-score-plp.py` | PLP | ✅ |
| `ref393674-score-pdp.py` | PDP | ✅ |
| `ref393674-score-basket.py` | 장바구니 | ✅ |
| `ref393674-score-member.py` | 회원(login) | ✅ |
| `ref393674-score-board.py` | 게시판 | ✅ |
| `ref393674-score-page.py` | 정적(About 등) | ✅ |
| `ref393674-score-paginate.py` | 페이징 전역 | ✅ |

**합격:** 각 스크립트 `total_score == 100` **및** `pass: true`.  
**불합격:** 100 미만이면 해당 FAIL 항목만 수정 → FTP → 재실측 (`workflows/06-verify-loop.md`).

### 2.2 MOBILE_WEB=false (필수, 수동+자동)

1. 관리자: 쇼핑몰 설정 → 모바일 → **「모바일 전용 디자인 사용설정」 사용안함**
2. 라이브 소스: `CAFE24.MOBILE_WEB=false` 확인 (`rules/responsive-mobile.md`)
3. `mobile-full` 스크립트 check **C1** (`#contents` 92% trap) PASS

> MCP·FTP로 관리자 설정 변경 불가 — 에이전트는 **탐지·중단·안내**만.

### 2.3 페이지 타입 최소 커버리지

| 타입 | 대표 URL 패턴 | score 스크립트 |
|------|---------------|----------------|
| main | `/` | mobile-full, header |
| PLP | `/product/list.html?cate_no=*` | plp |
| PDP | `/product/.../display/1/` | pdp |
| cart | `/order/basket.html` | basket |
| member | `/member/login.html` | member |
| board | 게시판 목록 | board |

### 2.4 에이전트 핑퐁 게이트 (워크플로우 08)

Phase A / B / C 각각 **사용자 「예」** 후 다음 단계 진행.  
기록 위치: `clients/{mall}/.workflow.md` (또는 `work/clients/{mall}/` 보조 로그)

| Phase | 사용자 확인 내용 | `.workflow.md` 기록 |
|-------|------------------|---------------------|
| **A** | HTML 타입 작업 skin 복사, MO 사용안함, 대표 미전환 | Phase A ✅ + 일시 |
| **B** | EZ base FTP overlay (`/sde_design/base/` + `_ref*/`) | Phase B ✅ + 일시 |
| **C** | 선별 EZ strip 또는 **스킵** (ecudemo: 스킵) | Phase C ✅/스킵 + 사유 |

---

## 3. 타임박스 제안

| 단계 | 권장 기간 | 산출물 |
|------|-----------|--------|
| 접속·Phase A | 0.5일 | OAuth/SFTP, `.workflow.md`, MO=false 확인 |
| Phase B overlay | 1–2일 | base + `_ref*/` FTP, layout 링크 |
| verify-loop (06) | 2–4일 | 9개 score 스크립트 전부 100 |
| Phase C (선택) | 0–1일 | strip 또는 스킵 문서화 |
| **파일럿 합격 판정** | — | 본 문서 §2 전항 PASS |

**총 권장:** 신규 템플릿 **5–8일**. ecudemo400786 B경로는 **9/9 PASS 완료** (2026-06-19).

---

## 4. 파일럿에 **불필요**한 것 (범위 밖)

| 항목 | 이유 |
|------|------|
| **npm 패키지** (`@cafe24/mcp-agent-kit`) | Phase 3 선택 — [`HYBRID-ARCHITECTURE-DRAFT.md`](HYBRID-ARCHITECTURE-DRAFT.md) |
| **전체 `run_preflight`** (모든 check 타입) | Phase 2 — 파일럿은 CLI score 스크립트 직접 실행으로 충분 |
| **전 페이지 스크린샷 diff** | 03-reference-renewal §6 — 100점 이후 선택 |
| **Easy 타입 관리자 등록** | F35 — HTML 타입 + EZ FTP만 |
| **모바일 전용 `/m/` 스킨** | F28/F34 — 반응형 단일 URL만 |
| **다른 몰 score 스크립트 일반화** | 파일럿 후 kit-roadmap |

**최소 MCP:** `get_kit_guides` + `cafe24_*` 8종 + (선택) `run_preflight` stub 1 check.

---

## 5. 판정 체크리스트 (한 장)

```
[ ] clients/{mall}/.workflow.md — Phase A/B/C 사용자 「예」 기록
[ ] CAFE24.MOBILE_WEB=false 확인
[ ] 9개 ref*-score-*.py → 전부 total_score=100, pass=true
[ ] 페이지 타입: main / PLP / PDP / cart / member / board 커버
[ ] (선택) MCP run_preflight(check=header) → CLI와 동일 점수
```

**합격 선언:** 위 필수 항목 전부 ✅ + 담당자 1회 라이브 스팟체크 (PC+390px).

---

## 6. 관련 문서

- [`workflows/06-verify-loop.md`](../workflows/06-verify-loop.md) — 채점 루프
- [`workflows/08-ez-three-step-pingpong.md`](../workflows/08-ez-three-step-pingpong.md) — 3단계 핑퐁
- [`HYBRID-ARCHITECTURE-DRAFT.md`](HYBRID-ARCHITECTURE-DRAFT.md) — MCP Phase 1–2
- [`getting-started/예시-데모몰.md`](../getting-started/예시-데모몰.md) — ecudemo Ref/Tgt
