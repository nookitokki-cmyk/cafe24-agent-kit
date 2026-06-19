# F 상황 인덱스 — 작업자·에이전트 공용 허브

> **읽는 법:** 증상이 생기면 **아래 표에서 F번호 찾기** → Q&A·프롬프트·상세 문서로 이동.  
> **두 갈래:** F1~F26 = 스킨·HTML 문법 함정 · F27~F35 = 레퍼런스 리뉴얼·검증 postmortem (2026-06 ecudemo400786)

---

## 빠른 찾기 (오늘 자주 나온 것)

| F코드 | 한 줄 | Q&A | 프롬프트 | 상세 |
|-------|-------|-----|----------|------|
| **F27** | 모바일 히어로 좌우 흰 여백 (`#contents` 92%) | [Q5](../getting-started/QnA-쉬운말로.md#f27) | [§05](../getting-started/프롬프트-템플릿.md#05-히어로-좌우-여백-contents-92) | [common-pitfalls §92%](common-pitfalls.md) · [ez-contents-width](../rules/ez-contents-width.md) |
| **F28** | 폰에서 `/m/` 기본 스킨만 보임 | [Q6](../getting-started/QnA-쉬운말로.md#f28) | [§04](../getting-started/프롬프트-템플릿.md#04-모바일-반응형-admin-off-안내-포함) | [common-pitfalls §mobile](common-pitfalls.md) · [responsive-mobile](../rules/responsive-mobile.md) |
| **F29** | 상품목록이 1200px로 좁음 | [Q7](../getting-started/QnA-쉬운말로.md#f29) | [§02](../getting-started/프롬프트-템플릿.md#02-plp-풀폭menupackagesortby-수정) | [common-pitfalls §narrow](common-pitfalls.md) |
| **F30** | PLP 배너·정렬 UI 구조가 다름 | [Q8](../getting-started/QnA-쉬운말로.md#f30) | [§02](../getting-started/프롬프트-템플릿.md#02-plp-풀폭menupackagesortby-수정) | [common-pitfalls §HTML](common-pitfalls.md) |
| **F31** | 장바구니 금액이 여러 줄로 깨짐 | [Q9](../getting-started/QnA-쉬운말로.md#f31) | [§03](../getting-started/프롬프트-템플릿.md#03-pdp--장바구니--회원--게시판) | [common-pitfalls §basket](common-pitfalls.md) |
| **F32** | 상품카드 글자 사이가 넓음 | [Q10](../getting-started/QnA-쉬운말로.md#f32) | [§07](../getting-started/프롬프트-템플릿.md#07-상품카드-행간description-타이트) | [measure-first](../workflows/04-measure-first.md) |
| **F33** | 「완료」인데 점수가 100 안 됨 | [Q11](../getting-started/QnA-쉬운말로.md#f33) | [§08](../getting-started/프롬프트-템플릿.md#08-자기검증-100점-루프-실토-먼저) | [verify-loop](../workflows/06-verify-loop.md) |
| **F34** | 관리자에서 모바일 설정을 꺼야 함 | [Q12](../getting-started/QnA-쉬운말로.md#f34) | [§04](../getting-started/프롬프트-템플릿.md#04-모바일-반응형-admin-off-안내-포함) · [§12](../getting-started/프롬프트-템플릿.md#12-관리자-설정-필요할-때) | [cafe24-admin-verify](../rules/cafe24-admin-verify.md) |
| **F35** | Easy 타입 + FTP/HTML 충돌 (GUI 깨짐) | [common-pitfalls §F35](common-pitfalls.md#f35--ez-gui--html-편집-충돌) | [07 Phase 0-D](../workflows/07-ez-on-legacy-setup.md) | [HTML 수정 FAQ](https://support.cafe24.com/hc/ko/articles/9131045034777) |
| **F36** | EZ 이식·통째 덮기 / ez-settings 무분별 삭제 / strip_ez | [brain §6 F36](CAFE24-SMARTDESIGN-AGENT.md) | [WORK-GUIDE §15](WORK-GUIDE.md) | `strip_ez.py` |
| **F3** | 올렸는데 2~5분 안 바뀜 (캐시) | [Q2](../getting-started/QnA-쉬운말로.md#f3) | [§10](../getting-started/프롬프트-템플릿.md#10-ftp-배포-후-캐시-확인) | [traps/INDEX](../traps/INDEX.md) |
| **F19** | 「이전 페이지」 한글·페이징 박스 깨짐 | [Q13](../getting-started/QnA-쉬운말로.md#f19) | [§06](../getting-started/프롬프트-템플릿.md#06-페이징-깨짐-ec-base-paginate) | [common-pitfalls §paginate](common-pitfalls.md) |

---

## 전체 마스터 표

| Code | 상황 한줄 | 관련 문서 | 오늘 실제 사례 |
|------|-----------|-----------|----------------|
| **C** | module 밖 `{$변수}` 금지 | [SMARTDESIGN-AGENT](CAFE24-SMARTDESIGN-AGENT.md) §4 | — |
| **F1** | `<section>` 120px 여백 → 상단 빈칸 | [traps/INDEX](../traps/INDEX.md) | — |
| **F2** | `overflow-x:hidden`이 sticky 깨짐 | traps/INDEX | — |
| **F3** | 업로드 후 2~5분 캐시·optimizer 지연 | traps/INDEX · [04-함정](../getting-started/04-자주-막히는-5가지.md) | ecudemo score FAIL을 격차로 오판 |
| **F4** | `@css`에 `?v=` 붙이면 CSS 깨짐 | traps/INDEX · 04-함정 | — |
| **F5** | find+perl 한 방에 → 조용히 실패 | traps/INDEX | — |
| **F6** | `.inner` 이중 패딩 | traps/INDEX | — |
| **F7** | logotop.css 로고 가운데 강제 | traps/INDEX | — |
| **F8** | GNB 가운데 absolute+translate | traps/INDEX | — |
| **F9** | css/module 두 번째 base 레이어 | traps/INDEX | — |
| **F10** | EZ `body max-width` 좌측 쏠림 | traps/INDEX | F27과 겹침 — MO는 **F27** 우선 |
| **F11** | `{$product_name}` alt 금지 | traps/INDEX | — |
| **F12** | Swiper v4/5 클래스 | traps/INDEX | — |
| **F13** | Grid + product_list width 25% | traps/INDEX | PLP 4열 축소 |
| **F14** | category.css `#category` margin | traps/INDEX | — |
| **F15** | 데이터 0건 빈 셸 | traps/INDEX | — |
| **F16** | `.detail_guide` 2열 flex | traps/INDEX | — |
| **F17** | PDP max-width 캡 → 양옆 빈공간 | traps/INDEX · [common-pitfalls §PDP](common-pitfalls.md) | ecudemo PDP 91→100 (`ref393674-sub-pdp`) |
| **F18** | `.infoArea margin-left` grid 잘림 | traps/INDEX | — |
| **F19** | 페이징 박스·화살표 base 스타일 | traps/INDEX · common-pitfalls §paginate | ecudemo 전 페이지 페이징 깨짐 |
| **F20** | select padding caret 겹침 | traps/INDEX | — |
| **F21** | 인라인 script `/` 이중 prefix | traps/INDEX | — |
| **F22** | @css 없는 파일 → base fallback | traps/INDEX | — |
| **F23** | SFTP 유령 스텁 | traps/INDEX | — |
| **F24** | 팝업 레이아웃 custom.css 미적용 | traps/INDEX | — |
| **F25** | `@layout` 경로 오타 | traps/INDEX | — |
| **F26** | `@layout` 안 부르는 고아 layout | traps/INDEX | — |
| **F27** | MO `#contents` 92% → 히어로 흰 gap | [ez-contents-width](../rules/ez-contents-width.md) | ecudemo400786 MO hero gap |
| **F28** | `/m/` 별도 mobile 스킨 | [responsive-mobile](../rules/responsive-mobile.md) | PC maeve / MO EZ 기본 |
| **F29** | PLP·PDP까지 1200px narrow | common-pitfalls §narrow | plp containerW ~1160 |
| **F30** | PLP HTML 구조 불일치 | common-pitfalls §근본원인3 | menupackage·sortby ul |
| **F31** | MO 장바구니 금액 줄바꿈 | common-pitfalls §basket | 10,000 / 원 / 12,500원 |
| **F32** | 상품카드 description 행간 | [measure-first](../workflows/04-measure-first.md) | PLP 카드 높이 과다 |
| **F33** | 검증 100점 미만 통과 처리 | [verify-loop](../workflows/06-verify-loop.md) | MO 100점 only |
| **F34** | 관리자 모바일 전용 디자인 ON | [cafe24-admin-verify](../rules/cafe24-admin-verify.md) | `CAFE24.MOBILE_WEB=true` |

---

## 작업자용 문서 연결

| 문서 | 용도 |
|------|------|
| [EZ-STRATEGY.md](EZ-STRATEGY.md) | **기본 EZ 전략** — strip (demo000) · ecudemo 스킵은 파일럿 예외 |
| [LEGACY-HUNTER.md](LEGACY-HUNTER.md) | **레거시 감사** — layout 고아·CSS 부채 grep (삭제 후보만, verify-loop 선행) |
| [키트-시작-가이드.md](../getting-started/키트-시작-가이드.md) | 배포본 첫 열기 · 워크플로·F27~34·명령 콤보 |
| [QnA-쉬운말로.md](../getting-started/QnA-쉬운말로.md) | 증상별 **[F?]** 태그 Q&A 18개 (쉬운 말) |
| [프롬프트-템플릿.md](../getting-started/프롬프트-템플릿.md) | F코드 붙은 복붙 프롬프트 12종 |
| [04-자주-막히는-5가지.md](../getting-started/04-자주-막히는-5가지.md) | 초보 5대 함정 ↔ F3·F4·C |
| [traps/INDEX.md](../traps/INDEX.md) | F1~F34 한 줄 + 등급 |

---

## 에이전트 읽기 순서

1. 이 표에서 F번호 확인  
2. `docs/CAFE24-SMARTDESIGN-AGENT.md` §6 (F1~F26 상세)  
3. F27+ 이면 `docs/common-pitfalls.md` 해당 섹션  
4. 수정 후 `workflows/06-verify-loop.md` score 스크립트
