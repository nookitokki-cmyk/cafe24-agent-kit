카페24 MCP 설정 (배포본 — 비밀 파일은 직접 추가)

1. pip install
   cd mcp && pip install -r requirements.txt

2. OAuth 앱 설정
   cafe24_config.example.py → cafe24_config_{몰ID}.py 복사 후 CLIENT_ID/SECRET/REDIRECT_URI 입력

3. (선택) SFTP
   sftp_{몰ID}.json 을 이 폴더에 추가 (비밀 — git/배포에 넣지 마세요)

4. Cursor MCP
   ../.cursor/mcp.json.example → ../.cursor/mcp.json 복사 후 Cursor 재시작
   상세: agent-kit/00_시작하기/05b-MCP-등록.md

5. OAuth 토큰
   python cli.py auth-url --mall {몰ID}
   python cli.py code "oauth-callback?code=..." --mall {몰ID}
