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

> **Windows:** `python` / `py -3`. **Mac/Linux:** `python` 대신 **`python3`** (아래 명령·MCP JSON `command` 모두 OS에 맞게).

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

1. **Windows** `.cursor/mcp.json.example` · **Mac** `.cursor/mcp.json.mac.example` → `.cursor/mcp.json` 로 복사 (Mac판은 `command`이 `python3`)
2. Cursor 재시작
3. MCP 목록 `cafe24-mcp` 초록색 확인

Settings → MCP → Edit Config 도 가능.

> **⚠️ MCP가 빨간불/안 뜰 때 (Windows):** `command: "python"`이 Microsoft Store 별칭으로 잡히는 PC에서는 서버가 조용히 실패합니다.
> 이때는 `.cursor/mcp.json`(또는 루트 `.mcp.json`)에서 `"command": "py"`, `"args": ["-3", ...기존 args...]` 로 바꾸고 재시작하세요.

#### Claude Code

`.mcp.json.example`(Windows) / `.mcp.json.mac.example`(Mac) → 프로젝트 루트에 **`.mcp.json`** 으로 복사.
(Cursor용 `.cursor/mcp.json` 과 **다른 파일** — Claude Code는 루트 `.mcp.json` 을 봅니다.)

재시작 후 처음 뜨는 **"이 프로젝트의 MCP 서버를 신뢰하시겠습니까?" → Yes**.
놓쳤으면 터미널에서 `claude mcp reset-project-choices` 후 다시 열기.

직접 편집 시 (Claude Code는 `${workspaceFolder}` 미지원 → `${CLAUDE_PROJECT_DIR:-.}`):

```json
{
  "mcpServers": {
    "cafe24-mcp": {
      "type": "stdio",
      "command": "python",
      "args": ["${CLAUDE_PROJECT_DIR:-.}/mcp/server.py"],
      "env": {
        "CAFE24_KIT_ROOT": "${CLAUDE_PROJECT_DIR:-.}/agent-kit",
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

---

### 4단계 — OAuth

[`MCP-OAUTH-GUIDE.md`](../connect/MCP-OAUTH-GUIDE.md) · **`/API발급`**

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
- [`DISTRIBUTION-KIT.md`](../connect/DISTRIBUTION-KIT.md) §4
- **`/접속세팅`** · **`/검증`**
