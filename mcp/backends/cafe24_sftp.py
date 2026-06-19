"""
카페24 SFTP 백엔드 (탐색·대량·쓰기) — 설계서 §4-2.

제공 기능:
  list(remote_path, depth)        파일/폴더 트리 (구조화된 목록 반환)
  read(remote_path)               파일 내용 텍스트 1건
  download(remote_path, local)    파일/폴더 로컬 저장 (폴더는 재귀 미러)
  backup(remote_path)             쓰기 전 자동 백업 → 로컬 백업본 경로 반환
  upload(local, remote_path)      업로드 ★운영 반영 — 호출 전 사용자 확인 필수

안전장치:
  - write_allowed 화이트리스트에 없는 경로로의 업로드는 무조건 거부
    (paransky97: /skin3~/skin9 만 허용, skin1/skin2/base 보호)
  - upload 는 기본적으로 backup 을 먼저 자동 실행 (auto_backup=True)

기존 검증된 패턴 출처:
  - banner_timeout 명시: paramiko 4+ 기본 무한대기 hang 방지 (slowagings)
  - 다운로드 실패 시 빈 파일 정리: 빈 껍데기로 덮어쓰는 사고 방지 (template-02)
  - 슬롯 화이트리스트: sftp_push.py ALLOWED_TARGETS (template-02)
"""
import os
import stat
import sys
from datetime import datetime

import paramiko

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import load_sftp_config  # noqa: E402

# mcp/ 폴더 (백업 저장 기준 위치)
MCP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 텍스트로 읽기엔 너무 큰 파일 보호 (5MB)
READ_MAX_BYTES = 5 * 1024 * 1024


class SftpWriteDenied(Exception):
    """화이트리스트에 없는 경로로 쓰기를 시도한 경우."""


class Cafe24SFTP:
    """몰 하나의 SFTP 클라이언트. 연결은 필요할 때 한 번만 열고 재사용.

    사용법:
        with Cafe24SFTP("paransky97") as sftp:
            tree = sftp.list("/skin4", depth=2)
            text = sftp.read("/skin4/index.html")
    """

    def __init__(self, mall_id: str = "paransky97"):
        self.mall_id = mall_id
        self.cfg = load_sftp_config(mall_id)
        self._transport = None
        self._sftp = None

    # ── 연결 관리 ─────────────────────────────────────────────

    def _client(self) -> paramiko.SFTPClient:
        """연결이 없으면 새로 열고, 있으면 재사용한다."""
        if self._sftp is not None:
            return self._sftp
        t = paramiko.Transport((self.cfg["host"], int(self.cfg["port"])))
        t.banner_timeout = 30  # paramiko 4+ 기본 무한대기 → hang 방지 (필수)
        t.connect(username=self.cfg["username"], password=self.cfg["password"])
        self._transport = t
        self._sftp = paramiko.SFTPClient.from_transport(t)
        return self._sftp

    def close(self):
        if self._sftp:
            self._sftp.close()
            self._sftp = None
        if self._transport:
            self._transport.close()
            self._transport = None

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    # ── 경로 도우미 ───────────────────────────────────────────

    @staticmethod
    def _norm(path: str) -> str:
        """원격 경로를 '/...' 형태로 통일한다."""
        path = (path or "/").replace("\\", "/").strip()
        if not path.startswith("/"):
            path = "/" + path
        return path.rstrip("/") or "/"

    def _check_writable(self, remote_path: str):
        """쓰기 화이트리스트 검사. 허용 밖이면 즉시 거부."""
        rp = self._norm(remote_path)
        for allowed in self.cfg.get("write_allowed", []):
            a = self._norm(allowed)
            if rp == a or rp.startswith(a + "/"):
                return
        raise SftpWriteDenied(
            f"쓰기 거부: {rp} 는 허용 목록에 없습니다. "
            f"허용: {self.cfg.get('write_allowed', [])} "
            "(skin1/skin2/base 등 운영·원본 보호)"
        )

    # ── 도구 1: 파일트리 listing ──────────────────────────────

    def list(self, remote_path: str = "/", depth: int = 1) -> list[dict]:
        """원격 폴더 트리를 구조화된 목록으로 돌려준다.

        반환 항목: {path, type(file|dir), size, mtime}
        depth=1 이면 바로 아래만, 2면 한 단계 더 들어간다.
        """
        sftp = self._client()
        out: list[dict] = []
        self._walk(sftp, self._norm(remote_path), 1, depth, out)
        return out

    def _walk(self, sftp, path: str, cur: int, max_depth: int, out: list):
        try:
            items = sorted(sftp.listdir_attr(path), key=lambda x: x.filename)
        except IOError:
            return
        for it in items:
            child = (path.rstrip("/") or "") + "/" + it.filename
            is_dir = stat.S_ISDIR(it.st_mode) if it.st_mode else False
            out.append({
                "path": child,
                "type": "dir" if is_dir else "file",
                "size": it.st_size,
                "mtime": datetime.fromtimestamp(it.st_mtime).isoformat(sep=" ")
                if it.st_mtime else None,
            })
            if is_dir and cur < max_depth:
                self._walk(sftp, child, cur + 1, max_depth, out)

    # ── 도구 2: 파일 내용 읽기 ────────────────────────────────

    def read(self, remote_path: str) -> str:
        """원격 텍스트 파일 1건의 내용을 돌려준다."""
        sftp = self._client()
        rp = self._norm(remote_path)
        size = sftp.stat(rp).st_size
        if size > READ_MAX_BYTES:
            raise IOError(
                f"{rp} 는 {size:,} bytes 로 너무 큽니다. download 를 사용하세요."
            )
        with sftp.open(rp, "r") as f:
            data = f.read()
        return data.decode("utf-8", errors="replace")

    # ── 도구 3: 다운로드 (파일/폴더) ──────────────────────────

    def download(self, remote_path: str, local_path: str) -> dict:
        """원격 파일/폴더를 로컬로 저장. 폴더면 재귀 미러.

        반환: {"files": 받은 개수, "failed": 실패 개수}
        """
        sftp = self._client()
        rp = self._norm(remote_path)
        result = {"files": 0, "failed": 0}
        attr = sftp.stat(rp)
        if stat.S_ISDIR(attr.st_mode):
            self._download_dir(sftp, rp, local_path, result)
        else:
            parent = os.path.dirname(os.path.abspath(local_path))
            os.makedirs(parent, exist_ok=True)
            self._get_file(sftp, rp, local_path, result)
        return result

    def _download_dir(self, sftp, remote_dir: str, local_dir: str, result: dict):
        os.makedirs(local_dir, exist_ok=True)
        try:
            entries = sftp.listdir_attr(remote_dir)
        except IOError:
            result["failed"] += 1
            return
        for it in entries:
            rp = remote_dir.rstrip("/") + "/" + it.filename
            lp = os.path.join(local_dir, it.filename)
            if stat.S_ISDIR(it.st_mode):
                self._download_dir(sftp, rp, lp, result)
            else:
                self._get_file(sftp, rp, lp, result)

    @staticmethod
    def _get_file(sftp, rp: str, lp: str, result: dict):
        try:
            sftp.get(rp, lp)
            result["files"] += 1
        except Exception:
            result["failed"] += 1
            # 받다 만 빈 껍데기가 남으면 지운다 (멀쩡한 파일을 빈 파일로
            # 덮어쓰는 사고 방지 — template-02 sftp_pull 패턴)
            if os.path.exists(lp) and os.path.getsize(lp) == 0:
                try:
                    os.remove(lp)
                except OSError:
                    pass

    # ── 도구 4: 쓰기 전 백업 ──────────────────────────────────

    def backup(self, remote_path: str) -> str | None:
        """원격 파일/폴더를 mcp/backups/{몰}/{시각}/ 아래로 백업.

        반환: 백업본 로컬 경로. 원격에 아직 없는 파일(신규)이면 None.
        """
        sftp = self._client()
        rp = self._norm(remote_path)
        try:
            sftp.stat(rp)
        except FileNotFoundError:
            return None  # 신규 파일 — 백업할 원본이 없음
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        dest = os.path.join(
            MCP_ROOT, "backups", self.mall_id, ts, rp.lstrip("/").replace("/", os.sep)
        )
        self.download(rp, dest)
        return dest

    # ── 도구 5: 업로드 ★운영 반영 ─────────────────────────────

    def upload(
        self,
        local_path: str | None = None,
        remote_path: str = "",
        content: str | None = None,
        auto_backup: bool = True,
    ) -> dict:
        """로컬 파일/폴더 또는 문자열(content)을 원격에 업로드.

        ★ 운영 서버 반영 — 호출하는 쪽(에이전트)이 반드시 사용자 확인을
          먼저 받아야 한다 (누끼토끼 절대룰).

        안전장치:
          1) write_allowed 화이트리스트 검사 (벗어나면 즉시 거부)
          2) auto_backup=True (기본) — 덮어쓰기 전 원본을 자동 백업

        반환: {"uploaded": n, "failed": n, "backup": 백업경로|None}
        """
        rp = self._norm(remote_path)
        self._check_writable(rp)

        backup_path = self.backup(rp) if auto_backup else None
        sftp = self._client()
        result = {"uploaded": 0, "failed": 0, "backup": backup_path}

        if content is not None:
            # 문자열을 바로 원격 파일로 저장 (에이전트가 생성한 코드 반영용)
            self._ensure_remote_dir(sftp, os.path.dirname(rp).replace("\\", "/"))
            with sftp.open(rp, "w") as f:
                f.write(content.encode("utf-8"))
            result["uploaded"] = 1
        elif local_path and os.path.isfile(local_path):
            self._ensure_remote_dir(sftp, os.path.dirname(rp).replace("\\", "/"))
            sftp.put(local_path, rp)
            result["uploaded"] = 1
        elif local_path and os.path.isdir(local_path):
            self._upload_dir(sftp, local_path, rp, result)
        else:
            raise FileNotFoundError(f"업로드할 원본이 없습니다: {local_path!r}")
        return result

    def _upload_dir(self, sftp, local_dir: str, remote_dir: str, result: dict):
        self._ensure_remote_dir(sftp, remote_dir)
        for name in sorted(os.listdir(local_dir)):
            lp = os.path.join(local_dir, name)
            rp = remote_dir.rstrip("/") + "/" + name
            if os.path.isdir(lp):
                self._upload_dir(sftp, lp, rp, result)
            else:
                try:
                    sftp.put(lp, rp)
                    result["uploaded"] += 1
                except Exception:
                    result["failed"] += 1

    @staticmethod
    def _ensure_remote_dir(sftp, remote_dir: str):
        """원격 폴더가 없으면 상위부터 차례로 만든다."""
        if not remote_dir or remote_dir == "/":
            return
        parts = remote_dir.strip("/").split("/")
        cur = ""
        for p in parts:
            cur += "/" + p
            try:
                sftp.stat(cur)
            except IOError:
                sftp.mkdir(cur)
