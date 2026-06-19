# 규칙 — Cafe24 관리자·개발자센터 안내 전 웹 검증

> **적용:** 에이전트가 쇼핑몰 **관리자 메뉴명**, **개발자센터 경로**, **editor_type 명칭** 을 사용자에게 안내하기 **전**.

---

## 필수 절차

1. **웹 검색 또는 공식 URL fetch** 로 현재(2026) 메뉴·문서명 확인
2. 확인한 **출처 URL·날짜** 를 답변 또는 문서에 1줄 인용
3. 공식 HTML 미확인 항목은 **「⚠️ 미확인 — ecsupport/관리자에서 재확인」** 표기

Firecrawl CLI 미인증 시: `developers.cafe24.com` · `docs/_evidence/*.html` 스크랩 우선.

---

## 2026-06-19 검증됨 (developers.cafe24.com HTML)

| 구분 | 공식 명칭 | URL |
|------|-----------|-----|
| 개발자센터 상위 | **Design** | https://developers.cafe24.com/design/front/design |
| 스마트디자인 | **스마트 디자인** > **스마트디자인 소개** | /design/front/smart/sdsupport |
| 모듈 가이드 | **스마트디자인 모듈** | https://sdsupport.cafe24.com/product/list.html?cate_no=61 |
| editor_type (API) | **H**: 스마트디자인(HTML) · **E**: 스마트디자인Easy | `docs/_evidence/phase-1e-api-quotes.txt` |
| 앱 OAuth | 개발자센터 → **Apps > App 관리** | phase-1b-api-quotes.txt |

**미확인 (안내 시 주의):** 운영 쇼핑몰 관리자 「디자인 → 디자인 FTP → 권한 신청」 등 **ecsupport 본문 미수집** (`OFFICIAL-AUDIT.md` A-2d).

---

## 금지

- 학습 데이터·기억만으로 관리자 메뉴 경로 작성
- 「디자인관리 > 스킨편집」 등 연도·몰 유형별로 다른 경로를 단정

---

## 참조

- `agent-kit/.claude/commands/레퍼런스인입.md`
- `agent-kit/docs/OFFICIAL-AUDIT.md`
