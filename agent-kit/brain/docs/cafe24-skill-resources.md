# 카페24 Skill 확장 자료 인덱스 (v2.4.0+)

> `.claude/skills/cafe24/` 안에 있는 자료. 작업 도중 필요할 때 핀포인트 로드 (전체 로드 X).

## ⚠️ v2.7.0 경고

`recipes/`·`templates/`는 비-카페24 출처(APapeIsName)에서 가짜 변수가 유입돼 **제거**됨.
카페24 변수 기준은 `references/variables.md`(검증본). 화면 조합은 검증된 `references/` + `snippets/`로.

---

## `snippets/` — 복사해서 쓰는 코드 조각

- `components/` (6) — header-sticky / product-card / banner-slider / footer-standard / breadcrumb / quick-view
- `css/` (8) — reset / typography / responsive-grid / ez-override / button-system / form-controls / modal-system / toast-notification
- `js/` (6, vanilla) — sticky-header / product-hover / scroll-animation / modal-toggle / tab-switcher / form-validator

---

## `design-tokens/` — Figma → CSS 토큰 자동 파이프라인 (4개)

`README.md` (워크플로우) · `tokens.schema.json` (검증) · `example-tokens.json` (예시) · `builder-guide.md` (변환 규칙)

---

## `brand-profile/` — 클라이언트 통합 프로필 (3개)

`README.md` · `brand-profile.schema.json` · `example-brand-profile.json`
클라이언트 메타·연락처·프로젝트·브랜드·페이지를 한 JSON에 통합.

---

## `workflows/cafe24-automation.md` — `/카페24-자동화` 6단계 파이프라인 문서

컨텍스트 로드 → 토큰 빌드 → HTML 생성 → 코드 리뷰 → qa-loop → SFTP 배포.

---

## `module-browser.html` — 시각 모듈 카탈로그

브라우저로 열면 19개 모듈을 그림으로 미리 볼 수 있는 단일 HTML. 검색·다크모드·복사 버튼.

---

## `references/troubleshooting.md` — 비코더 에러 5가지 + 수정 템플릿

모듈 미렌더링 / 변수 미치환 / EZ 오버라이드 / 모바일 깨짐 / 캐시 문제.

---

## 부속 인프라

- `.claude/agents/qa-checker.md` — Haiku 비주얼 검증 에이전트
- `.claude/skills/qa-loop/` — 합격 점수 0.85 자동 수정 루프
- `.claude/skills/카페24-자동화/SKILL.md` — 원클릭 파이프라인 슬래시 명령
