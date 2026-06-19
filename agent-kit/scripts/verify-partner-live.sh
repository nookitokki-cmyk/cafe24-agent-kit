#!/usr/bin/env bash
# Partner sample mall — web FTP live probe (credentials via env, never commit secrets)
# Usage:
#   PARTNER_MALL_ID=ecudemo400786 PARTNER_FTP_PASS='***' bash agent-kit/scripts/verify-partner-live.sh
# Optional: PARTNER_FTP_HOST, PARTNER_FTP_PORT (default port 21), PARTNER_FTP_USER
set -euo pipefail

MALL="${PARTNER_MALL_ID:?Set PARTNER_MALL_ID}"
HOST="${PARTNER_FTP_HOST:-${MALL}.ftp.cafe24.com}"
PORT="${PARTNER_FTP_PORT:-21}"
USER="${PARTNER_FTP_USER:-$MALL}"
PASS="${PARTNER_FTP_PASS:?Set PARTNER_FTP_PASS}"

python << PY
import ftplib, os, sys
host, port, user, pw = ${HOST@Q}, int(${PORT@Q}), ${USER@Q}, ${PASS@Q}
ftp = ftplib.FTP()
ftp.connect(host, port, timeout=25)
ftp.login(user, pw)
root = sorted(ftp.nlst())
print(f"OK FTP {user}@{host}:{port}")
print("ROOT:", root)
for sub in ("sde_design", "web"):
    if sub in root:
        ftp.cwd("/" + sub)
        print(f"/{sub}:", sorted(ftp.nlst())[:20])
        ftp.cwd("/")
for bad in ("skin1", "skin2", "base"):
    try:
        ftp.cwd("/" + bad)
        print(f"WARN: /{bad} exists at root (unusual for fresh partner sample)")
        ftp.cwd("/")
    except Exception:
        print(f"OK: /{bad} not at root")
ftp.quit()
print("PASS: partner FTP probe")
PY
