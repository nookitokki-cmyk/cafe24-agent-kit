---
name: 업로드준비
description: 카페24 SFTP 업로드 전 안전 점검, 백업, 승인 게이트가 필요할 때
---

사용자가 `/업로드준비` 를 요청했습니다.

## 하드 룰

- 이 명령은 곧바로 업로드하지 않습니다.
- `skin-audit` 실패 시 업로드 준비를 중단합니다.
- 백업과 사용자 승인 전에는 `put` 또는 SFTP 업로드를 실행하지 않습니다.
- 주문/결제 영역은 기본 업로드 대상에서 제외하고, 필요하면 별도 확인을 받습니다.

## Q1. 몰 ID

「업로드 준비할 몰 ID는 무엇인가요?」

예: `ecudemo402325`

## Q2. 원격 스킨 경로

「업로드 대상 스킨 루트는 무엇인가요?」

예:

```text
/skin1
/skin14
/sde_design/base
```

## 로컬 준비 명령

```bash
cd mcp
python cli.py upload-prepare --mall {몰ID} --remote-root {/skinN}
```

이 명령은 다음만 수행합니다.

1. `agent-kit/clients/{몰ID}/src` 로컬 스킨 audit
2. blocker가 없을 때 `upload-manifest.json` 생성
3. 업로드 대상 파일과 백업 필요 여부 표시
4. `approved: false`, `will_upload_now: false` 상태로 멈춤

## 승인 전 보고

사용자에게 반드시 이렇게 말합니다.

```text
여기부터는 실제 카페24 서버에 반영될 수 있습니다.
먼저 백업 후 업로드해야 합니다.
진행할까요?
```

승인 전에는 업로드하지 않습니다.

## 완료 예시

```text
[업로드준비]
- audit: 통과 또는 차단
- manifest: agent-kit/clients/{몰ID}/upload-manifest.json
- 승인 상태: false
- 다음: 백업 후 사용자 승인 시에만 업로드
```
