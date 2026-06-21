---
name: qa-loop
description: >
  css-builder ↔ qa-checker 수렴 루프. 코드 생성 후 합격 점수(0.85)가 나올 때까지
  자동으로 수정→재채점을 반복한다. 카페24/아임웹/식스샵 HTML/CSS 작업 완료 후 호출.
triggers:
  - qa-loop
  - qa 루프
  - 합격까지 반복
  - 점수 나올 때까지
---

# QA 수렴 루프 (qa-loop)

css-builder가 코드를 생성한 후, qa-checker가 합격 판정(PASS)을 줄 때까지
자동으로 수정→재채점을 반복하는 오케스트레이션 스킬.

---

## 설정값 (변경 가능)

| 변수 | 기본값 | 의미 |
|------|--------|------|
| `MAX_ITER` | 5 | 최대 반복 회차 |
| `THRESHOLD` | 0.85 | 합격 기준 (qa-checker와 동일) |
| `STALL_WINDOW` | 2 | N회 연속 개선폭 < 0.02 이면 정체로 판정 |

---

## 루프 실행 순서

### 준비

1. 검증 대상 파일 경로를 확인한다 (css-builder가 생성한 HTML/CSS).
2. `iteration = 1`, `history = []`, `prev_aggregate = null` 로 초기화한다.
3. 루프를 시작한다.

---

### 매 회차 (iteration 1 → MAX_ITER)

#### STEP A — qa-checker 호출

다음 정보를 포함해서 `qa-checker` 서브에이전트를 호출한다:

```
검증 파일: {파일 경로}
iteration: {현재 회차}
prev_aggregate: {이전 회차 종합 점수 또는 null}
```

qa-checker는 **JSON만** 반환한다. 그 JSON을 그대로 파싱한다.

#### STEP B — verdict 분기

**`PASS`인 경우:**
- 루프 종료 → [최종 보고 — 성공](#최종-보고--성공) 으로 이동

**`STALL`인 경우:**
- 루프 중단 → [최종 보고 — 정체](#최종-보고--정체) 로 이동
- 사람(대표님)에게 방향 결정 요청

**`NEEDS_WORK`인 경우:**
- STEP C로 진행

#### STEP C — css-builder 호출

qa-checker JSON의 `priority_fixes` + 각 축의 `notes` 를 css-builder에게 그대로 전달한다.

```
[css-builder 호출 메시지 형식]

qa-checker 채점 결과 (회차 {N}):
- 종합 점수: {aggregate} / 0.85 기준
- 레이아웃: {score} — {notes}
- 타이포그래피: {score} — {notes}
- 색상: {score} — {notes}
- 네이밍: {score} — {notes}
- 접근성: {score} — {notes}

우선 수정 항목:
1. {priority_fixes[0]}
2. {priority_fixes[1]}
3. {priority_fixes[2]}

위 항목만 수정하고 다른 부분은 건드리지 마세요.
```

#### STEP D — 회차 기록 및 반복

```
history.append({
  iteration: N,
  aggregate: {점수},
  verdict: {판정},
  axes: {축별 점수}
})
prev_aggregate = aggregate
iteration += 1
```

- `iteration > MAX_ITER` 이면 → [최종 보고 — 회차 소진](#최종-보고--회차-소진)
- 아니면 → STEP A 반복

---

## 정체(STALL) 감지 규칙

qa-checker가 `STALL`을 직접 판정하지만, 루프에서도 이중 확인한다:

```
최근 STALL_WINDOW(=2)회 history를 보고,
연속으로 (aggregate 개선폭 < 0.02) 이면 정체로 판정.
```

정체 판정 시 → 루프 강제 중단 → 사람에게 best-of 결과와 함께 보고

---

## 최종 보고 형식

### 최종 보고 — 성공

```
✅ QA 루프 완료 — {N}회차만에 합격

종합 점수: {aggregate} / 0.85

회차별 점수 추이:
  회차 1: {score}
  회차 2: {score}
  ...
  회차 N: {score} ← PASS

최종 축별 점수:
  레이아웃    {score}
  타이포그래피 {score}
  색상       {score}
  네이밍     {score}
  접근성     {score}
```

### 최종 보고 — 정체

```
⚠️ QA 루프 정체 — {N}회차에서 막힘

종합 점수: {aggregate} (목표 0.85 미달)
판단: {STALL_WINDOW}회 연속 개선폭 < 0.02

회차별 점수 추이:
  회차 1: {score}
  회차 2: {score}
  ...

현재 최선 결과 (회차 {best_iter}, 점수 {best_score}):
  레이아웃    {score} — {notes}
  타이포그래피 {score} — {notes}
  색상       {score} — {notes}
  네이밍     {score} — {notes}
  접근성     {score} — {notes}

선택지:
  A) 디자인 요구사항을 완화하고 현재 결과로 진행
  B) css-builder에게 특정 항목 집중 수정 지시 후 재시도
  C) 처음부터 다시 (ref-analyzer → css-builder)
```

### 최종 보고 — 회차 소진

```
⏱ QA 루프 최대 회차({MAX_ITER}회) 소진

종합 점수: {aggregate} (목표 0.85 미달)

회차별 점수 추이:
  회차 1 → {score}
  회차 2 → {score}
  ...
  회차 {MAX_ITER} → {score}

최선 결과: 회차 {best_iter}, 점수 {best_score}

위와 동일한 선택지(A/B/C)로 판단 요청
```

---

## 핵심 원칙 (APapeIsName에서 차용)

1. **측정과 수정 분리**: qa-checker(측정)와 css-builder(수정)는 서로 대화하지 않는다. 루프가 중간에서 JSON 전달만 한다.
2. **종료 조건은 코드가 정한다**: AI 재량으로 "이만하면 됐다"를 선언하지 않는다. threshold와 MAX_ITER가 결정한다.
3. **실패를 몰래 통과시키지 않는다**: STALL/소진 시 사람에게 best-of를 올리고 판단을 받는다.
4. **점수가 낮은 축만 수정한다**: 통과한 축(≥0.85)은 css-builder에게 전달하지 않는다.

---

## 사용 예시

```
대표님: "이 코드 QA 루프 돌려줘"
→ /oh-my-claudecode:qa-loop 또는 "qa-loop 실행해줘"

대표님: "최대 3번만 반복해"
→ MAX_ITER=3으로 설정 후 실행

대표님: "기준 좀 낮춰서 0.80으로"
→ THRESHOLD=0.80으로 설정 후 실행
```
