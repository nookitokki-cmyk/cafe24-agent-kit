---
name: API발급
description: 카페24 개발자센터 앱·OAuth·MCP 토큰 발급 핑퐁 (read_design)
---

사용자가 `/API발급` 을 요청했습니다. `connect/MCP-OAUTH-GUIDE.md` 순서를 **질문 하나씩** 진행.

## 규칙

- Scope 기본: **`mall.read_design` 만** (쓰기는 SFTP)
- `client_secret`·비밀번호 **채팅 입력 금지** → 로컬 config 파일만
- Redirect URI **HTTPS 필수** ✅ — http localhost는 ❌ 공식 등록값

## 질문 대본

0. 「**partners.cafe24.com** 로그인 → **Apps** → **App product** 들어갈 수 있나요? (화면: `connect/MCP-OAUTH-GUIDE.md`)」
1. 「**App URL** = `https://{몰ID}.cafe24.com` 넣었나요?」
2. 「**Redirect URI** = `https://{몰ID}.cafe24.com/oauth-callback` 넣었나요?」
3. 「**권한**은 **디자인(Design) 읽기**만 남겼나요? (나머지 삭제 권장)」
4. 「**API 버전** `2026-03-01` — config `API_VERSION` 과 같나요?」
5. 「**Client ID / Secret** 을 `mcp/config/cafe24_config_{몰ID}.py` 에만 저장했나요? (채팅 X)」
6. 「작업 **몰 ID**는? (`ecudemo400786` 등)」
7. 「**저장** 눌렀나요? → 이제 PC로 넘어갑니다. **브라우저 3단계:**」
8. 「터미널 `python cli.py auth-url --mall {몰ID}` → **출력 URL을 브라우저 주소창**에 붙여넣고 허용」
9. 「허용 후 주소창 `oauth-callback?code=...` URL → 터미널 `python cli.py code "URL" --mall {몰ID}` (채팅 X)」
10. 「`python cli.py status --mall {몰ID}` — `access_token_valid: true` 확인」

## PoC 우회 안내 (사용자가 로컬만 쓸 때)

「공식은 HTTPS 서버입니다. 지금은 학습용으로 주소창에서 code를 복사하는 **비공식 우회**입니다. ⚠️」

## 완료

- smoke_test 5/5 (가능 시)
- 다음: `/접속세팅`
