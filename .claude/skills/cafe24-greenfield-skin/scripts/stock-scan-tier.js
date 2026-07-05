// W4 4-tier stock CSS scanner (cafe24-greenfield-skin — mall-agnostic)
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { resolveConfig } = require('./lib/resolve-config');
const { applyBatchOverrides } = require('./lib/apply-batch-overrides');
const { RAW_BATCHES } = require('./config/batches');

const argv = process.argv.slice(2);
const cfg = resolveConfig(argv);
const BASE = cfg.base;
const OUT = cfg.wave4OutDir;
const PLP_CATE = cfg.overrides.plpCateNo || 24;
const BATCHES = applyBatchOverrides(RAW_BATCHES, cfg.overrides);

const STOCK_BORDER = ['215, 213, 213', '223, 223, 223', '232, 232, 232', '232, 228, 227', '209, 209, 209'];
const STOCK_COLOR = ['0, 139, 204', '0, 159, 250', '46, 46, 46'];
const TOKEN_LINE = ['235, 230, 223', '230, 223, 216', '20, 20, 19', '245, 245, 240'];
const TOKEN_POINT = ['204, 120, 92'];

const SUBUNIT_SELECTORS = [
  'form[id]',
  'fieldset',
  '.nk-join-row',
  'tr[id]',
  'li[id$="_wrap"]',
  '.agreeArea',
  '.ec-base-table',
  '.eTooltip',
  '.check',
];

const LOGIN_ID = cfg.loginId;
const LOGIN_PW = cfg.loadPassword();

async function login(page) {
  if (!LOGIN_PW) throw new Error('CAFE24_TEST_PW or sftp config password required for login batch');
  await page.goto(BASE + '/member/login.html', { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(800);
  await page.locator('input[name="member_id"], #member_id').first().fill(LOGIN_ID);
  await page.locator('input[name="member_passwd"], input[type="password"]').first().fill(LOGIN_PW);
  await page.locator('.nk-btn-login, a.btnLogin, .btnLogin').first().click();
  await page.waitForTimeout(2500);
  if (page.url().includes('/member/login')) throw new Error('login failed');
}

async function resolveOrderDetailUrl(page) {
  await page.goto(BASE + '/myshop/order/list.html', { waitUntil: 'domcontentloaded', timeout: 45000 });
  await page.waitForTimeout(1200);
  const href = await page.locator('a[href*="order/detail"], .orderList a[href*="detail"]').first().getAttribute('href').catch(() => null);
  if (href) {
    const p = href.startsWith('http') ? new URL(href).pathname + new URL(href).search : href;
    return p.startsWith('/') ? p : '/' + p;
  }
  return '/myshop/order/detail.html';
}

async function resolveProductDetailUrl(page) {
  await page.goto(BASE + '/product/list.html?cate_no=' + PLP_CATE, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await page.waitForTimeout(1200);
  const href = await page.locator('.nk-prd__thumb a[href*="detail"], .prdList a[href*="product/detail"], a[href*="/product/detail"]').first().getAttribute('href').catch(() => null);
  if (href) {
    const p = href.startsWith('http') ? new URL(href).pathname + new URL(href).search : href;
    return p.startsWith('/') ? p : '/' + p;
  }
  return '/product/detail.html?product_no=10';
}

function parseArgs(argv) {
  const tierIdx = argv.indexOf('--tier');
  const urlIdx = argv.indexOf('--url');
  const batchIdx = argv.indexOf('--batch');
  return {
    tier: tierIdx >= 0 ? argv[tierIdx + 1] : 'page',
    url: urlIdx >= 0 ? argv[urlIdx + 1] : null,
    batch: batchIdx >= 0 ? argv[batchIdx + 1] : null,
  };
}

function scanSubtree(root, stockBorder, scopeLabel) {
  const norm = (s) => (s || '').replace(/\s+/g, ' ').trim();
  const borderWidth = (val) => {
    if (!val || val === 'none') return 0;
    const m = norm(val).match(/^([\d.]+)px/);
    return m ? parseFloat(m[1]) : 0;
  };
  const isDefectBorder = (val) => borderWidth(val) > 0;
  const isStockColor = (val) => {
    if (!val) return false;
    return STOCK_COLOR.some((c) => val.includes(c));
  };
  const hits = [];
  const walk = (el, depth) => {
    if (depth > 14 || !el || el.nodeType !== 1) return;
    if (root !== el && !root.contains(el)) return;
    const r = el.getBoundingClientRect();
    if (r.width < 2 && r.height < 2) return;
    const tag = el.tagName.toLowerCase();
    if (['script', 'style', 'svg', 'path'].includes(tag)) return;
    const s = getComputedStyle(el);
    if (s.display === 'none' || s.visibility === 'hidden') return;
    const issues = [];
    const borderB = norm(s.borderBottom);
    const borderT = norm(s.borderTop);
    const borderL = norm(s.borderLeft);
    const borderR = norm(s.borderRight);
    const outline = norm(s.outline);
    const color = norm(s.color);
    const fs = s.fontSize;
    if (isDefectBorder(borderB)) issues.push('borderBottom:' + borderB);
    if (isDefectBorder(borderT)) issues.push('borderTop:' + borderT);
    if (isDefectBorder(borderL)) issues.push('borderLeft:' + borderL);
    if (isDefectBorder(borderR)) issues.push('borderRight:' + borderR);
    if (isDefectBorder(outline)) issues.push('outline:' + outline);
    if (isStockColor(color)) issues.push('color:' + color);
    if (fs === '12px' && ['input', 'select', 'textarea'].includes(tag)) issues.push('fontSize:12px');
    const before = getComputedStyle(el, '::before');
    if (before && before.display !== 'none' && before.content !== 'none' && before.content !== '""') {
      const bbg = norm(before.backgroundColor);
      if (stockBorder.some((c) => bbg.includes(c))) issues.push('::before bg:' + bbg);
      if (isDefectBorder(norm(before.borderBottom)) || isDefectBorder(norm(before.borderTop))) {
        issues.push('::before border');
      }
    }
    if (issues.length) {
      let sel = el.id ? '#' + el.id : el.className ? '.' + String(el.className).split(/\s+/).slice(0, 2).join('.') : tag;
      hits.push({ scope: scopeLabel, selector: sel, tag, issues, depth });
    }
    for (const ch of el.children) walk(ch, depth + 1);
  };
  walk(root, 0);
  return hits.slice(0, 40);
}

async function scanUrl(page, urlPath, tier) {
  const full = BASE + urlPath + (urlPath.includes('?') ? '&' : '?') + 'v=w4t' + Date.now();
  await page.goto(full, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await page.waitForTimeout(1200);

  const payload = await page.evaluate(({ tier, stockBorder, subunitSelectors, tokenLine, tokenPoint, stockBorderColors }) => {
    const norm = (s) => (s || '').replace(/\s+/g, ' ').trim();
    const borderWidth = (val) => {
      if (!val || val === 'none') return 0;
      const m = norm(val).match(/^([\d.]+)px/);
      return m ? parseFloat(m[1]) : 0;
    };
    const sideDefect = (widthVal, colorVal) => {
      if (borderWidth(widthVal) <= 0) return false;
      const c = norm(colorVal);
      if (!c || c === 'transparent' || c.includes('rgba(0, 0, 0, 0)')) return false;
      if (tokenLine.some((t) => c.includes(t))) return false;
      if (tokenPoint.some((t) => c.includes(t))) return false;
      if (stockBorderColors.some((t) => c.includes(t))) return true;
      return false;
    };
    const isStockColor = (val) => {
      if (!val) return false;
      return ['0, 139, 204', '0, 159, 250', '46, 46, 46'].some((c) => val.includes(c));
    };
    const scanSubtree = (root, scopeLabel) => {
      const hits = [];
      const walk = (el, depth) => {
        if (depth > 14 || !el || el.nodeType !== 1) return;
        if (root !== el && !root.contains(el)) return;
        const r = el.getBoundingClientRect();
        if (r.width < 2 && r.height < 2) return;
        const tag = el.tagName.toLowerCase();
        if (['script', 'style', 'svg', 'path'].includes(tag)) return;
        const s = getComputedStyle(el);
        if (s.display === 'none' || s.visibility === 'hidden') return;
        const issues = [];
        const borderB = norm(s.borderBottom);
        const borderT = norm(s.borderTop);
        const borderL = norm(s.borderLeft);
        const borderR = norm(s.borderRight);
        const outline = norm(s.outline);
        const color = norm(s.color);
        const fs = s.fontSize;
        if (sideDefect(borderB, s.borderBottomColor)) issues.push('borderBottom:' + borderB);
        if (sideDefect(borderT, s.borderTopColor)) issues.push('borderTop:' + borderT);
        if (sideDefect(borderL, s.borderLeftColor)) issues.push('borderLeft:' + borderL);
        if (sideDefect(borderR, s.borderRightColor)) issues.push('borderRight:' + borderR);
        if (sideDefect(outline, s.outlineColor)) issues.push('outline:' + outline);
        if (isStockColor(color)) issues.push('color:' + color);
        if (fs === '12px' && ['input', 'select', 'textarea'].includes(tag)) issues.push('fontSize:12px');
        const before = getComputedStyle(el, '::before');
        if (before && before.display !== 'none' && before.content !== 'none' && before.content !== '""') {
          const bbg = norm(before.backgroundColor);
          if (stockBorder.some((c) => bbg.includes(c))) issues.push('::before bg:' + bbg);
          if (sideDefect(norm(before.borderBottom), before.borderBottomColor) || sideDefect(norm(before.borderTop), before.borderTopColor)) {
            issues.push('::before border');
          }
        }
        if (issues.length) {
          let sel = el.id ? '#' + el.id : el.className ? '.' + String(el.className).split(/\s+/).slice(0, 2).join('.') : tag;
          hits.push({ scope: scopeLabel, selector: sel, tag, issues, depth });
        }
        for (const ch of el.children) walk(ch, depth + 1);
      };
      walk(root, 0);
      return hits.slice(0, 40);
    };

    function deriveXansFingerprint(classList) {
      const xans = [...classList].filter((c) => c.startsWith('xans-'));
      const specific = xans
        .filter((c) => !/^xans-element-?$/.test(c) && !/^xans-record-?$/.test(c) && c.includes('-'))
        .sort((a, b) => b.length - a.length);
      return specific[0] || xans.find((c) => !/^xans-element-?$/.test(c)) || 'unknown';
    }

    const blocks = [];
    if (tier === 'module') {
      const seen = new Set();
      const addModuleBlock = (el, mod, root) => {
        const key = mod + '|' + root;
        if (seen.has(key)) return;
        seen.add(key);
        const label = 'module:' + mod;
        const v = scanSubtree(el, label);
        blocks.push({ label, module: mod, root, violations: v, count: v.length });
      };

      document.querySelectorAll('[module]').forEach((el) => {
        const mod = (el.getAttribute('module') || '').trim();
        if (mod) addModuleBlock(el, mod, 'module-attr');
      });

      if (blocks.length === 0) {
        document.querySelectorAll('[class*="xans-element-"]').forEach((el) => {
          const fp = deriveXansFingerprint(el.classList);
          addModuleBlock(el, fp, 'xans-element');
        });
        if (blocks.length === 0) {
          document.querySelectorAll('[class*="xans-record-"]').forEach((el) => {
            const fp = deriveXansFingerprint(el.classList);
            addModuleBlock(el, fp, 'xans-record');
          });
        }
      }
    } else if (tier === 'submodule') {
      document.querySelectorAll('[module]').forEach((modEl) => {
        const mod = modEl.getAttribute('module') || 'unknown';
        const seen = new Set();
        subunitSelectors.forEach((sel) => {
          modEl.querySelectorAll(sel).forEach((el) => {
            if (seen.has(el)) return;
            seen.add(el);
            const idPart = el.id ? '#' + el.id : '';
            const clsPart = el.className ? '.' + String(el.className).split(/\s+/).filter(Boolean).slice(0, 2).join('.') : '';
            const label = 'submodule:' + mod + ':' + el.tagName.toLowerCase() + idPart + clsPart;
            const v = scanSubtree(el, label);
            blocks.push({ label, module: mod, subunit: sel, violations: v, count: v.length });
          });
        });
      });
    } else if (tier === 'section') {
      const seen = new Set();
      const roots = [];
      const popupRoots = document.querySelectorAll('#popup, #layer, .ec-base-layer, .ec-base-layer-area');
      popupRoots.forEach((el) => roots.push(el));
      document.querySelectorAll('[class*="nk-"]').forEach((el) => {
        const cls = String(el.className || '');
        if (!/\bnk-[a-z0-9_-]*(wrap|head|section|box|form|page|mbr|fid|fpi|fpm|fpq|myshop|inner|table|board|plp|pdp|order|etc|coupon|attend|shopinfo|prd)\b/i.test(cls)) return;
        let dominated = false;
        for (const r of roots) {
          if (r.contains(el) && r !== el) { dominated = true; break; }
        }
        if (!dominated) roots.push(el);
      });
      roots.forEach((el) => {
        const cls = String(el.className || '').split(/\s+/).slice(0, 2).join('.');
        const label = 'section:.' + cls;
        if (seen.has(label)) return;
        seen.add(label);
        const v = scanSubtree(el, label);
        blocks.push({ label, violations: v, count: v.length });
      });
    } else {
      const v = scanSubtree(document.body, 'page');
      blocks.push({ label: 'page', violations: v, count: v.length });
    }
    const total = blocks.reduce((n, b) => n + b.count, 0);
    return { url: location.href, tier, blocks, total, pass: total === 0 };
  }, { tier, stockBorder: STOCK_BORDER, subunitSelectors: SUBUNIT_SELECTORS, tokenLine: TOKEN_LINE, tokenPoint: TOKEN_POINT, stockBorderColors: STOCK_BORDER });

  return { path: urlPath, ...payload };
}

const FRAGMENT_ACCEPT = new Set(BATCHES.fragment || []);

async function main() {
  const { tier, url, batch } = parseArgs(argv);
  if (!['module', 'submodule', 'section', 'page'].includes(tier)) {
    console.error('Usage: --tier module|submodule|section|page [--url PATH | --batch default|member|myshop|w-b|popup]');
    process.exit(1);
  }

  let urls;
  const needsBatchLogin = batch === 'myshop' || batch === 'popup';
  const memberPerUrlLogin = batch === 'member';
  const isPopup = batch === 'popup';
  const isFragment = batch === 'fragment';
  if (url) urls = [url.startsWith('/') ? url : '/' + url];
  else urls = BATCHES[batch || 'default'] || BATCHES.default;

  const viewport = isPopup ? { width: 800, height: 640 } : { width: 1440, height: 900 };
  const browser = await chromium.launch();
  const report = { tier, batch: batch || 'default', login: null, scanned: [], totalViolations: 0, pass: true };

  let sharedPage = null;
  let sharedCtx = null;

  if (!memberPerUrlLogin) {
    sharedCtx = await browser.newContext({ viewport });
    sharedPage = await sharedCtx.newPage();
  }

  if (batch === 'product' || batch === 'w-b') {
    const probePage = sharedPage || (await (await browser.newContext({ viewport })).newPage());
    const detailPath = await resolveProductDetailUrl(probePage);
    urls = urls.map((u) => (u === '/product/detail.html' ? detailPath : u));
    if (!sharedPage) await probePage.context().close();
  }

  if (needsBatchLogin) {
    try {
      await login(sharedPage);
      report.login = 'ok';
      const detailPath = await resolveOrderDetailUrl(sharedPage);
      urls = urls.map((u) => (u === '/myshop/order/detail.html' ? detailPath : u));
    } catch (e) {
      report.login = String(e.message);
      fs.writeFileSync(path.join(OUT, '_stock-scan-tier-' + (batch || 'default') + '-' + tier + '-report.json'), JSON.stringify(report, null, 2));
      console.error('LOGIN FAIL', e.message);
      await browser.close();
      process.exit(1);
    }
  }

  for (const u of urls) {
    let page = sharedPage;
    let ctx = sharedCtx;
    if (memberPerUrlLogin) {
      ctx = await browser.newContext({ viewport });
      page = await ctx.newPage();
      if (memberUrlNeedsLogin(u)) {
        try {
          await login(page);
          report.login = 'ok';
        } catch (e) {
          report.login = String(e.message);
          report.scanned.push({ path: u, tier, error: 'login failed: ' + e.message });
          report.pass = false;
          await ctx.close();
          continue;
        }
      }
    }
    try {
      const r = await scanUrl(page, u, tier);
      if (isFragment && FRAGMENT_ACCEPT.has(u)) {
        r.accepted = '수용(부모페이지CSS상속·조각inc)';
        r.pass = true;
      }
      report.scanned.push(r);
      if (!isFragment || !r.accepted) report.totalViolations += r.total;
      if (!r.pass) report.pass = false;
      console.log(u, tier, 'violations=', r.total, r.accepted || '');
    } catch (e) {
      if (isFragment && FRAGMENT_ACCEPT.has(u)) {
        report.scanned.push({ path: u, tier, accepted: '수용(부모페이지CSS상속·조각inc)', pass: true });
        console.log(u, tier, '수용 fragment');
      } else {
        report.scanned.push({ path: u, tier, error: String(e).slice(0, 200) });
        report.pass = false;
      }
    }
    if (memberPerUrlLogin && ctx) await ctx.close();
  }

  await browser.close();
  const outPath = path.join(OUT, '_stock-scan-tier-' + (batch || 'default') + '-' + tier + '-report.json');
  fs.writeFileSync(outPath, JSON.stringify(report, null, 2));
  console.log('TIER=', tier, 'PASS=', report.pass, 'total=', report.totalViolations);
  process.exit(report.pass ? 0 : 1);
}

main().catch((e) => { console.error(e); process.exit(1); });
