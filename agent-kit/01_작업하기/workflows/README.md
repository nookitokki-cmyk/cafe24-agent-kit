# 워크플로우 정의 (01_작업하기/workflows/)

> 두뇌 문서가 정해 둔 작업 순서를 **실행 강제 가이드**로 격상시킨 폴더.
> `카페24-워크플로우` 전용 에이전트가 이 정의를 따라 단계를 진행·검증·재진입까지 자동 관리합니다.

---

## 제공되는 워크플로우 10종

| 워크플로우 | 파일 | 사용 시점 | 단계 수 |
|---|---|---|---|
| **full-renewal (전체 개편)** | [09-full-renewal.md](09-full-renewal.md) | **★A-to-Z 전체 페이지** 디자인 시스템 개편 — 유형별 재마크업/재스타일/JS재구축 자동 배분 `[검증됨·프로토타입]` | 8단계(0~7) |
| **production-skin-safety (배포 전 안전 점검)** | [10-production-skin-safety.md](10-production-skin-safety.md) | **SFTP 업로드 전** SmartDesign directive/module/variable/reference 보호영역 점검 | read-only 점검 |
| ez-three-step-pingpong | [08-ez-three-step-pingpong.md](08-ez-three-step-pingpong.md) | **압축 핑퐁** HTML skin → EZ FTP overlay → strip 스킵/선별 (07 요약 실행) | Phase A/B/C |
| ez-on-legacy-setup | [07-ez-on-legacy-setup.md](07-ez-on-legacy-setup.md) | **초기 세팅** 레거시 HTML 몰 + EZ base + `_ref*/` 레이어 | Phase 0~4 핑퐁 |
| reference-intake | [05-reference-intake.md](05-reference-intake.md) | **구현 전** 레퍼런스 URL 또는 시안 인입 (`/레퍼런스인입`) | 5단계 |
| measure-first | [04-measure-first.md](04-measure-first.md) | **수정 전** 폰트·여백 실측 (`/요소측정`) | 질문 핑퐁 |
| verify-loop | [06-verify-loop.md](06-verify-loop.md) | **구현 중** Phase별 score=100 only 자기검증 | 루프 |
| quick-fix | [01-quick-fix.md](01-quick-fix.md) | 단일 변경 (색·텍스트·이미지) | 3단계 |
| skin-build-standard | [02-skin-build-standard.md](02-skin-build-standard.md) | 큰 작업 (메인 리뉴얼·스킨 빌드) | 6단계 |
| reference-renewal | [03-reference-renewal.md](03-reference-renewal.md) | 레퍼런스/시안 1:1 구현 | 8단계 |

---

## 워크플로우 진입 방법

### 슬래시 명령 (가장 쉬움)
```
/카페24-워크플로우
```
→ `카페24-워크플로우` 에이전트가 어떤 워크플로우 쓸지 물어보고 자동 진행

### 상태 조회
이미 진행 중인 워크플로우 확인:
```
clients/{본인}/.workflow.md
```

---

## 처음 쓰는 작업자 권장 순서

1. **레거시 몰 + EZ (핑퐁 3단계)**: `08-ez-three-step-pingpong` — A HTML 복사 → B EZ overlay → C 선별/스킵
2. **레거시 몰 + EZ (전체)**: `07-ez-on-legacy-setup` — Phase 0 진단·판정 근거·Pre-flight
3. **첫 실습**: `01-quick-fix` — 3단계 짧음, 워크플로우 흐름 익히기
4. **두 번째**: `02-skin-build-standard` — 6단계 풀 플로우
5. **응용**: `05-reference-intake` → `03-reference-renewal` → `10-production-skin-safety` → `06-verify-loop` — 레퍼런스/시안 1:1 + 배포 전 안전 점검

---

## 관련 문서

- 잔여 작업 체크리스트: `brain/docs/REMAINING-WORK-CHECKLIST.md`
- 파일럿 수용 기준: `brain/docs/TEMPLATE-PILOT-ACCEPTANCE.md`
- 두뇌 문서: [`brain/docs/CAFE24-SMARTDESIGN-AGENT.md`](../../brain/docs/CAFE24-SMARTDESIGN-AGENT.md)
- 하이브리드 MCP 설계(초안): `brain/docs/HYBRID-ARCHITECTURE-DRAFT.md`
- 프로덕션 스킨 안전 점검: [`10-production-skin-safety.md`](10-production-skin-safety.md)
- 함정 회피: [`00_시작하기/04-자주-막히는-5가지.md`](../../00_시작하기/04-자주-막히는-5가지.md) (배포판 기준)
- 에이전트 헌법: 루트 [`CLAUDE.md`](../../CLAUDE.md)
