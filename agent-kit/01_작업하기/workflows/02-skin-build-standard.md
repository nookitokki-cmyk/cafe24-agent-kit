# 워크플로우: skin-build-standard (6단계 표준)

> 카페24 스킨 빌드·메인 페이지 리뉴얼·중대형 변경 시 사용하는 표준 워크플로우.
> `카페24-워크플로우` 에이전트가 이 정의를 따라 단계별로 진행·검증·재진입을 자동 관리합니다.

---

## 🎯 사용 시점

✅ 새 skin 통째 빌드 (skin1 복제 → skin7)
✅ 메인 페이지 통째 리뉴얼 (3섹션 이상 변경)
✅ EZ → HTML 모드 전환
✅ 디자인 시스템 재구축

❌ 색 한 줄만 수정 — `01-quick-fix` 사용
❌ 레퍼런스 URL 보고 통째 리뉴얼 — `03-reference-renewal` 사용

---

## 📋 6단계 정의

### ① 분석 (Analysis)

```yaml
목표: 현재 스킨 구조·EZ 잔존·module 사용 파악
산출물:
  - .workflow.md 의 "분석 결과" 섹션
  - 현재 skin의 디렉토리 트리
  - EZ 잔재 목록 (ezst-section·data-ez-* 등)
  - 사용 중인 module 목록 (product_listmain_N·xans-product 등)
  - 옵션·결제 로직이 어디 module 안인지
완료 기준:
  - 모든 ezst-section·data-ez-* 위치 파악됨
  - 옵션 module 위치 명시
  - 디자인 토큰 추출 (기존 색·폰트·간격)
자동 검증:
  - 없음 (분석은 검증보다 사용자 컨펌)
사용자 컨펌 게이트:
  - "이대로 진행해도 되겠어요?" → Y 면 ② 진입
```

#### 실행 흐름
1. `카페24-워크플로우` → `메인 에이전트(루트 CLAUDE.md)` 위임
2. `메인 에이전트(루트 CLAUDE.md)` 가 SFTP 로 skin 폴더 받아 분석
3. 두뇌 문서 함정(F1~F26·F35) 매칭하여 미리 발견된 함정 표시
4. 결과를 `.workflow.md` 에 기록
5. 사용자에게 결과 보여주고 컨펌 받음

---

### ② 클리닝 (Cleaning)

```yaml
목표: EZ 잔재·불필요 코드 제거, body·#wrap 초기화
산출물:
  - 정리된 skin 폴더 (백업 포함)
  - .workflow.md "클리닝 변경 목록"
완료 기준:
  - ezst-section 0개
  - data-ez-* 속성 0개
  - body max-width 해제됨 (필요 시)
  - #wrap overflow:hidden 해제됨 (F8 회피)
자동 검증:
  - code-reviewer (regex 룰 통과)
사용자 컨펌 게이트:
  - "옵션·결제 module 손상 없는지 라이브에서 한 번 확인" → Y 면 ③
```

#### 안전 장치
- 클리닝 전 skin 폴더 통째 백업 (`.backup-{날짜}`)
- module 손상 시 자동 롤백 옵션

---

### ③ 세팅 (Setup)

```yaml
목표: _nk/ 레이어 구축, 디자인 토큰·폰트·아이콘 정착
산출물:
  - _nk/css/tokens.css (디자인 토큰)
  - _nk/css/base.css (Pretendard + Phosphor)
  - _nk/inc/head.html (@import 집합)
  - _nk/css/{components,layout,utilities} 빈 골격
  - override-ez.css (또는 base.css 최상단) — **#container #contents width 블록 필수**
완료 기준:
  - Pretendard·Phosphor CDN 로드 확인
  - 디자인 토큰 CSS 변수로 정의됨
  - @css 지시어에 ?v=N 없음 (F3 회피)
  - **EZ 92% trap:** override 레이어 **첫 파일·첫 블록**에 `#container #contents { width:100% !important; margin:0 !important; }` (`brain/rules/ez-contents-width.md`, `brain/docs/snippets/ez-contents-override.css`)
  - DevTools 390px: `#contents` width = viewport (±4px)
자동 검증:
  - code-reviewer
  - qa-checker (라이브에서 폰트·아이콘 로드 확인)
사용자 컨펌 게이트:
  - "토큰·폰트 정상 적용?" → Y 면 ④
```

---

### ④ 생성 (Build)

```yaml
목표: 섹션별 _nk/inc/ + _nk/css/ 생성, @import 조립
산출물:
  - _nk/inc/{header,hero,banner,...}.html
  - _nk/css/{header,hero,banner,...}.css
  - 각 섹션의 nk- 접두사 클래스
완료 기준:
  - 모든 섹션이 **동일 base 템플릿** + `@media` 로 PC·MO 대응 (별도 `/sde_design/mobile/` HTML 금지 — `brain/rules/responsive-mobile.md`)
  - {$변수}는 module 안에만 (F2 회피)
  - anchorBoxId 2개 이상 (F4 회피)
  - 인라인 style 0
  - !important 0 (불가피 시 주석 명시)
자동 검증:
  - code-reviewer (regex 6종 룰)
  - 자동 grep 검증 (nk- 접두사·인라인 style·!important)
사용자 컨펌 게이트:
  - 로컬 미리보기 OK? → Y 면 ⑤
```

---

### ⑤ 검증 (Validation) — 가장 중요

```yaml
목표: 라이브 PC + 모바일 검증 통과
산출물:
  - 스크린샷 2장 (PC 1280·모바일 360)
  - 옵션·결제 1회 통과 기록
  - 콘솔 에러 0 확인
완료 기준:
  - 스크린샷이 의도와 일치
  - 콘솔 에러 0건
  - 4xx/5xx 0건
  - 옵션 선택·수량·장바구니 시나리오 1회 통과
  - 모바일 헤더·메뉴·결제 CTA 정상
자동 검증 (3중 게이트):
  - qa-checker (시각 1:1 비교)
  - code-reviewer (regex 룰)
  - 레퍼런스 있으면 /visual-verdict
재진입 트리거:
  - 검증 실패 시 ④ 생성으로 자동 복귀
사용자 컨펌 게이트:
  - 3중 검증 다 통과 → 사용자 직접 눈으로 1회 확인 → Y 면 ⑥
```

#### 검증 실패 시
- 어느 검증이 무엇 때문에 실패했는지 `.workflow.md` 에 기록
- 어느 섹션의 어떤 함정인지 두뇌 문서 함정(F1~F26·F35) 매핑
- ④ 단계로 자동 복귀, 해당 부분만 재작업

---

### ⑥ 출력 (Report)

```yaml
목표: 변경 요약 + 라이브 URL + 남은 이슈 보고
산출물:
  - .workflow.md "최종 보고" 섹션
  - 05_work-log.md 에 누적 기록
완료 기준:
  - 변경 파일 목록
  - 라이브 검증 URL
  - 남은 이슈 (있으면)
  - 다음 단계 제안 (있으면)
사용자 액션:
  - 클라이언트한테 보고할 메시지 작성 (선택)
  - 두뇌 문서에 새 함정 추가 (있으면)
```

---

## 🔄 단계 간 전환 규칙

```
①분석 → 컨펌 → ②클리닝 → 검증 → ③세팅 → 검증 → ④생성 → 검증 → ⑤검증 → 3중 게이트 → ⑥출력
                                                              ↓ 실패
                                                              ④재진입
```

- **단계 건너뛰기 절대 금지**
- 각 단계 게이트 조건 미달 시 다음 단계 차단
- 검증 실패 시 이전 단계로 자동 복귀

---

## 📊 상태 파일 (.workflow.md) 예시

```markdown
# 워크플로우 진행 상태

## 메타
- 클라: musatax
- 작업: 메인 페이지 리뉴얼
- 워크플로우: skin-build-standard
- 시작: 2026-06-08 14:00

## 진행
| 단계 | 상태 | 시작 | 완료 | 산출물 |
|---|---|---|---|---|
| ① 분석 | ✅ | 14:00 | 14:30 | analysis.md |
| ② 클리닝 | ✅ | 14:30 | 15:00 | (backup-20260608) |
| ③ 세팅 | ✅ | 15:00 | 15:40 | tokens.css·base.css |
| ④ 생성 | 🔄 | 15:40 | - | (진행 중: header·hero 완료, banner 작업 중) |
| ⑤ 검증 | ⏳ | - | - | - |
| ⑥ 출력 | ⏳ | - | - | - |

## 발견된 함정
- F1: skin1에 메인진열 견본 1개만 → 2개로 보강 필요 (④에서 처리)
- F8: #wrap overflow:hidden → 클리닝 완료

## 다음 액션
- ④에서 banner 섹션 마무리 → ⑤ 검증 진입
```

---

## 🚀 진입 명령

```
/카페24-워크플로우 시작
워크플로우: skin-build-standard
```

또는 자연어:
```
카페24-워크플로우 에이전트로 skin7 메인 리뉴얼 진행해줘.
6단계 표준 빌드.
```

---

## ⚠️ 주의

- ⑤ 검증 단계는 **절대 자동 통과 처리 금지** — 반드시 사용자가 눈으로 1회 확인
- ② 클리닝은 module 손상 위험 → 클리닝 후 라이브에서 옵션·결제 시나리오 1회 통과 필수
- 단계 건너뛰기를 사용자가 명시 요청해도 거부 (3회 거부 후 사용자 강제 우회 시에만 진행)
