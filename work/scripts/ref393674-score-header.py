#!/usr/bin/env python3
"""ref393674 헤더 Info 드롭다운·검색 패널 자기검증 — PASS = 100 only."""
import json
import sys
from dataclasses import asdict, dataclass

from playwright.sync_api import sync_playwright

from score_mall import parse_mall_config

PASS = 100
PLP_PATH = "/product/list.html?cate_no=24"


@dataclass
class Check:
    id: str
    label: str
    max_pts: int
    pts: int = 0
    ref: str = ""
    tgt: str = ""
    note: str = ""


def measure(page, url, hover: bool):
    page.goto(url, wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(1000)
    if hover:
        page.evaluate(
            """() => {
            document.querySelectorAll('#header.a-header .menu-main > ul > li').forEach(el => {
                const a = el.querySelector('a');
                if (a && a.textContent.trim() === 'Info') el.classList.add('force-hover');
            });
        }"""
        )
        page.add_style_tag(
            content="#header.a-header .menu-main li.force-hover .sub { display: block !important; }"
        )
        page.wait_for_timeout(200)
    sub = page.evaluate(
        """() => {
        const cs = (el) => el ? getComputedStyle(el) : null;
        const r = (el) => el ? el.getBoundingClientRect() : null;
        const sub = document.querySelector('#header.a-header .menu-main .sub');
        return {
            subDisplay: sub ? cs(sub).display : null,
            subTop: sub ? cs(sub).top : null,
            subH: sub ? r(sub).height : null,
            subItemCount: sub ? sub.querySelectorAll('li').length : 0,
        };
    }"""
    )
    page.evaluate("() => { document.body.classList.add('search-active'); }")
    page.wait_for_timeout(200)
    search = page.evaluate(
        """() => {
        const cs = (el) => el ? getComputedStyle(el) : null;
        const r = (el) => el ? el.getBoundingClientRect() : null;
        const panel = document.querySelector('#header.a-header .a-search');
        const mod = document.querySelector('#header.a-header .xans-layout-searchheader');
        const fieldset = panel ? panel.querySelector('fieldset') : null;
        return {
            searchActive: document.body.classList.contains('search-active'),
            panelDisplay: panel ? cs(panel).display : null,
            modDisplay: mod ? cs(mod).display : null,
            fieldsetW: fieldset ? r(fieldset).width : null,
            fieldsetBorder: fieldset ? cs(fieldset).borderBottomWidth : null,
        };
    }"""
    )
    return {**sub, **search}


def main():
    cfg = parse_mall_config()
    ref_url = cfg.url(PLP_PATH, target=False)
    tgt_url = cfg.url(PLP_PATH)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        pc = browser.new_page(viewport={"width": 1440, "height": 900})
        ref_pc = measure(pc, ref_url, True)
        tgt_pc = measure(pc, tgt_url, True)
        mo = browser.new_page(viewport={"width": 390, "height": 844}, is_mobile=True)
        ref_mo = measure(mo, ref_url, False)
        tgt_mo = measure(mo, tgt_url, False)
        browser.close()

    checks = []

    def add(cid, label, pts, ok, rv, tv):
        checks.append(Check(cid, label, pts, pts if ok else 0, str(rv), str(tv), "PASS" if ok else "FAIL"))

    add("D1", "PC Info sub 노출", 15, tgt_pc["subDisplay"] == "block" and (tgt_pc["subH"] or 0) > 50,
        ref_pc.get("subH"), tgt_pc.get("subH"))
    add("D2", "PC sub top 50px", 10, tgt_pc.get("subTop") == "50px", ref_pc.get("subTop"), tgt_pc.get("subTop"))
    add("D3", "PC sub 항목 6+", 10, (tgt_pc.get("subItemCount") or 0) >= 6, ref_pc.get("subItemCount"), tgt_pc.get("subItemCount"))
    add("S1", "PC search panel block", 15, tgt_pc.get("panelDisplay") == "block", ref_pc.get("panelDisplay"), tgt_pc.get("panelDisplay"))
    add("S2", "PC search module visible", 15, tgt_pc.get("modDisplay") == "block", ref_pc.get("modDisplay"), tgt_pc.get("modDisplay"))
    add("S3", "PC fieldset ~230px", 15, 200 <= (tgt_pc.get("fieldsetW") or 0) <= 260,
        ref_pc.get("fieldsetW"), tgt_pc.get("fieldsetW"))
    add("S4", "PC fieldset border-bottom", 10, tgt_pc.get("fieldsetBorder") == "1px",
        ref_pc.get("fieldsetBorder"), tgt_pc.get("fieldsetBorder"))
    add("M1", "MO search 숨김(ref 동일)", 10, tgt_mo.get("panelDisplay") == "none", ref_mo.get("panelDisplay"), tgt_mo.get("panelDisplay"))

    score = sum(c.pts for c in checks)
    total = round(score / 100 * 100)
    out = {
        "total_score": total,
        "pass": total >= PASS,
        "mall_id": cfg.mall_id,
        "ref_url": ref_url,
        "tgt_url": tgt_url,
        "checks": [asdict(c) for c in checks],
        "ref_pc": ref_pc,
        "tgt_pc": tgt_pc,
        "ref_mo": ref_mo,
        "tgt_mo": tgt_mo,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    sys.exit(0 if out["pass"] else 1)


if __name__ == "__main__":
    main()
