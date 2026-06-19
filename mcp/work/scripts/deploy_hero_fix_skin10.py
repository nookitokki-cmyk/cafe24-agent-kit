#!/usr/bin/env python3
"""US-004 hero fix — nookitokki002 skin10 mainBnr.css + main.css (rebuild4hero)."""
from __future__ import annotations

import sys
import time
from pathlib import Path

MCP_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(MCP_ROOT))

from backends.cafe24_sftp import Cafe24SFTP  # noqa: E402

MALL = "nookitokki002"
DEPLOY = MCP_ROOT / "work" / "deploy-rebuild4hero"
FILES = [
    ("mainBnr.css", "/skin10/_nk/css/mainBnr.css"),
    ("main.css", "/skin10/_nk/css/main.css"),
]


def retry(fn, attempts=8, delay=5):
    last = None
    for i in range(attempts):
        try:
            return fn()
        except Exception as e:
            last = e
            print(f"  retry {i + 1}/{attempts}: {e}")
            time.sleep(delay * (i + 1))
    raise last


def main() -> int:
    uploaded = 0
    failed: list[str] = []

    with Cafe24SFTP(MALL) as sftp:
        for local_name, remote in FILES:
            local = DEPLOY / local_name
            if not local.is_file():
                print(f"MISSING {local}")
                return 1
            try:
                bak = retry(lambda r=remote: sftp.backup(r))
                print(f"backup {remote} -> {bak}")
                retry(
                    lambda lp=local, rp=remote: sftp.upload(
                        local_path=str(lp), remote_path=rp, auto_backup=False
                    )
                )
                uploaded += 1
                print(f"  OK {remote}")
            except Exception as e:
                failed.append(f"{remote}: {e}")
                print(f"  FAIL {remote}: {e}")

    print(f"\nrebuild4hero uploaded={uploaded} failed={len(failed)}")
    print("verify: https://nookitokki002.cafe24.com/?v=rebuild4hero")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
