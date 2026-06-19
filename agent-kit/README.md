# 카페24 스킨 빌더 에이전트 키트

**카페24 + AI 작업자용 작업 키트** — 쇼핑몰·스킨을 에이전트와 함께 만들고, 레퍼런스·시안을 실제 몰에 옮깁니다. 강사·클라이언트·에이전트가 같은 문서·명령·게이트를 공유합니다.

→ **누구를 위한 키트인지:** [**이-키트는-누구-용인가.md**](이-키트는-누구-용인가.md)

**두뇌(규칙·함정·문법) + 접속 가이드 + OMC 명령** 이 한 폴더에 있습니다.  
모노레포 손발(MCP): [`../mcp/`](../mcp/)

---

## ⚠️ 동기화 (canonical path)

**정본(canonical) 작업 경로:** 배포 키트 루트 (`cafe24-agent-kit/` 또는 monorepo `cafe24-agent-workspace/`)  
OneDrive 등에 있는 복사본은 오래될 수 있습니다. 문서·워크플로·MCP 변경은 정본에서만 반영하세요.

---

## 3분 시작

1. Cursor 또는 Claude Code에서 배포 키트 루트 열기  
2. 첫 설치 → 채팅 **`/키트시작`** (또는 [`getting-started/키트-시작-가이드.md`](getting-started/키트-시작-가이드.md))  
3. 채팅: **`/도움말`** 또는 **`/접속세팅`**  
4. 처음이면 [`getting-started/00-아무것도-모를-때.md`](getting-started/00-아무것도-모를-때.md)  
5. **막히면** → [`docs/F-상황-인덱스.md`](docs/F-상황-인덱스.md) (**F1~F34** 증상·Q&A·프롬프트 한곳)  
6. 복붙 프롬프트: [`getting-started/프롬프트-템플릿.md`](getting-started/프롬프트-템플릿.md) · 명령 매칭: [`getting-started/OMC-명령어-매칭가이드.md`](getting-started/OMC-명령어-매칭가이드.md)  
7. **Q&A (쉬운 말):** [`getting-started/QnA-쉬운말로.md`](getting-started/QnA-쉬운말로.md) (용어 없이 18문답)

---

## 명령어 (OMC 스타일)

| 명령 | 용도 |
|------|------|
| `/키트시작` | zip 풀고 pip·import·smoke (5/9 정상) |
| `/새클라이언트` | `clients/_template` scaffold |
| `/MCP연결` | Cursor·Claude Code MCP 등록 |
| `/도움말` | 지도·문서 (구 `/카페24-시작`) |
| `/레퍼런스인입` | URL **또는** 시안 → 페이지표·실측 (코드 전) |
| `/접속세팅` | 파트너 vs 일반, 몰 ID, SFTP, skin 표 |
| `/API발급` | 개발자센터 OAuth · `mall.read_design` |
| `/요소측정` | 수정 전 폰트·여백 px |
| `/디자인수정` | 실측 후 코드 (구 `/카페24-새작업`) |
| `/프롬프트참고` | 상황별 복붙 프롬프트 문서 링크 |

전체: [`commands/COMMANDS.md`](commands/COMMANDS.md) · 매칭 가이드: [`getting-started/OMC-명령어-매칭가이드.md`](getting-started/OMC-명령어-매칭가이드.md)

---

## 폴더 맵

| 경로 | 내용 |
|------|------|
| `CLAUDE.md` | 에이전트 헌법·게이트 |
| `getting-started/` | **키트-시작-가이드** · **이-키트는-누구-용인가** · 접속·MCP 온보딩 00~05 · **프롬프트 템플릿** · **OMC 명령 매칭** |
| `docs/OFFICIAL-AUDIT.md` | 공식 대조 (✅/⚠️/❌) |
| `docs/MCP-OAUTH-GUIDE.md` | API 발급 튜토리얼 |
| **`docs/F-상황-인덱스.md`** | **F1~F34 허브** (증상·Q&A·프롬프트·postmortem) |
| `getting-started/QnA-쉬운말로.md` | **[F?]** 태그 Q&A 18개 |
| `getting-started/실측-격차-설명가이드.md` | 실측 격차 이유·대응 |
| `getting-started/프롬프트-템플릿.md` | F코드 붙은 복붙 프롬프트 12종 |
| `traps/INDEX.md` | F1~F34 한 줄 인덱스 |
| `workflows/` | 01~06 (인입·실측·verify-loop 포함) |
| `docs/common-pitfalls.md` | narrow·**EZ #contents 92%** postmortem |
| `docs/snippets/ez-contents-override.css` | `#container #contents` paste-ready |
| `docs/kit-roadmap.md` | score 스크립트·로드맵 |
| `docs/KIT-CHANGELOG-20260619.md` | ecudemo393674→400786 키트 변경 이력 |
| `rules/cafe24-admin-verify.md` | 관리자 안내 전 웹 검증 |
| `rules/responsive-mobile.md` | MO 단일 base 스킨 — **관리자 mobile OFF 필수** |
| `rules/ez-contents-width.md` | **필수** EZ MO 92% width override (`#container #contents`) |
| `.claude/commands/` | 슬래시 대본 |

---

## 검증

```bash
bash scripts/verify-kit.sh
```

---

_배포본: 키트 루트에서 `/키트시작` · `CHANGELOG.md` 참고_
