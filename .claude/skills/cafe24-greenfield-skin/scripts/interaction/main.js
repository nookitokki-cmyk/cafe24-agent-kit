const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { boot } = require('../lib/runtime');
const { BASE, OUT, cfg } = boot(process.argv.slice(2), '_main-interaction-scan-report.json');
const CACHE_BUST = process.env.MAIN_INTERACTION_V || 'w4-main-interaction';

(async () => {
  const browser = await chromium.launch();
  const report = { scannedAt: new Date().toISOString(), cacheBust: CACHE_BUST, tests: {} };

  // --- TC2: burger/drawer (MO) ---
  {
    const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
    await page.goto(`${BASE}/?v=${CACHE_BUST}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForSelector('#nkBurger', { timeout: 15000 });
    await page.click('#nkBurger');
    await page.waitForTimeout(400);
    const drawer = await page.evaluate(() => ({
      drawerOpen: document.getElementById('nkDrawer')?.classList.contains('is-open'),
      bodyOpen: document.body.classList.contains('nk-drawer-open'),
      ariaExpanded: document.getElementById('nkBurger')?.getAttribute('aria-expanded'),
      catLinks: document.querySelectorAll('.nk-drawer__link').length,
    }));
    report.tests.drawerOpen = {
      pass: drawer.drawerOpen && drawer.bodyOpen && drawer.ariaExpanded === 'true' && drawer.catLinks >= 1,
      ...drawer,
    };
    await page.click('#nkDrawerClose');
    await page.waitForTimeout(300);
    const closed = await page.evaluate(() => !document.getElementById('nkDrawer')?.classList.contains('is-open'));
    report.tests.drawerClose = { pass: closed };
    await page.close();
  }

  // --- TC3: search overlay open/submit (PC) ---
  {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    await page.goto(`${BASE}/?v=${CACHE_BUST}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForSelector('#nkSearchBtn', { timeout: 15000 });
    await page.click('#nkSearchBtn');
    await page.waitForTimeout(400);
    const openState = await page.evaluate(() => ({
      searchOpen: document.getElementById('nkSearch')?.classList.contains('is-open'),
      hasInput: !!document.querySelector('#nkSearch input[type="text"], #nkSearch input[name="keyword"]'),
    }));
    report.tests.searchOpen = { pass: openState.searchOpen && openState.hasInput, ...openState };

    const input = page.locator('#nkSearch input[type="text"], #nkSearch input[name="keyword"]').first();
    await input.fill('샘플');
    await Promise.all([
      page.waitForNavigation({ waitUntil: 'domcontentloaded', timeout: 30000 }).catch(() => null),
      page.locator('#nkSearch button[type="submit"], #nkSearch .nk-search__submit').first().click(),
    ]);
    await page.waitForTimeout(800);
    const afterSubmit = {
      url: page.url(),
      isSearchPage: /search\.html|product\/search/i.test(page.url()),
    };
    report.tests.searchSubmit = {
      pass: afterSubmit.isSearchPage,
      ...afterSubmit,
    };
    await page.close();
  }

  // --- TC4: scroll nk-scrolled (PC) ---
  {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    await page.goto(`${BASE}/?v=${CACHE_BUST}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForSelector('#header', { timeout: 15000 });
    const before = await page.evaluate(() => document.getElementById('header')?.classList.contains('nk-scrolled'));
    await page.evaluate(() => window.scrollTo(0, 200));
    await page.waitForTimeout(300);
    const afterScroll = await page.evaluate(() => document.getElementById('header')?.classList.contains('nk-scrolled'));
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForTimeout(300);
    const afterTop = await page.evaluate(() => !document.getElementById('header')?.classList.contains('nk-scrolled'));
    report.tests.scrollNkScrolled = {
      pass: !before && afterScroll && afterTop,
      before,
      afterScroll,
      afterTop,
    };
    await page.close();
  }

  // --- TC5: product card click → PDP ---
  {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    await page.goto(`${BASE}/?v=${CACHE_BUST}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForSelector('.nk-prd__link', { timeout: 15000 });
    const href = await page.locator('.nk-prd__link').first().getAttribute('href');
    await Promise.all([
      page.waitForNavigation({ waitUntil: 'domcontentloaded', timeout: 30000 }),
      page.locator('.nk-prd__link').first().click(),
    ]);
    await page.waitForTimeout(800);
    const pdp = await page.evaluate(() => ({
      url: location.href,
      hasProductDetailModule: !!document.querySelector('[module="product_detail"]'),
    }));
    pdp.href = href;
    pdp.isPdp = /product\/detail\.html/i.test(pdp.url) || pdp.hasProductDetailModule || /\/product\/[^/]+\/\d+/i.test(pdp.url);
    report.tests.productCardPdp = { pass: pdp.isPdp, ...pdp };
    await page.close();
  }

  // --- TC6: quick basket (if visible) ---
  {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    await page.goto(`${BASE}/?v=${CACHE_BUST}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(500);
    const quick = await page.evaluate(() => {
      const el = document.getElementById('quick');
      if (!el) return { exists: false, visible: false };
      const cs = getComputedStyle(el);
      const visible = cs.display !== 'none' && cs.visibility !== 'hidden' && el.getBoundingClientRect().width > 0;
      const basketLink = el.querySelector('a[href*="basket"]');
      return {
        exists: true,
        visible,
        display: cs.display,
        basketLinkHref: basketLink?.getAttribute('href') || null,
      };
    });
    if (!quick.visible) {
      report.tests.quickBasket = { pass: true, skipped: true, reason: '#quick hidden by design (nk-cafe24-reset §10)', ...quick };
    } else {
      await page.locator('#quick a[href*="basket"]').first().click();
      await page.waitForTimeout(800);
      const url = page.url();
      report.tests.quickBasket = {
        pass: /basket\.html/i.test(url),
        skipped: false,
        url,
        ...quick,
      };
    }
    await page.close();
  }

  report.pass = Object.values(report.tests).every((t) => t.pass);
  fs.writeFileSync(OUT, JSON.stringify(report, null, 2));
  console.log(JSON.stringify(report, null, 2));
  await browser.close();
  process.exit(report.pass ? 0 : 1);
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
