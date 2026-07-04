# 워크플로우 05 — 레퍼런스·시안 인입 (reference-intake)

> **소통 에이전트 = 게이트keeper.** 구현 전에 「무엇을·어떤 구조로·어떤 숫자로」 합의한다.  
> 명령: `/레퍼런스인입` · 승인 후 → `/디자인수정` 또는 `03-reference-renewal`

---

## 언제 쓰나

- 레퍼런스 URL만 있을 때 (maeve 등)
- 작업자 **HTML/CSS/JS** 또는 **Figma** 시안만 있을 때
- **A 또는 B 하나만** 있어도 시작 (둘 다 필수 아님)
- 「전 페이지 1:1」「레퍼런스/시안 1:1」 시작 **맨 처음**

---

## 입력 (최소)

| 필수 | 설명 |
|------|------|
| 타겟 몰 | `/접속세팅` — 몰 ID, skin_code, FTP |
| 시안 소스 **택1** | A: 레퍼런스 URL · B: HTML zip 또는 Figma |

| 선택 | 기본값 |
|------|--------|
| 범위 | **레퍼런스/시안에서 확인 가능한 페이지 전부** |
| 완료 | PC 1440 + MO 390 |
| 데이터 | 디자인만 (배너·상품은 별도 합의) |

**PC+MO 동일 템플릿일 때 (필수):**

- [ ] 사용자에게 「모바일 전용 디자인 사용설정」**사용안함** 확인 요청 — `brain/rules/responsive-mobile.md` §필수: 관리자 설정 (MCP·FTP 변경 불가)
- [ ] `CAFE24.MOBILE_WEB=false` 라이브 확인 후 인입표 승인·구현 진행

---

## 절차 (5단계 — 코드 금지 구간)

```
Q1~Q6 질문 핑퐁
  → 페이지 인벤토리
  → 페이지 타입 표
  → 실측 시트 (+ HTML 구조 격차)
  → 사용자 「예」
  → 03-reference-renewal 3단계~(구현)
```

### 1. 시안 소스 판별

| 소스 | 실측 방법 |
|------|-----------|
| URL | Playwright + `getComputedStyle` + DOM 구조 |
| HTML | 제공 CSS + DevTools 또는 파일 파싱 |
| Figma | Figma MCP — font, color, spacing, auto-layout |

### 2. 페이지 인벤토리

레퍼런스 URL에서 수집:

- `/` 메인
- GNB `product/list.html?cate_no=*`
- Info: `/pages/*`, `member/*`, `order/basket.html`, `board/*`
- 푸터: agreement, privacy, guide, contact

시안만 있을 때: 프레임/파일명 → 타겟 URL 매핑 (없으면 「신규」).

### 3. 페이지 타입 표

| 타입 | 대표 | container (maeve 실측 예) | HTML 특이 |
|------|------|---------------------------|-----------|
| `hero-main` | `/` | 100%, pad 0 | `body.layout.cc`, 히어로 |
| `plp-full` | Men PLP | 100%, pad 50px 20px 100px | **banner**, menupackage, sortby ul |
| `pdp-full` | PDP | 100%, pad 20px 20px 100px | detailArea 50/50 |
| `narrow` | About, Login, Cart | max 1200px, pad 50px 20px 100px | 중앙 정렬 |
| `board` | Notice, FAQ | narrow 동일 | ec-base-table |

**주의:** PLP는 `narrow`(1200px)가 **아님**. 타입표에 반드시 `plp-full` 구분.

### 4. 실측 시트

`04-measure-first.md` 템플릿 + 타입별 container·grid·header.

격차표 작성 시 형용사 금지 (`03-reference-renewal` §5).

### 5. 사용자 승인

- 「예」 → `clients/{몰}/reference-intake.md` 저장
- 「수정」 → 해당 행만 고친 뒤 재확인
- 승인 전 **FTP·HTML·CSS 수정 금지**

---

## 산출물

| 파일 | 내용 |
|------|------|
| `clients/{몰}/reference-intake.md` | 인벤토리 + 타입표 + 실측 + HTML 격차 |
| (선택) `work/ref-*-layout-measure.md` | PLP 등 상세 실측 |

---

## 다음 워크플로

| 상황 | 다음 |
|------|------|
| 레퍼런스/시안 1:1 | `03-reference-renewal` 3단계~ (섹션/페이지별) |
| 단일 색·문구 | `01-quick-fix` |
| 스킨 전체 재구축 | `02-skin-build-standard` |

---

## 토큰·품질 원칙

1. **인벤토리 끝까지 수정 금지** (03과 동일)
2. **페이지 타입 먼저** — container max-width 추측 금지
3. **EZ HTML vs ref HTML** — CSS만으로 안 되면 list.html 교체를 타입표에 명시
4. **캐시** — 업로드 후 `?v=N` · 2~5분 (`03` §7)
