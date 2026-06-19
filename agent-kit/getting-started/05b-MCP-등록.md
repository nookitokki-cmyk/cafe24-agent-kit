# 05b. MCP 등록하기 (Cursor · Claude Code)

> **대상:** `cafe24-agent-kit` 배포본을 처음 연 사람  
> **목표:** 채팅에서 `get_kit_guides` · `cafe24_list_themes` 등 MCP 도구 사용  
> **슬래시 명령:** **`/MCP연결`** · **`/키트시작`**

배포본에는 **`.cursor/mcp.json`이 들어 있지 않습니다.** (비밀·경로가 PC마다 다름)  
대신 **`.cursor/mcp.json.example`** 템플릿을 복사해 등록합니다.

---

## 사전 준비

| 항목 | 설명 |
|------|------|
| Python 3.10+ | `python --version` |
| IDE | **Cursor** 또는 **Claude Code** |
| 워크스페이스 | 배포 키트 **루트** (`cafe24-agent-kit/`) |
| Playwright (선택) | `run_preflight` 사용 시: `playwright install chromium` |
| 몰 ID | [02-몰ID-찾기.md](./02-몰ID-찾기.md) |

---

## 4단계 — 처음 한 번만

### 1단계 — Python 패키지

```bash
cd mcp
pip install -r requirements.txt
python -c "import server"
```

> Windows: `python` 대신 `py -3` — MCP JSON `command`도 동일하게.

---

### 2단계 — 몰 설정

```bash
cp cafe24_config.example.py cafe24_config_{몰ID}.py
```

`CLIENT_ID` / `CLIENT_SECRET` / `REDIRECT_URI` 를 **로컬 파일에만** 입력.  
신규 몰: **`/새클라이언트`** 또는 `python cli.py scaffold --mall {몰ID}`

---

### 3단계 — MCP 등록

#### Cursor

1. `.cursor/mcp.json.example` → `.cursor/mcp.json`
2. Cursor 재시작
3. MCP 목록 `cafe24-mcp` 초록색 확인

Settings → MCP → Edit Config 도 가능.

#### Claude Code

프로젝트 MCP 설정에 example 과 동일한 stdio 블록 추가:

```json
{
  "mcpServers": {
    "cafe24-mcp": {
      "type": "stdio",
      "command": "python",
      "args": ["${workspaceFolder}/mcp/server.py"],
      "cwd": "${workspaceFolder}/mcp",
      "env": {
        "CAFE24_KIT_ROOT": "${workspaceFolder}/agent-kit"
      }
    }
  }
}
```

---

### 4단계 — OAuth

[`MCP-OAUTH-GUIDE.md`](../docs/MCP-OAUTH-GUIDE.md) · **`/API발급`**

```bash
python cli.py auth-url --mall {몰ID}
python cli.py code "oauth-callback?code=..." --mall {몰ID}
python cli.py status --mall {몰ID}
```

---

## smoke_test 기대치

```bash
SMOKE_PREFLIGHT_ALL=0 python smoke_test.py
```

| 상태 | 결과 |
|------|------|
| config·토큰 **없음** | **5/9 정상** (exit 0, v2.2+) |
| 토큰·SFTP 있음 | 9/9+ 가능 |

진단: `python cli.py diagnose` 또는 MCP `diagnose_kit_setup`

---

## 자주 막히는 곳

| 증상 | 확인 |
|------|------|
| `No module named auth` | v2.0.1+ · `mcp/auth/`, `mcp/backends/` |
| MCP 빨간색 | pip · import server · JSON 경로 |
| smoke exit 1 (구버전) | v2.2+ 로 업데이트 |

---

## 다음

- [05-MCP-연결-개요.md](./05-MCP-연결-개요.md)
- [`DISTRIBUTION-KIT.md`](../docs/DISTRIBUTION-KIT.md) §4
- **`/접속세팅`** · **`/검증`**
