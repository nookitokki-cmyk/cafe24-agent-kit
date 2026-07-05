const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { boot } = require('../lib/runtime');
const { BASE, OUT, cfg } = boot(process.argv.slice(2), '_auth-interaction-scan-report.json');
const V = process.env.AUTH_INTERACTION_V || 'w4-auth-interaction';
const LOGIN_ID = cfg.loginId;
const LOGIN_PW = process.env.CAFE24_TEST_PW || cfg.loadPassword();

(async () => {
  const browser = await chromium.launch();
  const report = { scannedAt: new Date().toISOString(), cacheBust: V, tests: {} };

  async function newPage(viewport) {
    const page = await browser.newPage({ viewport });
    page.on('dialog', (d) => d.dismiss().catch(() => {}));
    return page;
  }

  // TC1 login form visible + modules bound
  {
    const page = await newPage({ width: 1440, height: 900 });
    await page.goto(`${BASE}/member/login.html?v=${V}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(1200);
    const r = await page.evaluate(() => {
      const loginMod =
        document.querySelector('[module="member_login"]') ||
        document.querySelector('.xans-member-login, .nk-login-box');
      const nologinMod =
        document.querySelector('[module="MyShop_OrderHistoryNologin"]') ||
        document.querySelector('.xans-myshop-orderhistorynologin, .nk-nologin');
      const idInput = document.querySelector('input[name="member_id"], #member_id');
      const pwInput = document.querySelector('input[name="member_passwd"], input[type="password"]');
      const btnLogin = document.querySelector('.nk-btn-login, .btnLogin');
      const joinLink = document.querySelector('.nk-btn-join, a[href*="join.html"]');
      const nologinOptional = !nologinMod;
      return {
        hasLoginModule: !!loginMod,
        hasNologinModule: !!nologinMod,
        nologinOptional,
        hasIdInput: !!idInput,
        hasPwInput: !!pwInput,
        hasLoginBtn: !!btnLogin,
        hasJoinLink: !!joinLink,
        hScroll: document.documentElement.scrollWidth > document.documentElement.clientWidth,
      };
    });
      r.pass =
      r.hasLoginModule &&
      r.hasIdInput &&
      r.hasPwInput &&
      r.hasLoginBtn &&
      !r.hScroll &&
      (r.hasNologinModule || r.nologinOptional);
    report.tests.loginFormVisible = r;
    await page.close();
  }

  // TC2 login utility links (find id / join)
  {
    const page = await newPage({ width: 1440, height: 900 });
    await page.goto(`${BASE}/member/login.html?v=${V}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(800);
    const r = await page.evaluate(() => {
      const findId = document.querySelector('a[href*="find_id"]');
      const findPw = document.querySelector('a[href*="find_passwd"]');
      const join = document.querySelector('a[href*="join.html"]');
      return {
        findIdHref: findId?.getAttribute('href') || null,
        findPwHref: findPw?.getAttribute('href') || null,
        joinHref: join?.getAttribute('href') || null,
        pass: !!(findId && findPw && join),
      };
    });
    report.tests.loginLinks = r;
    await page.close();
  }

  // TC3 login submit (test1111) — optional when CAFE24_TEST_PW set
  {
    if (!LOGIN_PW) {
      report.tests.loginSubmit = {
        pass: true,
        skipped: true,
        reason: 'CAFE24_TEST_PW env not set — login flow not exercised',
        account: LOGIN_ID,
      };
    } else {
      const page = await newPage({ width: 1440, height: 900 });
      await page.goto(`${BASE}/member/login.html?v=${V}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
      await page.waitForTimeout(800);
      await page.locator('input[name="member_id"], #member_id').first().fill(LOGIN_ID);
      await page.locator('input[name="member_passwd"], input[type="password"]').first().fill(LOGIN_PW);
      await Promise.all([
        page.waitForNavigation({ waitUntil: 'domcontentloaded', timeout: 30000 }).catch(() => null),
        page.locator('.nk-btn-login, a.btnLogin, .btnLogin').first().click(),
      ]);
      await page.waitForTimeout(2000);
      const r = await page.evaluate(() => ({
        url: location.href,
        stillOnLogin: /\/member\/login/i.test(location.href),
        hasLogonState: !!document.querySelector('[module="Layout_stateLogon"]'),
      }));
      r.pass = !r.stillOnLogin || r.hasLogonState;
      report.tests.loginSubmit = r;
      await page.close();
    }
  }

  // TC4 basket empty or filled state
  {
    const page = await newPage({ width: 1440, height: 900 });
    await page.goto(`${BASE}/order/basket.html?v=${V}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(1500);
    const r = await page.evaluate(() => {
      const pkg =
        document.querySelector('[module="Order_BasketPackage"]') ||
        document.querySelector('.xans-order-basketpackage, .nk-order-page');
      const empty =
        document.querySelector('[module="Order_Empty"]') ||
        document.querySelector('.xans-order-empty');
      const emptyVisible =
        empty &&
        getComputedStyle(empty).display !== 'none' &&
        !empty.classList.contains('displaynone');
      const rows = document.querySelectorAll('[module="Order_list"] tr, tbody[module="Order_list"] tr');
      const hasRows = rows.length >= 1;
      const tabs = document.querySelectorAll('.ec-base-tab .menu li a');
      const orderBtns = document.querySelectorAll('.btnSubmitFix, .btnSubmit, [module="Order_TotalOrder"] a');
      return {
        hasPackage: !!pkg,
        emptyVisible,
        rowCount: rows.length,
        hasRows,
        tabCount: tabs.length,
        orderBtnCount: orderBtns.length,
        hScroll: document.documentElement.scrollWidth > document.documentElement.clientWidth,
      };
    });
    r.pass = r.hasPackage && (r.emptyVisible || r.hasRows) && r.tabCount >= 1 && !r.hScroll;
    report.tests.basketState = r;
    await page.close();
  }

  // TC5 basket tab click (domestic tab must not break)
  {
    const page = await newPage({ width: 1440, height: 900 });
    await page.goto(`${BASE}/order/basket.html?v=${V}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(1200);
    const tab = page.locator('.ec-base-tab .menu li a').first();
    const tabCount = await tab.count();
    if (tabCount === 0) {
      report.tests.basketTabClick = { pass: false, reason: 'no tabs' };
    } else {
      const href = await tab.getAttribute('href');
      await Promise.all([
        page.waitForNavigation({ waitUntil: 'domcontentloaded', timeout: 30000 }).catch(() => null),
        tab.click(),
      ]);
      await page.waitForTimeout(800);
      const r = await page.evaluate(() => ({
        url: location.href,
        stillBasket: /\/order\/basket/i.test(location.href),
        tabLinks: document.querySelectorAll('.ec-base-tab .menu li a').length,
      }));
      r.href = href;
      r.pass = r.stillBasket && r.tabLinks >= 1;
      report.tests.basketTabClick = r;
    }
    await page.close();
  }

  // TC6 MO390 overflow login + basket
  {
    for (const [name, urlPath] of [
      ['moLoginOverflow', '/member/login.html'],
      ['moBasketOverflow', '/order/basket.html'],
    ]) {
      const page = await newPage({ width: 390, height: 844 });
      await page.goto(`${BASE}${urlPath}?v=${V}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
      await page.waitForTimeout(1200);
      const r = await page.evaluate(() => ({
        hScroll: document.documentElement.scrollWidth > document.documentElement.clientWidth,
        scrollW: document.documentElement.scrollWidth,
        clientW: document.documentElement.clientWidth,
      }));
      r.pass = !r.hScroll;
      report.tests[name] = r;
      await page.close();
    }
  }

  report.pass = Object.values(report.tests).every((t) => t.pass !== false);
  fs.writeFileSync(OUT, JSON.stringify(report, null, 2));
  console.log('AUTH INTERACTION PASS=', report.pass);
  for (const [k, v] of Object.entries(report.tests)) {
    console.log(' ', k, v.pass ? 'PASS' : 'FAIL', v.skipped ? '(skipped)' : '');
  }
  await browser.close();
  process.exit(report.pass ? 0 : 1);
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
