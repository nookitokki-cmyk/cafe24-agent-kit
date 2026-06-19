#!/usr/bin/env python3
"""ref393674 PLP 자기검증 — ref vs tgt 실측 채점 (100점 PASS only)."""
from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass, field

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print(json.dumps({"error": "playwright not installed", "score": 0}))
    sys.exit(1)

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


def near(a: float | None, b: float | None, tol: float) -> bool:
    if a is None or b is None:
        return False
    return abs(a - b) <= tol


MEASURE_JS = """() => {
    const cs = (el) => el ? getComputedStyle(el) : null;
    const rect = (el) => el ? el.getBoundingClientRect() : null;
    const container = document.querySelector('#container');
    const contents = document.querySelector('#contents');
    const prdList = document.querySelector('.prdList');
    const item = document.querySelector('.prdList .item');
    const menuPkg = document.querySelector('.xans-product-menupackage');
    const menuCat = document.querySelector('.menuCategory');
    const sortUl = document.querySelector('.sortby #type, #type');
    const sortSel = document.querySelector('#selArray');
    const count = document.querySelector('.xans-product-normalmenu .count, .product_normalmenu .count');
    const banner = document.querySelector('.xans-product-headcategory.banner, [module="product_headcategory"].banner');
    const titleArea = document.querySelector('.titleArea, .xans-product-headcategory.title');
    const path = document.querySelector('.xans-product-headcategory.path, [module="product_headcategory"].path');
    const normalPkg = document.querySelector('.xans-product-normalpackage');
    const wish = document.querySelector('.icon-wish');
    const hover = document.querySelector('.effect .hover[data-src]');
    const desc = document.querySelector('.prdList .item .description') || document.querySelector('li[id^=anchorBoxId] .description');
    const body = document.body;
    const cRect = rect(container);
    const pRect = rect(prdList);
    const iRect = rect(item);
    const bRect = rect(banner);
    const tRect = rect(titleArea);

    const moduleKids = (parent) => parent
        ? Array.from(parent.children).filter((el) => el.className && (
            el.classList.contains('xans-product-headcategory') ||
            el.classList.contains('xans-product-menupackage') ||
            el.classList.contains('xans-product-normalpackage') ||
            el.classList.contains('xans-product-normalpaging')
        )).map((el) => el.className.split(' ').find((c) => c.startsWith('xans-product-')) || el.className)
        : [];

    const contentsKids = moduleKids(contents);
    const containerKids = moduleKids(container);
    const menuIdxContents = contentsKids.indexOf('xans-product-menupackage');
    const normalIdxContents = contentsKids.indexOf('xans-product-normalpackage');
    const bannerIdxContents = contentsKids.findIndex((c) => String(c).includes('headcategory'));
    const menuOrderOk = menuIdxContents >= 0 && normalIdxContents >= 0 && menuIdxContents < normalIdxContents;
    const bannerBeforeMenu = bannerIdxContents >= 0 && menuIdxContents >= 0 && bannerIdxContents < menuIdxContents;

    let menuParentTag = null;
    if (menuPkg && menuPkg.parentElement) {
        menuParentTag = menuPkg.parentElement.id || menuPkg.parentElement.tagName;
    }
    const contentsDisplay = contents ? cs(contents).display : null;

    let descLH = null;
    let descFS = null;
    if (desc) {
        descLH = parseFloat(cs(desc).lineHeight);
        descFS = parseFloat(cs(desc).fontSize);
    }

    const bannerMap = banner ? banner.querySelector('map') : null;
    const bannerMapText = bannerMap ? (bannerMap.textContent || '').trim().slice(0, 60) : '';

    return {
        bodyClass: body.className,
        hasSubPlp: body.classList.contains('ref393674-sub-plp'),
        hasLayout: body.classList.contains('layout'),
        containerW: cRect ? cRect.width : null,
        containerPad: container ? cs(container).padding : null,
        contentsW: contents ? rect(contents).width : null,
        contentsDisplay,
        contentsKids,
        containerKids,
        menuOrderOk,
        bannerBeforeMenu,
        menuParentTag,
        prdListW: pRect ? pRect.width : null,
        prdListX: pRect ? pRect.x : null,
        itemW: iRect ? iRect.width : null,
        itemCount: document.querySelectorAll('.prdList .item').length,
        menuPkgDisplay: menuPkg ? cs(menuPkg).display : null,
        menuCatDisplay: menuCat ? cs(menuCat).display : null,
        menuCatVisible: menuCat ? menuCat.offsetHeight > 0 : false,
        sortUlDisplay: sortUl ? cs(sortUl).display : null,
        sortUlVisible: sortUl ? sortUl.offsetHeight > 0 : false,
        sortSelDisplay: sortSel ? cs(sortSel).display : null,
        countVisible: count ? count.offsetHeight > 0 : false,
        countText: count ? count.textContent.trim() : '',
        bannerH: bRect ? bRect.height : null,
        bannerExists: !!banner,
        bannerMapExists: !!bannerMap,
        bannerMapText,
        titleDisplay: titleArea ? cs(titleArea).display : null,
        titleH: tRect ? tRect.height : null,
        pathDisplay: path ? cs(path).display : null,
        hasWish: !!wish,
        hasHover: !!hover,
        col4: prdList ? prdList.getAttribute('data-pc') : null,
        descLH,
        descFS,
    };
}"""


def measure(page, url: str) -> dict:
    page.goto(url, wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(1500)
    return page.evaluate(MEASURE_JS)


def score_pc(ref: dict, tgt: dict) -> Report:
    r = Report(viewport="PC 1440")
    checks: list[Check] = []

    def add(cid, label, pts, ref_v, tgt_v, ok: bool, note: str = ""):
        checks.append(
            Check(
                id=cid,
                label=label,
                max_pts=pts,
                pts=pts if ok else 0,
                ref=str(ref_v),
                tgt=str(tgt_v),
                note=note or ("PASS" if ok else "FAIL"),
            )
        )

    add("S1", "body.layout + ref393674-sub-plp", 6, ref.get("hasLayout"), tgt.get("hasSubPlp"),
        bool(tgt.get("hasLayout") and tgt.get("hasSubPlp")))
    add("S2", "prdList data-pc=col4", 4, ref.get("col4"), tgt.get("col4"),
        bool(tgt.get("col4") and "col4" in str(tgt.get("col4"))))
    add("S3", "menupackage 노출", 8, ref.get("menuCatVisible"), tgt.get("menuCatVisible"),
        bool(tgt.get("menuCatVisible")))
    add("S4", "menupackage 순서 (banner→menu→normal)", 8,
        f"order={ref.get('menuOrderOk')}",
        f"order={tgt.get('menuOrderOk')} kids={tgt.get('contentsKids')}",
        bool(tgt.get("menuOrderOk") and tgt.get("bannerBeforeMenu")))
    add("S5", "#contents flex column full width (EZ 래퍼 보정)", 6,
        "no #contents",
        f"display={tgt.get('contentsDisplay')} w={round(tgt.get('contentsW') or 0)}",
        tgt.get("contentsDisplay") == "flex" and (tgt.get("contentsW") or 0) >= 1380)
    add("S6", "sortby ul(#type) 노출", 8, ref.get("sortUlVisible"), tgt.get("sortUlVisible"),
        bool(tgt.get("sortUlVisible")))
    add("S7", "count 노출", 4, ref.get("countVisible"), tgt.get("countVisible"),
        bool(tgt.get("countVisible")))
    add("S8", "path/title 숨김", 6,
        f"path={ref.get('pathDisplay')} titleH={ref.get('titleH')}",
        f"path={tgt.get('pathDisplay')} titleH={tgt.get('titleH')}",
        (tgt.get("titleH") or 0) < 5 and tgt.get("pathDisplay") == "none")
    add("S9", "icon-wish + hover markup", 5, ref.get("hasWish"), tgt.get("hasWish"),
        bool(tgt.get("hasWish") and tgt.get("hasHover")))

    ref_plw, tgt_plw = ref.get("prdListW"), tgt.get("prdListW")
    plw_ok = near(tgt_plw, ref_plw, 30) or near(tgt_plw, 1420, 30)
    add("L1", "prdList width ≈1420", 12, round(ref_plw or 0), round(tgt_plw or 0), plw_ok)

    ref_iw, tgt_iw = ref.get("itemW"), tgt.get("itemW")
    iw_ok = near(tgt_iw, ref_iw, 20) or near(tgt_iw, 355, 20)
    add("L2", "item width ≈355 (4열)", 12, round(ref_iw or 0), round(tgt_iw or 0), iw_ok)

    ref_cw, tgt_cw = ref.get("containerW"), tgt.get("containerW")
    add("L3", "container full width", 6, round(ref_cw or 0), round(tgt_cw or 0),
        near(tgt_cw, ref_cw, 40) or (tgt_cw or 0) >= 1400)

    pad = tgt.get("containerPad") or ""
    pad_ok = "50px" in pad and "20px" in pad
    add("L4", "container padding 50/20/100", 4, ref.get("containerPad"), pad, pad_ok)

    ref_lh, tgt_lh = ref.get("descLH"), tgt.get("descLH")
    lh_ok = near(tgt_lh, ref_lh, 2) if ref_lh and tgt_lh else False
    add("T1", "description line-height ±2px", 6,
        round(ref_lh or 0, 1), round(tgt_lh or 0, 1), lh_ok)

    banner_pts = 0
    banner_note = "FAIL"
    if tgt.get("bannerExists"):
        banner_pts += 2
        if tgt.get("bannerMapExists") and len(tgt.get("bannerMapText") or "") > 10:
            banner_pts += 3
            banner_note = "PASS (map text)"
        elif (tgt.get("bannerH") or 0) > 50:
            banner_pts += 3
            banner_note = "PASS (image)"
        else:
            banner_note = "PARTIAL (구조만)"
    checks.append(
        Check(
            id="D1",
            label="카테고리 배너 + map 텍스트",
            max_pts=5,
            pts=banner_pts,
            ref=f"h={round(ref.get('bannerH') or 0)} map={bool(ref.get('bannerMapExists'))}",
            tgt=f"h={round(tgt.get('bannerH') or 0)} map={bool(tgt.get('bannerMapExists'))}",
            note=banner_note,
        )
    )

    r.checks = checks
    return r


def score_mo(tgt: dict) -> Report:
    r = Report(viewport="MO 390")
    checks: list[Check] = []
    iw = tgt.get("itemW") or 0
    ok = 170 <= iw <= 210
    checks.append(
        Check(
            id="M1",
            label="item 2열 (~50%)",
            max_pts=8,
            pts=8 if ok else 0,
            ref="~195",
            tgt=str(round(iw)),
            note="PASS" if ok else "FAIL",
        )
    )
    sort_ok = tgt.get("sortSelDisplay") not in (None, "none")
    checks.append(
        Check(
            id="M2",
            label="MO sort select 노출",
            max_pts=4,
            pts=4 if sort_ok else 0,
            ref="select",
            tgt=str(tgt.get("sortSelDisplay")),
            note="PASS" if sort_ok else "FAIL",
        )
    )
    r.checks = checks
    return r


def main():
    cfg = parse_mall_config()
    ref_url = cfg.url(PLP_PATH, target=False)
    tgt_url = cfg.url(PLP_PATH)

    out: dict = {"pass_threshold": PASS, "mall_id": cfg.mall_id, "reports": []}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx_pc = browser.new_context(viewport={"width": 1440, "height": 900})
        page_pc = ctx_pc.new_page()
        ref = measure(page_pc, ref_url)
        tgt = measure(page_pc, tgt_url)
        pc = score_pc(ref, tgt)
        out["reports"].append(
            {
                "viewport": pc.viewport,
                "score": pc.score,
                "max": pc.max_score,
                "checks": [asdict(c) for c in pc.checks],
                "ref": ref,
                "tgt": tgt,
            }
        )

        ctx_mo = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
        page_mo = ctx_mo.new_page()
        tgt_mo = measure(page_mo, tgt_url)
        mo = score_mo(tgt_mo)
        out["reports"].append(
            {
                "viewport": mo.viewport,
                "score": mo.score,
                "max": mo.max_score,
                "checks": [asdict(c) for c in mo.checks],
                "tgt": tgt_mo,
            }
        )
        browser.close()

    pc_score = out["reports"][0]["score"]
    mo_score = out["reports"][1]["score"]
    pc_max = out["reports"][0]["max"]
    mo_max = out["reports"][1]["max"]
    total = round((pc_score + mo_score) / (pc_max + mo_max) * 100)
    out["total_score"] = total
    out["pass"] = total >= PASS
    print(json.dumps(out, ensure_ascii=False, indent=2))
    sys.exit(0 if out["pass"] else 1)


if __name__ == "__main__":
    main()
