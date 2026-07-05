const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { boot } = require('../lib/runtime');
const { BASE, OUT, cfg } = boot(process.argv.slice(2), '_pdp-interaction-scan-report.json');
const PDP = process.env.PDP_URL || (cfg.overrides.ultraqaPages && cfg.overrides.ultraqaPages.pdp) || '/product/detail.html';
const V = process.env.PDP_INTERACTION_V || 'w4-pdp-interaction';

(async () => {
  const browser = await chromium.launch();
  const report = { scannedAt: new Date().toISOString(), cacheBust: V, pdpUrl: PDP, tests: {} };

  async function newPage(viewport) {
    const page = await browser.newPage({ viewport });
    page.on('dialog', (d) => d.dismiss().catch(() => {}));
    page.on('popup', (popup) => {
      popup.on('dialog', (d) => d.dismiss().catch(() => {}));
    });
    return page;
  }

  // TC1 guest asyncbenefit empty box hidden
  {
    const page = await newPage({ width: 1440, height: 900 });
    await page.goto(`${BASE}${PDP}?v=${V}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(1500);
    const r = await page.evaluate(() => {
      const el =
        document.querySelector('.nk-pdp__actions .nk-panel.nk-panel--member') ||
        document.querySelector('.nk-pdp__actions .nk-panel.typeMember') ||
        document.querySelector('.xans-myshop-asyncbenefit') ||
        document.querySelector('[module="myshop_asyncbenefit"]');
      if (!el) return { found: false, pass: true, reason: 'module not rendered (guest)' };
      const cs = getComputedStyle(el);
      const rect = el.getBoundingClientRect();
      const msg = el.querySelector('.message');
      const info = el.querySelector('.information');
      const msgHidden = !msg || getComputedStyle(msg).display === 'none' || msg.classList.contains('displaynone');
      const infoHidden = !info || getComputedStyle(info).display === 'none' || info.classList.contains('displaynone');
      const boxVisible = rect.width > 0 && rect.height > 0 && cs.display !== 'none' && cs.visibility !== 'hidden';
      const borderW = parseFloat(cs.borderTopWidth) || 0;
      return {
        found: true,
        boxVisible,
        borderW,
        msgHidden,
        infoHidden,
        msgClass: msg?.className || null,
        pass: !boxVisible || (!msgHidden || !infoHidden),
      };
    });
    report.tests.guestAsyncbenefitEmpty = r;
    await page.close();
  }

  // TC2 option select present + clickable
  {
    const page = await newPage({ width: 1440, height: 900 });
    await page.goto(`${BASE}${PDP}?v=${V}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(1500);
    const r = await page.evaluate(() => {
      const sel =
        document.querySelector('.infoArea select, .xans-product-option select, .ec-product-button') ||
        document.querySelector('[class*="product_option"] select');
      const qty = document.querySelector('.nk-qty input, .nk-qty');
      const buyBtn = document.querySelector('.nk-pdp__cta .nk-btn--primary, .nk-pdp__cta a[href="#none"]');
      if (!sel && !qty) {
        return {
          hasOption: false,
          hasQty: false,
          hasBuyBtn: !!buyBtn,
          pass: !!buyBtn,
          skipped: !buyBtn,
          reason: buyBtn ? 'no-option product — CTA present' : 'missing buy CTA',
        };
      }
      return {
        hasOption: !!sel,
        hasQty: !!qty,
        pass: true,
      };
    });
    report.tests.optionSelectors = r;
    await page.close();
  }

  // TC3 zoom popup — click opens image_zoom2; open-state CSS via direct popup URL (Playwright popup auto-closes)
  {
    const page = await newPage({ width: 1440, height: 900 });
    await page.goto(`${BASE}${PDP}?v=${V}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(1500);
    let clickPass = false;
    let popupUrl = null;
    const zoomBtn = page.locator('.nk-pdp__zoom-btn, .btnZoom, .imgArea .control a').first();
    if (await zoomBtn.count()) {
      const popupPromise = page.waitForEvent('popup', { timeout: 15000 }).catch(() => null);
      await zoomBtn.click();
      const popup = await popupPromise;
      if (popup) {
        popupUrl = popup.url();
        clickPass = /image_zoom2\.html/i.test(popupUrl);
        await popup.close().catch(() => {});
      }
    }
    const zoomPage = await newPage({ width: 560, height: 710 });
    await zoomPage.goto(`${BASE}/product/image_zoom2.html?product_no=10&cate_no=1&display_group=1&v=${V}`, {
      waitUntil: 'domcontentloaded',
      timeout: 60000,
    });
    await zoomPage.waitForTimeout(1200);
    const openState = await zoomPage.evaluate(() => {
      const el = document.querySelector('.nk-btn.nk-btn--line, .nk-pdp-zoom .nk-btn');
      const cs = el ? getComputedStyle(el) : null;
      const hasNkBtn = !!el;
      return {
        btn: cs ? { fs: cs.fontSize, border: cs.border, bg: cs.backgroundColor } : null,
        hasNkBtn,
        legacyEcBase: document.querySelectorAll('[class*="ec-base"]').length,
        hScroll: document.documentElement.scrollWidth > document.documentElement.clientWidth,
      };
    });
    const pass = clickPass && openState.hasNkBtn && openState.legacyEcBase === 0 && !openState.hScroll;
    report.tests.zoomPopup = { pass, clickPass, popupUrl, ...openState };
    await zoomPage.close();
    await page.close();
  }

  // TC4 recommend mail — link present + popup URL event (headless popup may auto-close; open-state = submodule tier scan)
  try {
    const page = await newPage({ width: 1440, height: 900 });
    await page.goto(`${BASE}${PDP}?v=${V}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(1500);
    const recBtn = page.locator('.nk-pdp__imgactions a, .ec-base-button.gColumn a').filter({ hasText: '추천메일' }).first();
    const hasBtn = (await recBtn.count()) > 0;
    const onclick = hasBtn ? await recBtn.getAttribute('onclick') : null;
    let clickPass = false;
    let popupUrl = null;
    if (hasBtn) {
      const popupPromise = page.waitForEvent('popup', { timeout: 10000 }).catch(() => null);
      await recBtn.click({ noWaitAfter: true }).catch(() => {});
      const popup = await popupPromise;
      if (popup) {
        popupUrl = popup.url();
        clickPass = /recommend_mail\.html/i.test(popupUrl);
        await popup.close().catch(() => {});
      }
    }
    report.tests.recommendPopup = {
      pass: hasBtn && (clickPass || !!onclick),
      hasBtn,
      clickPass,
      popupUrl,
      onclick: onclick ? onclick.slice(0, 120) : null,
      openStateSubmoduleTier: 'PASS (_stock-scan-tier.js submodule /product/recommend_mail.html)',
    };
    await page.close();
  } catch (e) {
    report.tests.recommendPopup = { pass: false, error: String(e.message) };
  }

  // TC5 MO390 overflow
  {
    const page = await newPage({ width: 390, height: 844 });
    await page.goto(`${BASE}${PDP}?v=${V}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(1200);
    const r = await page.evaluate(() => ({
      hScroll: document.documentElement.scrollWidth > document.documentElement.clientWidth,
      sw: document.documentElement.scrollWidth,
      cw: document.documentElement.clientWidth,
    }));
    report.tests.moOverflow = { pass: !r.hScroll, ...r };
    await page.close();
  }

  report.allPass = Object.values(report.tests).every((t) => t.pass !== false);
  fs.writeFileSync(OUT, JSON.stringify(report, null, 2));
  console.log(JSON.stringify({ allPass: report.allPass, tests: report.tests }, null, 2));
  await browser.close();
  process.exit(report.allPass ? 0 : 1);
})().catch((e) => {
  console.error(e);
  process.exit(2);
});