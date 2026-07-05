# 페이지별 에이전트 오케스트레이션 (정본)

> 메인 세션 = **상위 지휘자 only**. 하위 에이전트 = **페이지 1개 담당 executor**.  
> 디자인 기준: `design.md` + `component-gallery.html` (외부 DS·아루나 참조 **사용 안 함**).

---

## 1. 에이전트 배치 구조

### 1-1. 시작 — 전체 페이지 목록 제시 (Human gate)

메인 세션 **첫 액션**: 이 몰의 전체 페이지를 타입별로 나열해 **사용자에게 보여줄 것**.

**데이터 소스** (우선순위):

1. `clients/{몰}/04_design/wave4-page-queue.md` — 타입별 URL·모듈 인벤토리
2. `clients/{몰}/04_design/wave4-status.md` — 193 URL 전수
3. `clients/{몰}/04_design/blank-slate-rebuild-queue.md` — blank-slate 진행 상태

**표시 형식** (최소):

| § | 타입 | 대표 URL 수 | 소스 경로 | blank-slate 상태 |
|---|------|:---:|---|---|
| 1 | 메인 | 1 | `layout/basic/main.html` + inc | —/WIP/PASS |
| 2 | PLP | 3+ | `product/list.html` … | |
| … | | | | |

사용자가 목록·순서를 확인하기 전 **하위 에이전트 착수 금지**.

### 1-2. 페이지 1개 = 하위 에이전트 1개

- **메인**: `Task`로 하위 에이전트 launch — `templates/page-agent-brief.md`를 채워 **그대로** 전달.
- **메인 금지**: 담당 페이지의 HTML/CSS **직접 작성·수정**.
- **병렬**: 파일 mutex 충돌 없을 때만 (동일 `nk-*.css` 동시 writer 금지 → `wave4-group-orchestration.md` §3).

**페이지 단위 정의**:

- 기본 = **wave4-page-queue §N-A의 URL 1행** (또는 동일 소스 파일 1개)
- inc 조각만 단독 작업 시: `nk-header.html` 등 — queue에 명시된 경우만

### 1-3. 하위 에이전트 내부 분해

담당 페이지 안에서 **반드시 이 순서**:

```
섹션(section / module 밖 nk-* 래퍼)
  → 모듈(module="" 블록 단위)
    → 유닛(폼 row · 카드 1칸 · 탭 패널 · 테이블 thead 등)
```

각 유닛에 **동일한 공통 작업 규칙** 적용 (§2).

### 1-4. 전 페이지 후 — 메인 통합 검수

모든 하위 에이전트 **페이지별 PASS** 후, 메인 세션이만 수행:

| 검수 축 | 확인 |
|---------|------|
| 클래스 네이밍 | `nk-` 접두사 · 페이지 간 동일 역할 = 동일 BEM 블록 (`nk-prd`, `nk-mbr-form` …) |
| 토큰 | `var(--nk-*)` only · `design.md` / `nk-tokens.css` 불일치 0 |
| 컴포넌트 재사용 | `component-gallery.html` 패턴 중복 구현 없음 |
| CSS writer | 타입별 단일 파일 (`nk-order.css` 등) · 충돌 diff 없음 |
| queue 동기화 | `blank-slate-rebuild-queue.md` 해당 행 PASS |

통합 검수 PASS 후에만 **전체 완료** 보고 (§4).

---

## 2. 공통 작업 규칙 (모든 하위 에이전트 동일)

> **단순 CSS 교체가 아님** — module **안쪽** 마크업을 `design.md`·`component-gallery` 패턴으로 **재구성**.

### 2-1. 자유롭게 바꿔도 되는 것 (L2 Inner — DISCARD → NEW)

- `module=""` 태그 **안쪽** div/li/span 구조·순서·개수·wrapper
- 클래스 체계 (`nk-` 접두사 신규 부여)
- 요소 배치 (flex/grid, hover 노출, 시각 계층)
- stock `ec-base-*` 골격 제거

### 2-2. 절대 유지 (L1 Binding — 모듈 계약)

| 항목 | 규칙 |
|------|------|
| `module="..."` | 속성·모듈명 · 설정변수 주석(줄바꿈 포함) |
| `{$...}` | 변수명 변경 금지 · module 안에서만 |
| `anchorBoxId` | 재구성 후에도 **≥2개 나란히** (1개 = 상품 1개만 출력) |
| form | `name`/`id`/`action`/`onclick` must-not-break |
| EZ 잔존 시 | `data-ez-*`, `<ez-prop>`, `<ez-var>` on header/footer — **삭제 금지** |

상세 체크: `module-contract-checklist.md`

### 2-3. CSS 규칙 (하위 에이전트)

- 해당 페이지 타입 **단일 writer** 파일만 수정 (`nk-board.css` 등)
- `/layout/basic/css/`, `/css/module/` **직접 수정 금지**
- 인라인 `style=""` 금지 · italic 금지 · 토큰 하드코딩 금지

---

## 3. 페이지별 진행 순서 (하위 에이전트 공통)

```
Step A — 3단 비교표 작성 → 사용자 확인 대기
Step B — 승인된 페이지만 코드 재작성
Step C — code-reviewer (module 계약 전용) → FAIL 시 Step B 반복
Step D — 메인 세션에 페이지 결과 보고 (PASS/FAIL·변경 파일·?v=)
```

### Step A — 3단 비교표

템플릿: `templates/page-markup-compare.md`

| 열 | 내용 |
|----|------|
| **현재 마크업** | 담당 페이지/모듈의 stock·ec-base 잔존 요약 |
| **목표 구조** | `design.md` + `component-gallery.html`에서 쓸 패턴 (블록명) |
| **재구성안** | NK 클래스·DOM 트리·유지할 변수/anchorBoxId 명시 |

**코드 착수 전 사용자 OK 필수.** (모호하면 추측 금지 — 질문)

### Step C — code-reviewer scope

프롬프트에 반드시 포함:

```
Diff: {담당 페이지 HTML}
Custom Instructions: module-contract-checklist.md 전항목만 검사.
  마크업 미관·CSS 품질은 이번 라운드 범위外.
```

---

## 4. 전체 완료 게이트

다음 **전부** 충족 전 **"전체 완료" 보고 금지**:

- [ ] `wave4-page-queue` / `blank-slate-rebuild-queue` — 담당 범위 **전행 PASS**
- [ ] 각 페이지 **code-reviewer 모듈 계약 PASS** 기록
- [ ] 메인 **통합 검수** (§1-4) PASS
- [ ] G8: `08-full-audit-pipeline.md` A→G (전 페이지 작업 후)
- [ ] 라이브 `?v=N` PC1440 + MO390 스크린샷 증거
- [ ] `05_work-log.md` 갱신

**일부 페이지만 PASS인 상태로 완료 보고 = 스킬 위반.**

---

## 5. 메인 → 하위 Task 프롬프트 골격

```
몰ID: {몰ID}
담당 페이지: {URL} · 소스: {src 경로}
정본: design.md · component-gallery.html · blank-slate-rebuild-queue §{N}

공통 작업 규칙: references/page-agent-orchestration.md §2

진행:
1. 3단 비교표 (templates/page-markup-compare.md) 작성 → 사용자 승인 대기
2. 승인 후 섹션→모듈→유닛 순 inner 재구성
3. code-reviewer module-contract-checklist PASS
4. 변경 파일 목록 + 라이브 ?v= 보고

금지: module 계약 훼손 · CSS만 덮어쓰기 · 다른 페이지 파일 수정
```

전체 brief: `templates/page-agent-brief.md`
