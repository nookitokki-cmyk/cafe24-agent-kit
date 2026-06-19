> ✅ **단일 기준(THE ONE) · v3 · 2026-06-20** — 이 폴더(`C:\dev\cafe24-agent-kit`)가 유일한 진짜 키트입니다. 다른 사본은 `_archive` 보관소(사용 금지). 현재 상태는 [`__지금상태_STATUS.md`](__지금상태_STATUS.md) 참고.

# cafe24-agent-kit

카페24 **두뇌(agent-kit)** + **손발(mcp)** 단일 기준 저장소.

## 빠른 시작

1. 이 폴더를 Cursor에서 연다  
2. 채팅: **`/도움말`** 또는 **`/접속세팅`**  
3. [`agent-kit/getting-started/00-아무것도-모를-때.md`](agent-kit/getting-started/00-아무것도-모를-때.md)

## 명령어 (OMC)

| 명령 | 설명 |
|------|------|
| `/도움말` | 지도 (구 `/카페24-시작`) |
| `/접속세팅` | FTP/SFTP·몰 ID·skin |
| `/API발급` | OAuth · `mall.read_design` |
| `/요소측정` | 수정 전 실측 |
| `/디자인수정` | 실측 후 코드 |

## 검증

```bash
bash agent-kit/scripts/verify-kit.sh    # 구조·문서 29항목
bash agent-kit/scripts/verify-live.sh   # 운영 MCP smoke 5/5 (토큰 필요)
```

실측 기록: [`agent-kit/docs/VERIFICATION-EVIDENCE.md`](agent-kit/docs/VERIFICATION-EVIDENCE.md)

## 문서

- 공식 대조: `agent-kit/docs/OFFICIAL-AUDIT.md`
- API 튜토리얼: `agent-kit/docs/MCP-OAUTH-GUIDE.md`
- 복제 기록: `MANIFEST.txt`
