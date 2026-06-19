#!/usr/bin/env python3
"""Upload nookitokki002 design-v1 main-polish package to SFTP /skin10."""
from __future__ import annotations

import sys
import time
from datetime import datetime
from pathlib import Path

MCP_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(MCP_ROOT))

from backends.cafe24_sftp import Cafe24SFTP  # noqa: E402

MALL = "nookitokki002"
REMOTE_SKIN = "/skin10"
DEPLOY = MCP_ROOT / "work" / "clients" / MALL / "design-v1" / "deploy"
TS = datetime.now().strftime("%Y%m%d-%H%M%S")

UPLOADS = [
    "index.html",
    "layout/basic/layout.html",
    "_nk/css/custom.css",
    "_nk/css/main.css",
    "_nk/css/product-cards.css",
    "_nk/css/mainBnr.css",
    "_nk/css/bnrArea1.css",
    "_nk/css/bnrArea2.css",
    "_nk/css/bnrArea3.css",
    "_nk/css/prdArea1.css",
    "_nk/css/prdArea2.css",
    "_nk/css/vodArea1.css",
    "_nk/css/rvArea.css",
    "_nk/css/bbsArea1.css",
    "_nk/css/insta.css",
    "_nk/css/header.css",
    "_nk/css/footer.css",
    "_nk/inc/prd.html",
    "_nk/inc/prdArea1.html",
    "_nk/inc/prdArea2.html",
    "_nk/inc/rvArea.html",
    "_nk/inc/bbsArea1.html",
    "_nk/inc/bnrArea2.html",
    "_nk/inc/insta.html",
    "layout/basic/css/custom.css",
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
    backup_path = None

    with Cafe24SFTP(MALL) as sftp:
        backup_path = retry(lambda: sftp.backup(REMOTE_SKIN))
        print(f"backup: {backup_path}")

        for rel in UPLOADS:
            local = DEPLOY / rel.replace("/", "\\") if "\\" in str(DEPLOY) else DEPLOY / rel
            if not local.exists():
                failed.append(f"{rel} (missing local)")
                continue
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

    print(f"\nTS={TS} uploaded={uploaded} failed={len(failed)}")
    if failed:
        for f in failed:
            print(f"  - {f}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
