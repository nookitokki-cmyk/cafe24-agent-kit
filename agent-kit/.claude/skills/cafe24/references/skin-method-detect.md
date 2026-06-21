# 카페24 작업 방식 판별 (작업 시작 전 필수) — HTML 네이티브 vs EZ 엎기

> **언제:** 카페24 스킨 작업 지시를 받으면 **코드를 만지기 전에 이것부터 확정한다.**
> **왜:** 카페24 작업은 2갈래이고, 방식에 따라 *base가 우리를 이기는 경로 · 후처리 · 함정*이 전부 다르다.
> 추측 금지 — 마커로 판별한다. 실측 근거: [`brain/docs/EZ-OVERLAY-FINDINGS.md`](../../../brain/docs/EZ-OVERLAY-FINDINGS.md)

---

## 0. 두 방식 (대표님 실제 워크플로우)

| | **A. HTML 네이티브** | **B. EZ 엎기 (EZ-on-legacy)** |
|---|---|---|
| 시작점 | 카페24 HTML 스마트디자인에서 바로 | Easy(EZ) 스킨을 HTML 스킨에 엎어서 |
| layout module 수 | 많음 (예: 37) | 적음 (예: 4) — 구조를 EZ가 가짐 |
| base가 이기는 주경로 | `css/module/*` 명시도 | **`sub_theme`/`add_theme*` late-load + `body.theme01`** |
| 후처리 | 토큰화 + `#nk-skinN` 스코프 | **strip(data-ez 제거)** + 테마CSS 차단 + 모듈/CSS 병합 |

---

## 1. 판별 마커 — FTP/파일 (가장 확실, 운영 전·후 모두)

**EZ 스킨 신호** (하나라도 있으면 = EZ → 분기 B):
- `ez/` 폴더 존재 (`ez-module.html`, `init.js`)
- `smart-banner/` · `svg/` · `preference/` 폴더 존재
- `layout.html` 에 `<body ... data-ez-theme="...">` / `data-ez-*` 속성 / `<ez-prop>` 블록
- `layout.html` 이 `sub_theme.css` · `add_theme01~02.css` · `add_layout.css` 를 `@css` 로 로드
- `window.EZST` 폴리필 스크립트 / `@js(/ez/init.js)`

**HTML 네이티브 신호** (= 분기 A):
- `ez/` 폴더 **없음** + `layout.html` 에 `module=` 다수 + `css/module/layout/*` 를 `@css` 로 직접 로드 + `data-ez` 0

> 빠른 한 줄: **`ez/` 폴더 있으면 EZ(B), 없으면 HTML(A).** 헷갈리면 `body[data-ez-theme]` 와 `sub_theme.css` 로드 여부로 확정.

빠른 점검 (FTP 읽기):
```bash
# ez/ 폴더 유무 = 1차 판별
curl -s --list-only --user "$ID:$PW" "ftp://$HOST/sde_design/{skin}/" | grep -x ez
# layout.html EZ 마커
curl -s --user "$ID:$PW" "ftp://$HOST/sde_design/{skin}/layout/basic/layout.html" | grep -c 'data-ez\|ez-prop\|EZST\|sub_theme'
```

---

## 2. 판별 마커 — 라이브/DOM (운영 중인 몰)

- **`scripts/diagnose-overrides.js` 실행** → 상단에 `방식: EZ-on-legacy` 또는 `HTML-native` 자동 출력.
- 콘솔 직접 확인:
  - `document.body.dataset.ezTheme` 값 있음 → EZ
  - `document.querySelectorAll('[data-ez]').length` > 0 → EZ (잔존 strip 안 됨)
  - `[...document.styleSheets].some(s=>/sub_theme|add_theme/.test(s.href||''))` → EZ 테마 로드 중

---

## 3. 판별 마커 — 관리자 (editor_type)

- 관리자 디자인 목록 / MCP `cafe24_list_themes` → `editor_type`: **H**=HTML, **E**=Easy.
- ⚠️ **F35**: Easy '**타입**'으로 등록된 스킨을 FTP로 대량 수정하면 GUI 메타가 깨진다. → **HTML 타입 복사본**을 만들어 거기서 작업(분기 B의 Phase A).

---

## 4. 분기별 작업 경로

### 분기 A — HTML 네이티브
- **워크플로우**: [`01_작업하기/workflows/02-skin-build-standard.md`](../../../01_작업하기/workflows/02-skin-build-standard.md)
- **base 이김 처방**: `css/module/*` 를 `#nk-skinN` 스코프 명시도로 이김 + 토큰화
- **주의 함정**: `traps.json` 중 `method: html-native | both`
- **진단**: `diagnose-overrides.js` (전역/헤더/PLP/PDP/폼 스윕)

### 분기 B — EZ 엎기 (EZ-on-legacy)
- **워크플로우**: [`07-ez-on-legacy-setup.md`](../../../01_작업하기/workflows/07-ez-on-legacy-setup.md) → [`08-ez-three-step-pingpong.md`](../../../01_작업하기/workflows/08-ez-three-step-pingpong.md) (Phase A/B/C) · 전략 [`EZ-STRATEGY.md`](../../../brain/docs/EZ-STRATEGY.md)
- **엎기 = 선별 이식 (통째 덮기 ❌)**: `layout/index` 만 엎으면 `sub_theme·add_theme*·add_layout.css` + `svg/` + `swiper` 가 **dangling** (EZ-11). 테마CSS·`svg/`·`ez/`·`smart-banner/`·swiper 까지 같이 가져온다.
- **base 이김 처방**: 테마CSS가 `</body>` 직전 **late-load** → 로드순서로는 못 이김 → **`#nk-skinN` ID 스코프 필수** + `body.theme01` 의 `#d0ac88`/테마폰트 차단
- **후처리(기본)**: **strip** (`data-ez` 제거, `strip_ez.py`) → HTML-clean. 파일럿 예외는 유지(`_ref*/` override) — [EZ-STRATEGY §4](../../../brain/docs/EZ-STRATEGY.md)
- **EZST 순서**: strip 시 `EZST.register` 가 `new Swiper` 보다 앞이면 슬라이더 깨짐 (F36 #5)
- **주의 함정**: `traps.json` 중 `method: ez-on-legacy | both`

### 분기 C — Easy 타입이 admin에 등록돼 있고 FTP 수정 요청
- **하지 말 것**: Easy 타입 스킨 직접 FTP 대량수정 (F35).
- **할 것**: HTML 타입 복사본 생성 → 분기 B로.

---

## 5. 한 줄 결론 (에이전트 기본 동작)

> 카페24 작업 지시 → **① `ez/` 폴더·`data-ez-theme` 로 방식 판별 → ② 분기 A(HTML) / B(EZ 엎기) 선언 → ③ 그 분기 함정만 로드해서 시작.** 운영 중이면 `diagnose-overrides.js` 로 방식 재확인.
