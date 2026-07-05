# /skin14 민감정보 점검

## 점검 범위
- 경로: `C:\nookitokki\cafe24-kit-작업본\web\cafe24\.Codex\clients\paransky97\src\skin14`
- 파일 수: 598개
- 주요 확장자: `.html`, `.css`, `.js`, `.json`, `.txt`, `.xml`, 이미지 파일

## 점검 항목
- 비밀번호, API 키, 토큰, Client Secret, Private Key
- `.env`, key/pem/token/credential 계열 파일명
- 이메일, 휴대폰, 전화번호, 사업자번호, 주민등록번호 패턴
- 계좌번호, 은행, 예금주 관련 하드코딩 값
- 로컬 PC 경로, 사용자명, OneDrive/Downloads 경로
- 누끼토끼/강의/데모/내부 작업 흔적

## 결과

### 고위험 민감정보
- 실제 비밀번호/API 키/토큰/Private Key: 발견 없음
- SFTP/OAuth 설정 파일: skin 폴더 내부 발견 없음
- 로컬 PC 경로/사용자명: 발견 없음

### 개인정보 패턴
- 실제 이메일: 발견 없음
  - `board/urgency/urgency.html`의 `master@domain.com`은 입력 예시 문구
- 실제 휴대폰/전화번호: 발견 없음
  - `000-0000-0000`은 입력 예시 문구
- 실제 사업자번호/주민등록번호: 발견 없음
- 실제 계좌번호: 발견 없음
  - `0000-000-00000`은 기본 템플릿 placeholder
  - 실제 계좌는 카페24 변수 `{$bank_acc_no}`, `{$bank_acc_owner}` 형태로만 노출

## 배포 전 주의할 비민감 항목
민감정보는 아니지만, 전체 폴더 배포 시 정리 여부를 판단해야 한다.

### 1. 누끼토끼 브랜드 노출
- `_nk/inc/insta.html`
- `@nookitokki`
- SnapWidget embed ID 포함
- 개인정보는 아니지만 클라이언트 사이트에 누끼토끼 인스타가 노출될 수 있으므로 배포 전 교체/삭제 권장

### 2. 강의/데모 파일
- `_class-demo/topbanner.html`
- `W5 강의 데모` 문구 포함
- 운영에는 불필요하므로 전체 배포 전 제외 권장

### 3. 백업 파일
- `_nk/_backup_footer_layoutbasic.html`
- `_nk/_backup_header_layoutbasic.html`
- 실제 민감정보는 발견되지 않았지만, 운영 배포 산출물에서는 제외 권장

### 4. 카페24 공개 식별자
- `paransky97`
- `ecimg.cafe24img.com/.../paransky97/...`
- `ez-settings.json`의 `mall_id`, `skin_code`, `skin_no`
- 쇼핑몰 공개 경로/스킨 메타 성격으로 판단. 비밀키는 아님

## 판정
- 개인정보/비밀번호/API 키 기준으로는 배포 차단급 민감정보 발견 없음
- 단, 브랜드 노출과 내부 데모/백업 파일은 배포 전 정리 권장
- 이미지 파일 내부의 시각적 개인정보는 OCR까지 수행하지 않았으므로, 배너 이미지에 사람 얼굴/연락처가 들어있는지는 별도 육안 확인 필요
