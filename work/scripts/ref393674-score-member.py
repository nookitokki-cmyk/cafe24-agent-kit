#!/usr/bin/env python3
"""ref393674 회원 로그인 자기검증 — PASS = 100 only."""
import json
import sys
from dataclasses import asdict, dataclass

from playwright.sync_api import sync_playwright

from score_mall import parse_mall_config

PASS = 100
LOGIN_PATH = "/member/login.html"


@dataclass
class Check:
    id: str
    label: str
    max_pts: int
    pts: int = 0
    ref: str = ""
    tgt: str = ""
    note: str = ""


def measure(page, url):
    page.goto(url, wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(1500)
    return page.evaluate(
        """() => {
        const cs = (el) => el ? getComputedStyle(el) : null;
        const r = (el) => el ? el.getBoundingClientRect() : null;
        const c = document.querySelector('#container');
        const login = document.querySelector('[module="member_login"], .xans-member-login');
        const btn = document.querySelector('.xans-member-login .btnSubmit, [module="member_login"] .btnSubmit');
        const title = document.querySelector('.titleArea h2');
        return {
            narrow: document.body.classList.contains('ref393674-sub-narrow'),
            layout: document.body.classList.contains('layout'),
            containerW: r(c)?.width,
            pad: cs(c)?.padding,
            loginW: login ? r(login).width : null,
            loginMaxW: login ? cs(login).maxWidth : null,
            btnBg: btn ? cs(btn).backgroundColor : null,
            btnW: btn ? r(btn).width : null,
            titleDisplay: title ? cs(title.parentElement).display : null,
            titleText: title ? title.textContent.trim() : null,
        };
    }"""
    )


def main():
    cfg = parse_mall_config()
    ref_url = cfg.url(LOGIN_PATH, target=False)
    tgt_url = cfg.url(LOGIN_PATH)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        pc = browser.new_page(viewport={"width": 1440, "height": 900})
        ref, tgt = measure(pc, ref_url), measure(pc, tgt_url)
        mo = browser.new_page(viewport={"width": 390, "height": 844}, is_mobile=True)
        tgt_mo = measure(mo, tgt_url)
        browser.close()

    checks = []

    def add(cid, label, pts, ok, rv, tv, note=""):
        checks.append(
            Check(cid, label, pts, pts if ok else 0, str(rv), str(tv), note or ("PASS" if ok else "FAIL"))
        )

    add("S1", "body.layout", 10, tgt["layout"], ref.get("layout"), tgt["layout"])
    add("L1", "container 1200px", 25, abs((tgt["containerW"] or 0) - 1200) < 30, ref["containerW"], tgt["containerW"])
    add("L2", "padding 50/20/100", 20, tgt["pad"] == "50px 20px 100px", ref["pad"], tgt["pad"])
    add("L3", "login form 400px", 20, abs((tgt["loginW"] or 0) - 400) < 20, ref["loginW"], tgt["loginW"])
    add("L4", "CTA 다크 #111", 15, "17, 17, 17" in (tgt.get("btnBg") or ""), ref.get("btnBg"), tgt.get("btnBg"))
    add("L5", "title 로그인 노출", 5, tgt.get("titleText") == "로그인" and tgt.get("titleDisplay") == "block",
        ref.get("titleText"), tgt.get("titleText"))
    add("M1", "MO container", 5, (tgt_mo["containerW"] or 0) >= 330, 390, tgt_mo["containerW"])

    score = sum(c.pts for c in checks)
    total = round(score / 100 * 100)
    out = {
        "total_score": total,
        "pass": total >= PASS,
        "mall_id": cfg.mall_id,
        "ref_url": ref_url,
        "tgt_url": tgt_url,
        "checks": [asdict(c) for c in checks],
        "ref": ref,
        "tgt": tgt,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    sys.exit(0 if out["pass"] else 1)


if __name__ == "__main__":
    main()
