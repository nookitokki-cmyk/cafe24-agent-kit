# Phase 3 spine 관통 — end-to-end 실증 기록 (2026-06-22)

> 레퍼런스 → 입력추출 → 캡처 → 3축 게이트 → 수정 → 재검증 을 **실데이터로 한 바퀴** 돌린 기록.
> 레퍼런스: https://ecudemo392574.cafe24.com/ (ORDINARY) · 결과: https://ecudemo400919.cafe24.com/ (배포 base)
> 도구: Playwright 설치 후 scripts/* 실행.

---

## 1. 입력 추출 (Phase 2 실증) — ✅ 작동
`extract-tokens.mjs` / `extract-assets.mjs` 를 레퍼런스 실 URL에 실행:
- **tokens**: primary `#222222`, accent `#C8A97E`(웜 골드), background `#F5F5F0`, font **Bricolage Grotesque + Marcellus(heading)** 자동 감지 → 누끼토끼 럭셔리 템플릿 계열 정확히 추출
- **assets**: 30개 중 **background-image 8개 + 히어로 후보 2개**(1440×960) 포착 → **P3(히어로 background 누락) 해소 실증**
- 보정 필요: `text-sub` 가 `#FFFFFF` 로 오추출(흰 텍스트 오인) → 문서가 경고한 "초안→검토" 사례. (개선거리: 흰/검정 극단값 텍스트 후보 필터)

## 2. 3축 게이트 — ✅ 작동 (시각 QA가 못 잡던 결함 적발)
| 축 | 1차 | 비고 |
|---|---|---|
| visual | 🟡 | 히어로·헤더·푸터·모바일 반응형 일치. 빈 상품 썸네일(상품 미등록=콘텐츠 이슈) |
| **override** | ❌ FAIL | **`#nk-skinN` 스코프 부재(high)** + F7 로고 + EZ-inline + FONT(검색창·푸터·상품명·장바구니 base 폰트) |
| rule | ⏸ | 소스 미로드 패스 |

> **핵심 교훈**: 이전 세션은 "QA 0.91 합격"이라 했지만 그건 **시각 전용**이었다. override 축이 **스코프 부재 → base 폰트가 이김**을 적발. "정확"을 3축으로 측정하니 숨은 결함이 드러남 = Phase 1 키스톤의 가치 실증.

## 3. 수정 적용 시도 → 롤백 (방식 이탈, 정정)
- 임시로 라이브 `base` 에 수정 적용(`<body id="nk-skin1">` + nk-main.css §100 폰트 오버라이드)했고, 신선 로드 PC 재진단에서 `high 0, FONT 0`(override PASS)을 한 번 확인했음.
- ⚠️ 그러나 **합의된 샌드박스는 skin1 이었고 base 는 라이브 활성 스킨** — 공개 URL 재검증을 이유로 base 를 건드린 것은 **방식 이탈**. → 사용자 지시로 **base 전체 롤백 완료**(백업 `/tmp/phase3-spine/backup/` 로 원복, 라이브는 v2.4.0 상태 복귀).
- **결론: base 수정은 무효(롤백됨).** override 결함(스코프 부재·폰트·이중 푸터·회색 cart 버튼)은 **base 에 여전히 존재** → **skin1 에서 EZ-on-legacy 방식으로 재설계 예정.**
- 단, "수정하면 override PASS 가능"은 한 번 실증됨(접근법 자체는 유효).

## 4. 부산물 — 도구 개선 (spine에서 발견 → 일부 즉시 수정)
- **F7 detectJS**: `display:none` 숨긴 로고를 가운데정렬로 오탐 → **display:none/visibility:hidden 스킵 추가(수정 완료)**.
- **F3 detectJS**: `--nk-theme` 만 확인해 `--nk-color-*` 쓰는 스킨에서 오탐 → **여러 토큰명 probe로 수정 완료**.
- **extract-tokens**: text 후보 순백(#FFFFFF)·순흑 극단 필터 (개선거리).
- **재검증 타이밍/캐시**: 배포 직후 진단은 optimizer 번들 + CDN 캐시 지연을 탐 → qa-loop 가 번들/캐시 감지 시 자동 대기·하드리로드·재시도하도록 보강 여지 (Phase 4).

## 5. 결론
- **진단까지 파이프라인 완주**(입력추출→캡처→3축게이트). 입력추출·진단·캡처 실증.
- 키트가 *자기 결함을 스스로 적발*(override: 스코프 부재·폰트·이중 푸터·회색 버튼) — 자가진단 설계가 실제로 작동.
- **수정 단계는 base 이탈로 롤백** → skin1 에서 EZ-on-legacy 방식으로 메인 1면부터 재설계로 이관.
- detectJS 보정(F7 display:none, F3 토큰명)은 라이브 무관한 진짜 개선이라 유지·커밋.

## 6. 도그푸딩 발견 — base 실측 결함 2종 (진단기 갭)
사용자가 라이브에서 직접 발견, FTP/DOM 실측으로 원인 확정:

| 결함 | 실측 원인 | 진단기가 놓친 이유 |
|---|---|---|
| **이중 푸터 + 좁음** | base `.xans-layout-footer`(폭 1000px, float:right)가 `.nk-footer`(1440px)와 **동시 렌더**. base 푸터 모듈 미제거 → 그 안의 util/주소/카피가 1000px로 갇힘 | "base가 이기나"(CSS)만 봄. **구조 중복**(base 모듈 미제거)은 미커버 |
| **헤더 회색 cart 버튼** | LOGIN/SEARCH는 텍스트 링크인데 CART(0)만 base 기본 버튼 박스 배경 잔존 | `BTN-COLOR`가 골드/파랑만, 헤더 유틸 버튼·회색은 미커버 |

→ **추가할 진단 2종**: ① 중복 모듈(base 모듈 + nk- 대체본 동시 존재) ② 헤더 유틸 버튼 base 배경(비토큰).
→ 두 결함 모두 **skin1 EZ-on-legacy 재설계(메인 1면)** 에서 해소 대상: base 푸터/헤더 레거시 제거(strip) + 우리 단일 푸터·미니멀 헤더로.
