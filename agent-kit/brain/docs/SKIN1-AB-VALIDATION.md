# skin1 A/B 실증 — 키트 두 방식(HTML 네이티브 vs EZ-on-legacy) 검증 (2026-06-22)

> 목적: 이 키트가 **두 작업 방식을 모두 지원**하는지 실데이터로 검증.
> 사용자가 Figma/URL 투입 → 키트가 ① HTML 네이티브(A) / ② EZ-on-legacy(B) 중 하나를 골라 진행하는 구조의 타당성 실증.
> 대상 몰: ecudemo400919 `skin1` (실측 = **HTML 네이티브**: `ez/` 없음, layout module 37, data-ez 0)
> 디자인 소스: 재설계 메인(ORDINARY, 레퍼런스 ecudemo392574 토큰 추출). 미리보기 URL: `https://ecudemo400919.cafe24.com/index.html?skin=skin1`
> 선행: [`EZ-OVERLAY-FINDINGS.md`](EZ-OVERLAY-FINDINGS.md)(skin1/skin2 정밀비교) · [`SPINE-VALIDATION.md`](SPINE-VALIDATION.md)

---

## 0. 결론 한 줄
**키트는 두 방식 모두 처리 가능**(진단이 방식 자동 판별 + 방식별 함정 검출 + 게이트 통과). 단 **HTML 네이티브가 출발점이면 A안이 명백히 우월**(파일 4 vs 63, EZ 함정 0 vs 2). EZ-on-legacy(B)는 *EZ 몰이 출발점일 때* 의미.

---

## 1. 작업 경계 (중요)
- 메인페이지는 `index.html` → `<!--@layout(/layout/basic/main.html)-->`. **메인만 바꾸려면 `main.html` + `index.html`만** 손대면 됨.
- `layout.html`(서브페이지 공통)·base는 **무수정** → 상품목록·상세·게시판 등 서브페이지 100% 안전.
- 스코프: `body#nk-skin1`. base가 `#main`을 안 쓰는 것 확인 후 `id="main"` → `id="nk-skin1"`로 전환(진단기 컨벤션·명시도).

## 2. A안 (HTML 네이티브) — 3축 게이트 통과
- 추가 파일 **4개**: `_nk/css/nk-tokens.css`·`nk-main.css`(`:root` 토큰 + `#nk-skin1` 스코프), `layout/basic/main.html`, `index.html`.
- 카페24 모듈 바인딩 보존(헤더 LogoTop/SearchHeader/category/state, 푸터 footer/Info/LogoBottom, 메인 product_listmain_1·2 각 anchorBox 2개).
- 핸드오버 결함 2종 해소: 헤더 회색 cart 박스 → 텍스트 링크, 이중 푸터 → 단일 4컬럼.
- **게이트**: override high **0**/dangling 0 · rule blocking **0** · visual 레퍼 톤·구조 일치. (남은 medium: F7 로고=디자인상 중앙 의도 / EZ-INLINE 13곳=상품모듈 원본 인라인 보존)

## 3. B안 (EZ-on-legacy) — 경로 실증
- Phase A: `skin1` 원본 복사. Phase B: skin2 EZ 조각 **선별이식**(sub_theme·add_theme01/02·add_layout·sub_style·main·slideMenu·swiper + svg/·ez/·smart-banner/) → **dangling 0**(EZ-11 실증, 참조 36건 전부 존재). `preference/*.ini`는 카페24 시스템 파일이라 FTP 쓰기 거부(550)되나 미참조라 무관.
- EZ 테마 활성(`body.theme01 data-ez-theme` + 테마CSS late-load + EZST + ez/init.js).
- **진단 결과**: A안엔 없던 함정 2종 추가 검출 — **EZ-METHOD**(방식 자동 판별), **EZ-BODY-THEME**(theme01 #d0ac88 골드·테마폰트 상시 주입, EZ-3 출처 확정). high 0(`#nk-skin1` 스코프가 테마를 이김).
- **시각**: A안과 거의 동일(스코프 승리 + ez/init.js가 HTML skin에서 완전 동작 안 함). → "EZ 잘 엎어도 A로 수렴 + 잔재 부담"의 실증.
- 추가 파일 **약 63개**(EZ 조각 50 + nk).

## 4. A vs B 비교표
| 항목 | A (HTML) | B (EZ-on-legacy) |
|---|---|---|
| 추가 파일 | 4 | ~63 |
| dangling | — | 0 (선별이식) |
| override high | 0 | 0 |
| EZ 함정 | 0 | EZ-METHOD·EZ-BODY-THEME |
| 시각 | 의도대로 | A와 거의 동일 |
| 후처리 | 불필요 | strip 필요 |

## 5. 키트 개선 (이번 세션 반영)
- **preflight.mjs 모바일 UA 결함 수정** — 모바일을 `isMobile:true`+모바일 UA로 봐 카페24가 *별도 모바일 스킨*을 띄워 오진단(S1·F3·BASEFONT). → 데스크톱 UA+좁은 뷰포트로 보정(capture-pair 규칙과 통일). 보정 후 PC/모바일 동일하게 high 0.

## 6. A안 도그푸딩 개선거리 (후속)
- 상품 진열 **가격 변수 미표시**(이 스킨 원본 description에 가격 변수 없음 → 추측 주입 금지, 카페24 변수 확인 후 추가 대상).
- 헤더 GNB **카테고리 li 3개 하드코딩**(대분류 수 > 3이면 잘림 가능 — 반복 틀 확인).
- `header-login-btn` 클래스 JS 의존 여부 확인 후 정리.
- 콘텐츠(디자인 무관): 히어로 배경 이미지·상품 미등록 → 관리자 등록 시 채워짐.

## 7. 산출물 경로 (로컬, 휘발 주의)
- A안 작업본: `~/Downloads/cafe24-400919-work/skin1-A/`
- B안 작업본: `~/Downloads/cafe24-400919-work/skin1-B/`
- skin1 원본 백업: `~/Downloads/cafe24-400919-backup_2026-06-22/`
- 캡처: `/tmp/phase3-spine/shots_A`·`shots_B` / 진단: `diag_A4.json`·`diag_B1.json` (`/tmp` 휘발성)
- **현재 라이브 skin1 = B안 상태**(EZ 잔재). 최종은 A안 복원 권장(work/skin1-A 재업로드).
