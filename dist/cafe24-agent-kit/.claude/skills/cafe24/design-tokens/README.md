# Design Token Pipeline (Figma → 카페24 CSS)

> Figma 디자인을 카페24 스킨에 1:1로 옮길 때, "색상 코드 하나하나 직접 옮기는 작업"을 자동화하는 파이프라인입니다.
> 비코더는 Figma URL만 넘기면 됩니다. 나머지는 AI가 자동 처리합니다.

---

## 이게 왜 필요한가요?

기존 워크플로우의 문제:
- Figma 시안 받음 → 색상 hex 코드를 눈으로 보고 손으로 옮김 → 오타·누락 발생
- "primary 색상이 #2B6CB0인지 #2B6BB0인지" 헷갈리는 상황 반복
- 클라이언트가 색상 한 번 바꾸면 모든 CSS를 다시 손봐야 함

Design Token Pipeline의 해결:
- Figma URL → `figma-explorer` 에이전트가 자동 추출 → `design-tokens.json` 생성
- `css-builder` 에이전트가 JSON을 읽고 `:root { --nk-color-primary: #xxx; }` 자동 생성
- 클라이언트 색상 변경 시 → JSON만 수정하면 모든 CSS 자동 갱신

---

## 전체 흐름

```
[1] Figma URL 입력
    ↓
[2] figma-explorer 에이전트 호출
    → 색상 / 폰트 / 간격 / 그림자 / 반경 토큰 자동 추출
    ↓
[3] design-tokens.json 생성 (이 파일이 진실의 원천)
    ↓
[4] css-builder 에이전트가 JSON 읽기
    → :root { ... } CSS 변수 생성
    → Pretendard / Phosphor / nk- 접두사 규칙 자동 적용
    ↓
[5] 카페24 스킨에 주입
    → top.html 또는 head 영역에 <style> 삽입
    → 또는 별도 nk-tokens.css 파일로 SFTP 업로드
    ↓
[6] (선택) brand-profile.json 동기화
    → 클라이언트 폴더의 brand-profile.json에도 토큰 저장
    → 다음 작업 시 자동 재사용
```

---

## 토큰 문서의 두 형식 (JSON vs MD)

토큰은 목적에 따라 **두 가지 형식**으로 존재합니다. 역할이 다릅니다.

| 형식 | 파일 | 누가 읽나 | 역할 |
|---|---|---|---|
| **JSON** | `example-tokens.json` | 기계(css-builder) | `:root{}` CSS 변수로 자동 변환하는 **주입용 원본** |
| **MD(분석문서)** | `examples/design-analysis-example.md` | 사람·AI 판단용 | 색·폰트·컴포넌트가 **왜 이렇게 정해졌는지** 맥락까지 담은 **설계 근거 문서** |

- **JSON**은 값만 있는 순수 데이터라 기계가 정확히 파싱해 주입합니다.
- **MD 분석문서**는 YAML frontmatter에 토큰을 담고, 그 아래 산문으로 "이 크림 캔버스가 브랜드 정체성인 이유", "이 코랄은 어디에만 쓰는지" 같은 **판단 기준**을 설명합니다. AI가 "왜 이 색인지"를 이해하고 응용하려면 이 문서가 필요합니다.
- 예시(`examples/design-analysis-example.md`)는 Claude 브랜드 디자인 시스템을 분석한 실제 문서입니다. **형식(frontmatter 토큰 + 산문 근거)** 을 참고하세요.

> 정리: **JSON = 기계 주입용 값 / MD = 사람·AI 판단용 근거.** 둘은 같은 토큰을 다른 목적으로 담습니다.

---

## 사용 방법 (비코더용)

### 방법 1: 슬래시 명령으로 한 번에 (권장)

`cafe24-agent-kit` 레포의 `/레퍼런스인입` 명령어를 확장하면 다음 흐름이 됩니다:

```
/레퍼런스인입
→ Q1: 시안 소스? "B) 작업자 시안 (Figma)"
→ Figma URL 입력
→ ✨ Design Token 자동 추출 단계 추가됨
→ design-tokens.json 자동 생성 (확인 후 승인)
→ 페이지 인벤토리 + 실측 시트 작성
→ 토큰 기반 CSS 생성 (css-builder)
→ SFTP 업로드 대기
```

### 방법 2: 단독 호출

특정 클라이언트의 토큰만 추출하고 싶을 때:

```
"https://www.figma.com/design/{file-id}/{name}?node-id=42-15 이 시안에서
design token만 뽑아서 [클라이언트명]/design-tokens.json으로 저장해줘"
```

메인 세션이 `figma-explorer` 에이전트를 호출해서 처리합니다.

---

## 산출물

```
web/cafe24/.claude/clients/{client-name}/
├── design-tokens.json       ← 이 파이프라인의 핵심 산출물
├── 04_design/
│   └── nk-tokens.css        ← JSON에서 자동 생성된 CSS
└── ...
```

- `design-tokens.json` — 진실의 원천. 클라이언트가 색상 바꾸면 이것만 수정.
- `nk-tokens.css` — `:root` CSS 변수 모음. SFTP 업로드 대상.

---

## JSON 스키마

자세한 구조는 `tokens.schema.json` 참고. 핵심 필드:

```json
{
  "client": "demo-brand",
  "source": "figma",
  "figma_url": "https://figma.com/design/...",
  "extracted_at": "2026-06-21",

  "colors": {
    "primary": "#2B2B2B",
    "accent": "#C8A97E",
    "background": "#F9F7F4",
    "text": "#1A1A1A",
    "text-sub": "#666666",
    "border": "#E5E5E5"
  },

  "typography": {
    "font-family": "Pretendard",
    "heading": { "weight": 700, "size": "32px", "line-height": "1.3" },
    "body":    { "weight": 400, "size": "15px", "line-height": "1.6" },
    "caption": { "weight": 400, "size": "13px", "line-height": "1.5" }
  },

  "spacing": {
    "xs": "4px",  "sm": "8px",   "md": "16px",
    "lg": "24px", "xl": "40px",  "2xl": "64px"
  },

  "radius": { "sm": "4px", "md": "8px", "lg": "16px", "full": "9999px" },

  "shadow": {
    "sm": "0 1px 2px rgba(0,0,0,0.05)",
    "md": "0 4px 8px rgba(0,0,0,0.08)",
    "lg": "0 8px 24px rgba(0,0,0,0.12)"
  },

  "breakpoints": {
    "mobile": "375px",
    "tablet": "768px",
    "desktop": "1280px",
    "wide": "1440px"
  }
}
```

---

## 생성되는 CSS 예시

위 JSON에서 `nk-tokens.css`가 다음과 같이 자동 생성됩니다:

```css
/* Auto-generated from design-tokens.json — 2026-06-21 */
/* Source: Figma — demo-brand */

:root {
  /* 색상 */
  --nk-color-primary: #2B2B2B;
  --nk-color-accent: #C8A97E;
  --nk-color-background: #F9F7F4;
  --nk-color-text: #1A1A1A;
  --nk-color-text-sub: #666666;
  --nk-color-border: #E5E5E5;

  /* 타이포그래피 */
  --nk-font-family: 'Pretendard', sans-serif;
  --nk-heading-weight: 700;
  --nk-heading-size: 32px;
  --nk-heading-lh: 1.3;
  --nk-body-weight: 400;
  --nk-body-size: 15px;
  --nk-body-lh: 1.6;

  /* 간격 */
  --nk-space-xs: 4px;
  --nk-space-sm: 8px;
  --nk-space-md: 16px;
  --nk-space-lg: 24px;
  --nk-space-xl: 40px;
  --nk-space-2xl: 64px;

  /* 반경 */
  --nk-radius-sm: 4px;
  --nk-radius-md: 8px;
  --nk-radius-lg: 16px;
  --nk-radius-full: 9999px;

  /* 그림자 */
  --nk-shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --nk-shadow-md: 0 4px 8px rgba(0, 0, 0, 0.08);
  --nk-shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.12);
}

/* 브레이크포인트는 @media에서 사용 (CSS 변수 불가) */
/* mobile: 375px / tablet: 768px / desktop: 1280px / wide: 1440px */
```

---

## 사용처별 적용 가이드

### top.html 직접 주입 (가장 간단)
```html
<head>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@latest/dist/web/static/pretendard.css">

  <!-- 여기에 nk-tokens.css 내용 통째로 붙여넣기 -->
  <style>
    :root { --nk-color-primary: #2B2B2B; ... }
  </style>
</head>
```

### 별도 CSS 파일로 SFTP 업로드 (권장)
```
1. nk-tokens.css 를 SFTP로 /web/upload/(스킨번호)/ 에 업로드
2. top.html에 <link rel="stylesheet" href="/web/upload/nk-tokens.css"> 삽입
3. 컴포넌트 CSS에서 var(--nk-color-primary) 식으로 참조
```

### EZ 에디터 호환 주의
- EZ 에디터는 인라인 style을 자주 덮어씁니다
- 토큰 사용 컴포넌트는 `references/troubleshooting.md`의 "EZ 오버라이드 패턴" 참고
- `class="nk-...---ez-safe"` 패턴으로 EZ 영향 회피

---

## 토큰 변경 시 워크플로우

클라이언트가 "primary 색상 좀 더 진하게 해주세요" 요청:

1. `design-tokens.json` 열고 `colors.primary` 값만 변경
2. `css-builder` 에이전트에 "토큰 다시 빌드" 요청
3. `nk-tokens.css` 자동 재생성
4. `deploy-assistant`로 SFTP 재업로드
5. 클라이언트에게 변경 보고 (`client-writer`)

CSS 파일 여러 군데를 손볼 필요 없음. **토큰 JSON 한 군데만 수정**.

---

## 제한 사항

- **Figma MCP 서버 연결 필수** — `figma-explorer` 에이전트가 사용
- **Figma 디자인 토큰 사용 권장** — Variable 또는 Style이 정의되지 않은 시안은 추출 정확도 낮음
- **그라데이션·복합 그림자** — 자동 추출 가능하지만 수동 검토 권장
- **이미지 토큰** (배경 패턴 등) — 별도 다운로드 필요

---

## 다음 단계 로드맵

이 파이프라인의 v2 계획:
- [ ] `brand-profile.json` 시스템과 통합 (한 클라이언트 = 토큰 + 메타데이터)
- [ ] 토큰 변경 시 자동 시각 회귀 테스트 (qa-checker 활용)
- [ ] Figma Variables → 다크모드 토큰 자동 매핑
- [ ] `/카페24-자동화` 원클릭 명령에 통합

---

## 관련 문서

- 워크플로우 통합: `.claude/skills/레퍼런스인입/SKILL.md`
- CSS 토큰 사용 예: `~/.claude/skills/cafe24/snippets/css/nk-typography.css`
- 트러블슈팅: `~/.claude/skills/cafe24/references/troubleshooting.md`
- 모디파이어: `~/.claude/skills/cafe24/references/modifiers.md`
