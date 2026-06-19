#!/usr/bin/env python3
"""ref393674 전역 ec-base-paginate 자기검증 — board @390/1440, PASS = 100 only."""
import json
import sys
from dataclasses import asdict, dataclass

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print(json.dumps({"error": "playwright not installed", "total_score": 0, "pass": False}))
    sys.exit(1)

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


def measure(page, url: str) -> dict:
    page.goto(url, wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(1500)
    return page.evaluate(
        """() => {
        const pag = document.querySelector('.ec-base-paginate.typeList:not(.hide)');
        if (!pag) return { found: false };
        const cs = (el) => el ? getComputedStyle(el) : null;
        const r = (el) => el ? el.getBoundingClientRect() : null;
        const prev = pag.querySelector(':scope > a');
        const next = pag.querySelector(':scope > a:last-of-type');
        const ol = pag.querySelector('ol');
        const li = ol ? ol.querySelector('li') : null;
        const num = li ? li.querySelector('a') : null;
        const allA = [...pag.querySelectorAll(':scope > a')];
        const kids = [...pag.children];
        const cy = (el) => {
            const rect = r(el);
            return Math.round(rect.y + rect.height / 2);
        };
        const kidCys = kids.map(cy);
        const cySpread = kidCys.length ? Math.max(...kidCys) - Math.min(...kidCys) : 99;
        const aYs = allA.map(a => Math.round(r(a).y));
        const olY = ol ? Math.round(r(ol).y) : null;
        const stacked = aYs.length >= 2 && new Set(aYs).size > 1;
        const olInline = ol && ['inline-flex', 'inline-block', 'flex'].includes(cs(ol).display);
        const prevFs = prev ? parseFloat(cs(prev).fontSize) : null;
        const numBorder = num ? parseFloat(cs(num).borderTopWidth) : null;
        return {
            found: true,
            textAlign: cs(pag).textAlign,
            marginLeft: cs(pag).marginLeft,
            marginRight: cs(pag).marginRight,
            prevFontSize: prevFs,
            prevColor: prev ? cs(prev).color : null,
            prevText: prev ? prev.textContent.trim().slice(0, 12) : null,
            olDisplay: ol ? cs(ol).display : null,
            olListStyle: ol ? cs(ol).listStyleType : null,
            liDisplay: li ? cs(li).display : null,
            numBorder,
            thisUnderline: num && num.classList.contains('this')
                ? cs(num).textDecorationLine : null,
            stacked,
            olInline,
            aligned: cySpread <= 2,
            cySpread,
            pagDisplay: cs(pag).display,
        };
    }"""
    )


def main():
    cfg = parse_mall_config()
    tgt_board = cfg.url(BOARD_PATH)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        pc = browser.new_page(viewport={"width": 1440, "height": 900})
        mo = browser.new_page(viewport={"width": 390, "height": 844}, is_mobile=True)
        tgt_pc = measure(pc, tgt_board)
        tgt_mo = measure(mo, tgt_board)
        browser.close()

    checks: list[Check] = []

    def add(cid, label, pts, ok, rv, tv, note=""):
        checks.append(
            Check(cid, label, pts, pts if ok else 0, str(rv), str(tv), "PASS" if ok else note or "FAIL")
        )

    if not tgt_pc.get("found"):
        out = {
            "total_score": 0,
            "pass": False,
            "mall_id": cfg.mall_id,
            "error": "paginate not found on board",
            "tgt_pc": tgt_pc,
            "url": tgt_board,
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        sys.exit(1)

    def is_zero(val):
        if val is None:
            return False
        try:
            return float(val) == 0
        except (TypeError, ValueError):
            return False

    add("P1", "PC prev font-size 0 (text hidden)", 20, is_zero(tgt_pc.get("prevFontSize")), "0", tgt_pc.get("prevFontSize"))
    add("P2", "PC ol inline horizontal", 15, tgt_pc.get("olInline"), "inline-flex", tgt_pc.get("olDisplay"))
    add("P3", "PC prev/next not stacked", 15, tgt_pc.get("aligned"), True, tgt_pc.get("stacked"))
    add("P4", "PC num border 0", 15, is_zero(tgt_pc.get("numBorder")), "0", tgt_pc.get("numBorder"))
    add("P5", "PC text-align center", 10, tgt_pc.get("textAlign") == "center", "center", tgt_pc.get("textAlign"))
    add("P6", "PC .section margin trap off", 10, float(tgt_pc.get("marginLeft", "0").replace("px", "") or 0) < 5,
        "~0", tgt_pc.get("marginLeft"))

    add("M1", "MO prev font-size 0", 10, is_zero(tgt_mo.get("prevFontSize")), "0", tgt_mo.get("prevFontSize"))
    add("M2", "MO aligned row", 5, tgt_mo.get("aligned"), True, tgt_mo.get("stacked"))

    score = sum(c.pts for c in checks)
    total = round(score / 100 * 100)
    out = {
        "total_score": total,
        "pass": total >= PASS,
        "mall_id": cfg.mall_id,
        "checks": [asdict(c) for c in checks],
        "tgt_pc": tgt_pc,
        "tgt_mo": tgt_mo,
        "url": tgt_board,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    sys.exit(0 if out["pass"] else 1)


if __name__ == "__main__":
    main()
