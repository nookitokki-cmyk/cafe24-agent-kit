# 규칙 — 전체 해상도 대응 (와이드 끝단 포함, 필수)

> **MANDATORY:** 검증은 **모바일(375)부터 와이드(2560)까지 전 구간**에서 한다.
> **1440만 보면 와이드 전용 버그를 놓친다.** 특히 콘텐츠 `max-width` 상한, 카드 이미지 미충전은
> 1440 이하에선 멀쩡해 보이고 **1600 초과 화면에서만 드러난다.**

---

## 왜 필요한가 (실제 사고 — ecudemo400125)

`nk-skin.css` 원본에 두 가지가 박혀 있었다:

```css
#main #contents .nk-best { width:100%; max-width:1600px; ... }  /* ← 상한 */
#main .nk-best .prdImg img { width:100%; ... }                  /* ← 잎만, 줄기 누락 */
```

| 폭 | 증상 |
|----|------|
| ≤1440 | **정상으로 보임** (콘텐츠가 1600보다 좁아 상한 미발동) |
| 1920 | 콘텐츠가 1520 밴드에 갇힘, 양옆 200px 빈 여백, 카드 이미지 220px |
| 2560 | 양옆 **520px** 빈 여백, 카드만 가운데 좁게 |

→ **레거시도 오버라이드 오류**다(상한값 가정 오류 + 체인 미완성). 그런데 **1440에서만 검증해서 못 잡았다.**
이 규칙은 그 재발을 막는다.

---

## 검증 폭 (필수)

| tag | width | 목적 |
|-----|-------|------|
| mobile | 375 (또는 390) | 모바일 스태킹·드로어 ([responsive-mobile.md](responsive-mobile.md)) |
| tablet | 768 | 중간 브레이크포인트 |
| pc | 1440 | 표준 데스크톱 |
| **wide** | **1920** | **상한 버그 발동 구간 — 필수** |
| **ultrawide** | **2560** | **풀블리드 레퍼 1:1 검증 — 필수** |

> 레퍼런스가 **풀블리드(full-bleed)**면 **1600 초과 폭 캡처는 생략 불가**.
> `capture-pair.mjs`가 이제 `pc/mobile/wide/ultrawide`를 기본 캡처한다.

---

## 함정 ① — 콘텐츠 `max-width` 상한 (와이드에서 좁은 밴드)

레퍼를 **재보지 않고** `max-width:1600px` 같은 상한을 박으면, 그 폭 초과 화면에서
콘텐츠가 가운데 좁은 띠 + 양옆 거대한 빈 여백이 된다(2560에서 양옆 520px).

| ✅ MUST | ❌ NEVER |
|---------|----------|
| 상한은 **레퍼가 실제로 상한이 있을 때만**. 측정으로 확인 | "보기 좋겠지" 추정으로 `max-width` 박기 |
| 풀블리드면 `max-width:none` + 좌우 `padding`(예 30px) | `width:100%`+`padding`인데 `box-sizing` 누락 → 우측 오버플로 |
| **와이드에서 ref↔live 컨테이너 좌우 좌표 측정** | 1440에서만 보고 "정렬 OK" 판정 |

```css
/* 풀블리드 콘텐츠 — 레퍼가 풀폭일 때 상한 금지 */
#main #contents .nk-best {
  box-sizing: border-box;   /* width100%+padding 합산 → 우측 오버플로 방지 */
  width: 100%; max-width: none; margin: 0; padding: 0 30px;
}
```

## 함정 ② — 카드 이미지가 카드를 못 채움 (체인이 `inline`)

base가 `.thumbnail / .prdImg / a`를 `inline`으로 두면, 이미지에 `width:100%`만 걸어도
**이미지 자연폭(예 220px)에 갇혀** 카드(450px)를 못 채운다. **잎(img)만 칠하고 줄기를 안 편 것.**

```css
/* 썸네일 체인을 블록 풀폭으로 — 와이드에서 이미지가 카드를 채우도록 */
#main .nk-best .thumbnail,
#main .nk-best .prdImg,
#main .nk-best .prdImg > a { display: block; width: 100%; }
```

---

## 검증 (capture-pair)

```bash
node .claude/skills/cafe24/scripts/capture-pair.mjs <레퍼URL> <라이브URL>
# → pc(1440) · mobile(390) · wide(1920) · ultrawide(2560) 캡처
```

**PASS 기준:** 모든 폭에서 ref↔live **콘텐츠 좌우 좌표·카드 폭·이미지 충전**이 일치.
와이드에서 빈 여백이 레퍼보다 크면 함정 ①, 카드보다 이미지가 작으면 함정 ②.

---

## 관련

- [responsive-mobile.md](responsive-mobile.md) — 모바일(단일 base @media) + 관리자 설정
- [ez-contents-width.md](ez-contents-width.md) — EZ `#contents` 92% 폭 (좁은 끝단)
- [`references/accuracy-gate.md`](../../../.claude/skills/cafe24/references/accuracy-gate.md) — 3축 합격 게이트(폭 전 구간)
- [`02_막혔을때/함정-INDEX.md`](../../02_막혔을때/함정-INDEX.md)
