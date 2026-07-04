"""
카페24 Admin API 백엔드 (읽기 전용) — 설계서 §4-1.

제공 기능:
  list_themes()            디자인(스킨) 목록 + 타입(H/E) 메타데이터
  read_page(skin_no, path) 스킨 파일 1건의 소스(카페24 보관 정본)
  auth_status()            토큰 유효시간·scope 진단

모든 호출 전에 TokenManager 가 토큰 만료를 검사해 자동 갱신한다.
혹시 서버 쪽 사정으로 401이 오면 한 번 더 강제 갱신 후 재시도한다.
"""
import os
import sys

import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth.oauth import AuthError, TokenManager  # noqa: E402


class Cafe24ApiError(Exception):
    """API 호출이 200이 아닌 응답을 돌려준 경우."""


class Cafe24API:
    """몰 하나에 대한 Admin API 읽기 클라이언트.

    사용법:
        api = Cafe24API("demo000")
        themes = api.list_themes()
        page = api.read_page(4, "/layout/basic/layout.html")
    """

    def __init__(self, mall_id: str = "demo000"):
        self.tm = TokenManager(mall_id)
        self.cfg = self.tm.cfg

    # ── 공통 GET 호출 (자동갱신 + 401 재시도 1회) ───────────────

    def _get(self, path: str, params: dict | None = None) -> dict:
        token = self.tm.get_access_token()
        resp = self._raw_get(path, token, params)

        # 401 = 토큰이 서버에서 무효 처리된 경우 → 강제 갱신 후 딱 1번 재시도
        if resp.status_code == 401:
            tok = self.tm.load_token()
            if tok and tok.get("refresh_token"):
                token = self.tm.refresh(tok["refresh_token"])["access_token"]
                resp = self._raw_get(path, token, params)

        if resp.status_code != 200:
            raise Cafe24ApiError(
                f"GET {path} 실패 {resp.status_code}: {resp.text[:400]}"
            )
        return resp.json()

    def _raw_get(self, path: str, token: str, params: dict | None) -> requests.Response:
        return requests.get(
            f"{self.tm.base_url}{path}",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "X-Cafe24-Api-Version": self.cfg.API_VERSION,
            },
            params=params or {},
            timeout=20,
        )

    # ── 도구 1: 디자인 목록 ────────────────────────────────────

    def list_themes(self) -> list[dict]:
        """디자인(스킨) 목록. editor_type H=스마트디자인(HTML), E=Easy.

        skin_code 가 API 와 SFTP 두 백엔드를 잇는 다리다 (⚠️ 실측 2026-06-10, 공식 문장 없음 — agent-kit OFFICIAL-AUDIT §E-2a).
        """
        data = self._get("/api/v2/admin/themes", params={"limit": 100})
        return [
            {
                "skin_no": th.get("skin_no"),
                "skin_code": th.get("skin_code"),
                "skin_name": th.get("skin_name"),
                "editor_type": th.get("editor_type"),
                "usage_type": th.get("usage_type"),
            }
            for th in data.get("themes", [])
        ]

    # ── 도구 2: 스킨 파일 1건 읽기 (정본) ──────────────────────

    def read_page(self, skin_no: int, path: str) -> dict:
        """스킨 파일 1건의 소스를 읽는다.

        skin_no: list_themes() 가 알려주는 스킨 번호
        path   : 스킨 루트 기준 경로 (예: /layout/basic/layout.html)
        """
        if not path.startswith("/"):
            path = "/" + path
        data = self._get(
            f"/api/v2/admin/themes/{skin_no}/pages",
            params={"path": path},
        )
        # 응답 모양이 {"page": {...}} 또는 {"pages": [...]} 일 수 있어 둘 다 처리
        page = data.get("page") or data.get("pages") or data
        if isinstance(page, list):
            page = page[0] if page else {}
        return page

    # ── 도구 3: 인증 상태 진단 ─────────────────────────────────

    def auth_status(self) -> dict:
        """토큰 유효시간·scope 요약 (비밀값 미포함)."""
        return self.tm.status()
