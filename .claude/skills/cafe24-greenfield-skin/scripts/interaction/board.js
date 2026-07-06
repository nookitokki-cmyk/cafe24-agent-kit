const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { boot } = require('../lib/runtime');
const { BASE, OUT } = boot(process.argv.slice(2), '_board-interaction-scan-report.json');
const V = process.env.BOARD_INTERACTION_V || 'w4-board-interaction';

(async () => {
  const browser = await chromium.launch();
  const report = { scannedAt: new Date().toISOString(), cacheBust: V, tests: {} };

  // TC1: list → read (free board)
  {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    await page.goto(`${BASE}/board/free/list.html?board_no=1&v=${V}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForSelector('.nk-board td.title a, .nk-board .subject a', { timeout: 15000 });
    const subjectLink = page.locator('.nk-board td.title a, .nk-board .subject a').first();
    await Promise.all([
      page.waitForNavigation({ waitUntil: 'domcontentloaded', timeout: 30000 }),
      subjectLink.click(),
    ]);
    await page.waitForTimeout(800);
    const readState = await page.evaluate(() => ({
      url: location.href,
      hasReadModule: !!document.querySelector('[module*="board_read"], .xans-board-read'),
      hasNkBoardRead: !!document.querySelector('.nk-board--read, .nk-board'),
      isRead: /read\.html/i.test(location.href) || /\/article\//i.test(location.href),
    }));
    report.tests.listToRead = {
      pass: readState.isRead && (readState.hasReadModule || readState.hasNkBoardRead),
      ...readState,
    };
    await page.close();
  }

  // TC2: write link (login redirect acceptable; admin displaynone → direct URL)
  {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    await page.goto(`${BASE}/board/free/list.html?board_no=1&v=${V}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
    const writeBtn = page.locator('.nk-board__buttons a.btnSubmitFix:not(.displaynone), a[href*="write.html"]:not(.displaynone)').first();
    const hasVisibleWrite = (await writeBtn.count()) > 0 && (await writeBtn.isVisible().catch(() => false));
    if (!hasVisibleWrite) {
      await page.goto(`${BASE}/board/free/write.html?board_no=1&v=${V}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
      await page.waitForTimeout(800);
      const direct = await page.evaluate(() => ({
        url: location.href,
        isWrite: /write\.html/i.test(location.href),
        isLogin: /login\.html/i.test(location.href),
        hasWriteForm: !!document.querySelector('[module*="board_write"], form[name="boardWriteForm"]'),
      }));
      report.tests.writeLink = {
        pass: direct.isWrite || direct.isLogin || direct.hasWriteForm,
        skipped: true,
        reason: 'write btn displaynone — direct URL',
        ...direct,
      };
    } else {
      await Promise.all([
        page.waitForNavigation({ waitUntil: 'domcontentloaded', timeout: 30000 }).catch(() => null),
        writeBtn.click(),
      ]);
      await page.waitForTimeout(800);
      const after = await page.evaluate(() => ({
        url: location.href,
        isWrite: /write\.html/i.test(location.href),
        isLogin: /login\.html/i.test(location.href),
        hasWriteForm: !!document.querySelector('[module*="board_write"], form[name="boardWriteForm"]'),
      }));
      report.tests.writeLink = {
        pass: after.isWrite || after.isLogin || after.hasWriteForm,
        ...after,
      };
    }
    await page.close();
  }

  // TC3: pagination click (free list)
  {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    await page.goto(`${BASE}/board/free/list.html?board_no=1&v=${V}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForSelector('.nk-board__paginate ol a, .xans-board-paging ol a', { timeout: 15000 }).catch(() => null);
    const pageLinks = await page.locator('.nk-board__paginate ol a, .xans-board-paging ol a').count();
    if (pageLinks < 2) {
      report.tests.paginationClick = { pass: true, skipped: true, reason: 'single page only', pageLinks };
    } else {
      const page2 = page.locator('.nk-board__paginate ol a, .xans-board-paging ol a').nth(1);
      await Promise.all([
        page.waitForNavigation({ waitUntil: 'domcontentloaded', timeout: 30000 }).catch(() => null),
        page2.click(),
      ]);
      await page.waitForTimeout(800);
      const after = await page.evaluate(() => ({
        url: location.href,
        rows: document.querySelectorAll('.nk-board__table tbody tr, .boardList tbody tr').length,
        hasPaginate: !!document.querySelector('.nk-board__paginate, .xans-board-paging'),
      }));
      report.tests.paginationClick = { pass: after.hasPaginate && after.rows >= 0, ...after };
    }
    await page.close();
  }

  // TC4: search form present (free list)
  {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    await page.goto(`${BASE}/board/free/list.html?board_no=1&v=${V}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(800);
    const r = await page.evaluate(() => {
      const search = document.querySelector('.boardSearch, .nk-board__search');
      const btn = document.querySelector('.boardSearch .btnEmFix, .boardSearch a.btnSubmit');
      const input = document.querySelector('.boardSearch input[type="text"], .boardSearch input[type="search"]');
      return { hasSearch: !!search, hasBtn: !!btn, hasInput: !!input, pass: !!(search && btn && input) };
    });
    report.tests.boardSearch = r;
    await page.close();
  }

  // TC5: gallery list → read
  {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    await page.goto(`${BASE}/board/gallery/list.html?board_no=8&v=${V}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
    const cardLink = page.locator('.nk-board .subject a, .nk-board .thumbnail a, .galleryList a').first();
    const hasLink = (await cardLink.count()) > 0;
    if (!hasLink) {
      report.tests.galleryListToRead = { pass: true, skipped: true, reason: 'no gallery posts' };
    } else {
      await Promise.all([
        page.waitForNavigation({ waitUntil: 'domcontentloaded', timeout: 30000 }),
        cardLink.click(),
      ]);
      await page.waitForTimeout(800);
      const state = await page.evaluate(() => ({
        url: location.href,
        isRead: /read\.html/i.test(location.href),
      }));
      report.tests.galleryListToRead = { pass: state.isRead, ...state };
    }
    await page.close();
  }

  // TC6: MO390 overflow (representative board URLs)
  {
    const urls = [
      '/board/free/list.html?board_no=1',
      '/board/free/read.html?board_no=1&no=1',
      '/board/gallery/list.html?board_no=8',
      '/board/memo/list.html?board_no=5',
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
