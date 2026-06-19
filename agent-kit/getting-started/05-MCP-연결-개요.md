# 05. MCP 연결 개요 (손발)

> **비유:** MCP는 에이전트에게 **리모컨**을 주는 것이다. 리모컨 없이도 파일관리자로 할 수 있지만, 자동화는 MCP가 편하다.

**배포 키트를 처음 연다면** → MCP 등록·설치 순서는 [**05b-MCP-등록.md**](./05b-MCP-등록.md) (4단계)를 먼저 보세요. 슬래시 **`/MCP연결`** · **`/키트시작`**

---

## 무엇을 하나요?

| 도구 | 하는 일 |
|------|---------|
| `cafe24_list_themes` | 스킨 목록 (skin_no, skin_code) ✅ |
| `cafe24_read_page` | HTML 한 파일 읽기 ✅ |
| `cafe24_sftp_*` | SFTP로 파일 읽기·업로드 ⚠️ 연결은 발급 정보 |

모노레포: `../mcp/README.md`

---

## 최소 권한 (이 키트 기본)

**`mall.read_design` 만** — 디자인 **읽기**. 쓰기는 SFTP로 합니다. ✅ [Scope 문서](https://developers.cafe24.com/app/front/app/develop/api/scope)

---

## 처음 연결 순서

0. **파트너센터:** [partners.cafe24.com](https://partners.cafe24.com/) → **Apps** → **App product** → 항목 입력·저장  
1. [MCP-OAUTH-GUIDE.md](../docs/MCP-OAUTH-GUIDE.md) — 화면별 입력 + **브라우저 3단계**  
2. 채팅 **`/API발급`** — 에이전트 핑퐁  
3. `python cli.py status --mall {몰ID}` — `access_token_valid: true`

### Redirect URI 등록 **다음** (많이 헷갈리는 부분)

| 단계 | 어디서 | 무엇 |
|------|--------|------|
| 1 | **터미널** | `python cli.py auth-url --mall {몰ID}` |
| 2 | **브라우저 주소창** | 출력 URL 붙여넣기 → 관리자 **허용** |
| 3 | **터미널** | `python cli.py code "oauth-callback?code=..." --mall {몰ID}` |

허용만 하고 3단계를 안 하면 `token: "없음"` 으로 남습니다.

---

## 안전

- `client_secret`·비밀번호는 **채팅에 붙이지 마세요**
- 업로드 전 **`cafe24_sftp_backup`** + 사용자 OK
