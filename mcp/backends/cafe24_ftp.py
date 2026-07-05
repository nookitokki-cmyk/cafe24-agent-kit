"""
카페24 FTP 백엔드 (파트너 웹 FTP · port 21).

Cafe24SFTP 와 동일한 public API(list/read/download/backup/upload)를 제공한다.
config/sftp_{mall}.json 에 "protocol": "ftp" 가 있으면 server 가 이 백엔드를 사용한다.
"""
from __future__ import annotations

import ftplib
import io
import os
import stat
from datetime import datetime
from typing import Callable

import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import load_sftp_config  # noqa: E402

from backends.cafe24_sftp import (  # noqa: E402
    MCP_ROOT,
    READ_MAX_BYTES,
    SftpWriteDenied,
)


class Cafe24FTP:
    """몰 하나의 FTP 클라이언트 (ftplib). Cafe24SFTP 와 같은 메서드 시그니처."""

    def __init__(self, mall_id: str = "ecudemo400786"):
        self.mall_id = mall_id
        self.cfg = load_sftp_config(mall_id)
        self._ftp: ftplib.FTP | None = None

    def _client(self) -> ftplib.FTP:
        if self._ftp is not None:
            try:
                self._ftp.voidcmd("NOOP")
                return self._ftp
            except Exception:
                self.close()
        ftp = ftplib.FTP()
        ftp.connect(self.cfg["host"], int(self.cfg.get("port", 21)), timeout=30)
        ftp.login(self.cfg["username"], self.cfg["password"])
        self._ftp = ftp
        return ftp

    def close(self):
        if self._ftp:
            try:
                self._ftp.quit()
            except Exception:
                try:
                    self._ftp.close()
                except Exception:
                    pass
            self._ftp = None

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    @staticmethod
    def _norm(path: str) -> str:
        path = (path or "/").replace("\\", "/").strip()
        if not path.startswith("/"):
            path = "/" + path
        return path.rstrip("/") or "/"

    def _check_writable(self, remote_path: str):
        rp = self._norm(remote_path)
        for allowed in self.cfg.get("write_allowed", []):
            a = self._norm(allowed)
            if rp == a or rp.startswith(a + "/"):
                return
        raise SftpWriteDenied(
            f"쓰기 거부: {rp} 는 허용 목록에 없습니다. "
            f"허용: {self.cfg.get('write_allowed', [])}"
        )

    def _cwd_abs(self, ftp: ftplib.FTP, abs_path: str):
        ftp.cwd("/")
        parts = [p for p in abs_path.strip("/").split("/") if p]
        for p in parts:
            ftp.cwd(p)

    def _mlsd(self, ftp: ftplib.FTP, path: str) -> list[tuple[str, dict]]:
        self._cwd_abs(ftp, path)
        try:
            entries = list(ftp.mlsd())
            if entries and all(not facts.get("type") for _, facts in entries):
                raise ftplib.error_perm("mlsd facts incomplete")
            return entries
        except ftplib.error_perm:
            lines: list[str] = []
            ftp.retrlines("LIST", lines.append)
            out: list[tuple[str, dict]] = []
            for line in lines:
                parts = line.split(None, 8)
                if len(parts) < 9:
                    continue
                name = parts[8]
                if name in (".", ".."):
                    continue
                is_dir = parts[0].startswith("d")
                out.append((name, {"type": "dir" if is_dir else "file", "size": parts[4]}))
            return out

    def list(self, remote_path: str = "/", depth: int = 1) -> list[dict]:
        ftp = self._client()
        out: list[dict] = []
        self._walk(ftp, self._norm(remote_path), 1, depth, out)
        return out

    def _walk(self, ftp: ftplib.FTP, path: str, cur: int, max_depth: int, out: list):
        try:
            entries = self._mlsd(ftp, path)
        except ftplib.error_perm:
            return
        for name, facts in sorted(entries, key=lambda x: x[0].lower()):
            if name in (".", ".."):
                continue
            child = (path.rstrip("/") or "") + "/" + name
            is_dir = facts.get("type") == "dir"
            size = int(facts.get("size", 0) or 0)
            modify = facts.get("modify")
            mtime = None
            if modify and len(modify) >= 14:
                try:
                    mtime = datetime.strptime(modify[:14], "%Y%m%d%H%M%S").isoformat(sep=" ")
                except ValueError:
                    pass
            out.append({
                "path": child,
                "type": "dir" if is_dir else "file",
                "size": size,
                "mtime": mtime,
            })
            if is_dir and cur < max_depth:
                self._walk(ftp, child, cur + 1, max_depth, out)

    def read(self, remote_path: str) -> str:
        ftp = self._client()
        rp = self._norm(remote_path)
        buf = io.BytesIO()
        self._cwd_abs(ftp, os.path.dirname(rp) or "/")
        filename = rp.split("/")[-1]
        ftp.retrbinary(f"RETR {filename}", buf.write)
        data = buf.getvalue()
        if len(data) > READ_MAX_BYTES:
            raise IOError(f"{rp} 는 {len(data):,} bytes 로 너무 큽니다.")
        return data.decode("utf-8", errors="replace")

    def _is_dir(self, ftp: ftplib.FTP, rp: str) -> bool:
        parent = os.path.dirname(rp) or "/"
        name = rp.split("/")[-1]
        try:
            for entry_name, facts in self._mlsd(ftp, parent):
                if entry_name == name:
                    return facts.get("type") == "dir"
        except ftplib.error_perm:
            pass
        return False

    def download(self, remote_path: str, local_path: str) -> dict:
        ftp = self._client()
        rp = self._norm(remote_path)
        result = {"files": 0, "failed": 0}
        is_dir = self._is_dir(ftp, rp)

        if is_dir:
            self._download_dir(ftp, rp, local_path, result)
        else:
            parent = os.path.dirname(os.path.abspath(local_path))
            os.makedirs(parent, exist_ok=True)
            self._get_file(ftp, rp, local_path, result)
        return result

    def _download_dir(self, ftp: ftplib.FTP, remote_dir: str, local_dir: str, result: dict):
        os.makedirs(local_dir, exist_ok=True)
        try:
            entries = self._mlsd(ftp, remote_dir)
        except ftplib.error_perm:
            result["failed"] += 1
            return
        for name, facts in entries:
            if name in (".", ".."):
                continue
            rp = remote_dir.rstrip("/") + "/" + name
            lp = os.path.join(local_dir, name)
            if facts.get("type") == "dir":
                self._download_dir(ftp, rp, lp, result)
            else:
                self._get_file(ftp, rp, lp, result)

    def _get_file(self, ftp: ftplib.FTP, rp: str, lp: str, result: dict):
        try:
            buf = io.BytesIO()
            self._cwd_abs(ftp, os.path.dirname(rp) or "/")
            ftp.retrbinary(f"RETR {rp.split('/')[-1]}", buf.write)
            with open(lp, "wb") as f:
                f.write(buf.getvalue())
            result["files"] += 1
        except Exception:
            result["failed"] += 1
            if os.path.exists(lp) and os.path.getsize(lp) == 0:
                try:
                    os.remove(lp)
                except OSError:
                    pass

    def backup(self, remote_path: str) -> str | None:
        rp = self._norm(remote_path)
        ftp = self._client()
        parent = os.path.dirname(rp) or "/"
        name = rp.split("/")[-1]
        try:
            exists = any(entry_name == name for entry_name, _facts in self._mlsd(ftp, parent))
        except ftplib.error_perm:
            exists = False
        if not exists:
            return None
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        dest = os.path.join(
            MCP_ROOT, "backups", self.mall_id, ts, rp.lstrip("/").replace("/", os.sep)
        )
        self.download(rp, dest)
        return dest

    def upload(
        self,
        local_path: str | None = None,
        remote_path: str = "",
        content: str | None = None,
        auto_backup: bool = True,
    ) -> dict:
        rp = self._norm(remote_path)
        self._check_writable(rp)
        backup_path = self.backup(rp) if auto_backup else None
        ftp = self._client()
        result = {"uploaded": 0, "failed": 0, "backup": backup_path}

        remote_dir = os.path.dirname(rp).replace("\\", "/") or "/"
        self._ensure_remote_dir(ftp, remote_dir)
        filename = rp.split("/")[-1]

        if content is not None:
            bio = io.BytesIO(content.encode("utf-8"))
            self._cwd_abs(ftp, remote_dir)
            ftp.storbinary(f"STOR {filename}", bio)
            result["uploaded"] = 1
        elif local_path and os.path.isfile(local_path):
            self._cwd_abs(ftp, remote_dir)
            with open(local_path, "rb") as f:
                ftp.storbinary(f"STOR {filename}", f)
            result["uploaded"] = 1
        elif local_path and os.path.isdir(local_path):
            self._upload_dir(ftp, local_path, rp, result)
        else:
            raise FileNotFoundError(f"업로드할 원본이 없습니다: {local_path!r}")
        return result

    def _upload_dir(self, ftp: ftplib.FTP, local_dir: str, remote_dir: str, result: dict):
        self._ensure_remote_dir(ftp, remote_dir)
        for name in sorted(os.listdir(local_dir)):
            lp = os.path.join(local_dir, name)
            rp = remote_dir.rstrip("/") + "/" + name
            if os.path.isdir(lp):
                self._upload_dir(ftp, lp, rp, result)
            else:
                try:
                    parent = os.path.dirname(rp) or "/"
                    self._ensure_remote_dir(ftp, parent)
                    self._cwd_abs(ftp, parent)
                    with open(lp, "rb") as f:
                        ftp.storbinary(f"STOR {name}", f)
                    result["uploaded"] += 1
                except Exception:
                    result["failed"] += 1

    def _ensure_remote_dir(self, ftp: ftplib.FTP, remote_dir: str):
        rd = self._norm(remote_dir)
        if rd == "/":
            return
        parts = rd.strip("/").split("/")
        ftp.cwd("/")
        for p in parts:
            try:
                ftp.cwd(p)
            except ftplib.error_perm:
                ftp.mkd(p)
                ftp.cwd(p)


def open_remote(mall_id: str):
    """protocol 에 따라 SFTP 또는 FTP 클라이언트를 연다."""
    cfg = load_sftp_config(mall_id)
    if cfg.get("protocol", "sftp").lower() == "ftp":
        return Cafe24FTP(mall_id)
    from backends.cafe24_sftp import Cafe24SFTP  # noqa: WPS433

    return Cafe24SFTP(mall_id)
