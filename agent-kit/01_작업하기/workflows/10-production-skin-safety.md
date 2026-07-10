# 10. 프로덕션 스킨 안전 점검

이 문서는 카페24 스킨을 실제 배포하기 전에 깨지기 쉬운 영역을 먼저 찾는 절차입니다. 목적은 “없는 파일을 만들어 맞추기”가 아니라, Cafe24가 서버에서 채우는 영역과 로컬 스킨이 책임지는 영역을 구분하는 것입니다.

## 언제 쓰나요?

- 기존 스킨을 크게 리뉴얼하기 전
- 외부 제작사가 만든 완성형 스킨을 NK 방식으로 옮기기 전
- 상품목록, 상품상세, 게시판, 회원, 주문 경계까지 한 번에 점검할 때
- SFTP 업로드 전 “이 파일을 정말 내가 고쳐도 되는지” 확인해야 할 때

## 핵심 원칙

1. `module="..."`은 Cafe24가 데이터를 넣는 자리입니다. 삭제하면 화면이 비거나 주문/상품 기능이 깨질 수 있습니다.
2. `{$...}`는 Cafe24 서버가 바꾸는 변수입니다. 직접 지우거나 일반 텍스트로 바꾸면 안 됩니다.
3. `<!--@css(...)-->`, `<!--@js(...)-->`, `<!--@import(...)-->`, `<!--@layout(...)-->`, `<!--@contents-->`는 SmartDesign 연결선입니다.
4. `/order/ec_orderform/` 계열은 보호 영역입니다. 기본값으로 수정하지 않습니다.
5. 다국어몰은 직접 URL을 하드코딩하지 않고 `Layout_multishopList` 계열 모듈을 유지합니다.
6. 접근 불가 파일은 빈 파일로 만들지 않습니다. “로컬 스냅샷에 없음”과 “Cafe24 런타임 제공”을 분리해서 기록합니다.

## 로컬 점검 명령

키트 루트에서 실행합니다.

```bash
python mcp/cli.py skin-audit agent-kit/clients/_verified-template/src --json-out tmp/skin-audit.json
```

결과 파일에서 확인할 항목:

- `summary`: directive, module, variable, reference 수량
- `criteria`: v2.13 안전 기준별 통과 여부
- `reference_edges`: 어떤 파일이 어떤 리소스를 참조하는지
- `blockers`: 로컬 스킨 소유 파일 누락 또는 위험 참조
- `warnings`: 인코딩 fallback 등 점검 중 주의할 내용

## 결과를 읽는 방법

| 항목 | 쉬운 의미 | 행동 |
|---|---|---|
| `smartdesign_directives_found` | SmartDesign 연결선이 남아 있음 | false면 업로드 전 중단 |
| `modules_found` | Cafe24 데이터 삽입 자리가 남아 있음 | false면 HTML을 다시 확인 |
| `variables_found` | `{$...}` 서버 변수가 남아 있음 | false면 변수 삭제 여부 확인 |
| `order_ec_orderform_protected` | 주문/결제 보호 영역을 로컬 파일처럼 다루지 않음 | false면 주문 경계 수정 중단 |
| `smartdesign_define_not_treated_as_file` | `@define`을 실제 파일 누락으로 오해하지 않음 | false면 analyzer 결과 확인 |
| `multishop_module_source_of_truth` | 다국어몰 source-of-truth가 Cafe24 module임 | false면 하드코딩 링크 의심 |
| `idio_value_prefix_not_core_behavior` | `value-mshop-*` 같은 설정값을 핵심 동작으로 오해하지 않음 | false면 JS 해석 재검토 |
| `missing_skin_owned_refs_reported` | 스킨 소유 누락 참조를 숨기지 않음 | false면 누락 파일 먼저 해결 |

## 배포 전 금지 항목

- 접근 불가 파일을 빈 파일로 만들어 업로드
- `order/ec_orderform/**` 직접 수정
- `value-mshop-*` 값만 보고 다국어몰 링크 생성
- 없는 JS 파일이 있는 것처럼 가정
- `module="..."`이나 `{$...}`를 디자인 편의상 삭제
- SFTP 업로드를 사용자 확인 없이 실행

## 통과 기준

- SmartDesign directive가 남아 있어야 합니다.
- Cafe24 module과 변수가 남아 있어야 합니다.
- 보호 영역이 분류되어야 합니다.
- missing reference가 있으면 숨기지 말고 보고해야 합니다.
- 배포 전에는 반드시 백업과 rollback 경로를 확인해야 합니다.

## MCP에서 쓰는 경우

로컬 스냅샷 폴더를 만든 뒤 `analyze_skin_snapshot` MCP tool에 그 폴더 경로를 넘깁니다. 이 tool은 read-only입니다. SFTP 접속, 업로드, 삭제, 원격 변경을 하지 않습니다.
