# /카페24-자동화 — 원클릭 파이프라인

> 카페24 클라이언트 작업을 명령어 하나로 처음부터 끝까지 자동 진행하는 워크플로우.
> 비코더는 클라이언트명만 넘기면 됩니다. 나머지는 누끼토끼 에이전트 팀이 알아서 처리합니다.

---

## 사용법

### 트리거 표현 (자연어)
다음 표현 중 아무거나 사용:
- "demo-brand 카페24 자동화 돌려줘"
- "/카페24-자동화 demo-brand"
- "demo-brand 한 번에 진행해줘"
- "demo-brand 토큰 새로 빌드하고 SFTP까지"

### 슬래시 명령 등록 (선택)
`~/.claude/commands/카페24-자동화.md` 파일로 등록하면 `/카페24-자동화 {client}` 형태로 호출 가능.
(파일 내용은 이 문서 하단의 "슬래시 명령 정의" 섹션 복사)

---

## 전체 흐름 (6단계)

```
입력: /카페24-자동화 {client}
  ↓
[1] 컨텍스트 로드 (brand-profile.json + design-tokens.json)
  ↓
[2] design-tokens.json → nk-tokens.css 자동 생성 (css-builder)
  ↓
[3] 페이지별 HTML 생성·갱신 (cafe24-ez + templates/{type}.html)
  ↓
[4] 코드 리뷰 (code-reviewer Opus, 누끼토끼 규칙 검증)
  ↓
[5] qa-loop 합격 점수 0.85까지 자동 수정 (qa-checker + 재수정)
  ↓
[6] SFTP 업로드 (deploy-assistant) + 완료 보고 (client-writer 초안)
```

---

## 각 단계 상세

### 1단계: 컨텍스트 로드

```
~/.claude/skills/cafe24/workflows/ 또는 메인 세션이 실행:

  read web/cafe24/.claude/clients/{client}/brand-profile.json
  read web/cafe24/.claude/clients/{client}/design-tokens.json

산출: 메모리에 컨텍스트 로드
  - tone, voice, target, keywords
  - design tokens (colors, typography, spacing)
  - pages[] 작업 대상 목록
  - constraints
```

검증:
- `brand-profile.json` 없으면 → "신규 클라이언트 온보딩 먼저 진행할까요?" 질문
- `design-tokens.json` 없으면 → "Figma URL 입력해서 토큰 추출할까요?" 질문

### 2단계: CSS 토큰 빌드

```
css-builder 에이전트 호출:
  input: design-tokens.json
  rule:  ~/.claude/skills/cafe24/design-tokens/builder-guide.md
  output: clients/{client}/04_design/nk-tokens.css
```

자동 검증:
- 누락 색상 0개
- `!important` 없음
- WCAG AA 대비비 통과

### 3단계: 페이지별 HTML 생성·갱신

```
brand-profile.json 의 pages[] 순회:
  for page in pages where status == "pending" or status == "design":

    cafe24-ez 에이전트 호출:
      input:
        - template: ~/.claude/skills/cafe24/templates/{page.type}.html
        - tokens: nk-tokens.css
        - brand: brand-profile.json brand 섹션
        - figma_node: page.figma_node (있으면 figma-explorer 사전 호출)

      산출: clients/{client}/{page.path 매핑}/{page.type}.html
```

각 페이지 작업 후 brand-profile.json 의 page.status를 "implementation"으로 자동 업데이트.

### 4단계: 코드 리뷰 (필수)

```
code-reviewer (Opus) 에이전트 호출:
  대상: 3단계에서 생성/수정된 모든 HTML/CSS
  체크:
    - nk- 접두사 준수
    - Pretendard / Phosphor 외 폰트·아이콘 없음
    - 인라인 style 없음
    - !important 없음 (또는 주석 사유)
    - italic 없음
    - 색상 대비 WCAG AA
    - 모바일 터치 타겟 44px
    - alt 텍스트 있음
    - 모듈 변수 모듈 scope 안에 사용
```

실패 시:
- 자동 수정 가능: cafe24-ez 재호출로 수정
- 자동 수정 어려움: 사용자에게 보고 후 중단

### 5단계: qa-loop 시각 검증

```
qa-loop 스킬 호출:
  대상: 4단계 통과한 페이지들
  비교: Figma 원본 시안 vs 실제 렌더링 스크린샷
  합격 기준: 점수 0.85 이상

  loop:
    qa-checker 점수 측정
    if 점수 < 0.85:
      cafe24-ez 재호출 (피드백 반영)
    else:
      break
```

최대 3회 반복 후 미합격이면 사용자에게 보고.

### 6단계: 배포 + 보고

```
deploy-assistant 에이전트 호출:
  대상: 5단계 합격한 HTML/CSS/JS
  방식: SFTP 업로드 (platform_detail.ftp_configured == true 일 때만)
  경로: 카페24 스킨 폴더 (skin_code 기반)

완료 후:
  - brand-profile.json history[] 항목 추가
    { "date": "오늘", "action": "/카페24-자동화 실행 완료 (N개 페이지)", "by": "/카페24-자동화" }
  - 각 page.status를 "deployed"로 갱신

client-writer 에이전트 호출:
  brand.voice 적용한 완료 보고 메시지 초안 생성
  → 사용자가 검토 후 클라이언트에게 전송
```

---

## 옵션 플래그

### 부분 실행

특정 페이지만 처리:
```
/카페24-자동화 demo-brand --pages=hero-main,plp-full
```

토큰만 새로 빌드 (HTML 건드리지 않음):
```
/카페24-자동화 demo-brand --only-tokens
```

리뷰·QA 건너뛰기 (긴급 핫픽스):
```
/카페24-자동화 demo-brand --skip-review --skip-qa
```
⚠️ 권장하지 않음. 사용자가 명시적으로 요청할 때만.

배포 안 함 (로컬 확인만):
```
/카페24-자동화 demo-brand --no-deploy
```

---

## 안전 장치

### 자동 백업
SFTP 업로드 전 `deploy-assistant`가 카페24 서버의 기존 파일을 자동 백업:
```
{스킨 폴더}/_backup/{YYYY-MM-DD_HHMMSS}/
```

### 변경 사항 미리보기
3-6단계 시작 전, 메인 세션이 사용자에게 변경 요약 표시 + 승인 요청:
```
다음 작업을 진행합니다:
- 페이지: hero-main, plp-full (2개)
- 토큰 변경: primary #2B2B2B → 동일 (변경 없음)
- 예상 소요: 약 5-10분

진행할까요? (예/아니오/일부만)
```

### 실패 시 롤백
6단계 SFTP 업로드 중 실패 시:
- 자동 백업에서 복구
- 사용자에게 실패 보고
- history[] 에 실패 기록

---

## 비코더용 사용 시나리오

### 시나리오 1: 신규 클라이언트 전체 작업
```
대표님: "demo-brand 새로 시작하는데 한 번에 진행해줘"
→ 메인이 brand-profile.json 없는 것 감지
→ "신규 클라이언트 온보딩 먼저 진행할까요?" 질문
→ 온보딩 완료 후 /카페24-자동화 자동 실행
```

### 시나리오 2: 색상만 변경 후 재배포
```
대표님: "demo-brand primary 좀 더 진하게 #1A1A1A로"
→ 메인이 design-tokens.json 수정
→ /카페24-자동화 demo-brand --only-tokens --skip-qa 자동 실행
→ SFTP 재업로드까지 1분 내 완료
```

### 시나리오 3: 특정 페이지만 작업
```
대표님: "demo-brand 상품 상세만 다시 만들어줘"
→ /카페24-자동화 demo-brand --pages=pdp-full
→ PDP만 처리, 다른 페이지 그대로
```

---

## 슬래시 명령 정의

다음 내용을 `~/.claude/commands/카페24-자동화.md`에 저장하면 슬래시 명령으로 등록됩니다:

```markdown
---
description: 카페24 클라이언트 작업 원클릭 파이프라인 (토큰 빌드·HTML 생성·리뷰·QA·SFTP 배포)
---

사용자가 `/카페24-자동화 {client}` 를 요청했습니다.

**역할:** 카페24 자동화 파이프라인 지휘자.

상세: `~/.claude/skills/cafe24/workflows/cafe24-automation.md`

## 진행 절차

1. 인자 파싱: `{client}` + 옵션 플래그(`--pages`, `--only-tokens`, `--skip-review`, `--skip-qa`, `--no-deploy`)
2. `web/cafe24/.claude/clients/{client}/brand-profile.json` 로드 (없으면 온보딩 안내)
3. 변경 요약을 사용자에게 미리 보여주고 승인 받음
4. 6단계 파이프라인 실행 (cafe24-automation.md 참조)
5. 단계별 진행 상태 보고 (긴 작업이라 진행률 표시)
6. 완료 보고 + client-writer 메시지 초안 제시

## 금지

- 사용자 승인 전 자동 SFTP 업로드
- `brand-profile.json` 없는 클라이언트에 강제 실행
- code-reviewer / qa-checker 건너뛰기 (--skip 플래그 명시 시만)
- 실패한 단계 무시하고 다음 단계 진행
```

---

## 관련 문서

- 컨텍스트: `../brand-profile/README.md`
- 토큰: `../design-tokens/README.md`
- 스타터: `../templates/`
- 리뷰: `.claude/agents/code-reviewer.md` (키트 내장 — cafe24 전용 룰 + traps.json 연동)
- QA: `~/.claude/skills/qa-loop/SKILL.md`
- 배포: `~/.claude/agents/deploy-assistant.md`
- 메시지: `~/.claude/agents/client-writer.md`
