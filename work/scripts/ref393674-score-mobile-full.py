#!/usr/bin/env python3
"""ref393674 comprehensive mobile audit — PASS only at 100/100 (390×844, main URL)."""
from __future__ import annotations

import json
import re
import sys
from dataclasses import asdict, dataclass, field
from urllib.request import urlopen

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print(json.dumps({"error": "playwright not installed", "total_score": 0, "pass": False}))
    sys.exit(1)

from score_mall import parse_mall_config

PASS = 100

PAGES = {
    "home": "/",
    "plp": "/product/list.html?cate_no=24",
    "pdp": "/product/샘플상품-2/10/category/24/display/1/",
    "login": "/member/login.html",
    "basket": "/order/basket.html",
}


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
    checks: list[Check] = field(default_factory=list)

    @property
    def score(self) -> int:
        return sum(c.pts for c in self.checks)

    @property
    def max_score(self) -> int:
        return sum(c.max_pts for c in self.checks)


def fetch_mobile_web(base: str, path: str = "/") -> bool | None:
    url = base.rstrip("/") + path
    try:
        html = urlopen(url, timeout=30).read().decode("utf-8", errors="replace")
        m = re.search(r"CAFE24\.MOBILE_WEB\s*=\s*(true|false)", html, re.I)
        return m.group(1).lower() == "true" if m else None
    except Exception as e:
        return None


def near(a: float | None, b: float | None, tol: float) -> bool:
    if a is None or b is None:
        return False
    return abs(float(a) - float(b)) <= tol


def measure_page(page, url: str) -> dict:
    page.goto(url, wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(1800)
    return page.evaluate(
        """() => {
        const cs = (el) => el ? getComputedStyle(el) : null;
        const r = (el) => el ? el.getBoundingClientRect() : null;
        const header = document.querySelector('#header.a-header');
        const btnMenu = document.querySelector('#header.a-header .btn-menu, .btn-menu');
        const menuMain = document.querySelector('#header.a-header .menu-main');
        const logo = document.querySelector('#header.a-header .logo img, #header.a-header .logo span, #header.a-header .logo a');
        const searchPanel = document.querySelector('#header.a-header .a-search');
        const searchMod = document.querySelector('#header.a-header .xans-layout-searchheader');
        const container = document.querySelector('#container');
        const contents = document.querySelector('#contents');
        const contentsRect = contents ? r(contents) : null;
        const prdList = document.querySelector('.prdList');
        const item = document.querySelector('.prdList .item');
        const sortUl = document.querySelector('.sortby #type, #type');
        const sortSel = document.querySelector('#selArray');
        const footer = document.querySelector('#footer, footer');
        const footerLinks = footer ? footer.querySelectorAll('a') : [];
        const swiper = document.querySelector('.swiper-container, .swiper');
        const swiperSlides = document.querySelectorAll('.swiper-slide');
        const hero = document.querySelector('.main-sec1');
        const heroRect = hero ? r(hero) : null;
        const bottomNav = document.querySelector('.bottom-nav, #bottom-nav, .RTMB, [class*="bottomNav"]');
        const rtmb = document.querySelector('[class*="RTMB"], .rtmb');
        const bodyFont = cs(document.body)?.fontSize;
        const btnSubmit = document.querySelector('.btnSubmit, .btnSubmitFix');
        const loginBtn = document.querySelector('.xans-member-login .btnSubmit');
        const tapCandidates = [btnSubmit, loginBtn, btnMenu].filter(Boolean);
        const tapBtn = tapCandidates.find((el) => el.offsetWidth > 0 && el.offsetHeight > 0) || btnMenu;
        const scrollW = document.documentElement.scrollWidth;
        const clientW = document.documentElement.clientWidth;
        let minBodyFont = 99;
        document.querySelectorAll('p, span, li, a, td, th, label, .desc, .price').forEach(el => {
            if (el.offsetHeight <= 0) return;
            const fs = parseFloat(cs(el)?.fontSize || '0');
            if (fs > 0 && fs < minBodyFont) minBodyFont = fs;
        });
        if (minBodyFont === 99) minBodyFont = parseFloat(bodyFont || '0');
        return {
            url: location.href,
            bodyClass: document.body.className,
            hasAHeader: !!header,
            btnMenuDisplay: btnMenu ? cs(btnMenu).display : null,
            btnMenuW: btnMenu ? r(btnMenu).width : null,
            btnMenuH: btnMenu ? r(btnMenu).height : null,
            menuMainDisplay: menuMain ? cs(menuMain).display : null,
            logoW: logo ? r(logo).width : null,
            logoH: logo ? r(logo).height : null,
            searchPanelDisplay: searchPanel ? cs(searchPanel).display : null,
            searchModDisplay: searchMod ? cs(searchMod).display : null,
            containerW: r(container)?.width,
            containerPadL: container ? parseFloat(cs(container).paddingLeft) : null,
            containerPadR: container ? parseFloat(cs(container).paddingRight) : null,
            contentsW: contentsRect ? contentsRect.width : null,
            contentsFullWidth: contentsRect ? contentsRect.width >= clientW - 4 : null,
            prdListW: prdList ? r(prdList).width : null,
            itemW: item ? r(item).width : null,
            itemCount: document.querySelectorAll('.prdList .item').length,
            sortUlVisible: sortUl ? sortUl.offsetHeight > 0 && cs(sortUl).display !== 'none' : false,
            sortSelDisplay: sortSel ? cs(sortSel).display : null,
            footerExists: !!footer,
            footerH: footer ? r(footer).height : null,
            footerLinkCount: footerLinks.length,
            footerFirstLinkH: footerLinks.length ? r(footerLinks[0]).height : null,
            swiperExists: !!swiper,
            swiperSlideCount: swiperSlides.length,
            heroX: heroRect ? heroRect.x : null,
            heroW: heroRect ? heroRect.width : null,
            heroFullBleed: heroRect ? heroRect.x <= 2 && heroRect.width >= clientW - 4 : null,
            bottomNavVisible: bottomNav ? bottomNav.offsetHeight > 0 && cs(bottomNav).display !== 'none' : false,
            rtmbVisible: rtmb ? rtmb.offsetHeight > 0 : false,
            horizontalOverflow: scrollW > clientW + 2,
            scrollW, clientW,
            minBodyFont,
            tapTargetW: tapBtn ? r(tapBtn).width : null,
            tapTargetH: tapBtn ? r(tapBtn).height : null,
            h1Family: (document.querySelector('h1') && cs(document.querySelector('h1')).fontFamily) || null,
        };
    }"""
    )


def measure_parity(ref: dict, tgt: dict) -> dict:
    keys = ["btnMenuDisplay", "menuMainDisplay", "searchPanelDisplay", "logoW", "itemW"]
    gaps = {}
    for k in keys:
        rv, tv = ref.get(k), tgt.get(k)
        if k.endswith("W") and rv is not None and tv is not None:
            gaps[k] = {"ref": rv, "tgt": tv, "delta": round(abs(float(rv) - float(tv)), 1)}
        else:
            gaps[k] = {"ref": rv, "tgt": tv, "match": rv == tv}
    return gaps


def score_mobile_full(ref_pages: dict, tgt_pages: dict, mobile_web_main: bool | None, mobile_web_m: bool | None) -> Report:
    rep = Report()
    checks: list[Check] = []

    def add(cid, label, pts, ok, rv="", tv="", note=""):
        checks.append(
            Check(
                cid,
                label,
                pts,
                pts if ok else 0,
                str(rv),
                str(tv),
                note or ("PASS" if ok else "FAIL"),
            )
        )

    # 10 pts — MOBILE_WEB=false on main URL
    mw_ok = mobile_web_main is False
    add(
        "MW1",
        "CAFE24.MOBILE_WEB=false (main URL)",
        10,
        mw_ok,
        mobile_web_main,
        mobile_web_main,
        "PASS" if mw_ok else "CRITICAL: MOBILE_WEB still true — separate mobile skin",
    )

    plp = tgt_pages.get("plp", {})
    home = tgt_pages.get("home", {})
    ref_plp = ref_pages.get("plp", {})
    ref_home = ref_pages.get("home", {})

    # 15 pts — Header
    burger_ok = plp.get("btnMenuDisplay") not in (None, "none") and (plp.get("btnMenuH") or 0) >= 30
    gnb_hidden = plp.get("menuMainDisplay") == "none"
    logo_ok = (plp.get("logoH") or 0) >= 20 and (plp.get("logoH") or 99) <= 60
    header_pts = 0
    if burger_ok:
        header_pts += 6
    if gnb_hidden:
        header_pts += 5
    if logo_ok:
        header_pts += 4
    checks.append(
        Check(
            "H1",
            "Header: burger visible, GNB hidden, logo scale",
            15,
            header_pts,
            f"burger={ref_plp.get('btnMenuDisplay')} gnb={ref_plp.get('menuMainDisplay')}",
            f"burger={plp.get('btnMenuDisplay')} gnb={plp.get('menuMainDisplay')} logoH={plp.get('logoH')}",
            "PASS" if header_pts == 15 else f"PARTIAL {header_pts}/15",
        )
    )

    # 10 pts — Search MO behavior
    search_ok = plp.get("searchPanelDisplay") == "none" and ref_plp.get("searchPanelDisplay") == "none"
    add(
        "S1",
        "Search MO hidden panel (ref parity)",
        10,
        search_ok,
        ref_plp.get("searchPanelDisplay"),
        plp.get("searchPanelDisplay"),
    )

    # 10 pts — PLP grid
    iw = plp.get("itemW") or 0
    col2_ok = 170 <= iw <= 210
    pad_l = plp.get("containerPadL") or 0
    pad_r = plp.get("containerPadR") or 0
    pad_ok = near(pad_l, 15, 3) and near(pad_r, 15, 3)
    sort_ok = not plp.get("sortUlVisible") and plp.get("sortSelDisplay") not in (None, "none")
    plp_pts = (4 if col2_ok else 0) + (3 if pad_ok else 0) + (3 if sort_ok else 0)
    checks.append(
        Check(
            "P1",
            "PLP: 2-col grid, padding 15px, sort select",
            10,
            plp_pts,
            f"itemW~195 pad15",
            f"itemW={iw} padL={pad_l} padR={pad_r} sort={plp.get('sortSelDisplay')}",
            "PASS" if plp_pts == 10 else f"PARTIAL {plp_pts}/10",
        )
    )

    # 10 pts — #contents viewport width (EZ 92% trap — rules/ez-contents-width.md)
    home_cw = home.get("contentsW") or 0
    plp_cw = plp.get("contentsW") or 0
    home_vw = home.get("clientW") or 390
    plp_vw = plp.get("clientW") or 390
    home_contents_ok = home.get("contentsFullWidth") is True
    plp_contents_ok = plp.get("contentsFullWidth") is True
    contents_ok = home_contents_ok and plp_contents_ok
    add(
        "C1",
        "#contents width ≥ viewport−4 at 390px (/, PLP) — EZ 92% trap",
        10,
        contents_ok,
        f"home={ref_home.get('contentsW')} plp={ref_plp.get('contentsW')}",
        f"home={home_cw}/{home_vw} plp={plp_cw}/{plp_vw}",
        "PASS" if contents_ok else "FAIL: #contents still ~92% — use #container #contents width:100% !important",
    )

    # 15 pts — Hero/main
    swiper_ok = home.get("swiperExists") and (home.get("swiperSlideCount") or 0) >= 1
    overflow_ok = not home.get("horizontalOverflow") and not plp.get("horizontalOverflow")
    hero_bleed_ok = home.get("heroFullBleed") is True
    hero_pts = (5 if swiper_ok else 0) + (4 if overflow_ok else 0) + (6 if hero_bleed_ok else 0)
    checks.append(
        Check(
            "R1",
            "Hero/main: swiper, no overflow, hero full-bleed (x≤2, w≥vw-4)",
            15,
            hero_pts,
            f"slides={ref_home.get('swiperSlideCount')} heroX={ref_home.get('heroX')} heroW={ref_home.get('heroW')}",
            f"slides={home.get('swiperSlideCount')} heroX={home.get('heroX')} heroW={home.get('heroW')} bleed={home.get('heroFullBleed')}",
            "PASS" if hero_pts == 15 else f"PARTIAL {hero_pts}/15",
        )
    )

    # 10 pts — Typography / tap targets
    font_ok = (plp.get("minBodyFont") or 0) >= 12
    tap_ok = (plp.get("tapTargetH") or 0) >= 44 or (plp.get("tapTargetW") or 0) >= 44
    typo_pts = (5 if font_ok else 0) + (5 if tap_ok else 0)
    checks.append(
        Check(
            "T1",
            "Typography ≥12px body, tap targets ≥44px",
            10,
            typo_pts,
            "12px / 44px",
            f"minFont={plp.get('minBodyFont')} tap={plp.get('tapTargetW')}x{plp.get('tapTargetH')}",
            "PASS" if typo_pts == 10 else f"PARTIAL {typo_pts}/10",
        )
    )

    # 10 pts — Footer
    footer_ok = plp.get("footerExists") and (plp.get("footerH") or 0) > 50
    links_ok = (plp.get("footerLinkCount") or 0) >= 3
    tappable = (plp.get("footerFirstLinkH") or 0) >= 20
    foot_pts = (4 if footer_ok else 0) + (3 if links_ok else 0) + (3 if tappable else 0)
    checks.append(
        Check(
            "F1",
            "Footer: not broken, links tappable",
            10,
            foot_pts,
            "footer ok",
            f"h={plp.get('footerH')} links={plp.get('footerLinkCount')}",
            "PASS" if foot_pts == 10 else f"PARTIAL {foot_pts}/10",
        )
    )

    # 10 pts — No EZ junk
    ez_ok = not plp.get("bottomNavVisible") and not plp.get("rtmbVisible") and plp.get("hasAHeader")
    add(
        "E1",
        "No EZ junk (bottom-nav, RTMB, white boxes)",
        10,
        ez_ok,
        "clean",
        f"bottomNav={plp.get('bottomNavVisible')} rtmb={plp.get('rtmbVisible')} aHeader={plp.get('hasAHeader')}",
    )

    # 20 pts — Ref parity (5 key elements)
    parity = measure_parity(ref_plp, plp)
    parity_score = 0
    parity_notes = []
    if parity.get("btnMenuDisplay", {}).get("match"):
        parity_score += 4
    else:
        parity_notes.append("btnMenu")
    if parity.get("menuMainDisplay", {}).get("match"):
        parity_score += 4
    else:
        parity_notes.append("menuMain")
    if parity.get("searchPanelDisplay", {}).get("match"):
        parity_score += 4
    else:
        parity_notes.append("search")
    lw = parity.get("logoW", {})
    if lw.get("ref") is not None and near(lw.get("tgt"), lw.get("ref"), 15):
        parity_score += 4
    else:
        parity_notes.append(f"logoW Δ{lw.get('delta')}")
    iw_p = parity.get("itemW", {})
    if iw_p.get("ref") is not None and near(iw_p.get("tgt"), iw_p.get("ref"), 25):
        parity_score += 4
    else:
        parity_notes.append(f"itemW Δ{iw_p.get('delta')}")
    checks.append(
        Check(
            "Q1",
            "Ref parity: 5 key elements vs ref (390px)",
            20,
            parity_score,
            json.dumps({k: v.get("ref") for k, v in parity.items()}),
            json.dumps({k: v.get("tgt") for k, v in parity.items()}),
            "PASS" if parity_score == 20 else f"GAPS: {', '.join(parity_notes)} ({parity_score}/20)",
        )
    )

    rep.checks = checks
    return rep


def main():
    cfg = parse_mall_config()
    ref_base = cfg.ref_base
    tgt_base = cfg.tgt_base

    mobile_web_main = fetch_mobile_web(tgt_base, "/")
    mobile_web_m = fetch_mobile_web(tgt_base, "/m/")

    ref_pages: dict = {}
    tgt_pages: dict = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)

        ref_page = ctx.new_page()
        tgt_page = ctx.new_page()
        for key, path in PAGES.items():
            ref_pages[key] = measure_page(ref_page, ref_base + path)
            tgt_pages[key] = measure_page(tgt_page, tgt_base + path)
        browser.close()

    report = score_mobile_full(ref_pages, tgt_pages, mobile_web_main, mobile_web_m)
    raw = report.score
    mx = report.max_score
    total = round(raw / mx * 100) if mx else 0
    out = {
        "total_score": total,
        "raw_score": raw,
        "max_score": mx,
        "pass_threshold": PASS,
        "pass": total >= PASS,
        "mall_id": cfg.mall_id,
        "ref_base": ref_base,
        "tgt_base": tgt_base,
        "mobile_web": {"main": mobile_web_main, "m_path": mobile_web_m},
        "checks": [asdict(c) for c in report.checks],
        "ref_pages": ref_pages,
        "tgt_pages": tgt_pages,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    sys.exit(0 if out["pass"] else 1)


if __name__ == "__main__":
    main()
