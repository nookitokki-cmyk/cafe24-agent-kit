#!/usr/bin/env python3
"""ref393674 정적 페이지(About+Contact) 자기검증 — PASS = 100 only."""
import json
import sys
from dataclasses import asdict, dataclass

from playwright.sync_api import sync_playwright

from score_mall import parse_mall_config

PASS = 100
PAGE_PATHS = [
    ("about", "/pages/about.html"),
    ("contact", "/pages/contact.html"),
]


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
        const pageEl = document.querySelector('.ref393674-page');
        const p = document.querySelector('.ref393674-page p');
        const dl = document.querySelector('.ref393674-contact dl');
        return {
            layout: document.body.classList.contains('layout'),
            narrow: document.body.classList.contains('ref393674-sub-narrow'),
            containerW: r(c)?.width,
            pad: cs(c)?.padding,
            pageW: pageEl ? r(pageEl).width : null,
            pageMaxW: pageEl ? cs(pageEl).maxWidth : null,
            textAlign: pageEl ? cs(pageEl).textAlign : null,
            lineH: p ? cs(p).lineHeight : null,
            hasDl: !!dl,
            imgW: document.querySelector('.ref393674-page img') ? r(document.querySelector('.ref393674-page img')).width : null,
        };
    }"""
    )


def score_page(name: str, tgt: dict, tgt_mo: dict) -> list[Check]:
    checks = []
    pfx = name.upper()[:1]

    def add(cid, label, pts, ok, rv, tv):
        checks.append(Check(f"{pfx}{cid}", f"{name}: {label}", pts, pts if ok else 0, str(rv), str(tv), "PASS" if ok else "FAIL"))

    add("1", "layout + page wrapper", 10, tgt["layout"] and tgt.get("pageMaxW") == "700px", "700px", tgt.get("pageMaxW"))
    add("2", "container 1200px", 15, abs((tgt["containerW"] or 0) - 1200) < 30, 1200, tgt["containerW"])
    add("3", "padding 50/20/100", 10, tgt["pad"] == "50px 20px 100px", "50px 20px 100px", tgt["pad"])
    add("4", "text-align center", 10, tgt.get("textAlign") == "center", "center", tgt.get("textAlign"))
    if name == "about":
        add("5", "img max-width", 10, (tgt.get("imgW") or 0) >= 600, 700, tgt.get("imgW"))
        add("6", "line-height 23.4px", 5, tgt.get("lineH") in ("23.4px", "20.8px", "24px"), "23.4px", tgt.get("lineH"))
    else:
        add("5", "contact dl", 15, tgt.get("hasDl"), True, tgt.get("hasDl"))
    add("M", "MO container", 5, (tgt_mo["containerW"] or 0) >= 330, 390, tgt_mo["containerW"])
    return checks


def main():
    cfg = parse_mall_config()
    pages = [(name, cfg.url(path)) for name, path in PAGE_PATHS]

    all_checks: list[Check] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        pc = browser.new_page(viewport={"width": 1440, "height": 900})
        mo = browser.new_page(viewport={"width": 390, "height": 844}, is_mobile=True)
        for name, url in pages:
            tgt = measure(pc, url)
            tgt_mo = measure(mo, url)
            all_checks.extend(score_page(name, tgt, tgt_mo))
        browser.close()

    score = sum(c.pts for c in all_checks)
    total_max = sum(c.max_pts for c in all_checks)
    total = round(score / total_max * 100)
    out = {
        "total_score": total,
        "pass": total >= PASS,
        "mall_id": cfg.mall_id,
        "tgt_base": cfg.tgt_base,
        "pages": [{"name": name, "url": url} for name, url in pages],
        "checks": [asdict(c) for c in all_checks],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    sys.exit(0 if out["pass"] else 1)


if __name__ == "__main__":
    main()
