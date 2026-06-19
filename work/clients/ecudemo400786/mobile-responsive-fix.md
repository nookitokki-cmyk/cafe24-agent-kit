# 모바일 별도 스킨 → 반응형 단일 템플릿 — ecudemo400786

> **일자:** 2026-06-19  
> **레퍼런스:** ecudemo393674 (maeve) — PC·MO 동일 base 스킨 + `@media`

---

## 근본 원인

| # | 원인 | 증거 |
|---|------|------|
| 1 | **모바일 전용 디자인 사용 ON** | `/m/` → `CAFE24.MOBILE_WEB=true`, `is_mobile:true` (400786). 레퍼런스 393674는 `/m/` 에서도 `MOBILE_WEB=false` |
| 2 | **에이전트가 `base/` 만 배포** | FTP `/sde_design/base/_ref393674` 존재, `/sde_design/mobile/_ref393674` 비어 있음 (수정 전) |
| 3 | **EZ skin16 기본 구조** | `/sde_design/mobile/` 별도 트리 (기본 모바일 EZ 스킨) |
| 4 | **모바일 layout.html 미동기화** | mobile `layout.html` 2334B, `_ref393674` CSS 링크 없음 vs base 6671B |

**결과:** PC URL은 maeve `_ref393674` 헤더·스타일, `/m/` 은 카페24 기본 모바일 스킨(카테고리 펼침·`mobile_ko_KR` 아이콘).

---

## 적용한 FTP 수정 (2026-06-19)

`work/deploy-ec400786/` → **base + mobile 동시 업로드** (68 files × 2):

| 원격 경로 | 내용 |
|-----------|------|
| `/sde_design/base/_ref393674/` | CSS·JS·inc (기존) |
| `/sde_design/mobile/_ref393674/` | **동일 레이어 신규 동기화** |
| `/sde_design/mobile/layout/basic/` | base 와 동일 layout·header·footer |
| `/sde_design/mobile/pages/`, `product/list*.html`, `index.html` | 커스텀 페이지 동기화 |

**After:** `/m/` 에서도 `#header.a-header`, `_ref393674` body class 확인.

---

## 관리자 설정 (반응형 단일 URL — **필수 권장**)

FTP 동기화만으로는 Cafe24가 여전히 **별도 mobile 스킨 경로**를 사용할 수 있다.  
레퍼런스 393674처럼 **PC 스킨 하나 + `@media`** 로 통일하려면 아래 설정 필요.

> 출처: [카페24 Help — 반응형 디자인 적용](https://support.cafe24.com/hc/ko/articles/8466336842009) · [모바일 쇼핑몰 디자인 FAQ](https://support.cafe24.com/hc/ko/articles/17472519536409) (2026-06-19 fetch)

1. **관리자** 로그인
2. **쇼핑몰 설정 → 사이트 설정 → 쇼핑몰 환경 설정**
3. **모바일** 탭 → **기본설정 → 사용설정**
4. **「모바일 전용 디자인 사용설정」** → **「사용안함」**
5. **저장**

**기대 결과:**

- `CAFE24.MOBILE_WEB=false` (393674 와 동일)
- `/m/` 접속 시에도 PC base 스킨 + viewport + `@media (max-width: 1023px)` 적용
- Playwright 390×844 **메인 URL** (`/product/list.html?cate_no=24`) 에서 `.btn-menu` block, `#header.a-header` 존재

---

## 검증 URL

| 항목 | URL | 기대 |
|------|-----|------|
| PC 1440 | https://ecudemo400786.cafe24.com/product/list.html?cate_no=24 | maeve header, container 100% |
| MO 390 (메인 URL) | 동일 URL, viewport 390 | `.btn-menu` 표시, MO search 숨김 |
| `/m/` (관리자 OFF 후) | https://ecudemo400786.cafe24.com/m/ | PC 스킨과 동일 HTML (393674 패턴) |

```bash
cd work/scripts
python ref393674-score-header.py   # MO 390 on main URL — 100 PASS
```

---

## 예방 (agent-kit)

- `rules/responsive-mobile.md` — MO 작업 = base `@media` only
- `docs/common-pitfalls.md` §모바일 별도 스킨
- 인입 Q4: PC 1440 + MO 390 **동일 템플릿**
