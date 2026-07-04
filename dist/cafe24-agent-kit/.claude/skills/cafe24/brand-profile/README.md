# Brand Profile 시스템

> 클라이언트 한 명 = brand-profile.json 한 개. 모든 에이전트가 이 한 파일을 참조해서 일관된 작업을 수행합니다.
> 비코더는 새 작업 시작할 때마다 "이 클라이언트 색상이 뭐였지?" "톤은?" "어떤 페이지 만들기로 했지?"를 다시 답할 필요가 없습니다.

---

## 왜 필요한가요?

### 기존 워크플로우의 문제
- 클라이언트 폴더에 `CLAUDE.md` 텍스트 파일로 정보 저장 → AI가 항목별로 파싱하기 어려움
- 새 작업 시작할 때마다 "이 클라이언트 톤이 뭐였죠?" 반복 질문
- 색상·페이지 타입·연락처가 흩어져 있어서 일관성 깨짐
- 클라이언트가 늘어날수록 작업 시작 비용 증가

### brand-profile.json의 해결
- JSON 형식 → AI가 정확한 필드값 파싱
- 한 파일에 클라이언트 메타·디자인 참조·페이지 구성 통합
- 새 작업 시작 시 `brand-profile.json` 자동 로드 → 컨텍스트 즉시 복원
- 클라이언트별 작업 히스토리·산출물 트래킹 가능

---

## 전체 구조

```
web/cafe24/.claude/clients/{client}/
├── brand-profile.json       ← 이 시스템의 핵심
├── design-tokens.json       ← brand-profile.json이 참조
├── CLAUDE.md                ← 사람이 읽는 요약 (brand-profile.json에서 자동 생성)
├── 01_요청사항/
├── 02_수정사항/
├── 03_references/
├── 04_design/
│   └── nk-tokens.css        ← design-tokens.json에서 자동 생성
└── 05_work-log.md
```

---

## 파일 역할 분리

| 파일 | 역할 | 누가 수정 |
|---|---|---|
| `brand-profile.json` | 클라이언트 메타 + 디자인 참조 + 페이지 구성 | 메인 세션 / 자동 |
| `design-tokens.json` | 색상·폰트·간격 토큰만 | `figma-explorer` / 자동 |
| `nk-tokens.css` | CSS 변수 자동 생성물 | `css-builder` / 자동 |
| `CLAUDE.md` | 사람이 읽는 요약 | brand-profile.json에서 자동 동기화 |

> **진실의 원천 = `brand-profile.json` + `design-tokens.json`**. 다른 파일은 이 둘에서 파생.

---

## 라이프사이클

### 1. 신규 클라이언트 온보딩

```
사용자: "새 클라이언트 왔어, demo-brand"
→ 메인 세션이 web/cafe24/.claude/clients/demo-brand/ 생성
→ brand-profile.json 초기 골격 작성 (질문으로 채움)
→ Figma URL 있으면 design-tokens.json 추출 (figma-explorer)
→ CLAUDE.md 자동 생성
```

### 2. 작업 진행 중 갱신

```
사용자: "이 클라이언트 톤을 좀 더 럭셔리하게 가요"
→ brand-profile.json의 tone 필드 수정
→ CLAUDE.md 자동 재생성
```

### 3. 다음 작업 시작

```
사용자: "demo-brand 메인 페이지 수정"
→ 메인 세션이 brand-profile.json 자동 로드
→ "이 클라이언트는 럭셔리 미니멀 톤, 페이지 타입은 hero-main + plp-full + pdp-full,
   primary는 #2B2B2B, accent는 #C8A97E" 즉시 인지
→ cafe24-ez 에이전트에 컨텍스트 자동 전달
```

---

## 스키마 핵심 필드

자세한 구조는 `brand-profile.schema.json` 참고. 핵심:

```json
{
  "client": "demo-brand",
  "platform": "cafe24",

  "contact": {
    "company": "데모브랜드",
    "person": "김OO 대표",
    "email": "contact@demo-brand.com",
    "phone": "010-XXXX-XXXX"
  },

  "project": {
    "name": "쇼핑몰 리뉴얼",
    "start_date": "2026-06-21",
    "deadline": "2026-08-31",
    "status": "design"
  },

  "platform_detail": {
    "mall_id": "demo-brand",
    "skin_code": "2",
    "editor_type": "H",
    "ftp_configured": true
  },

  "brand": {
    "tone": "럭셔리 미니멀 — 절제된 톤, 여백 강조",
    "voice": "차분하고 정중함",
    "target": "30-50대 여성, 안티에이징 관심",
    "keywords": ["슬로우에이징", "미니멀", "본질"]
  },

  "design_tokens": "./design-tokens.json",

  "pages": [
    { "type": "hero-main", "path": "/", "status": "design" },
    { "type": "plp-full", "path": "/product/list", "status": "pending" },
    { "type": "pdp-full", "path": "/product/detail", "status": "pending" }
  ],

  "constraints": {
    "font": "Pretendard",
    "icon": "Phosphor",
    "css_prefix": "nk-",
    "no_italic": true
  },

  "history": [
    { "date": "2026-06-21", "action": "프로젝트 시작" }
  ]
}
```

---

## 에이전트별 활용

### `cafe24-ez` (실무)
- 모든 작업 시작 시 brand-profile.json 로드
- `brand.tone` / `constraints.font` / `design_tokens` 참조
- `pages[]` 배열에서 작업 대상 페이지 확인

### `figma-explorer`
- `design_tokens` 필드의 파일 경로에 결과 저장
- `brand-profile.json`의 `tone`을 추출 가이드로 사용

### `css-builder`
- design-tokens.json 읽고 nk-tokens.css 생성
- `constraints.css_prefix` 적용

### `client-writer`
- `contact.person` / `brand.voice` 참조해서 메시지 톤 조정
- `brand.tone`을 메시지 어조에 반영

### `deploy-assistant`
- `platform_detail.ftp_configured` 확인 후 SFTP 업로드

### `contract-maker`
- `contact` + `project` 정보를 계약서·견적서에 자동 주입

---

## 통합 시나리오

### 시나리오: 클라이언트 색상 변경 요청

```
1. 사용자: "demo-brand primary 좀 더 진하게"

2. 메인 세션 처리:
   - design-tokens.json 의 colors.primary 수정
   - brand-profile.json 의 history[] 항목 추가
     { "date": "...", "action": "primary 색상 변경 (#2B2B2B → #1A1A1A)" }

3. 자동 트리거:
   - css-builder → nk-tokens.css 재생성
   - deploy-assistant → SFTP 재업로드 대기
   - client-writer → 적용 보고 메시지 초안

4. 산출물 일관성:
   - CLAUDE.md 의 색상 섹션도 자동 동기화
   - 다음 작업부터 새 색상 자동 인지
```

### 시나리오: 신규 페이지 추가

```
1. 사용자: "demo-brand 이벤트 페이지도 추가하자"

2. 메인 세션 처리:
   - brand-profile.json 의 pages[] 에 항목 추가
     { "type": "narrow", "path": "/event/landing", "status": "pending" }

3. 다음 작업 시:
   - cafe24-ez 가 자동으로 이 페이지 타입 인지
   - templates/narrow.html 기반으로 시작
   - 동일 토큰 적용
```

---

## CLAUDE.md 자동 동기화

`brand-profile.json` 수정 시 `CLAUDE.md`를 다음 템플릿으로 자동 생성/갱신:

```markdown
# {client} — {project.name}

## 기본 정보
- 플랫폼: {platform}
- 클라이언트: {contact.company} / {contact.person}
- 시작일: {project.start_date}
- 마감일: {project.deadline}
- 현재 상태: {project.status}

## 브랜드
- 톤: {brand.tone}
- 보이스: {brand.voice}
- 타깃: {brand.target}
- 키워드: {brand.keywords | join(", ")}

## 디자인 시스템
- 토큰: ./design-tokens.json (참조)
- 폰트: {constraints.font}
- 아이콘: {constraints.icon}
- CSS 접두사: {constraints.css_prefix}

## 페이지 구성
{pages | format-as-table}

## 작업 히스토리
(자세한 내용은 brand-profile.json history[] 참조)
```

---

## 마이그레이션 (기존 CLAUDE.md → brand-profile.json)

기존 클라이언트는 CLAUDE.md 텍스트만 있는 경우가 많습니다.
다음 명령으로 변환:

```
사용자: "demo-brand 의 CLAUDE.md 를 brand-profile.json 으로 마이그레이션"
→ 메인 세션이 CLAUDE.md 파싱
→ brand-profile.json 골격 생성 (빈 필드는 사용자에게 질문)
→ design-tokens.json 분리 (있으면)
→ CLAUDE.md 는 자동 생성물로 전환
```

---

## 관련 파일

- 스키마 정의: `brand-profile.schema.json`
- 예시: `example-brand-profile.json`
- Design Token 연동: `../design-tokens/README.md`
- 자동화 워크플로우: `../workflows/cafe24-automation.md`
