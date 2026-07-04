# 입력 파이프라인 — 레퍼런스 URL / Figma → 토큰 + 에셋 (Phase 2)

> 키트 목표의 **정문(front door)**: 비코더가 가진 *레퍼런스 URL 또는 Figma 시안* 을
> 카페24 구현의 재료(디자인 토큰 + 이미지 인벤토리)로 자동 변환한다.
> 출력은 ③매핑·④코드생성(`css-builder`·`cafe24-ez`)의 입력이 된다.

---

## 두 입력 경로

### A. 레퍼런스 URL (실사이트)
```
node scripts/extract-tokens.mjs --url <레퍼런스> --client 몰ID --out tokens.json
node scripts/extract-assets.mjs --url <레퍼런스> --out assets.json
```
- **extract-tokens.mjs** — computed style 에서 색·폰트·타입스케일 추출 → `design-tokens.json` 포맷(초안). (P4 해소: 색상코드 수기입력 제거)
- **extract-assets.mjs** — `<img src/srcset/data-src>` + `<picture>` + **computed `background-image`** + `<video poster>` 까지 전부 수집, **히어로 후보** 표시. (P3 해소: 히어로/배너 background 누락)
- 둘 다 **데스크톱 UA 1440** 고정.

### B. Figma 시안
- `design-tokens/` 파이프라인 (figma-explorer → 토큰 JSON). `design-tokens/README.md` 참조.
- 산출물 포맷은 A와 동일(`example-tokens.json`) → 이후 단계 공통.

---

## ⚠️ 추출값은 초안 — 반드시 검토

- `extract-tokens.mjs` 의 `colors.primary/accent/background` 는 **휴리스틱 매핑**이다. `_candidates` 를 보고 보정.
- 폰트: 레퍼 폰트는 **참고용**. NOOKITOKKI 표준은 Pretendard — 클라이언트 지시 없으면 Pretendard 유지.
- spacing: 자동추출 아님(표준 스케일). 필요 시 조정.
- 이미지: URL 목록만 수집(다운로드 X). 실제 사용 전 저작권·교체 여부 판단.

---

## 전체 흐름에서의 위치
```
[입력: URL 또는 Figma]
  → (이 문서) extract-tokens + extract-assets / figma 토큰   → tokens.json + assets.json
  → ①-b 컴포넌트 갤러리 생성 (component-gallery/)   → nk-components.css + example-gallery.html
        · 토큰(값)으로 버튼·폼·카드 "완성 부품"을 조립해 진열대에서 로컬 QA
  → ② 방식 판별 (skin-method-detect.md)
  → ③ 매핑 → ④ 코드 생성 (토큰 + 갤러리 부품 재사용)
  → ⑤ 배포 → ⑥ 3축 합격 게이트 (accuracy-gate.md)
```
- 정확도 검증은 ⑥에서 **레퍼런스 vs 결과 시각 비교**(capture-pair.mjs + qa-checker)로 닫힌다 → 입력 추출이 부정확해도 게이트가 잡아낸다.
