---
description: Cursor·Claude Code 공통 MCP stdio 등록 (mcp.json)
---

사용자가 `/MCP연결` 을 요청했습니다. **한 번에 질문 하나.**

상세 문서: `getting-started/05b-MCP-등록.md`

## Q1. IDE

「**Cursor** 를 쓰나요, **Claude Code** 를 쓰나요?」

### Cursor

1. `.cursor/mcp.json.example` → `.cursor/mcp.json` 복사
2. Cursor **완전 종료** 후 재시작
3. MCP 목록에서 `cafe24-mcp` **초록색** 확인

또는 Settings → MCP → Edit Config → example 내용 붙여넣기

### Claude Code

1. 프로젝트 루트에 `.mcp.json` 또는 Claude Code MCP 설정 파일 편집
2. example 과 동일 구조:

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

3. `command` 를 본인 PC의 `python` / `py -3` 경로에 맞출 것

## Q2. import 선행

「`cd mcp && pip install -r requirements.txt` 와 `python -c "import server"` 를 통과했나요?」

- 실패 → **`/키트시작`** Q2~Q3

## Q3. 연결 확인

「채팅에서 MCP **`get_kit_guides`** 를 호출해 `kit_version` 이 보이나요?」

- 실패 → JSON 경로 · `cwd` · Python 경로 재확인
- 성공 → **`/API발급`** (토큰 없을 때)

## 완료

```
[MCP연결 완료]
- IDE: Cursor | Claude Code
- 다음: /API발급 또는 diagnose_kit_setup (MCP)
```
