# OMC 스타일 명령어 레지스트리

> 에이전트는 사용자가 슬래시 명령을 치면 **해당 파일의 대본**을 따릅니다.  
> **한 번에 질문 하나.** 답 없으면 다음 단계 금지.

---

## 주 명령 — 온보딩 (v2.2+)

| 명령 | 파일 | 역할 |
|------|------|------|
| `/키트시작` | `.claude/commands/키트시작.md` | zip 풀고 pip·import·smoke (5/9 정상) |
| `/새클라이언트` | `.claude/commands/새클라이언트.md` | `clients/_template` scaffold |
| `/MCP연결` | `.claude/commands/MCP연결.md` | Cursor·Claude Code MCP 등록 |

---

## 주 명령 — 작업 (기존)

| 명령 | 파일 | 역할 |
|------|------|------|
| `/도움말` | `.claude/commands/도움말.md` | 전체 지도·문서 링크 |
| `/레퍼런스인입` | `.claude/commands/레퍼런스인입.md` | URL **또는** 시안 → 인벤토리·실측 |
| `/접속세팅` | `.claude/commands/접속세팅.md` | 파트너 vs 일반, 몰 ID, SFTP, skin |
| `/API발급` | `.claude/commands/API발급.md` | OAuth·MCP 토큰 핑퐁 |
| `/요소측정` | `.claude/commands/요소측정.md` | 수정 전 숫자 수집 |
| `/디자인수정` | `.claude/commands/디자인수정.md` | 실측 후 코드 작업 게이트 |

---

## 주 명령 — 검증·운영 (v2.2+)

| 명령 | 파일 | 역할 |
|------|------|------|
| `/검증` | `.claude/commands/검증.md` | `run_preflight` · score 해석 |
| `/캐시확인` | `.claude/commands/캐시확인.md` | `?v=N` · 캐시 대기 · 스킨 경로 |
| `/EZ제거` | `.claude/commands/EZ제거.md` | Phase C strip 게이트 |
| `/버전확인` | `.claude/commands/버전확인.md` | VERSION · kit-update |

상황별: [`getting-started/OMC-명령어-매칭가이드.md`](../getting-started/OMC-명령어-매칭가이드.md)

---

## 별칭 (구 명령 → 신 명령)

| 구 명령 | 신 명령 |
|---------|---------|
| `/카페24-시작` | `/도움말` |
| `/카페24-도와줘` | `/도움말` + [04-함정](../getting-started/04-자주-막히는-5가지.md) |
| `/카페24-새작업` | `/디자인수정` — **신규 몰은 `/새클라이언트`** |
| `/카페24-워크플로우` | `workflows/` + 전용 에이전트 |

---

## traps 인덱스

문제 생기면 [`traps/INDEX.md`](../traps/INDEX.md)

---

## 공식 대조

[`docs/OFFICIAL-AUDIT.md`](../docs/OFFICIAL-AUDIT.md)
