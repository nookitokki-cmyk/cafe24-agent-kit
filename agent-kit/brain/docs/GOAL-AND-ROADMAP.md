# 카페24 에이전트 키트 — 핵심 목표 · 목표적합성 진단 · 로드맵

> 작성: 2026-06-22 · 근거: 핸드오버(roadmap/distribution/test-findings/ordinary-deploy) + v2.4.0 + 실서버(ecudemo400919) 실측

---

## 0. 핵심 목표 (THE GOAL)

> **카페24 자동화 에이전트.** 카페24를 잘 모르는 **비코더**가 이 키트를 설치하면,
> 본인이 가진 **레퍼런스 URL 또는 Figma 시안**으로 카페24 스마트디자인(**EZ / HTML 둘 다**)에
> **정확하게 구현**하게 한다.

핵심 단어 3개: **비코더 / 입력(URL·Figma) / 정확한 구현(EZ·HTML).** 이 셋이 다 충족돼야 목표 달성.

---

## 1. 목표를 파이프라인으로 분해 (North Star)

```
[입력: 레퍼런스 URL 또는 Figma 시안]
  ① 의도 추출      → 토큰(색·폰트·간격) + 레이아웃 + 컴포넌트 + 페이지타입
  ② 방식 판별·분기  → EZ-on-legacy(B) vs HTML-native(A)        ★ 2026-06-22 구축됨
  ③ 매핑           → 의도 → 카페24 모듈/구조 (recipes·modules·templates)
  ④ 코드 생성      → 분기별 스킨 코드 (토큰 주입, nk-, EZ/HTML)
  ⑤ 배포           → SFTP
  ⑥ 검증·자가수정   → 레퍼런스 대비 시각 일치 + base 오버라이드 진단 → 합격까지 루프
[출력: 카페24에 정확히 구현된 스킨 (PC+모바일)]
```

---

## 2. 목표적합성 진단 (현재 키트, 솔직하게)

### 강한 곳 ✅
- **② 방식 판별·분기** — `skin-method-detect.md` + `diagnose-overrides.js` 자동판정 + traps `method` 축 (2026-06-22 신규)
- **③ 매핑 지식층** — variables / modifiers / modules / recipes / `traps.json`(47종) — 두껍고 실서버 검증 일부 완료
- **④ 빌딩블록** — templates(5) / snippets(20) / design-tokens / brand-profile (단, 🧪 실험적)
- **⑤ 배포** — SFTP MCP (파트너 웹FTP 포함) 자동
- **온보딩 문서** — 비코더용 00_시작하기 + 용어집 + 실패복구

### 약한 고리 (목표 달성을 막는 3대 병목)
| 단계 | 문제 | 근거 |
|---|---|---|
| 🔴 **① 입력 추출** | 레퍼런스 **URL→토큰 자동화 부재**(수동 입력) · 히어로/배경 **이미지 추출 누락** · Figma 토큰은 🧪실험적 | test-findings P3·P4 |
| 🔴 **⑥ 검증·자가수정** | qa-checker가 스크린샷에서 **코드 내용을 환각**해 오채점 → "정확"을 보장하는 **closed-loop 없음**. diagnose는 base충돌은 잡지만 *"레퍼런스와 일치하나"* 는 아직 | test-findings P1 |
| 🟠 **④ EZ 분기 생성** | templates/snippets가 **HTML 편향** → EZ 스킨 생성·strip 자동화 경로가 얇음 (판별은 되나 생성은 미완) | test-findings P5 |

### 그 외 목표 저해 요인
- v2.4.0 핵심 자료 다수가 **🧪실험적**(라이브 미검증) — 이번 세션에 diagnose 셀렉터 2버그(F7·F14)가 실서버에서 발견된 것이 *"문서만으론 정확을 보장 못 함"* 의 증거
- **code-reviewer가 키트 외부(전역) 의존** → 키트만 배포하면 리뷰 게이트가 빔
- **배포(npm/plugin) 미정** → "초보자가 설치하면" 의 *설치* 자체가 아직 미완 (distribution 핸드오버 결정 보류)

> **한 줄 결론:** 키트는 *지식·빌딩블록·방식분기* 까지 잘 깔렸으나, 목표의 양 끝 — **입력 추출(①)과 정확성 검증(⑥)** — 이 약해서 **end-to-end 가 닫힌 적이 없다.** "정확하게"를 측정·보장하는 루프가 핵심 결손.

---

## 3. 경험자라면 이렇게 한다 (접근 원칙)

1. **"정확"부터 정의한다 (acceptance bar).** 측정 못 하면 만들 수 없다. 제안 기준: 핵심 페이지 **PC+모바일 시각일치 점수** + **base-override 0 dangling** + **traps 클린**.
2. **폭(breadth)보다 척추(spine).** 레퍼런스 1개 → HTML 스킨 1개 → 핵심 3페이지 → 합격까지, **end-to-end 한 번 관통**(vertical slice). 그 다음에 EZ 분기·Figma 입력·페이지 확대.
3. **약한 고리부터.** 중간(지식/템플릿)은 이미 강하다 → **입력 추출(①) + 검증 루프(⑥)** 양 끝을 먼저 친다.
4. **루프를 닫는다.** 신뢰 가능한 시각검증(qa-checker를 **시각 전용**으로 재설계 + 레퍼런스 vs 결과 스크린샷 diff)으로 **자가수정** 가능하게.
5. **도그푸딩으로 실험적→안정.** 실서버에서 돌려 검증(문서 신뢰 금지 — F7/F14 버그가 증거).
6. **그 다음 배포.** 초보자 설치 경로(npm/plugin)는 spine 이 닫힌 뒤.

---

## 4. 로드맵 (재정렬 — 목표 역산)

| Phase | 내용 | 목적 | 비고 |
|---|---|---|---|
| **0. 마무리** ✅ | detectJS 2버그(F7·F14) 수정 · nk-ez-override §10 repo 동기화 · code-reviewer 키트 내장 | 자립성·정확성 기반 | **완료 2026-06-22** (commit feat/self-diagnose-and-method-gate) |
| **1. ★ 검증 루프 (키스톤)** ✅ | "정확" 정의(accuracy-gate.md) + qa-checker **시각 전용** 재설계 + qa-loop **3축 게이트**(visual+override+rule) + capture-pair.mjs(레퍼 vs 결과 캡처) + 자동화 워크플로우 정렬 | "정확하게"를 **측정·보장** | **완료 2026-06-22**. 남은 정합성 검증은 Phase 3 spine 관통에서 실증 |
| **2. 입력 강화** 🔄 | 레퍼런스 **URL→토큰 자동**(P4, extract-tokens.mjs) + 히어로/배경 **이미지 추출**(P3, extract-assets.mjs) + input-pipeline.md | 파이프라인 front door | **빌드중**: 스크립트·문서 완료. 남음: 실 URL 추출 정확도 검증(Phase 3 spine)·Figma 토큰 안정화 |
| **3. spine 관통** | 레퍼런스 1개 → **HTML 스킨**(ecudemo400919) → main+PLP+PDP → 합격까지. 성공 후 **EZ 분기** 동일 관통 | end-to-end 1회 증명 | vertical slice |
| **4. 실험적→안정** | 관통 과정에서 templates/snippets/pipeline/`/카페24-자동화` 검증·승격 | 🧪 → ✅ | **v2.4.1 릴리스** |
| **5. 비코더 원버튼 + 배포** | `/카페24-자동화` 정비 + npm/plugin 결정·실행 | "설치하면" 실현 | distribution 핸드오버 |

**추천 시작:** Phase 0(마무리) → **Phase 1(검증 루프)**. 이유: *정확성을 측정하는 루프*가 없으면 입력·생성을 아무리 잘 만들어도 "정확"을 증명할 수 없다. 루프가 닫히면 그게 Phase 2~4의 자동 채점기가 된다.

---

## 5. 기존 계획과의 관계
- 이전 세션의 "Phase A(진단 기반)" = 완료(traps.json + diagnose-overrides.js + preflight). 이 로드맵 Phase 1의 **부품**으로 흡수됨.
- 이전 "Phase B(code-reviewer 내장)" = 이 로드맵 **Phase 0** 으로 편입.
- roadmap 핸드오버 10종 = v2.4.0 으로 대부분 구현(🧪) → 이 로드맵 **Phase 4(안정화)** 대상.
