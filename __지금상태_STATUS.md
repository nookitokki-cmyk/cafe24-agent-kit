# ✅ 카페24 에이전트 키트 — 단일 기준 (THE ONE)

- 위치: C:\dev\cafe24-agent-kit  (← 작업은 여기서만)
- 버전: v3 통합 / 2026-06-20
- 다른 곳의 사본은 전부 구버전·보관용. 헷갈리면 이 파일을 보세요.

## 어디까지 했나 (재발 방지 현재상태)
- [x] Step 0  불변 백업 zip 8개 (OneDrive\문서\개발\_archive\cafe24-kit-원본스냅샷_2026-06-20\, 무결성 검증완료)
- [x] Step 1-1 새 폴더 생성 (OneDrive/git 밖 = 시크릿·충돌 위험 차단)
- [x] Step 1-3 깨끗한 부분만 복사 (비밀파일·임시물 제외)
- [x] Step 1-4 핵심자산 12종 전부 포함 (설계서 MCP-DESIGN.md · 손발 mcp · 두뇌 agent-kit)
- [x] Step 1-5 시크릿 0개 (verify-kit.sh 비번 스크럽 완료)
- [x] Step 1-7 사본 정리: 안전한 4곳 보관소 이동 완료 (agent-kit · agent-kit-cafe24-agent-final · 키트-배포판 · 키트-백업) / cafe24-agent-workspace 1곳은 실행중 앱이 사용중이라 **보류** / OneDrive 라이브 3곳(mcp·api-poc·web-cafe24/agent-kit)은 Step 2에서 연결 정리
- [x] Step 2  보안 정리 + 기술수정: ①build-dist 클라제외+demo000 ②SFTP 호스트키검증 (①②는 v2.2.3에 이미 반영 확인) / ③verify-kit·verify-live 실측·이식형 재작성 → code-reviewer 검토 → 보완 → 실행 ALL PASS / git 초기화·2커밋(로컬, push 안 함)
- [ ] Step 3  익명화 흡수
- [ ] Step 4~6 (계획 파일 참조)

## 다음 할 일
Step 3: 익명화 흡수 — PARANSKY97-EZ-INVESTIGATION 등 → reference-case (실명·도메인 제거) + slowagings/template 학습 흡수.
(보류: ① cafe24-agent-workspace는 앱 종료 후 _archive로 이동 ② OneDrive 라이브 mcp는 현재 환경 유지 — 새 키트로의 MCP 연결 전환은 별도 결정 ③ git push는 Step 6에서 승인 후)

## 핵심 자산 위치
- 설계서: api-poc\MCP-DESIGN.md  (로드맵 1~4단계 완료 기록)
- 손발(MCP): mcp\  (server.py, auth\oauth.py, backends\cafe24_api.py·cafe24_sftp.py, kit_tools.py)
- 두뇌: agent-kit\  (CLAUDE.md, docs\, workflows\, traps\, getting-started\)

## 전체 계획서
C:\Users\gdgdg.한비\.claude\plans\mossy-jumping-newt.md