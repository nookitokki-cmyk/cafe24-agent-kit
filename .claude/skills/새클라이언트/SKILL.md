---
name: 새클라이언트
description: 새 몰 프로젝트 scaffold — clients/_template 복제·config 안내
---

사용자가 `/새클라이언트` 를 요청했습니다. **한 번에 질문 하나.**

> `/카페24-새작업` 은 **디자인 코드 작업** 별칭입니다. 신규 몰은 **이 명령**을 씁니다.

## Q1. 몰 ID

「작업할 **몰 ID**를 알려주세요. (`https://{몰ID}.cafe24.com`)」

- 형식: 영소문자·숫자·`_`·`-` (3~32자)

## Q2. scaffold 실행

터미널 (또는 MCP `scaffold_client`):

```bash
cd mcp
python cli.py scaffold --mall {몰ID}
```

생성되는 것:

| 경로 | 내용 |
|------|------|
| `agent-kit/clients/{몰ID}/` | `_template` 복제 |
| `clients/{몰ID}/.workflow.md` | 워크플로 상태 파일 |
| `mcp/config/cafe24_config_{몰ID}.py` | 없을 때만 example 복사 |

이미 `clients/{몰ID}/` 가 있으면 **덮어쓰지 않음** — 사용자에게 확인.

## Q2-1. scaffold 완료 기준 (v2.12.0)

`clients/_template` 는 **CSS 없는 scaffold** 로 유지한다. `_template` 복제만으로 카페24 토대가 끝난 것이 아니다.

새 클라이언트 토대는 아래 3가지를 확인해야 완료로 본다:

- [ ] `agent-kit/clients/{몰ID}/src/_nk/css/` 에 표준 CSS 4종을 생성하거나 기존 표준본에서 복사: `nk-tokens.css`, `nk-cafe24-reset.css`, `nk-base.css`, `nk-stock.css`
- [ ] 실제 사용 layout include(`layout/basic/layout.html`, `main.html` 등)에 4종 CSS `<!--@css(/_nk/css/...)-->` 로드가 들어감
- [ ] 커스텀 적용 대상 `<body>` 에 `nk-skin` scope가 있음 (`<body ... class="nk-skin">` 또는 기존 class에 `nk-skin` 추가)

> `nk-stock.css` 는 layout include로 로드되고 `body.nk-skin` 범위에 들어온 페이지에서만 효과가 있다. scaffold 완료 보고 시 "파일 존재 + layout include + body.nk-skin"을 함께 확인한다.

## Q3. config 확인

「`mcp/config/cafe24_config_{몰ID}.py` 에 **CLIENT_ID/SECRET** 을 로컬 파일에만 넣었나요? (채팅 X)」

- 아니오 → **`/API발급`**

## Q4. SFTP (해당 시)

「디자인 SFTP/FTP 정보는 `mcp/config/sftp_{몰ID}.json` 에 넣었나요? (비밀번호 채팅 X)」

- 미정 → **`/접속세팅`** 후 `write_allowed` 설정

## 완료 시 출력

```
[새클라이언트 완료]
- 몰 ID: {몰ID}
- 클라이언트 폴더: agent-kit/clients/{몰ID}/
- 다음: /MCP연결 → /API발급 → /접속세팅
```
