# ✅ 카페24 에이전트 키트 — 단일 기준 (THE ONE)

- 위치: C:\dev\cafe24-agent-kit  (← 작업은 여기서만)
- 버전: **v2.4.0** / 2026-06-21
- 다른 곳의 사본은 전부 구버전·보관용. 헷갈리면 이 파일을 보세요.

## 어디까지 했나 (재발 방지 현재상태)
- [x] Step 0  불변 백업 zip 8개 (OneDrive\문서\개발\_archive\cafe24-kit-원본스냅샷_2026-06-20\, 무결성 검증완료)
- [x] Step 1-1 새 폴더 생성 (OneDrive/git 밖 = 시크릿·충돌 위험 차단)
- [x] Step 1-3 깨끗한 부분만 복사 (비밀파일·임시물 제외)
- [x] Step 1-4 핵심자산 12종 전부 포함 (설계서 MCP-DESIGN.md · 손발 mcp · 두뇌 agent-kit)
- [x] Step 1-5 시크릿 0개 (verify-kit.sh 비번 스크럽 완료)
- [x] Step 1-7 사본 정리: 안전한 4곳 보관소 이동 완료 (agent-kit · agent-kit-cafe24-agent-final · 키트-배포판 · 키트-백업) / cafe24-agent-workspace 1곳은 실행중 앱이 사용중이라 **보류** / OneDrive 라이브 3곳(mcp·api-poc·web-cafe24/agent-kit)은 Step 2에서 연결 정리
- [x] Step 2  보안 정리 + 기술수정: ①build-dist 클라제외+demo000 ②SFTP 호스트키검증 (①②는 v2.2.3에 이미 반영 확인) / ③verify-kit·verify-live 실측·이식형 재작성 → code-reviewer 검토 → 보완 → 실행 ALL PASS / git 초기화·2커밋(로컬, push 안 함)
- [x] Step 3  익명화: clients 1GB 백업✅ + 비번누출 0✅ + 코드 기본값 (구 클라명)→demo000·(구 클라명)→reference-case 치환(import OK)✅ / 문서 익명화는 Step 4a에서 완료
- [x] Step 4  초보자 친화 재편 ✅: [4a ✅] 문서 익명화 + 내부/증거문서 _archive 격리 → 배포본 클라식별자 0(가드 제외) / [4b ✅] 폴더 재편(사람용 00_시작하기·01_작업하기·02_막혔을때 ↔ 기계용 brain·connect·.claude, git rename 보존) + 깨진 링크 0 + 클라누출 추가제거(SLOWAGINGS·paransky) + MCP코드·셸스크립트 새 구조 + 진입점 6→1 통합 + verify-kit ALL PASS / [4c ✅] 입문자료 4종(0-이키트가뭔가요·용어집·첫수정-1건-성공·실패복구-가이드) + 범용 독자로 범위 정정(강의 맥락 단어 0)
- [x] Step 6  출고 ✅: force-push로 원격 main 교체 + Release 발행. v2.3.0=재편·입문자료 / v2.3.1=설치-안내+범용 온보딩(몰ID만)+.pyc제외 / v2.3.2=설치-안내 핑퐁 / v2.3.3=Mac지원(mcp.json.mac.example) / v2.3.4=수정자 레퍼런스+파트너 웹FTP 설정법+clients gitignore / v2.3.5=파트너센터 웹FTP=자동 업로드 명문화(수동 오안내 차단) / v2.3.6=프롬프트 #13(EZ overlay)+디자인수정 게이트 분기+설치안내 zip이름. 구버전은 `v2.2.0~2.2.3`·`backup/pre-v3-v2.2.3` 태그로 보존.
- [x] **Step 7  v2.4.0 출고 (2026-06-21) ✅**: cafe24 skill 풀스택 확장 — 45개 신규 파일 + 6개 갱신. **안정 자료 ✅**: troubleshooting / variables 마스터 사전(15섹션 250+ 변수) / modifiers 확장 / recipes 7개 / module-browser.html (19개 모듈 시각 카탈로그). **실험적 🧪**: templates 5종 / snippets 20개 (HTML 6+CSS 8+JS 6) / design-tokens 파이프라인 / brand-profile JSON / workflows + `/카페24-자동화` 명령 / qa-checker + qa-loop. **현재 latest = v2.4.0**. 사전 처리 완료: slowagings → demo-brand 가상 클라이언트 치환(0 잔여), 절대 경로 → ~/.claude/ 치환. 검증 안 된 자료에 🧪 표시 — 누끼토끼 실 클라이언트 작업 검증 후 안정화 예정.
- [ ] Step 5 (후순위·선택) · Step 5.5 (후순위·선택)
- [ ] Step 8 (후순위·선택): v2.4.0 실험적 자료(🧪) 실 클라이언트 검증 → v2.4.1 안정화 릴리스

## 다음 할 일
**Step 0~4 + Step 6 + Step 7(v2.4.0 출고) 완료.** 원격 `nookitokki-cmyk/cafe24-agent-kit` main + Release **latest = v2.4.0**. 남은 건 **선택 사항만**: Step 5(자동 함정 발굴·H+EZ 교리·preflight score 스크립트 키트 편입) / Step 5.5(키트로 데모몰 스킨 1개 dogfooding) / **Step 8(v2.4.0 실험적 자료 🧪 실 클라이언트 검증 → v2.4.1 안정화)** / (필요 시) 수동 복사본 보유자에게 폐기통지.
(보류: ① cafe24-agent-workspace는 앱 종료 후 _archive로 이동 ② OneDrive 라이브 mcp는 현재 환경 유지 — 새 키트로의 MCP 연결 전환은 별도 결정 ③ git push는 Step 6에서 승인 후)

## 핵심 자산 위치
- 설계서: api-poc\MCP-DESIGN.md  (로드맵 1~4단계 완료 기록)
- 손발(MCP): mcp\  (server.py, auth\oauth.py, backends\cafe24_api.py·cafe24_sftp.py, kit_tools.py)
- 두뇌: agent-kit\  (사람용 00_시작하기\·01_작업하기\·02_막혔을때\ / 기계용 brain\·connect\·.claude\ / CLAUDE.md·README.md)

## 전체 계획서
C:\Users\gdgdg.한비\.claude\plans\mossy-jumping-newt.md