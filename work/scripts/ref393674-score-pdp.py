#!/usr/bin/env python3
"""ref393674 PDP 자기검증 — PASS = 100 only."""
from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass, field

from playwright.sync_api import sync_playwright

from score_mall import parse_mall_config

PASS = 100
REF_PATH = "/product/sample-product-01/11/category/24/display/1/"
TGT_PATH = "/product/샘플상품-2/10/category/24/display/1/"


@dataclass
class Check:
    id: str
    label: str
    max_pts: int
    pts: int = 0
    ref: str = ""
    tgt: str = ""
    note: str = ""


@dataclass
class Report:
    viewport: str
    checks: list[Check] = field(default_factory=list)

    @property
    def score(self) -> int:
        return sum(c.pts for c in self.checks)

    @property
    def max_score(self) -> int:
        return sum(c.max_pts for c in self.checks)


def near(a, b, tol):
    if a is None or b is None:
        return False
    return abs(float(a) - float(b)) <= tol


def measure(page, url):
    page.goto(url, wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(2000)
    return page.evaluate(
        """() => {
        const cs = (el) => el ? getComputedStyle(el) : null;
        const rect = (el) => el ? el.getBoundingClientRect() : null;
        const container = document.querySelector('#container');
        const detail = document.querySelector('.xans-product-detail, [module="product_detail"]');
        const area = document.querySelector('.detailArea');
        const img = document.querySelector('.imgArea');
        const info = document.querySelector('.infoArea');
        const path = document.querySelector('.path, .section.path');
        const btn = document.querySelector('.xans-product-action .btnSubmit, .btnSubmit');
        const h1 = document.querySelector('.headingArea h1, .infoArea h1');
        return {
            bodyClass: document.body.className,
            hasPdp: document.body.classList.contains('ref393674-sub-pdp'),
            hasLayout: document.body.classList.contains('layout'),
            containerW: rect(container)?.width,
            containerPad: cs(container)?.padding,
            detailW: rect(detail)?.width,
            areaDisplay: cs(area)?.display,
            areaW: rect(area)?.width,
            imgW: rect(img)?.width,
            infoW: rect(info)?.width,
            infoPos: cs(info)?.position,
            pathDisplay: path ? cs(path).display : null,
            pathH: rect(path)?.height ?? 0,
            btnBg: btn ? cs(btn).backgroundColor : null,
            h1Size: h1 ? cs(h1).fontSize : null,
            h1Family: h1 ? cs(h1).fontFamily : null,
        };
    }"""
    )


def score_pc(ref, tgt) -> Report:
    r = Report(viewport="PC 1440")
    c: list[Check] = []

    def add(cid, label, pts, rv, tv, ok, note=""):
        c.append(Check(cid, label, pts, pts if ok else 0, str(rv), str(tv), "PASS" if ok else note or "FAIL"))

    add("S1", "layout + ref393674-sub-pdp", 10, ref.get("hasLayout"), tgt.get("hasPdp"),
        tgt.get("hasLayout") and tgt.get("hasPdp"))
    add("S2", "container padding 20/20/100", 15, ref.get("containerPad"), tgt.get("containerPad"),
        tgt.get("containerPad") == "20px 20px 100px")
    add("S3", "container width ≈1440", 10, round(ref.get("containerW") or 0), round(tgt.get("containerW") or 0),
        near(tgt.get("containerW"), 1440, 40))
    add("S4", "path 숨김", 10, ref.get("pathDisplay"), tgt.get("pathDisplay"),
        tgt.get("pathDisplay") == "none" or (tgt.get("pathH") or 0) < 5)
    add("L1", "detailArea flex 2열", 15, ref.get("areaDisplay"), tgt.get("areaDisplay"),
        tgt.get("areaDisplay") == "flex" and (tgt.get("imgW") or 0) > 300 and (tgt.get("infoW") or 0) > 300)
    add("L2", "infoArea sticky", 10, ref.get("infoPos"), tgt.get("infoPos"),
        tgt.get("infoPos") == "sticky")
    add("L3", "detail 영역 풀폭(≥1200)", 10, round(ref.get("areaW") or 0), round(tgt.get("areaW") or 0),
        (tgt.get("areaW") or 0) >= 1200)
    btn_ok = (
        tgt.get("btnBg") in ("rgb(0, 0, 0)", "rgb(34, 34, 34)", "#000", "#222")
        or (tgt.get("btnBg") or "").startswith("rgb(0")
        or "0, 0, 0" in (tgt.get("btnBg") or "")
    )
    add("L4", "CTA btnSubmit 다크", 10, ref.get("btnBg"), tgt.get("btnBg"), btn_ok)
    add("T1", "h1 display font", 10, ref.get("h1Family"), tgt.get("h1Family"),
        "Bricolage" in (tgt.get("h1Family") or "") or "bricolage" in (tgt.get("h1Family") or "").lower())

    r.checks = c
    return r


def score_mo(tgt) -> Report:
    r = Report(viewport="MO 390")
    ok = (tgt.get("containerW") or 0) >= 360
    r.checks = [Check("M1", "container 풀폭 MO", 10, 10 if ok else 0, "390", str(round(tgt.get("containerW") or 0)),
                  "PASS" if ok else "FAIL")]
    return r


def main():
    cfg = parse_mall_config()
    ref_url = cfg.url(REF_PATH, target=False)
    tgt_url = cfg.url(TGT_PATH)

    out = {"pass_threshold": PASS, "mall_id": cfg.mall_id, "ref_url": ref_url, "tgt_url": tgt_url, "reports": []}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        pc_page = browser.new_page(viewport={"width": 1440, "height": 900})
        ref = measure(pc_page, ref_url)
        tgt = measure(pc_page, tgt_url)
        pc = score_pc(ref, tgt)
        out["reports"].append({"viewport": pc.viewport, "score": pc.score, "max": pc.max_score,
                               "checks": [asdict(x) for x in pc.checks], "ref": ref, "tgt": tgt})
        mo_page = browser.new_page(viewport={"width": 390, "height": 844}, is_mobile=True)
        tgt_mo = measure(mo_page, tgt_url)
        mo = score_mo(tgt_mo)
        out["reports"].append({"viewport": mo.viewport, "score": mo.score, "max": mo.max_score,
                               "checks": [asdict(x) for x in mo.checks], "tgt": tgt_mo})
        browser.close()

    s = sum(r["score"] for r in out["reports"])
    m = sum(r["max"] for r in out["reports"])
    out["total_score"] = round(s / m * 100)
    out["pass"] = out["total_score"] >= PASS
    print(json.dumps(out, ensure_ascii=False, indent=2))
    sys.exit(0 if out["pass"] else 1)


if __name__ == "__main__":
    main()
