# 03. 접속 — 웹 FTP vs 디자인 SFTP

> **비유:** 웹 FTP는 **관리자용 작은 창고 문**, 디자인 SFTP는 **디자이너용 별도 창고 문**이다. 열쇠가 다르다.

---

## 파트너센터 샘플몰 → 웹 FTP

| 항목 | 안내 | 출처 등급 |
|------|------|-----------|
| 누가 | 파트너센터에서 만든 **샘플몰** | ⚠️ 실무 분기 |
| 무엇 | **웹 FTP** (디자인 SFTP 신청과 다름) | ⚠️ |
| 호스트 예 | `{몰ID}.ftp.cafe24.com` | ⚠️ 실측: `ecudemo400786.ftp.cafe24.com` |
| 포트 예 | **21**(FTP), 3822(SFTP) 등 **발급·화면 값** | ⚠️ ❌ 22 고정 아님 |
| 프로토콜 | **FTP** 또는 SFTP — 발급 화면 기준 | ⚠️ 실측 2026-06-19: `ecudemo400786` = **FTP 21** |
| 로그인 | 몰 ID + 임시/파트너 비밀번호 | ⚠️ |
| **편집 경로** | **`/sde_design/base/`**, **`/sde_design/mobile/`** | ⚠️ 2차 실측 |
| 루트에 없음 | `/{skin_code}` (`/skin1`, `/skin14` 등) | ⚠️ 일반 몰과 **다름** |
| 웹FTP 용어 | Admin API 상품 이미지 옵션 「C : 웹FTP 등록」 | ✅ |

**에이전트 규칙:** 파트너라고 하면 **디자인 FTP 권한 신청**을 먼저 시키지 않는다. **`/{skin_code}` 규칙을 파트너에 그대로 적용하지 않는다.**

---

## 일반 운영 몰 → 디자인 SFTP

| 항목 | 안내 | 출처 등급 |
|------|------|-----------|
| 누가 | 실제 운영 중인 쇼핑몰 관리자 | ⚠️ 실무 |
| 준비 | 관리자 **디자인 FTP 권한 신청** → 승인 후 SFTP 정보 발급 | ⚠️ 메뉴 경로 공식 HTML 미수집 |
| 호스트 | **발급된 호스트 그대로** | ❌ 반례: `ecimg-ftp-cNN.cafe24img.com` (몰ID.ftp 아님) |
| 포트 | **발급된 포트** (8008, 22 등) | ⚠️ |
| 프로토콜 | SFTP(SSH)로 쓰는 경우 많음 | ✅ 실측 |

---

## 공통 — 파일 올릴 때

1. **몰 ID** 확인 ([02](./02-몰ID-찾기.md))  
2. **`cafe24_list_themes`** 로 `skin_code` 확인 ✅ API  
3. SFTP 경로 = **`/{skin_code}`** ⚠️ 실측 ([AUDIT §E-2a](../brain/docs/OFFICIAL-AUDIT.md))  
4. **`skin_no`와 폴더 숫자가 같다고 가정하지 말 것** ⚠️  
5. **`editor_type` E( Easy )라도 SFTP `/{skin_code}` 접근 가능할 수 있음** ⚠️ 실측 2026-06-19

---

## MCP 설정 (손발)

| 파일 | 용도 |
|------|------|
| `mcp/config/cafe24_config_{몰ID}.py` | client_id, secret, REDIRECT_URI (HTTPS) |
| `mcp/config/{몰ID}.token.json` | OAuth 토큰 (자동 생성) |
| `mcp/config/sftp_{몰ID}.json` | 업로드 접속 정보 — **FTP·SFTP 공용 파일** |

> ⚠️ **파일 이름은 `sftp_` 지만 웹 FTP도 이 파일을 씁니다.** 안에 `"protocol": "ftp"` 를 넣으면 모든 도구(`cafe24_sftp_*`)가 자동으로 **웹 FTP(파트너센터)** 로 동작합니다. (없으면 SFTP로 시도 → 파트너센터에서 실패)

**① 파트너센터 (웹 FTP)** — `mcp/config/sftp_{몰ID}.json`:
```json
{
  "protocol": "ftp",
  "host": "{몰ID}.ftp.cafe24.com",
  "port": 21,
  "username": "{발급 아이디(보통 몰ID)}",
  "password": "********",
  "write_allowed": ["/sde_design/base", "/sde_design/mobile"]
}
```

**② 일반 운영몰 (SFTP)** — 같은 파일, `protocol` 생략:
```json
{
  "host": "{발급 호스트}",
  "port": 22,
  "username": "{발급 아이디}",
  "password": "********",
  "write_allowed": ["/{skin_code}"]
}
```

비밀번호·secret은 **채팅에 붙이지 마세요.**  
모노레po만 clone: OneDrive `api-poc/cafe24_config.py` 자동 탐색 또는 py 복사.

- [05-MCP-연결-개요.md](./05-MCP-연결-개요.md)  
- [../connect/MCP-OAUTH-GUIDE.md](../connect/MCP-OAUTH-GUIDE.md)
