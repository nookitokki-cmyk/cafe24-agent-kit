# "정확하게 구현됨"의 정의 — 3축 합격 게이트 (Phase 1 키스톤)

> 키트의 핵심 목표는 *레퍼런스/Figma → 카페24 정확 구현*. "정확"을 **측정 가능**하게 정의하지 않으면 자동화가 합격 여부를 판단할 수 없다.
> 이 문서가 그 **합격 계약(acceptance contract)** 이다. qa-loop·`/카페24-자동화`·code-reviewer 가 이 게이트를 따른다.

---

## 0. 한 줄 정의

> **"정확"** = 다음 **3축이 모두 통과**할 때. (하나라도 실패하면 미완 — 자가수정 루프 계속)
> `정확 = visual PASS  AND  override PASS  AND  rule PASS`

세 축은 **서로 다른 것을 본다 — 절대 섞지 않는다** (P1 환각의 원인이 축 혼선이었음):

| 축 | 누가 본다 | 무엇을 (보이는 것 vs 코드) | 도구 |
|---|---|---|---|
| **visual** | qa-checker (Haiku) | **화면에 보이는 것만** — 레퍼런스 vs 결과 스크린샷 | 스크린샷 비교 |
| **override** | diagnose (스크립트) | base 가 우리를 이겼나 + dangling | `scripts/diagnose-overrides.js` / `preflight.mjs` |
| **rule** | code-reviewer (Opus) | **코드 규칙** — nk-/스코프/!important/토큰 | `.claude/agents/code-reviewer.md` |

> ⚠️ **qa-checker 는 코드(클래스명·nk-·인라인 style·줄번호)를 언급/채점하지 않는다.** 그건 code-reviewer 몫. qa-checker 는 픽셀만 본다.

---

## 1. 축별 합격 기준

### ① visual (시각 일치) — qa-checker
- 입력: **레퍼런스 스크린샷** + **결과(라이브) 스크린샷**, **PC(1280~1440) + 모바일(375)** 둘 다
- 채점 축(보이는 것만): `layout`(0.30) · `color`(0.25) · `typography`(0.25) · `imagery`(0.20, 이미지·여백·비율·정렬)
- **합격: aggregate ≥ 0.85 AND 모든 축 ≥ 0.70 AND PC·모바일 둘 다 충족**
- 코드축(naming/accessibility) **없음** — rule 축으로 이관

### ② override (base 충돌 없음) — diagnose-overrides.js / preflight.mjs
- **합격: `❌(high)` 발견 = 0  AND  dangling(404) = 0**
- 방식(method)별: EZ-on-legacy 면 `EZ-RESIDUE`(strip 목표 0)·`EZ-DANGLING` 도 점검
- `🟡(low)` 는 경고(합격 가능), `⚠️(medium)` 는 사유 없으면 감점

### ③ rule (코드 규칙) — code-reviewer
- **합격: `blocking` = 0**
- blocking: nk- 누락 / `#nk-skinN` 스코프 누락 / 인라인 style / italic / 카페24 원본 직접수정 / 사유 없는 !important / bare 태그 글로벌 침범 / 토큰 하드코딩
- `warning` 은 합격 가능(다음 회차 반영)

---

## 2. 게이트 판정

```
정확 PASS  ⟺  visual.aggregate ≥ 0.85 (PC·모바일, 각 축 ≥ 0.70)
            AND override.high == 0  AND override.dangling == 0
            AND rule.blocking == 0
```

| 판정 | 조건 | 다음 |
|---|---|---|
| **PASS** | 3축 전부 통과 | 완료 보고 (라이브 URL + PC/모바일 스크린샷 증거) |
| **NEEDS_WORK** | 1축 이상 실패 | 실패 축의 fix 수집 → 자가수정 → 재실행 |
| **STALL** | 2회 연속 개선폭 < 0.02 | 사람 개입 요청 (자동 루프 중단, 원인 보고) |

---

## 3. 루프 (qa-loop 가 구현)

```
1) 결과 스킨 라이브 배포(또는 프리뷰)
2) 3축 병렬 실행:
     visual   = qa-checker(레퍼 vs 결과 스크린샷, PC+모바일)
     override = diagnose-overrides.js (PC+모바일) 또는 preflight.mjs
     rule     = code-reviewer (변경 파일)
3) 게이트 판정 (§2)
4) PASS → 종료 / NEEDS_WORK → 3축 fix 통합 → 작성 에이전트(cafe24-ez 등) 재호출 → (1)
5) STALL → 중단 + 사람 보고
```

- **작성 ↔ 검증 레인 분리**: 수정은 cafe24-ez/css-builder, 채점은 qa-checker/code-reviewer (자가승인 금지).
- **증거 필수**: "완료"는 PC+모바일 스크린샷 + override 0 + rule 0 리포트가 있을 때만.

---

## 4. 왜 3축인가 (설계 근거)
- **P1 교훈**: qa-checker(스크린샷)가 코드 내용을 환각해 오채점 → 시각/코드/충돌을 **한 채점기에 섞으면 신뢰 붕괴**. 셋을 분리해 각자 자기 영역만 본다.
- **목표 직결**: "정확"은 ① 보이는 게 레퍼와 같고(visual) ② base 에 안 졌고(override) ③ 규칙을 지킨(rule) 상태. 셋이 AND 여야 비코더가 믿고 쓸 수 있다.
