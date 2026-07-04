---
name: MCP연결
description: Cursor·Claude Code 공통 MCP stdio 등록 (mcp.json)
---

사용자가 `/MCP연결` 을 요청했습니다. **한 번에 질문 하나.**

상세 문서: `00_시작하기/05b-MCP-등록.md`

## Q1. IDE

「**Cursor** 를 쓰나요, **Claude Code** 를 쓰나요?」

### Cursor

1. `.cursor/mcp.json.example` → `.cursor/mcp.json` 복사
2. Cursor **완전 종료** 후 재시작
3. MCP 목록에서 `cafe24-mcp` **초록색** 확인

또는 Settings → MCP → Edit Config → example 내용 붙여넣기

### Claude Code

1. **`.mcp.json.example`**(Windows) / **`.mcp.json.mac.example`**(Mac) → 프로젝트 루트에 **`.mcp.json`** 으로 복사
   - ⚠️ Cursor용 `.cursor/mcp.json` 과 **다른 파일**. Claude Code는 **루트 `.mcp.json`** 을 봄
2. Claude Code 재시작 → 처음 뜨는 **"이 프로젝트의 MCP 서버를 신뢰하시겠습니까?" → Yes**
   - 놓쳤으면 터미널에서 `claude mcp reset-project-choices` 후 다시 열기
3. `command` 가 본인 PC의 `python` / `python3` / `py -3` 와 맞는지 확인

> 직접 편집 시 구조 (Claude Code는 `${workspaceFolder}` 미지원 → `${CLAUDE_PROJECT_DIR:-.}` 사용):
> ```json
> {
>   "mcpServers": {
>     "cafe24-mcp": {
>       "type": "stdio",
>       "command": "python",
>       "args": ["${CLAUDE_PROJECT_DIR:-.}/mcp/server.py"],
>       "env": {
>         "CAFE24_KIT_ROOT": "${CLAUDE_PROJECT_DIR:-.}/agent-kit",
>         "PYTHONUNBUFFERED": "1"
>       }
>     }
>   }
> }
> ```

## Q2. import 선행

「`cd mcp && pip install -r requirements.txt` 와 `python -c "import server"` 를 통과했나요?」

- 실패 → **`/키트시작`** Q2~Q3

## Q3. 연결 확인 (도구 이름은 몰라도 됩니다 — 내가 확인)

사용자에게 도구 이름을 시키지 말 것. **새 창(새 세션)** 을 연 뒤 사용자는 자연어 한마디면 된다:

> **"카페24 연결됐는지 확인해줘"**

이 말이 들어오면 내가 `get_kit_guides` 를 호출해 `kit_version` 을 확인한다.
- `kit_version` 이 나오면 → 성공 → **`/API발급`** (토큰 없을 때)
- 도구가 안 보이면(아직 로드 전) → 「**새 창을 열고 다시 `/MCP연결`**」 안내
- 그래도 실패 → `.mcp.json` 경로 · Python 경로 재확인

> 왜 새 창이 필요한가: MCP는 **세션이 시작될 때 한 번** 로드됩니다. 방금 `.mcp.json`을 만든 이 세션엔 아직 없으니, 새 세션에서 확인합니다.

## 완료

```
[MCP연결 완료]
- IDE: Cursor | Claude Code
- 다음: /API발급 또는 diagnose_kit_setup (MCP)
```
