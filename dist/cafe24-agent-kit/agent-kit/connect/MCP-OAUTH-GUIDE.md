# 카페24 MCP — OAuth 발급 튜토리얼 (초보자용)

> **핑퐁 규칙:** 에이전트는 **한 번에 질문 하나**. 답 없으면 다음 단계 금지.  
> **Scope 기본값:** `mall.read_design` 만 (최소 권한).  
> **공식 대조:** [`OFFICIAL-AUDIT.md`](../brain/docs/OFFICIAL-AUDIT.md) §B

---

## 시작 전

- 카페24 **파트너센터** 또는 **개발자센터** 계정
- 작업할 쇼핑몰 **관리자**로 앱 허용할 수 있어야 함 ✅ [oauth/process](https://developers.cafe24.com/app/front/app/develop/oauth/process)

---

## ★ 들어가는 길 (파트너센터 — 샘플몰·파트너 작업 기본)

파트너·샘플몰 작업자는 보통 **여기**로 들어갑니다. (developers.cafe24.com 직접 접속과 **같은 App 설정 화면**으로 연결되는 경우가 많습니다.)

```text
① https://partners.cafe24.com/  로그인
        ↓
② Apps (앱)
        ↓
③ App product (앱 상품) — 만든 앱 선택 또는 신규 등록
        ↓
④ 화면 항목별 입력 (아래 「개발자센터 화면」 표)
        ↓
⑤ 저장
        ↓
⑥ PC 터미널 「브라우저 3단계」(OAuth 토큰)  ← ★ 여기를 빼먹으면 MCP 안 됨
```

> **한 줄:** 파트너센터에서 **항목 넣고 저장** = ①~⑤. **그다음 PC에서 auth-url → 허용 → code** = ⑥.

---

## 단계표 (공식 순서)

| # | 사용자가 할 일 | 공식/실무 |
|---|----------------|-----------|
| 1 | [partners.cafe24.com](https://partners.cafe24.com/) 로그인 → **Apps** → **App product** | ⚠️ 파트너 실무 경로 |
| 2 | (일반 몰) [developers.cafe24.com](https://developers.cafe24.com) → Apps > App 관리 | ✅ 공식 문서 경로 |
| 3 | **기본정보** · **Redirect URI** · **권한(Design 읽기)** 입력 후 저장 | 아래 화면 표 |
| 4 | `mcp/config/cafe24_config_{몰ID}.py` 작성 | 로컬 |
| 5 | **브라우저 3단계** — 허용 + code 교환 | oauth/process |
| 6 | `python cli.py status` / `themes` | 로컬 |

---

## ★ 브라우저 3단계 (Redirect URI 등록 **다음**에 꼭 할 일)

개발자센터에서 Redirect URI만 넣고 끝이 **아닙니다.** 토큰 파일은 **이 3단계** 후에 생깁니다.

### A. 터미널 — 인증 URL 만들기

`mcp/` 폴더에서:

```bash
cd mcp
python cli.py auth-url --mall ecudemo400786
```

(본인 몰 ID로 `--mall` 값을 바꿉니다.)

### B. 브라우저 — 주소창에 URL 붙여넣기

1. 터미널에 출력된 **`https://....cafe24api.com/api/v2/oauth/authorize?...` 전체**를 복사
2. **Chrome 등 주소창**에 붙여넣고 Enter
3. **해당 몰 관리자**로 로그인 → 앱 **「허용」**

> ❌ Cursor 채팅에 URL을 치는 게 아닙니다. **브라우저 주소창**입니다.

### C. 터미널 — `code` 를 토큰으로 교환 (1분 안)

허용 후 주소창이 대략 이렇게 바뀝니다 (404여도 URL만 있으면 OK):

```text
https://{몰ID}.cafe24.com/oauth-callback?code=XXXX&state=...
```

1. **주소창 URL 전체** 복사 (채팅·노션에 붙이지 말 것)
2. 터미널:

```bash
python cli.py code "복사한_URL_전체" --mall ecudemo400786
```

3. `토큰 발급 완료` 가 나오면 → `mcp/config/{몰ID}.token.json` 생성됨

### D. 확인

```bash
python cli.py status --mall ecudemo400786
python cli.py themes --mall ecudemo400786
```

| `status` 결과 | 의미 |
|---------------|------|
| `"token": "없음"` | B~C 단계 미완료 |
| `access_token_valid: true` | **연결 완료** |

---

## 흐름 한 장 (요약)

```text
개발자센터 Redirect URI 등록
        ↓
터미널: python cli.py auth-url --mall {몰ID}
        ↓
브라우저 주소창: 출력된 authorize URL 열기 → 허용
        ↓
터미널: python cli.py code "oauth-callback?code=..." --mall {몰ID}
        ↓
터미널: python cli.py status / themes
```

채팅 명령: **`/API발급`** — 에이전트가 위 순서를 질문 하나씩 안내합니다.

---

## ★ 개발자센터 화면 — 항목별로 뭘 넣나 (MCP·디자인 읽기용)

> **두 세계를 구분하세요.**  
> **① 개발자센터(앱 등록)** = 카페24에 “이 앱 쓸게요” 등록  
> **② 터미널+브라우저(OAuth)** = 내 PC에 **토큰 파일** 만들기  
> ①만 하고 ②를 안 하면 MCP는 **절대** 동작하지 않습니다.

### 1) 기본정보

| 화면 항목 | MCP용 입력값 | 필수? | 비고 |
|-----------|--------------|-------|------|
| **App URL** | `https://{몰ID}.cafe24.com` | ✅ | 예: `https://ecudemo400786.cafe24.com` |
| 새 창 / 팝업 | 아무거나 | △ | MCP CLI 흐름과 **무관** |
| **Redirect URI(s)** | `https://{몰ID}.cafe24.com/oauth-callback` | ✅ **가장 중요** | `mcp/config`의 `REDIRECT_URI`와 **한 글자도 같아야** 함. Enter로 여러 개 가능 |

### 2) API 정보 — 권한 (쇼핑몰 운영자)

**이 키트 기본:** 디자인 **읽기만** → Scope **`mall.read_design`**

| 화면 | MCP용 권장 | 지금 화면처럼 전부 켜면? |
|------|------------|-------------------------|
| **디자인(Design)** | ✅ **읽기** (쓰기는 SFTP/FTP로) | 읽기+쓰기도 동작은 함. 키트는 **읽기만** 권장 |
| 상품·주문·회원·게시판 등 | ❌ **삭제** | 불필요. 심사·보안 리스크 ↑ |
| 앱(Application) | △ 보통 그대로 둠 | 앱 설치 메타용 |

> 파일 수정은 API 쓰기가 아니라 **FTP/SFTP** 로 합니다. API에 쓰기 권한까지 줄 필요 **없음**.

**쇼핑몰 고객 권한:** MCP 디자인 작업만이면 **고객 식별자 등 추가 불필요**.

### 3) API 정보 — 나머지

| 화면 항목 | MCP용 | 비고 |
|-----------|-------|------|
| **타임존** | `Asia/Seoul` | ✅ 그대로 |
| **운영자 권한확인 URI** | 비워도 됨 | 판매용 앱 아니면 생략 |
| **유형** | Web application (Authorization Code) | ✅ 기본값 |
| **버전관리** | `2026-03-01` (Current) | `cafe24_config_*.py`의 `API_VERSION`과 **동일** |
| **Client ID / Secret** | 복사 → **로컬 파일만** | 채팅·Git·공유 채널 **금지** |
| **Front API** | **사용안함** | Admin API(MCP)만 쓰면 됨 |
| **WebHook** | **등록 안 함** | MCP 로컬 작업에 불필요 |

### 4) 개발자센터 저장 후 → PC에서 할 일 (체크리스트)

```text
[개발자센터] Redirect URI + Design 읽기 권한 + 저장
      ↓
[PC] mcp/config/cafe24_config_{몰ID}.py  ← Client ID/Secret/Redirect/Scope
      ↓
[터미널] python cli.py auth-url --mall {몰ID}
      ↓
[브라우저 주소창] 출력 URL → 허용
      ↓
[터미널] python cli.py code "oauth-callback?code=..." --mall {몰ID}
      ↓
[터미널] python cli.py status / themes  → access_token_valid: true
```

### 5) ecudemo400786 기준 — 지금 화면 판정

| 항목 | 상태 |
|------|------|
| App URL | ✅ 맞음 |
| Redirect URI | ✅ 맞음 (`oauth-callback`) |
| Client ID | ✅ config와 일치 |
| API 버전 | ✅ 2026-03-01 |
| 권한 | ⚠️ **Design 읽기만 남기고 나머지 삭제 권장** (지금은 과다) |
| OAuth 토큰 | ✅ 이미 발급됨 (`ecudemo400786.token.json`) |

---

로컬 개발용 `http://localhost:8888/callback` 예제는 **공식 Redirect 규칙과 충돌**합니다. ❌ AUDIT §B-5a

학습용으로 브라우저 주소창에서 `code`를 **수동 복사**하는 방법은 실무에서 쓰이지만, **공식 흐름은 HTTPS 서버가 code를 받는 것**입니다. ⚠️

---

## 설정 파일 예시 (비밀 제외)

`mcp/config/cafe24_config.example.py` 를 복사해 `cafe24_config_{몰ID}.py` 로 저장.

필수:
- `MALL_ID`
- `CLIENT_ID`, `CLIENT_SECRET` (파일에만)
- `REDIRECT_URI` — **HTTPS**
- `SCOPE = "mall.read_design"`
- `API_VERSION`

---

## 에이전트 명령

채팅: **`/API발급`** — 위 표를 질문 형태로 진행합니다.

---

## 토큰 수명 (✅ 공식)

| 토큰 | 시간 |
|------|------|
| 인증 code | 1분 |
| access_token | 2시간 |
| refresh_token | 발급 후 14일 |

[retoken](https://developers.cafe24.com/app/front/app/develop/oauth/retoken)
