---
name: EZ제거
description: Phase C EZ strip — strip_ez.py·사용자 승인 게이트
---

사용자가 `/EZ제거` 를 요청했습니다. **한 번에 질문 하나.**

전략: [`brain/docs/EZ-STRATEGY.md`](../../brain/docs/EZ-STRATEGY.md) — 기본 **strip** (demo000). ecudemo400786 Phase C 스킵은 **예외**.

## Q1. Phase B 완료

「Phase B (EZ overlay + `_ref*/`) 가 끝났고 **Pre-flight C1 PASS** 인가요?」

- 아니오 → `01_작업하기/workflows/08-ez-three-step-pingpong.md` Phase B 먼저

## Q2. strip 범위

「**전량 strip** (layout·index·product) 인가요, **선별** 인가요?」

- 레퍼런스: `clients/demo000/.workflow.md`

## Q3. 백업

「`cafe24_sftp_backup` 또는 로컬 deploy 스냅샷 **백업 OK**인가요?」

- 아니오 → 백업 후 진행

## Q4. 사용자 승인 (필수)

「Phase C strip 을 **실행해도 될까요?** (예/아니오)」

- **아니오** → 중단
- **예** → 아래 도구 (에이전트가 실행, 사용자 컨펌 후)

```bash
# 대상 경로는 몰·스킨에 맞게
python mcp/work/scripts/strip_ez.py --help
```

워크플로: `01_작업하기/workflows/08-ez-three-step-pingpong.md` Phase C

## 완료

```
[EZ제거 게이트]
- strip 실행 여부: 사용자 「예」 후에만
- 다음: 06-verify-loop · score-plp 등
```
