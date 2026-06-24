# OMC 스타일 명령어 레지스트리

> 에이전트는 사용자가 슬래시 명령을 치면 **해당 파일의 대본**을 따릅니다.  
> **한 번에 질문 하나.** 답 없으면 다음 단계 금지.

---

## 주 명령 — 온보딩 (v2.2+)

| 명령 | 파일 | 역할 |
|------|------|------|
| `/키트시작` | `.claude/skills/키트시작/SKILL.md` | zip 풀고 pip·import·smoke (5/9 정상) |
| `/새클라이언트` | `.claude/skills/새클라이언트/SKILL.md` | `clients/_template` scaffold |
| `/MCP연결` | `.claude/skills/MCP연결/SKILL.md` | Cursor·Claude Code MCP 등록 |

---

## 주 명령 — 작업 (기존)

| 명령 | 파일 | 역할 |
|------|------|------|
| `/도움말` | `.claude/skills/도움말/SKILL.md` | 전체 지도·문서 링크 |
| `/레퍼런스인입` | `.claude/skills/레퍼런스인입/SKILL.md` | URL **또는** 시안 → 인벤토리·실측 |
| `/접속세팅` | `.claude/skills/접속세팅/SKILL.md` | 파트너 vs 일반, 몰 ID, SFTP, skin |
| `/API발급` | `.claude/skills/API발급/SKILL.md` | OAuth·MCP 토큰 핑퐁 |
| `/요소측정` | `.claude/skills/요소측정/SKILL.md` | 수정 전 숫자 수집 |
| `/디자인수정` | `.claude/skills/디자인수정/SKILL.md` | 실측 후 코드 작업 게이트 |

---

## 주 명령 — 검증·운영 (v2.2+)

| 명령 | 파일 | 역할 |
|------|------|------|
| `/검증` | `.claude/skills/검증/SKILL.md` | `run_preflight` · score 해석 |
| `/캐시확인` | `.claude/skills/캐시확인/SKILL.md` | `?v=N` · 캐시 대기 · 스킨 경로 |
| `/EZ제거` | `.claude/skills/EZ제거/SKILL.md` | Phase C strip 게이트 |
| `/버전확인` | `.claude/skills/버전확인/SKILL.md` | VERSION · kit-update |

상황별: [`00_시작하기/OMC-명령어-매칭가이드.md`](../00_시작하기/OMC-명령어-매칭가이드.md)

---

## (참고) 폐기된 구 별칭

구 별칭 `/카페24-시작`·`/카페24-도와줘`·`/카페24-새작업` 은 **v2.6.0에서 폐기**되었습니다. 각각 `/도움말` · `/도움말`+[04-함정](../00_시작하기/04-자주-막히는-5가지.md) · `/디자인수정`(신규 몰은 `/새클라이언트`) 를 직접 사용하세요. `/카페24-워크플로우` 는 정규 명령으로 유지됩니다.

---

## traps 인덱스

문제 생기면 [`02_막혔을때/함정-INDEX.md`](../02_막혔을때/함정-INDEX.md)

---

## 공식 대조

[`brain/docs/OFFICIAL-AUDIT.md`](../brain/docs/OFFICIAL-AUDIT.md)
