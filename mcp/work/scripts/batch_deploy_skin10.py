#!/usr/bin/env python3
"""Batch SFTP deploy nookitokki002 design-v1/deploy → /skin10."""
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
MANIFEST = MCP_ROOT / "work" / "clients" / MALL / "design-v1" / "DEPLOY-MANIFEST.txt"
TS = datetime.now().strftime("%Y%m%d-%H%M%S")


def load_manifest() -> list[str]:
    paths: list[str] = []
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        paths.append(line.replace("\\", "/"))
    return paths


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
    files = load_manifest()
    uploaded = 0
    failed: list[str] = []
    backup_path = None

    with Cafe24SFTP(MALL) as sftp:
        backup_path = retry(lambda: sftp.backup(REMOTE_SKIN))
        print(f"backup: {backup_path}")

        for rel in files:
            local = DEPLOY / rel
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

    print(f"\nTS={TS} uploaded={uploaded} failed={len(failed)} backup={backup_path}")
    if failed:
        for f in failed:
            print(f"  - {f}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
