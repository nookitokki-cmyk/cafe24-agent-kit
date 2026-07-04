---
name: qa-loop
description: >
  정확성 3축 합격 게이트(visual + override + rule)가 모두 통과할 때까지 수정→재검증을
  자동 반복하는 수렴 루프. 카페24/아임웹/식스샵 HTML/CSS 작업·배포 후 호출.
  "정확"의 정의는 references/accuracy-gate.md.
triggers:
  - qa-loop
  - qa 루프
  - 합격까지 반복
  - 점수 나올 때까지
  - 정확까지 반복
---

# QA 수렴 루프 (qa-loop) — 3축 합격 게이트

작성 에이전트(cafe24-ez/css-builder)가 만든 결과가 **"정확"(3축 PASS)** 이 될 때까지
자동으로 수정→재검증을 반복한다. **"정확"의 정의 = `references/accuracy-gate.md`.**

> 핵심: 세 검증기는 **서로 다른 것만** 본다 (P1 환각 방지). qa-checker=시각, diagnose=base충돌, code-reviewer=코드규칙.

---

## 3축 (accuracy-gate.md)

| 축 | 검증기 | 합격 |
|---|---|---|
| **visual** | `qa-checker` (시각 전용, 레퍼 vs 결과 스크린샷 PC+모바일) | aggregate ≥ 0.85, 각 축 ≥ 0.70, PC·모바일 둘 다 |
| **override** | `scripts/diagnose-overrides.js` / `preflight.mjs` | `❌(high)` = 0, dangling = 0 |
| **rule** | `.claude/agents/code-reviewer.md` (코드 규칙) | `blocking` = 0 |

```
정확 PASS ⟺ visual PASS AND override PASS AND rule PASS
```

---

## 설정값

| 변수 | 기본값 | 의미 |
|------|--------|------|
| `MAX_ITER` | 5 | 최대 반복 회차 |
| `VISUAL_THRESHOLD` | 0.85 | visual 합격 기준 |
| `STALL_WINDOW` | 2 | N회 연속 visual 개선폭 < 0.02 이면 정체 |

---

## 루프 실행 순서

### 준비
1. 검증 대상: 변경 파일 경로 + **라이브/프리뷰 URL**(시각·override 검증용) + **레퍼런스 스크린샷**.
   - 레퍼런스 없으면 visual 채점 불가 → 중단하고 레퍼런스 요청.
2. `iteration = 1`, `history = []`, `prev_visual = null`.

### 매 회차 (1 → MAX_ITER)

#### STEP A — 3축 병렬 검증
세 검증을 **병렬로** 호출(서로 맥락 공유 금지):

1. **visual** — `qa-checker` 호출: 레퍼런스 스크린샷 + 결과 스크린샷(PC+모바일) + `iteration` + `prev_aggregate`. → JSON.
2. **override** — `scripts/diagnose-overrides.js` 를 라이브에 주입(PC+모바일) 또는 `preflight.mjs <url>` 실행. → `❌(high)` 수 + dangling 수.
3. **rule** — `code-reviewer` 호출: 변경 파일 경로 + 작업 방식(html/ez). → JSON `blocking[]`.

#### STEP B — 게이트 판정
```
visualPass   = (PC.aggregate ≥ 0.85 AND mobile.aggregate ≥ 0.85 AND 모든 축 ≥ 0.70)
overridePass = (high == 0 AND dangling == 0)
rulePass     = (blocking.length == 0)
PASS         = visualPass AND overridePass AND rulePass
```
- **PASS** → [성공 보고]
- **visual STALL**(2회 연속 개선폭<0.02) → [정체 보고] + 사람 요청
- 그 외 → STEP C

#### STEP C — 수정 지시 (작성 에이전트 재호출)
세 축의 실패 항목을 **통합**해 cafe24-ez(또는 css-builder)에 전달:
```
[수정 지시 — 회차 {N}]
■ 시각 차이 (qa-checker, 보이는 현상):
  - {visual.priority_fixes ...}
■ base 충돌 (diagnose, ❌/dangling):
  - {override 항목: ID·증상·처방 CSS}
■ 코드 규칙 위반 (code-reviewer, blocking):
  - {rule.blocking: rule·file·line·fix}

위 항목만 수정. 다른 부분 건드리지 말 것. 처방의 SKIN은 실제 #nk-skin{번호}로.
```
> 통과한 축은 전달하지 않는다.

#### STEP D — 기록·반복
```
history.append({ iteration:N, visual_pc, visual_mobile, high, dangling, blocking, verdict })
prev_visual = visual.aggregate
iteration += 1
```
- `iteration > MAX_ITER` → [회차 소진 보고]
- 아니면 STEP A 반복

---

## 최종 보고

### 성공
```
✅ 정확 합격 — {N}회차
  visual:   PC {pc} / MO {mobile}  (≥0.85)
  override: high 0, dangling 0
  rule:     blocking 0
증거: 라이브 URL + PC/모바일 스크린샷
```

### 정체 / 회차 소진
```
⚠️ 미합격 — {정체|회차소진}
  visual:   PC {pc} / MO {mobile}
  override: high {n}, dangling {n}
  rule:     blocking {n}
최선 회차 {best}: {요약}
선택지:
  A) 요구 완화하고 현재로 진행
  B) 특정 축(visual/override/rule) 집중 수정 후 재시도
  C) 처음부터 (ref 재분석 → 재생성)
```

---

## 핵심 원칙
1. **3축 분리**: 시각/충돌/규칙을 한 채점기에 섞지 않는다 (P1 환각의 근본 차단).
2. **측정 ↔ 수정 분리**: 검증기와 작성 에이전트는 직접 대화하지 않는다(루프가 JSON만 전달). 자가승인 금지.
3. **종료는 게이트가 정한다**: AI 재량으로 "됐다" 선언 금지 — 3축 AND + MAX_ITER.
4. **실패 은폐 금지**: STALL/소진 시 best-of 와 함께 사람에게 보고 (F33: 점수 미달 완료보고 금지).
5. **통과 축은 안 건드린다**.

---

## 사용 예시
```
"qa-loop 돌려줘" / "정확까지 반복"  → 3축 게이트 루프
"최대 3번만"  → MAX_ITER=3
"visual 기준 0.80으로"  → VISUAL_THRESHOLD=0.80
```
