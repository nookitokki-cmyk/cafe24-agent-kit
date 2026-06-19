#!/usr/bin/env python3
"""ref393674 장바구니 자기검증 — PASS = 100 only."""
import json, sys
from dataclasses import asdict, dataclass, field
from playwright.sync_api import sync_playwright

from score_mall import parse_mall_config

PASS = 100
BASKET_PATH = "/order/basket.html"
PDP_TGT_PATH = "/product/샘플상품-2/10/category/24/display/1/"

@dataclass
class Check:
    id: str; label: str; max_pts: int; pts: int = 0
    ref: str = ""; tgt: str = ""; note: str = ""

def measure(page, url):
    page.goto(url, wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(1500)
    return page.evaluate("""() => {
        const c = document.querySelector('#container');
        const contents = document.querySelector('#contents');
        const cs = (el) => el ? getComputedStyle(el) : null;
        const r = (el) => el ? el.getBoundingClientRect() : null;
        const thead = document.querySelector('.xans-order-basketpackage thead');
        const btn = document.querySelector('.xans-order-totalbutton .btnSubmit, .btnSubmit');
        const sumPrice = document.querySelector('.xans-order-basketpackage .sumPrice');
        const payTotal = document.querySelector('.xans-order-basketpackage .totalSummary .total');
        const orderFix = document.querySelector('#orderFixArea');
        const vw = document.documentElement.clientWidth;
        const sumLines = sumPrice ? sumPrice.innerText.trim().split('\\n').filter(Boolean).length : 0;
        const totalLines = payTotal ? payTotal.innerText.trim().split('\\n').filter(Boolean).length : 0;
        const strong = sumPrice ? sumPrice.querySelector('strong') : null;
        const won = sumPrice ? sumPrice.querySelector('.notranslate, span:not(.label)') : null;
        const priceSameLine = sumPrice && strong && won ? Math.abs(r(strong).top - r(won).top) <= 4 : false;
        const payEl = document.querySelector('.xans-order-basketpackage .totalSummary .total .paymentPrice');
        const titleEl = document.querySelector('.xans-order-basketpackage .totalSummary .total .title');
        const totalSameLine = payEl && titleEl ? Math.abs(r(payEl).top - r(titleEl).top) <= 4 : false;
        return {
            narrow: document.body.classList.contains('ref393674-sub-narrow'),
            layout: document.body.classList.contains('layout'),
            containerW: r(c)?.width,
            contentsW: r(contents)?.width,
            viewportW: vw,
            maxW: cs(c)?.maxWidth,
            pad: cs(c)?.padding,
            hasThead: !!thead,
            theadDisplay: thead ? cs(thead).display : null,
            btnBg: btn ? cs(btn).backgroundColor : null,
            hasItem: !!document.querySelector('.xans-order-basketpackage .ec-base-prdInfo') || !!sumPrice,
            sumPriceLines: sumLines,
            sumPriceWS: sumPrice ? cs(sumPrice).whiteSpace : null,
            totalLines: totalLines,
            orderFixVisible: orderFix ? cs(orderFix).display !== 'none' && r(orderFix).height > 0 : false,
            priceSameLine: priceSameLine,
            totalSameLine: totalSameLine,
        };
    }""")

def main():
    cfg = parse_mall_config()
    ref_url = cfg.url(BASKET_PATH, target=False)
    tgt_url = cfg.url(BASKET_PATH)
    pdp_url = cfg.url(PDP_TGT_PATH)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        pc = browser.new_page(viewport={"width": 1440, "height": 900})
        ref, tgt = measure(pc, ref_url), measure(pc, tgt_url)
        mo = browser.new_page(viewport={"width": 390, "height": 844}, is_mobile=True)
        mo.goto(pdp_url, wait_until="networkidle", timeout=60000)
        mo.wait_for_timeout(2000)
        for sel in (".btnSubmit.sizeL", ".xans-product-action .btnSubmit", "a.btnSubmit", "#actionCart"):
            cart_btn = mo.query_selector(sel)
            if cart_btn and cart_btn.is_visible():
                cart_btn.click()
                mo.wait_for_timeout(3500)
                break
        tgt_mo = measure(mo, tgt_url)
        browser.close()

    checks = []
    def add(cid, label, pts, ok, rv, tv):
        checks.append(Check(cid, label, pts, pts if ok else 0, str(rv), str(tv), "PASS" if ok else "FAIL"))

    add("S1", "ref393674-sub-narrow", 15, tgt["narrow"], ref.get("narrow"), tgt["narrow"])
    add("L1", "container 1200px", 25, abs((tgt["containerW"] or 0) - 1200) < 30, ref["containerW"], tgt["containerW"])
    add("L2", "padding 50/20/100", 20, tgt["pad"] == "50px 20px 100px", ref["pad"], tgt["pad"])
    add("L3", "thead 숨김 또는 빈 장바구니", 15,
        tgt["theadDisplay"] == "none" or not tgt["hasThead"],
        ref.get("theadDisplay"), tgt.get("hasThead"))
    add("L4", "CTA 다크", 15, "0, 0, 0" in (tgt.get("btnBg") or "") or "17, 17, 17" in (tgt.get("btnBg") or "") or tgt.get("btnBg") == "rgb(34, 34, 34)", ref.get("btnBg"), tgt.get("btnBg"))
    add("M1", "MO container", 3, (tgt_mo["containerW"] or 0) >= 360, 390, tgt_mo["containerW"])
    contents_ok = (tgt_mo["contentsW"] or 0) >= (tgt_mo["viewportW"] or 390) - 34
    add("M2", "MO #contents full (not 92%)", 3, contents_ok, tgt_mo["viewportW"], tgt_mo["contentsW"])
    wrap_ok = tgt_mo["hasItem"] and tgt_mo.get("priceSameLine") and tgt_mo.get("totalSameLine")
    add("M3", "MO price same line (strong+won, total)", 2, wrap_ok, tgt_mo.get("priceSameLine"), tgt_mo.get("totalSameLine"))
    add("M4", "MO orderFix hidden", 2, not tgt_mo.get("orderFixVisible"), False, tgt_mo.get("orderFixVisible"))

    score = sum(c.pts for c in checks)
    total = round(score / 100 * 100)
    out = {
        "total_score": total,
        "pass": total >= PASS,
        "mall_id": cfg.mall_id,
        "ref_url": ref_url,
        "tgt_url": tgt_url,
        "pdp_url": pdp_url,
        "checks": [asdict(c) for c in checks],
        "ref": ref,
        "tgt": tgt,
        "tgt_mo": tgt_mo,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    sys.exit(0 if out["pass"] else 1)

if __name__ == "__main__":
    main()
