#!/usr/bin/env python3
"""
카페24 Admin API '읽기' 검증 PoC (read-only) — 수동 코드 방식

카페24는 Redirect URI를 HTTPS만 허용하므로, 로컬 HTTPS 서버 대신
'브라우저 주소창 코드 복사' 방식을 쓴다.

사용법:
  1) python read_skins.py url
       -> 인증 주소 출력. 브라우저에서 열고 '허용' 클릭.
       -> 허용하면 https://localhost:8888/callback?code=XXXX&state=YYYY 로 이동(빈화면/오류 정상).
       -> 그 주소창 전체 URL(또는 code 값)을 복사.
  2) python read_skins.py code "<복사한 URL 또는 code 값>"
       -> 토큰 교환 + 디자인 목록 + 스킨 소스 읽기.

수정(쓰기)은 하지 않는다. scope = mall.read_design.
"""
import base64
import json
import os
import sys
import urllib.parse

import requests

import cafe24_config as cfg

HERE = os.path.dirname(__file__)
TOKEN_FILE = os.path.join(HERE, "cafe24.token.json")


def base_url() -> str:
    return f"https://{cfg.MALL_ID}.cafe24api.com"


def build_auth_url() -> str:
    params = {
        "response_type": "code",
        "client_id": cfg.CLIENT_ID,
        "state": "nookitokki_poc",
        "redirect_uri": cfg.REDIRECT_URI,
        "scope": cfg.SCOPE,
    }
    return f"{base_url()}/api/v2/oauth/authorize?" + urllib.parse.urlencode(params)


def extract_code(raw: str) -> str:
    raw = raw.strip().strip('"').strip("'")
    if "code=" in raw:
        qs = urllib.parse.urlparse(raw).query or raw.split("?", 1)[-1]
        code = urllib.parse.parse_qs(qs).get("code", [None])[0]
        if code:
            return code
    return raw  # 사용자가 code 값만 붙여넣은 경우


def exchange_token(code: str) -> dict:
    basic = base64.b64encode(
        f"{cfg.CLIENT_ID}:{cfg.CLIENT_SECRET}".encode()
    ).decode()
    resp = requests.post(
        f"{base_url()}/api/v2/oauth/token",
        headers={
            "Authorization": f"Basic {basic}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": cfg.REDIRECT_URI,
        },
        timeout=20,
    )
    if resp.status_code != 200:
        print(f"ERROR 토큰 교환 실패 {resp.status_code}: {resp.text}", file=sys.stderr)
        sys.exit(1)
    tok = resp.json()
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        json.dump(tok, f, ensure_ascii=False, indent=2)
    print(f"[토큰] access_token 발급 완료 (만료: {tok.get('expires_at')})", flush=True)
    return tok


def api_get(path: str, access_token: str, params=None) -> requests.Response:
    return requests.get(
        f"{base_url()}{path}",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Cafe24-Api-Version": cfg.API_VERSION,
        },
        params=params or {},
        timeout=20,
    )


def read_skins(access_token: str):
    print("\n[목록] 디자인(테마) 조회 ...", flush=True)
    r = api_get("/api/v2/admin/themes", access_token)
    print("  status:", r.status_code, flush=True)
    if r.status_code != 200:
        print("  응답:", r.text[:600], flush=True)
        return
    themes = r.json().get("themes", [])
    print(f"  총 {len(themes)}개 디자인:", flush=True)
    for th in themes:
        print(
            f"    - skin_no={th.get('skin_no')} "
            f"editor_type={th.get('editor_type')} "
            f"name={th.get('skin_name')!r} usage={th.get('usage_type')}",
            flush=True,
        )

    target = next((t for t in themes if t.get("editor_type") == "H"), None)
    if not target:
        print("\n[소스] HTML(스마트디자인) 스킨이 없어 소스 읽기 생략.", flush=True)
        return
    skin_no = target["skin_no"]
    test_path = "/layout/basic/layout.html"
    print(f"\n[소스] skin_no={skin_no} 의 {test_path} 읽기 ...", flush=True)
    r = api_get(
        f"/api/v2/admin/themes/{skin_no}/pages",
        access_token,
        params={"path": test_path},
    )
    print("  status:", r.status_code, flush=True)
    if r.status_code == 200:
        data = r.json()
        out = os.path.join(HERE, "sample_page.json")
        with open(out, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        src = json.dumps(data, ensure_ascii=False)
        print(f"  응답 길이: {len(src)} chars (앞 500자):\n", flush=True)
        print(src[:500], flush=True)
        print(f"\n  전체 응답 저장: {out}", flush=True)
    else:
        print("  응답:", r.text[:600], flush=True)


def main():
    if not cfg.MALL_ID:
        print("ERROR: cafe24_config.py 의 MALL_ID 를 채워주세요.", file=sys.stderr)
        sys.exit(1)
    mode = sys.argv[1] if len(sys.argv) > 1 else "url"

    if mode == "url":
        url = build_auth_url()
        with open(os.path.join(HERE, "auth_url.txt"), "w", encoding="utf-8") as f:
            f.write(url + "\n")
        print("아래 주소를 브라우저에 붙여넣고 '허용'을 누르세요:\n", flush=True)
        print(url, flush=True)
        print(
            "\n허용 후 이동되는 https://localhost:8888/... 주소창 URL을 복사해서 알려주세요.",
            flush=True,
        )
    elif mode == "code":
        if len(sys.argv) < 3:
            print('사용법: python read_skins.py code "<URL 또는 code>"', file=sys.stderr)
            sys.exit(1)
        code = extract_code(sys.argv[2])
        tok = exchange_token(code)
        read_skins(tok["access_token"])
    else:
        print(f"알 수 없는 모드: {mode} (url | code)", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
