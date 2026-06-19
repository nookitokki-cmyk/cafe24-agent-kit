#!/usr/bin/env python3
"""ref393674 게시판(Notice free/1) 자기검증 — PASS = 100 only."""
import json
import sys
from dataclasses import asdict, dataclass

from playwright.sync_api import sync_playwright

from score_mall import parse_mall_config

PASS = 100
BOARD_PATH = "/board/free/list.html?board_no=1"


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
        const table = document.querySelector('.xans-board-listpackage .ec-base-table');
        const th = document.querySelector('.xans-board-listpackage thead th');
        const title = document.querySelector('.titleArea h2, .xans-board-title .title');
        const pag = document.querySelector('.ec-base-paginate.typeList');
        const prev = pag ? pag.querySelector(':scope > a:first-child') : null;
        const next = pag ? pag.querySelector(':scope > a:last-child') : null;
        const ol = pag ? pag.querySelector('ol') : null;
        return {
            layout: document.body.classList.contains('layout'),
            narrow: document.body.classList.contains('ref393674-sub-narrow'),
            containerW: r(c)?.width,
            pad: cs(c)?.padding,
            tableW: table ? r(table).width : null,
            tableBorderTop: table ? cs(table).borderTopWidth : null,
            thExists: !!th,
            titleText: title ? title.textContent.trim() : null,
            hasListPkg: !!document.querySelector('.xans-board-listpackage'),
            hasPaginate: !!pag,
            prevFontSize: prev ? cs(prev).fontSize : null,
            prevTextVisible: prev ? (parseFloat(cs(prev).fontSize) < 1 || cs(prev).color === 'rgba(0, 0, 0, 0)' || cs(prev).color === 'transparent') : null,
            pagDisplay: pag ? cs(pag).display : null,
            olDisplay: ol ? cs(ol).display : null,
            pagH: pag ? r(pag).height : null,
        };
    }"""
    )


def main():
    cfg = parse_mall_config()
    ref_url = cfg.url(BOARD_PATH, target=False)
    tgt_url = cfg.url(BOARD_PATH)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        pc = browser.new_page(viewport={"width": 1440, "height": 900})
        ref, tgt = measure(pc, ref_url), measure(pc, tgt_url)
        mo = browser.new_page(viewport={"width": 390, "height": 844}, is_mobile=True)
        tgt_mo = measure(mo, tgt_url)
        browser.close()

    checks = []

    def add(cid, label, pts, ok, rv, tv):
        checks.append(Check(cid, label, pts, pts if ok else 0, str(rv), str(tv), "PASS" if ok else "FAIL"))

    add("S1", "body.layout + listpackage", 15, tgt["layout"] and tgt["hasListPkg"], ref.get("layout"), tgt.get("hasListPkg"))
    add("L1", "container 1200px", 25, abs((tgt["containerW"] or 0) - 1200) < 30, ref["containerW"], tgt["containerW"])
    add("L2", "padding 50/20/100", 20, tgt["pad"] == "50px 20px 100px", ref["pad"], tgt["pad"])
    add("L3", "table 존재·폭", 20, (tgt["tableW"] or 0) > 900, ref.get("tableW"), tgt.get("tableW"))
    add("L4", "테이블 border-top", 10, tgt.get("tableBorderTop") == "1px", ref.get("tableBorderTop"), tgt.get("tableBorderTop"))
    add("P1", "페이징 존재", 5, tgt.get("hasPaginate"), ref.get("hasPaginate"), tgt.get("hasPaginate"))
    prev_ok = tgt.get("prevFontSize") == "0px" or tgt.get("prevTextVisible")
    add("P2", "이전/다음 텍스트 숨김", 15, prev_ok, ref.get("prevFontSize"), tgt.get("prevFontSize"))
    add("M1", "MO container", 5, (tgt_mo["containerW"] or 0) >= 330, 390, tgt_mo["containerW"])
    mo_prev_ok = tgt_mo.get("prevFontSize") == "0px" or tgt_mo.get("prevTextVisible")
    add("M2", "MO 페이징 숨김", 5, mo_prev_ok, tgt_mo.get("prevFontSize"), tgt_mo.get("prevFontSize"))

    score = sum(c.pts for c in checks)
    max_total = sum(c.max_pts for c in checks)
    total = round(score / max_total * 100)
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
