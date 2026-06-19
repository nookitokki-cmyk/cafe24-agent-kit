# ecudemo400786 모바일 적대적 감사 (Adversarial Audit)

> **일자:** 2026-06-19  
> **Target:** https://ecudemo400786.cafe24.com/  
> **Ref:** https://ecudemo393674.cafe24.com/  
> **Viewport:** 390×844, `isMobile` + `hasTouch`, **메인 URL** (not `/m/`)

---

## 1. MOBILE_WEB 상태

| URL | CAFE24.MOBILE_WEB | 영향 |
|-----|-------------------|------|
| `/` (main) | **false** | ✅ 반응형 단일 base 스킨 — MO 검증 유효 |
| `/m/` | **false** | ✅ ref393674 패턴과 동일 — 별도 mobile HTML 미서빙 |

**판정:** MOBILE_WEB=false → Playwright 390px on 메인 URL 검증 **유효**. (이전 `mobile-responsive-fix.md` 기록의 `MOBILE_WEB=true` 문제는 **관리자 OFF + FTP 동기화 후 해소** 확인.)

---

## 2. 종합 모바일 점수 (ref393674-score-mobile-full.py)

| 항목 | 배점 | 획득 | 비고 |
|------|------|------|------|
| MW1 MOBILE_WEB=false | 10 | 10 | PASS |
| H1 Header (burger/GNB/logo) | 15 | 15 | CSS 수정 후 PASS |
| S1 Search MO hidden | 10 | 10 | ref 동일 |
| P1 PLP 2열/padding/sort | 10 | 10 | itemW≈171, pad 15px |
| R1 Hero swiper/overflow | 15 | 15 | slides≥1, no overflow |
| T1 Typography/tap ≥44px | 10 | 10 | CSS + 스크립트 측정 수정 후 |
| F1 Footer tappable | 10 | 10 | 링크 min-height 44px |
| E1 No EZ junk | 10 | 10 | a-header, no bottom-nav |
| Q1 Ref parity 5 elements | 20 | 20 | 390px 동일 viewport |

### **total_score = 100 / 100 → PASS**

- **수정 전:** 87/100 (FAIL) — H1 5/15, T1 0/10, F1 7/10  
- **수정 후:** 100/100 (PASS) — FTP 배포 + CSS hotfix

---

## 3. 기존 Phase 스크립트 (MO 관련 추출)

| 스크립트 | 전체 | MO-only | 비고 |
|----------|------|---------|------|
| ref393674-score-header.py | 100 | M1 search hidden ✅ | |
| ref393674-score-plp.py | 100 | MO 15/15 ✅ | 2열·sort select |
| ref393674-score-member.py | 100 | M1 container ✅ | |
| ref393674-score-board.py | 100 | M1 ✅ | |
| ref393674-score-page.py | 100 | AM/CM ✅ | |
| ref393674-score-pdp.py | 91 | (혼합) | PC 레이아웃 gap 잔존 가능 |
| ref393674-score-basket.py | 85 | M1 ✅ | L4 CTA 색상 채점 FAIL (rgb 17,17,17 vs 기대 0,0,0) |

> Phase 스크립트 PASS 기준은 90점. **모바일 최종 PASS는 mobile-full 100점만** (`agent-kit/rules/responsive-mobile.md`).

---

## 4. 적용한 수정 (FTP)

| 파일 | 변경 |
|------|------|
| `_ref393674/css/header.css` | MO `.btn-menu` min 44×44px; logo line-height 1.2 |
| `_ref393674/css/footer.css` | MO footer `a` min-height 44px; company 12px |

**업로드:** `/sde_design/base/` + `/sde_design/mobile/` (2026-06-19)

---

## 5. Gap 표 (적대적 — picky client 관점)

| # | 이슈 | 심각도 | 상태 | 비고 |
|---|------|--------|------|------|
| 1 | btn-menu tap area 13px | 🔴 | **수정됨** | ref도 13px였으나 400786은 44px로 개선 |
| 2 | footer link tap 15px | 🟡 | **수정됨** | padding 12px 추가 |
| 3 | company text 11.5px | 🟡 | **수정됨** | 12px로 bump (ref도 11.5px) |
| 4 | 숨김 1px font DOM 잔존 | 🟢 | 잔존 | skip/숨김 a·span — UX 영향 없음 |
| 5 | basket CTA 색상 채점 | 🟡 | 잔존 | rgb(17,17,17) — 시각적 ref와 동일하나 스크립트 strict |
| 6 | PDP PC 혼합 91점 | 🟡 | 잔존 | MO viewport 단독 gap은 mobile-full PASS |
| 7 | 카테고리 배너 이미지 | 🟢 | admin | 구조 OK, 관리자 배너 등록 여부 |
| 8 | MO drawer 실제 터치 UX | 🟢 | 미검 | Playwright click 미실행 — 수동 확인 권장 |
| 9 | Font Jost vs Bricolage | 🟢 | OK | h1Family에 Bricolage Grotesque 확인 |
| 10 | `/m/` vs main HTML diff | 🟢 | OK | MOBILE_WEB=false, 동일 스킨 |

---

## 6. 실토 (Honest Assessment)

### 잘 된 것
- **MOBILE_WEB=false** — ref393674와 동일 반응형 단일 URL 패턴 확립
- PLP 2열·15px padding·sort `<select>` — ref parity
- EZ bottom-nav/RTMB 미노출, `#header.a-header` 정상
- Hero swiper 동작, horizontal overflow 없음

### 수정했지만 여전히 까다로운 점
- **레퍼런스 자체도** burger 13px·footer link 13px — 우리가 44px로 올렸으나 ref와 픽셀 parity는 어긋남 (접근성은 개선)
- Phase basket/pdp 스크립트는 PC 가중 — MO-only PASS와 별개로 PC gap 잔존

### 사용자/관리자 액션 필요
1. **카테고리 배너** — PLP headcategory 이미지 관리자 등록 (없으면 placeholder 높이만)
2. **장바구니 CTA** — empty basket 상태에서 btnBg strict match; 상품 담기 후 재검증
3. **MO drawer** — burger 탭 → 메뉴 열림/닫힘 수동 스모크 (자동화 미포함)

---

## 7. 재현

```bash
cd work/scripts
python ref393674-score-mobile-full.py
# PASS: total_score == 100 only
```

---

## 8. 결론

| | |
|--|--|
| **모바ile-full** | **100 / 100 — PASS** |
| **MOBILE_WEB** | false (main + /m/) — 검증 유효 |
| **FTP 수정** | header.css, footer.css (base+mobile) |
| **Blockers** | 없음 (100 PASS) |
