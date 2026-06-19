# OAuth 5분 — 브라우저 3단계만

> 전체 튜토리얼: [`MCP-OAUTH-GUIDE.md`](./MCP-OAUTH-GUIDE.md) · 파트너센터 앱 등록은 그 문서 ①~⑤

Redirect URI를 개발자센터에 넣었다면, **PC에서 아래 3단계**만 하면 토큰 파일이 생깁니다.

---

## 1. 터미널 — 인증 URL

```bash
cd mcp
python cli.py auth-url --mall {몰ID}
```

`{몰ID}`를 본인 쇼핑몰 ID로 바꿉니다.

---

## 2. 브라우저 — **주소창**에 붙여넣기

| ✅ 맞음 | ❌ 틀림 |
|--------|--------|
| Chrome **맨 위 주소창** (URL 입력하는 곳) | Cursor·채팅 입력창 |
| | Google **검색창** (검색어로 취급됨) |

1. 터미널에 출력된 `https://....cafe24api.com/api/v2/oauth/authorize?...` **전체** 복사
2. 브라우저 **주소창**에 붙여넣고 Enter
3. 해당 몰 **관리자**로 로그인 → 앱 **「허용」**

---

## 3. 터미널 — `code` 교환 (1분 안)

허용 후 주소창이 대략 이렇게 바뀝니다:

```text
https://{몰ID}.cafe24.com/oauth-callback?code=XXXX&state=...
```

- **404 페이지가 떠도 괜찮습니다.** 주소창 URL에 `code=`만 있으면 됩니다.
- URL **전체**를 복사 (채팅·노션에 붙이지 말 것)

```bash
python cli.py code "복사한_URL_전체" --mall {몰ID}
```

`토큰 발급 완료` → `mcp/config/{몰ID}.token.json` 생성됨.

---

## 확인

```bash
python cli.py status --mall {몰ID}
```

`"token": "없음"`이 아니면 성공.
