#!/usr/bin/env python3
"""Emergency recovery deploy — nookitokki002 skin10 (minimal stable files)."""
from __future__ import annotations

import sys
import time
from pathlib import Path

MCP_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(MCP_ROOT))

from backends.cafe24_sftp import Cafe24SFTP  # noqa: E402

MALL = "nookitokki002"
REMOTE_SKIN = "/skin10"
DEPLOY = MCP_ROOT / "work" / "clients" / MALL / "design-v1" / "deploy"

RECOVERY_FILES = [
    "index.html",
    "layout/basic/layout.html",
    "_nk/css/main.css",
    "_nk/css/bnrArea2.css",
    "_nk/inc/bnrArea1.html",
    "_nk/inc/bnrArea2.html",
    "_nk/inc/prdTab.html",
]


def retry(fn, attempts=5, delay=3):
    last = None
    for i in range(attempts):
        try:
            return fn()
        except Exception as e:
            last = e
            if i < attempts - 1:
                time.sleep(delay * (i + 1))
    raise last


def main() -> int:
    uploaded = 0
    failed: list[str] = []

    with Cafe24SFTP(MALL) as sftp:
        backup_path = retry(lambda: sftp.backup(REMOTE_SKIN))
        print(f"backup: {backup_path}")

        for rel in RECOVERY_FILES:
            local = DEPLOY / rel
            remote = f"{REMOTE_SKIN}/{rel}"
            try:
                r = retry(
                    lambda lp=local, rp=remote: sftp.upload(
                        local_path=str(lp), remote_path=rp, auto_backup=False
                    )
                )
                uploaded += r.get("uploaded", 1)
                print(f"  OK {rel}")
            except Exception as e:
                failed.append(f"{rel}: {e}")
                print(f"  FAIL {rel}: {e}")

    print(f"\nrecovery uploaded={uploaded} failed={len(failed)} backup={backup_path}")
    if failed:
        for f in failed:
            print(f"  - {f}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
