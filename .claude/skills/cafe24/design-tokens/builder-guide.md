# Token Builder Guide (JSON → CSS)

> 이 문서는 `css-builder` 에이전트가 `design-tokens.json`을 읽고 `nk-tokens.css`를 생성할 때 따라야 하는 변환 규칙입니다.
> AI가 정확하게 토큰을 변환하도록 하기 위한 **계약서**입니다.

---

## 입력

- 파일: `web/cafe24/.claude/clients/{client}/design-tokens.json`
- 스키마: `~/.claude/skills/cafe24/design-tokens/tokens.schema.json` 준수 필수
- 검증 실패 시 변환 중단하고 사용자에게 검증 오류 보고

---

## 출력

- 파일: `web/cafe24/.claude/clients/{client}/04_design/nk-tokens.css`
- 인코딩: UTF-8 (BOM 없음)
- 줄 끝: LF
- 들여쓰기: 스페이스 2칸

---

## 변환 규칙

### 1. 헤더 주석 (필수)

생성된 파일 맨 위에 다음 주석 삽입:

```css
/*!
 * Auto-generated from design-tokens.json
 * Client: {client}
 * Source: {source} ({figma_url || "manual"})
 * Generated: {extracted_at}
 * Version: {version}
 *
 * ⚠️ 이 파일을 직접 수정하지 마세요.
 *     design-tokens.json을 수정하고 css-builder를 다시 실행하세요.
 */
```

### 2. 색상 토큰

`colors.{key}` → **flat 토큰명** (아래 대응표 — 토큰명에 `color` 네임스페이스를 끼운 옛 어휘 출력 금지):

| JSON 키 | flat 토큰명 |
|---|---|
| `colors.primary` | `--nk-point-active` |
| `colors.accent` | `--nk-point` |
| `colors.background` | `--nk-bg` |
| `colors.surface` | `--nk-bg2` |
| `colors.text` | `--nk-font` |
| `colors.text-sub` | `--nk-sub` |
| `colors.text-inverse` | `--nk-on-point` |
| `colors.border` | `--nk-border` |
| `colors.error` | `--nk-error` |
| `colors.success` | `--nk-success` |
| `colors.warning` | `--nk-warning` |

```css
:root {
  --nk-point-active: #2B2B2B;
  --nk-point: #C8A97E;
  /* ... */
}
```

규칙:
- 대응표에 없는 key는 flat 관례로 신설(`--nk-{key}`) — 네임스페이스 계층을 끼우지 않는다
- 누락 시 변환 안 함 (기본값 주입 금지)
- 8자리 hex(`#RRGGBBAA`)는 그대로 보존

### 3. 타이포그래피 토큰

`typography.font-family` → `--nk-font-family`
`typography.{level}.{prop}` → `--nk-{level}-{prop}`

```css
:root {
  --nk-font-family: 'Pretendard', sans-serif;

  --nk-heading-weight: 700;
  --nk-heading-size: 32px;
  --nk-heading-lh: 1.3;
  --nk-heading-letter-spacing: -0.02em;

  --nk-body-weight: 400;
  --nk-body-size: 15px;
  --nk-body-lh: 1.6;
}
```

규칙:
- `line-height` → `lh` (CSS 변수명 단축)
- font-family는 항상 `'Pretendard'` 우선, `sans-serif` fallback 자동 추가
- font-family에 italic 키워드가 있어도 무시 (누끼토끼 표준: italic 금지)

### 4. 간격 / 반경 / 그림자 — 리터럴 승격 · 단일 radius

간격(`spacing.*`)·그림자(`shadow.*`)는 **CSS 변수로 출력하지 않는다.**
컴포넌트 고유 여백·그림자는 컴포넌트 CSS에 **리터럴**로 기술한다(검증본 관례: 핵심 색·폰트·치수만 `var()`, 컴포넌트 고유 값은 리터럴).

- 간격 기준값: sm=8px · md=16px · lg=24px — JSON 값은 컴포넌트 작성 시 리터럴 참조용
- 그림자 기준값: 예) `0 2px 8px rgba(0,0,0,.08)` — 사용처에 리터럴로 기술
- 반경(`radius.*`)은 **단일 토큰 `--nk-radius`로 수렴** — 값은 `radius.md`(부재 시 4px). sm/lg/full 등 다른 단계는 호출부 리터럴 또는 fallback으로 보존

```css
:root {
  --nk-radius: 8px; /* radius.md — 단일 수렴 */
}
```

### 5. 브레이크포인트 — @media에 주입

브레이크포인트는 CSS 변수로 못 씁니다. 대신 파일 하단에 미디어 쿼리 가이드 주석을 삽입:

```css
/* 브레이크포인트 가이드 (CSS 변수 사용 불가, @media에서 직접 사용)
 * mobile:  375px
 * tablet:  768px
 * desktop: 1280px
 * wide:    1440px
 *
 * 예시:
 *   @media (min-width: 768px) { ... }
 *   @media (min-width: 1280px) { ... }
 */
```

### 6. 페이지 타입 / tone / notes

이 필드들은 CSS로 변환하지 않습니다. 사람이 보는 메타데이터.

다만 파일 끝에 참조 주석으로 남깁니다:

```css
/* 이 클라이언트 설정
 * page_types: hero-main, plp-full, pdp-full
 * tone: 럭셔리 미니멀 — 절제된 톤, 여백 강조
 */
```

---

## 검증 (변환 후 필수 확인)

1. **누락 색상 0개** — `colors.primary`, `text`, `background`는 반드시 출력
2. **단위 일관성** — px/rem 혼용 검토
3. **`!important` 금지** — 생성된 CSS에 없어야 함
4. **WCAG AA 대비비 확인** — `colors.text` vs `colors.background` 4.5:1 이상
5. **컴파일 검증** — 생성된 CSS를 PostCSS 또는 Stylelint로 파싱

---

## 갱신 시 동작

`design-tokens.json`이 변경되었을 때:

1. `version` 자동 증가:
   - 색상·폰트 패밀리 변경 → MINOR (1.0.0 → 1.1.0)
   - 토큰 추가만 → PATCH (1.0.0 → 1.0.1)
   - 키 이름 변경·삭제 → MAJOR (1.0.0 → 2.0.0)
2. `extracted_at` 오늘 날짜로 갱신
3. CSS 헤더 주석의 `Generated`, `Version` 동기화
4. 변경 항목을 사용자에게 diff로 보고
5. `deploy-assistant`에 SFTP 재업로드 알림

---

## 통합 시나리오

### 시나리오 A: 신규 클라이언트 (Figma 시안 있음)

```
1. /레퍼런스인입 실행
2. Q1 답변: "B) 작업자 시안 (Figma)"
3. Figma URL 입력
4. figma-explorer → design-tokens.json 추출 (스키마 검증)
5. 사용자에게 토큰 요약 보여주고 확인 받음
6. css-builder → nk-tokens.css 생성
7. /레퍼런스인입의 나머지 단계 (페이지 인벤토리·실측 시트) 계속
```

### 시나리오 B: 기존 클라이언트 색상 변경

```
1. 사용자: "demo-brand primary 좀 더 진하게 #1A1A1A로 바꿔줘"
2. 메인 세션이 design-tokens.json 열고 colors.primary 수정
3. version PATCH 또는 MINOR 증가
4. css-builder 자동 호출 → nk-tokens.css 재생성
5. deploy-assistant → SFTP 재업로드
6. client-writer → 클라이언트에게 적용 보고 초안
```

### 시나리오 C: 스크린샷에서 추출 (Figma 없음)

```
1. 클라이언트가 PDF·이미지로 시안 보냄
2. ref-analyzer가 색상·간격을 시각 분석으로 추출
3. design-tokens.json 임시 생성 (source: "screenshot")
4. 사용자 검토 후 확정
5. css-builder → nk-tokens.css 생성
```

---

## 한계와 fallback

### Figma Variable 없는 시안
- figma-explorer가 노드별 색상을 카운팅해서 빈도 기반 추출
- "이 색상이 정말 primary인가요?" 확인 질문 필수

### 그라데이션
- 자동 추출은 가능, 다만 단순화될 수 있음 (3-stop → 2-stop)
- 복잡 그라데이션은 별도 `--nk-gradient-xxx` 변수 + linear-gradient() 문자열로 저장

### 폰트가 Pretendard 아님
- 누끼토끼 표준은 Pretendard 고정
- 클라이언트 별도 지시가 있을 때만 변경
- 그 외 경우 사용자에게 "Pretendard로 변경 OK?" 확인 후 진행

---

## 관련 파일

- 스키마 정의: `tokens.schema.json`
- 예시: `example-tokens.json`
- 워크플로우: `README.md`
- 호출 에이전트: `figma-explorer`, `css-builder`
