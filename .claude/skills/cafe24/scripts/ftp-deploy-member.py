# -*- coding: utf-8 -*-
import sys, ftplib, io, os

HOST = "ecudemo402307.ftp.cafe24.com"
PORT = 21
USER = "ecudemo402307"
PW = "1q2w3e4r5t!"
LOCAL = r"C:\nookitokki\cafe24-kit-작업본\agent-kit\clients\ecudemo402307\src\_nk\css\nk-member.css"
REMOTES = ["/sde_design/base/_nk/css/nk-member.css", "/sde_design/mobile/_nk/css/nk-member.css"]

def exists(ftp, path):
    d = os.path.dirname(path)
    name = os.path.basename(path)
    try:
        names = ftp.nlst(d)
        return any(os.path.basename(n) == name for n in names)
    except Exception as e:
        return False

with open(LOCAL, "rb") as f:
    data = f.read()
print("local bytes:", len(data))

ftp = ftplib.FTP()
ftp.connect(HOST, PORT, timeout=60)
ftp.login(USER, PW)
ftp.set_pasv(True)
print("connected", ftp.getwelcome())

for rp in REMOTES:
    if exists(ftp, rp):
        ftp.storbinary("STOR " + rp, io.BytesIO(data))
        # verify size
        try:
            sz = ftp.size(rp)
        except Exception:
            sz = "?"
        print("UPLOADED", rp, "size", sz)
    else:
        print("SKIP (not found)", rp)

ftp.quit()
print("done")
