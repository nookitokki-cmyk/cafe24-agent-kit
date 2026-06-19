# 에이전트 가이드

- 카페24 스킨·스마트디자인 작업 시 **`cafe24-mcp`** (`mcp/server.py`)를 사용합니다.
- 기본 워크플로·F-index·다음 Read 경로는 MCP **`get_kit_guides`** 를 먼저 호출하세요 (Sixshop `get_mcp_guides`와 동일 패턴).
- 깊은 규칙·함정은 `get_kit_guides`가 가리키는 `agent-kit/CLAUDE.md` 및 `agent-kit/workflows/`를 Read 하세요.
- MCP·OAuth 미설정이면 `agent-kit/docs/MCP-OAUTH-GUIDE.md`와 `/접속세팅`부터 도와주세요.
