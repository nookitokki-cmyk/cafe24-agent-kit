# 규칙 — 반응형 모바일 (단일 base 스킨)

> **필수:** 모바일 UI는 **별도 mobile 스킨 HTML이 아니라** `/sde_design/base/` 템플릿의 **`@media` 쿼리**로 구현한다.

---

## 필수: 관리자 설정

> **MCP·FTP·API로 변경 불가.** 사용자가 카페24 **관리자에서 직접** 설정해야 한다.

| 항목 | 내용 |
|------|------|
| **메뉴 경로** | 쇼핑몰 설정 → 사이트 설정 → 쇼핑몰 환경 설정 → **모바일** 탭 → **기본설정** → **사용설정** → **「모바일 전용 디자인 사용설정」** → **「사용안함」** → 저장 |
| **Help Center** | [모바일 전용 디자인 사용설정](https://support.cafe24.com/hc/ko/articles/8466336842009) |
| **검증** | 페이지 소스(또는 DevTools)에서 `CAFE24.MOBILE_WEB=false` 확인 — `true`이면 `/m/` 별도 mobile 스킨이 서빙됨 |

**에이전트 의무:** PC+MO **동일 base 템플릿** + `@media` 작업을 시작하기 **전**, 그리고 FTP 배포 **후** 사용자에게 위 관리자 경로를 **그대로 붙여넣어** 안내하고 「사용안함」 설정·`CAFE24.MOBILE_WEB=false` 확인을 요청한다.

---

## 원칙

| ✅ DO | ❌ DON'T |
|-------|----------|
| `base/` layout·header·CSS에 `@media (max-width: 1023px)` 추가 | `/sde_design/mobile/` 전용 HTML/CSS 신규 작성 |
| FTP 업로드 기본 경로: `/sde_design/base/` | mobile만 수정하고 base 미반영 |
| Playwright **390×844** on **메인 URL** (예: `/product/list.html`) | `/m/` URL만 검증 (별도 스킨 오판) |
| 인입 완료 기준: PC 1440 + MO 390 **동일 템플릿** | 「모바일은 나중에 mobile 스킨에서」 |

---

## 작업 시작 전 체크

1. **FTP:** `/sde_design/mobile/` 존재 여부 확인 (`mcp ls /sde_design --mall {몰ID}`)
2. **라이브:** `CAFE24.MOBILE_WEB` — `false` 이면 반응형 단일 스킨 (393674 패턴)
3. **관리자:** 「모바일 전용 디자인 사용설정」= **사용안함** ([Help Center](https://support.cafe24.com/hc/ko/articles/8466336842009))
4. **layout.html:** `viewport` meta + `<!--@css(/_ref393674/...)` 링크 존재

---

## mobile 스킨이 이미 있을 때

| 상황 | 조치 |
|------|------|
| 관리자에서 mobile 전용 **OFF** 가능 | OFF 후 base만 유지 (권장) |
| mall 정책상 mobile 경로 필수 | `base` 커스텀 레이어를 **mobile에 동기화** (임시). 문서에 「관리자 OFF 권장」 명시 |
| 에이전트가 base만 배포함 | **회귀** — mobile에 `_ref393674` 없으면 `/m/` 기본 EZ 노출 |

---

## 검증 (score 스크립트)

```python
# 메인 URL — /m/ 아님
TGT = "https://{몰}.cafe24.com/product/list.html?cate_no=24"
mo = browser.new_page(viewport={"width": 390, "height": 844}, is_mobile=True)
```

- `#header.a-header` · `.btn-menu` display · `ref393674-*` body class
- **모바일 PASS 기준:** `ref393674-score-mobile-full.py` 및 **모든** `ref393674-score-*.py` → **`total_score = 100` only**
- Phase별 스크립트(`ref393674-score-*.py`)는 PC+MO 혼합 — MO 전용 판정은 mobile-full 사용

```bash
cd work/scripts
python ref393674-score-mobile-full.py   # 390×844, 5 URLs, PASS = 100 only
```

---

## 관련

- `docs/common-pitfalls.md` §모바일 별도 스킨
- `workflows/06-verify-loop.md` §반응형 MO
- `rules/cafe24-admin-verify.md` — 관리자 경로 안내 전 웹 fetch
