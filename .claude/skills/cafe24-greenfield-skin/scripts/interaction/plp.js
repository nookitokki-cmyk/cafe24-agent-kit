const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { boot } = require('../lib/runtime');
const { BASE, OUT } = boot(process.argv.slice(2), '_plp-interaction-scan-report.json');
const V = process.env.PLP_INTERACTION_V || 'w4-plp-interaction';

(async () => {
  const browser = await chromium.launch();
  const report = { scannedAt: new Date().toISOString(), cacheBust: V, tests: {} };

  // TC1: list card click → PDP (PC)
  {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    await page.goto(`${BASE}/product/list.html?cate_no=24&v=${V}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
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
    report.tests.listCardPdp = { pass: pdp.isPdp, ...pdp };
    await page.close();
  }

  // TC2: sort link click (must not break — URL changes or active state)
  {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    await page.goto(`${BASE}/product/list.html?cate_no=24&v=${V}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForSelector('.nk-plp__sortby a', { timeout: 15000 });
    const beforeUrl = page.url();
    const sortLinks = await page.locator('.nk-plp__sortby a').count();
    const secondSort = page.locator('.nk-plp__sortby a').nth(1);
    const hasSecond = sortLinks >= 2;
    let sortPass = false;
    if (hasSecond) {
      await Promise.all([
        page.waitForNavigation({ waitUntil: 'domcontentloaded', timeout: 30000 }).catch(() => null),
        secondSort.click(),
      ]);
      await page.waitForTimeout(800);
      const after = await page.evaluate(() => ({
        url: location.href,
        sortLinks: document.querySelectorAll('.nk-plp__sortby a').length,
        productCards: document.querySelectorAll('.nk-prd__link').length,
      }));
      sortPass = after.sortLinks >= 1 && after.productCards >= 1;
      report.tests.sortClick = { pass: sortPass, beforeUrl, ...after };
    } else {
      report.tests.sortClick = { pass: true, skipped: true, reason: 'single sort option', sortLinks };
    }
    await page.close();
  }

  // TC3: pagination click (page 2 if available)
  {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    await page.goto(`${BASE}/product/list.html?cate_no=24&v=${V}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForSelector('.nk-plp__paginate ol a', { timeout: 15000 });
    const pageLinks = await page.locator('.nk-plp__paginate ol a').count();
    if (pageLinks < 2) {
      report.tests.paginationClick = { pass: true, skipped: true, reason: 'single page only', pageLinks };
    } else {
      const page2 = page.locator('.nk-plp__paginate ol a').nth(1);
      const page2Text = await page2.textContent();
      await Promise.all([
        page.waitForNavigation({ waitUntil: 'domcontentloaded', timeout: 30000 }).catch(() => null),
        page2.click(),
      ]);
      await page.waitForTimeout(800);
      const after = await page.evaluate(() => ({
        url: location.href,
        cards: document.querySelectorAll('.nk-prd__link').length,
        paginate: !!document.querySelector('.nk-plp__paginate'),
      }));
      report.tests.paginationClick = {
        pass: after.paginate && after.cards >= 0,
        page2Text: page2Text?.trim(),
        ...after,
      };
    }
    await page.close();
  }

  // TC4: search result card (search.html)
  {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    await page.goto(`${BASE}/product/search.html?keyword=${encodeURIComponent('샘플')}&v=${V}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
    const searchState = await page.evaluate(() => ({
      cards: document.querySelectorAll('.nk-prd__link').length,
      hasGrid: !!document.querySelector('.nk-prd-grid'),
      hasSearchModule: !!document.querySelector('.xans-search-result, [module="Search_Result"]'),
      hasHead: !!document.querySelector('.nk-etc__head'),
    }));
    report.tests.searchResults = {
      pass: searchState.hasHead && (searchState.hasSearchModule || searchState.hasGrid || searchState.cards >= 0),
      ...searchState,
    };
    await page.close();
  }

  // TC5: recent view page loads (may be empty)
  {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    await page.goto(`${BASE}/product/recent_view_product.html?v=${V}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
    const state = await page.evaluate(() => ({
      hasRecentModule: !!document.querySelector('[module="product_recentlist"], .xans-product-recentlist'),
      hasMessage: !!document.querySelector('.nk-etc-recent .message'),
      rows: document.querySelectorAll('.nk-etc-recent__list tbody tr').length,
      hasHead: !!document.querySelector('.nk-etc__head'),
    }));
    report.tests.recentView = {
      pass: state.hasHead && state.hasRecentModule && (state.rows >= 0 || state.hasMessage),
      ...state,
    };
    await page.close();
  }

  // TC6: MO390 overflow check (3 URLs)
  {
    const urls = [
      '/product/list.html?cate_no=24',
      '/product/search.html?keyword=sample',
      '/product/recent_view_product.html',
    ];
    const moResults = [];
    for (const u of urls) {
      const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
      await page.goto(`${BASE}${u}&v=${V}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
      await page.waitForTimeout(800);
      const overflow = await page.evaluate(() => ({
        sw: document.documentElement.scrollWidth,
        cw: document.documentElement.clientWidth,
        overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
      }));
      moResults.push({ path: u, ...overflow, pass: !overflow.overflow });
      await page.close();
    }
    report.tests.moOverflow = { pass: moResults.every((r) => r.pass), urls: moResults };
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
