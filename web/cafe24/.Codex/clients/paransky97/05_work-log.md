# 작업 로그

## 2026-06-27
- 카페24 신규 클라이언트 `paransky97` 온보딩 폴더 생성.
- Tally/Notion 제출 내역 없음으로 확인.
- 수동 요청사항 입력 대기 상태로 초기 문서 작성.
- OAuth/API 제외, SFTP 접속세팅만 진행하기로 확인.
- SFTP 발급 정보 확인 대기.
- `mcp/config/sftp_paransky97.json` 입력용 설정 파일 생성.
- SFTP 루트 읽기 테스트 성공: `/base`, `/mobile`, `/skin14`, `/skin16`, `/skin2`, `/web` 확인.
- 업로드 허용 경로는 아직 미지정 상태로 유지.
- `/skin14` 전체 다운로드 진행: 598개 성공 / 51개 실패.
- 실패 항목은 주로 `order/ec_orderform` 계열 SFTP 유령 항목으로 확인.
- base 의존성 점검 문서 작성: `01_요청사항/2026-06-27_skin14-base-dependency-check.md`.
- `/skin14` 민감정보 점검 완료: 비밀번호/API 키/개인 연락처 등 배포 차단급 민감정보 발견 없음.
- 배포 전 정리 권장 항목 확인: `@nookitokki` 인스타 위젯, `_class-demo`, `_nk/_backup_*`.
