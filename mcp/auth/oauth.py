"""
카페24 OAuth 토큰 관리 — 발급·저장·자동갱신.

토큰 수명 구조 (설계서 §5):
  access_token  : 2시간.  만료되면 refresh_token 으로 자동 재발급.
  refresh_token : 2주(쓸 때마다 다시 2주로 연장). 이마저 만료되면
                  사용자가 브라우저에서 1회 '허용'을 다시 눌러야 한다.

토큰은 mcp/config/{mall_id}.token.json 에 저장한다 (git 제외).
PoC 토큰(api-poc/cafe24.token.json)이 있으면 첫 실행 때 자동으로 가져온다.
"""
import base64
import json
import os
import shutil
import urllib.parse
from datetime import datetime, timedelta

import requests

import sys

# mcp/ 폴더를 import 경로에 추가 (auth/ 안에서 config 패키지를 찾기 위함)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import load_mall_config, token_file_path, CAFE24_ROOT  # noqa: E402

# PoC 시절 토큰 파일 위치 (demo000 마이그레이션용)
POC_TOKEN = os.path.join(CAFE24_ROOT, "api-poc", "cafe24.token.json")

# 만료 직전 호출이 실패하지 않도록 두는 여유 시간(초)
EXPIRY_MARGIN_SEC = 60


class AuthError(Exception):
    """토큰 발급/갱신 실패. 메시지에 사용자가 해야 할 일을 담는다."""


class TokenManager:
    """몰 하나의 토큰을 책임지는 관리자.

    사용법:
        tm = TokenManager("demo000")
        token = tm.get_access_token()   # 만료됐으면 알아서 갱신
    """

    def __init__(self, mall_id: str = "demo000"):
        self.mall_id = mall_id
        self.cfg = load_mall_config(mall_id)
        self.token_file = token_file_path(mall_id)
        self._migrate_poc_token()

    # ── 기본 정보 ──────────────────────────────────────────────

    @property
    def base_url(self) -> str:
        return f"https://{self.cfg.MALL_ID}.cafe24api.com"

    def _basic_auth_header(self) -> str:
        """토큰 발급용 Basic 인증 헤더 값 (client_id:secret 을 base64로)."""
        raw = f"{self.cfg.CLIENT_ID}:{self.cfg.CLIENT_SECRET}".encode()
        return "Basic " + base64.b64encode(raw).decode()

    # ── 토큰 파일 읽기/쓰기 ────────────────────────────────────

    def _migrate_poc_token(self):
        """PoC 토큰 파일이 있고 새 위치에 토큰이 없으면 복사해 온다."""
        if os.path.exists(self.token_file) or not os.path.exists(POC_TOKEN):
            return
        try:
            with open(POC_TOKEN, encoding="utf-8") as f:
                tok = json.load(f)
        except (OSError, json.JSONDecodeError):
            return
        if tok.get("mall_id") == self.mall_id:
            shutil.copyfile(POC_TOKEN, self.token_file)

    def load_token(self) -> dict | None:
        """저장된 토큰을 읽는다. 없으면 None."""
        if not os.path.exists(self.token_file):
            return None
        with open(self.token_file, encoding="utf-8") as f:
            return json.load(f)

    def _save_token(self, tok: dict):
        """토큰을 저장한다. 쓰다 말고 죽어도 파일이 깨지지 않게
        임시 파일에 먼저 쓰고 통째로 바꿔치기한다."""
        tmp = self.token_file + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(tok, f, ensure_ascii=False, indent=2)
        os.replace(tmp, self.token_file)

    # ── 만료 판정 ──────────────────────────────────────────────

    @staticmethod
    def _parse_dt(value: str) -> datetime:
        """카페24가 주는 '2026-06-10T01:02:01.000' 형식을 datetime으로."""
        return datetime.fromisoformat(value)

    def _is_expired(self, expires_at: str | None) -> bool:
        if not expires_at:
            return True
        try:
            dt = self._parse_dt(expires_at)
        except ValueError:
            return True
        return datetime.now() >= dt - timedelta(seconds=EXPIRY_MARGIN_SEC)

    # ── 핵심: 유효한 access_token 확보 ─────────────────────────

    def get_access_token(self) -> str:
        """유효한 access_token 을 돌려준다. 만료면 자동 갱신.

        refresh_token 까지 만료면 AuthError 를 던진다
        (이때는 auth_url() 로 다시 1회 동의를 받아야 함).
        """
        tok = self.load_token()
        if tok is None:
            raise AuthError(
                f"저장된 토큰이 없습니다. 'python cli.py auth-url' 로 "
                f"인증 주소를 만들어 브라우저에서 허용해 주세요. (몰: {self.mall_id})"
            )

        # access_token 이 아직 살아 있으면 그대로 사용
        if not self._is_expired(tok.get("expires_at")):
            return tok["access_token"]

        # access 만료 → refresh 가 살아 있으면 자동 갱신
        if self._is_expired(tok.get("refresh_token_expires_at")):
            raise AuthError(
                "refresh_token(2주)까지 만료되었습니다. "
                "'python cli.py auth-url' 로 재동의가 필요합니다."
            )
        return self.refresh(tok["refresh_token"])["access_token"]

    def refresh(self, refresh_token: str) -> dict:
        """refresh_token 으로 새 access_token 을 발급받고 저장한다.

        주의: 카페24는 갱신할 때 refresh_token 도 새것으로 바꿔 주므로
        응답을 받는 즉시 저장해야 한다 (옛 토큰은 못 쓰게 됨).
        """
        resp = requests.post(
            f"{self.base_url}/api/v2/oauth/token",
            headers={
                "Authorization": self._basic_auth_header(),
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            },
            timeout=20,
        )
        if resp.status_code != 200:
            raise AuthError(
                f"토큰 갱신 실패 {resp.status_code}: {resp.text[:300]} "
                "— 'python cli.py auth-url' 로 재동의가 필요할 수 있습니다."
            )
        tok = resp.json()
        self._save_token(tok)
        return tok

    # ── 최초 1회 동의 (refresh 만료 시에만 필요) ────────────────

    def auth_url(self) -> str:
        """사용자가 브라우저에서 '허용'을 누를 인증 주소를 만든다."""
        params = {
            "response_type": "code",
            "client_id": self.cfg.CLIENT_ID,
            "state": f"nookitokki_mcp_{self.mall_id}",
            "redirect_uri": self.cfg.REDIRECT_URI,
            "scope": self.cfg.SCOPE,
        }
        return f"{self.base_url}/api/v2/oauth/authorize?" + urllib.parse.urlencode(params)

    @staticmethod
    def extract_code(raw: str) -> str:
        """허용 후 이동된 URL 전체에서 code 값만 뽑아낸다."""
        raw = raw.strip().strip('"').strip("'")
        if "code=" in raw:
            qs = urllib.parse.urlparse(raw).query or raw.split("?", 1)[-1]
            code = urllib.parse.parse_qs(qs).get("code", [None])[0]
            if code:
                return code
        return raw  # 사용자가 code 값만 붙여넣은 경우

    def exchange_code(self, code_or_url: str) -> dict:
        """인증 code 를 토큰으로 교환하고 저장한다."""
        code = self.extract_code(code_or_url)
        resp = requests.post(
            f"{self.base_url}/api/v2/oauth/token",
            headers={
                "Authorization": self._basic_auth_header(),
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": self.cfg.REDIRECT_URI,
            },
            timeout=20,
        )
        if resp.status_code != 200:
            raise AuthError(f"토큰 교환 실패 {resp.status_code}: {resp.text[:300]}")
        tok = resp.json()
        self._save_token(tok)
        return tok

    # ── 진단용 ────────────────────────────────────────────────

    def status(self) -> dict:
        """토큰 상태 요약 (비밀값은 포함하지 않음)."""
        tok = self.load_token()
        if tok is None:
            return {"mall_id": self.mall_id, "token": "없음"}
        return {
            "mall_id": self.mall_id,
            "scopes": tok.get("scopes"),
            "access_token_expires_at": tok.get("expires_at"),
            "access_token_valid": not self._is_expired(tok.get("expires_at")),
            "refresh_token_expires_at": tok.get("refresh_token_expires_at"),
            "refresh_token_valid": not self._is_expired(
                tok.get("refresh_token_expires_at")
            ),
            "token_file": self.token_file,
        }
