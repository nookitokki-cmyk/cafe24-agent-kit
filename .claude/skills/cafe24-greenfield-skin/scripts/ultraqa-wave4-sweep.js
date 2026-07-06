// G8 ultraqa-wave4 (cafe24-greenfield-skin — mall-agnostic)
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { resolveConfig } = require('./lib/resolve-config');
const { resolveUltraqaPages } = require('./lib/apply-batch-overrides');
const { grepPreflightHigh } = require('./lib/grep-preflight');
const { DEFAULT_ULTRAQA_PAGES } = require('./config/ultraqa-pages');

const argv = process.argv.slice(2);
const cfg = resolveConfig(argv);
const BASE = cfg.base;
const OUT = path.join(cfg.wave4OutDir, '_ultraqa-wave4-report.json');
const PAGES = resolveUltraqaPages(DEFAULT_ULTRAQA_PAGES, cfg.overrides);
const STOCK_HOVER = ['rgb(0, 139, 204)', 'rgb(0, 159, 250)', '#008bcc', '#009ffa'];
const CREAM = 'rgb(250, 249, 245)';
const CORAL = 'rgb(204, 120, 92)';

const report = {
  timestamp: new Date().toISOString(),
  criteria: {},
  overflow: {},
  variableLeak: [],
  hoverLegacy: [],
  mobileWeb: null,
  defects: [],
};

async function checkOverflow(page, key) {
  const w = await page.evaluate(() => ({
    sw: document.documentElement.scrollWidth,
    cw: document.documentElement.clientWidth,
    bodyNk: document.body.classList.contains('nk-skin'),
    mobileWeb: document.body.getAttribute('data-mobile-web'),
  }));
  report.overflow[key] = w;
  if (w.sw > w.cw + 2) report.defects.push({ key, type: 'overflow', sw: w.sw, cw: w.cw });
  return w;
}

async function checkVariableLeak(page) {
  return page.evaluate(() => {
    const leaks = [];
    const visible = (el) => {
      if (!el) return false;
      let n = el;
      while (n && n !== document.body) {
        const s = getComputedStyle(n);
        if (s.display === 'none' || s.visibility === 'hidden' || s.opacity === '0') return false;
        n = n.parentElement;
      }
      const r = el.getBoundingClientRect();
      return r.width > 0 && r.height > 0;
    };
    const walk = (el) => {
      if (!el || el.nodeType !== 3) {
        for (const ch of el.childNodes || []) walk(ch);
        return;
      }
      const t = el.textContent || '';
      if (/\{\$[a-zA-Z_]/.test(t)) {
        const parent = el.parentElement;
        if (parent && visible(parent)) leaks.push(t.trim().slice(0, 80));
      }
    };
    walk(document.body);
    return leaks.slice(0, 10);
  });
}

async function run() {
  const preflight = grepPreflightHigh(cfg.cssDir);
  report.criteria.preflightHigh0 = preflight;

  const browser = await chromium.launch();
  const vps = [
    ['pc1440', { width: 1440, height: 900 }, undefined],
    ['mo390', { width: 390, height: 844 }, 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'],
  ];

  for (const [vpName, vp, ua] of vps) {
    const ctx = await browser.newContext({ viewport: vp, userAgent: ua });
    const page = await ctx.newPage();
    for (const [name, url] of PAGES) {
      const key = `${name}-${vpName}`;
      try {
        await page.goto(`${BASE}${url}?v=w4g8`, { waitUntil: 'domcontentloaded', timeout: 45000 });
        await page.waitForTimeout(1200);
        const w = await checkOverflow(page, key);
        if (vpName === 'mo390' && name === 'index') {
          report.mobileWeb = { mobileWebAttr: w.mobileWeb, bodyNk: w.bodyNk, pass: w.bodyNk && w.mobileWeb !== 'true' };
        }
        const leaks = await checkVariableLeak(page);
        if (leaks.length) report.variableLeak.push({ key, leaks });
      } catch (e) {
        report.defects.push({ key, type: 'error', msg: String(e).slice(0, 200) });
      }
    }
    await ctx.close();
  }

  const ctx2 = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const p2 = await ctx2.newPage();
  await p2.goto(`${BASE}/?v=w4g8`, { waitUntil: 'domcontentloaded' });
  await p2.waitForTimeout(1200);

  const gnb = p2.locator('.nk-gnb__link').first();
  if (await gnb.count()) {
    await gnb.hover();
    await p2.waitForTimeout(600);
    const sub = await p2.evaluate(() => {
      const el = document.querySelector('.nk-gnb__item .sub-category, .nk-gnb__item > ul, .nk-gnb__sub');
      if (!el) return null;
      const s = getComputedStyle(el);
      return { bg: s.backgroundColor, color: s.color };
    });
    report.criteria.gnbHover = sub;
    if (sub && !sub.bg.includes('250, 249, 245') && sub.bg !== CREAM) {
      report.hoverLegacy.push({ where: 'gnb-dropdown', bg: sub.bg });
    }
  }

  const cta = await p2.evaluate(() => {
    const el = document.querySelector('.nk-pdp__actions .btnSubmit, .nk-btn-coral, a[class*="btnSubmit"]');
    if (!el) return null;
    const s = getComputedStyle(el);
    return { bg: s.backgroundColor, color: s.color };
  });
  report.criteria.ctaSample = cta;

  await p2.goto(`${BASE}/product/list.html?cate_no=${cfg.overrides.plpCateNo || 24}&v=w4g8`);
  await p2.waitForTimeout(1000);
  const linkHover = await p2.evaluate(() => {
    const a = document.querySelector('.nk-prd__thumb a, .prdList a');
    if (!a) return null;
    a.dispatchEvent(new MouseEvent('mouseenter', { bubbles: true }));
    const s = getComputedStyle(a);
    return { color: s.color };
  });
  if (linkHover && STOCK_HOVER.some((c) => linkHover.color.includes(c.replace('rgb(', '').replace(')', '')))) {
    report.hoverLegacy.push({ where: 'plp-link', color: linkHover.color });
  }

  await ctx2.close();
  await browser.close();

  const screenCount = Object.keys(report.overflow).length;
  report.criteria.overflow0 = { screens: screenCount, defects: report.defects.filter((d) => d.type === 'overflow').length, pass: report.defects.filter((d) => d.type === 'overflow').length === 0 };
  report.criteria.variableLeak0 = { leaks: report.variableLeak.length, pass: report.variableLeak.length === 0 };
  report.criteria.hoverLegacy0 = { hits: report.hoverLegacy.length, pass: report.hoverLegacy.length === 0 };
  report.criteria.mobileWebFalse = report.mobileWeb || { pass: false };

  report.pass =
    preflight.pass &&
    report.criteria.overflow0.pass &&
    report.criteria.variableLeak0.pass &&
    report.criteria.mobileWebFalse.pass &&
    report.criteria.hoverLegacy0.pass;

  fs.writeFileSync(OUT, JSON.stringify(report, null, 2));
  console.log('ULTRAQA pass=', report.pass, 'screens=', screenCount, 'overflow defects=', report.criteria.overflow0.defects);
  console.log('preflight=', preflight.pass, 'vars=', report.criteria.variableLeak0.pass, 'hover=', report.criteria.hoverLegacy0.pass);
  process.exit(report.pass ? 0 : 1);
}

run().catch((e) => { console.error(e); process.exit(1); });
