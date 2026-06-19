#!/usr/bin/env python3
"""Phase C full EZ strip runner for nookitokki002 skin10."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

MCP_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(MCP_ROOT))

from backends.cafe24_sftp import Cafe24SFTP  # noqa: E402

MALL = "nookitokki002"
REMOTE_SKIN = "/skin10"
TS = datetime.now().strftime("%Y%m%d-%H%M%S")
WORK_ROOT = MCP_ROOT / "work" / "clients" / MALL / f"ez-strip-{TS.split('-')[0]}"
SRC_DIR = WORK_ROOT / "skin10-src"
STRIPPED_DIR = WORK_ROOT / "skin10-stripped"
STRIP_SCRIPT = MCP_ROOT / "work" / "scripts" / "strip_ez.py"
REPORT_PATH = WORK_ROOT / "strip-report.json"


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


def count_ez_in_dir(root: Path) -> tuple[int, int]:
    html_files = list(root.rglob("*.html"))
    with_ez = 0
    total_hits = 0
    for fp in html_files:
        try:
            text = fp.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        hits = text.count("data-ez") + text.lower().count("<ez-prop")
        if hits:
            with_ez += 1
            total_hits += hits
    return len(html_files), with_ez


def main() -> int:
    WORK_ROOT.mkdir(parents=True, exist_ok=True)

    print(f"=== 1) Server backup {REMOTE_SKIN} ===")
    with Cafe24SFTP(MALL) as sftp:
        backup_path = retry(lambda: sftp.backup(REMOTE_SKIN))
    print(f"Backup: {backup_path}")

    print(f"=== 2) Download {REMOTE_SKIN} -> {SRC_DIR} ===")
    if SRC_DIR.exists():
        shutil.rmtree(SRC_DIR)
    SRC_DIR.mkdir(parents=True)

    def do_download():
        with Cafe24SFTP(MALL) as sftp:
            return sftp.download(REMOTE_SKIN, str(SRC_DIR))

    dl = retry(do_download)
    print(f"Downloaded: {dl['files']} files, failed={dl['failed']}")

    html_before, ez_files_before = count_ez_in_dir(SRC_DIR)
    print(f"HTML files: {html_before}, with EZ markup: {ez_files_before}")

    print(f"=== 3) Copy to stripped workspace ===")
    if STRIPPED_DIR.exists():
        shutil.rmtree(STRIPPED_DIR)
    shutil.copytree(SRC_DIR, STRIPPED_DIR)

    print("=== 4) strip_ez preview ===")
    preview = subprocess.run(
        [sys.executable, str(STRIP_SCRIPT), str(STRIPPED_DIR), "--remove-runtime"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    print(preview.stdout)
    if preview.returncode != 0:
        print(preview.stderr, file=sys.stderr)
        return preview.returncode

    print("=== 5) strip_ez --write ===")
    write = subprocess.run(
        [sys.executable, str(STRIP_SCRIPT), str(STRIPPED_DIR), "--write", "--remove-runtime"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    print(write.stdout)
    if write.returncode != 0:
        print(write.stderr, file=sys.stderr)
        return write.returncode

    _, ez_files_after = count_ez_in_dir(STRIPPED_DIR)
    # residual grep (excluding skip files)
    residual = []
    skip = {"ez/ez-module.html", "smart-banner/init/ez-initialize.html"}
    for fp in STRIPPED_DIR.rglob("*.html"):
        rel = fp.relative_to(STRIPPED_DIR).as_posix()
        if rel in skip:
            continue
        text = fp.read_text(encoding="utf-8", errors="replace")
        if "data-ez" in text or "<ez-prop" in text.lower():
            residual.append(rel)

    changed_files = []
    for fp in STRIPPED_DIR.rglob("*.html"):
        rel = fp.relative_to(STRIPPED_DIR).as_posix()
        orig = SRC_DIR / rel
        if not orig.exists():
            continue
        if fp.read_bytes() != orig.read_bytes():
            changed_files.append(rel)

    # sample before/after
    samples = []
    for rel in ["index.html", "layout/basic/header.html", "layout/basic/layout.html", "product/list.html"]:
        if (SRC_DIR / rel).exists():
            before = (SRC_DIR / rel).read_text(encoding="utf-8", errors="replace")[:400]
            after = (STRIPPED_DIR / rel).read_text(encoding="utf-8", errors="replace")[:400]
            samples.append({"file": rel, "before_snippet": before, "after_snippet": after})

    print(f"=== 6) Upload {len(changed_files)} changed HTML files ===")
    uploaded = 0
    failed = 0
    upload_backup = None
    with Cafe24SFTP(MALL) as sftp:
        for rel in sorted(changed_files):
            local = STRIPPED_DIR / rel
            remote = f"{REMOTE_SKIN}/{rel.replace(os.sep, '/')}"
            try:
                r = retry(lambda lp=local, rp=remote: sftp.upload(local_path=str(lp), remote_path=rp, auto_backup=False))
                uploaded += r["uploaded"]
                failed += r["failed"]
            except Exception as e:
                print(f"FAIL {rel}: {e}")
                failed += 1

    report = {
        "mall": MALL,
        "remote_skin": REMOTE_SKIN,
        "timestamp": TS,
        "pre_strip_backup": backup_path,
        "work_dir": str(WORK_ROOT),
        "html_total": html_before,
        "html_with_ez_before": ez_files_before,
        "html_with_ez_after": ez_files_after,
        "files_changed": len(changed_files),
        "changed_file_list": changed_files,
        "residual_ez_files": residual,
        "uploaded": uploaded,
        "upload_failed": failed,
        "samples": samples,
    }
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"\nReport saved: {REPORT_PATH}")
    return 0 if failed == 0 and not residual else 1


if __name__ == "__main__":
    raise SystemExit(main())
