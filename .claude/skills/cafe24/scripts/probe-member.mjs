import { chromium } from 'playwright';
const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1440, height: 960 }, isMobile: false });
const page = await ctx.newPage();
await page.goto('https://ecudemo402307.cafe24.com/member/join.html', { waitUntil: 'networkidle', timeout: 45000 });
const data = await page.evaluate(() => {
  const out = {};
  const wrap = document.querySelector('.nk-join-wrap');
  out.hasWrap = !!wrap;
  const inp = document.querySelector('.nk-join-wrap input[type="text"], .nk-join-wrap input[type="password"]');
  if (inp) {
    const cs = getComputedStyle(inp);
    out.input = { border: cs.border, borderBottom: cs.borderBottom, background: cs.backgroundColor, height: cs.height, borderRadius: cs.borderRadius, padding: cs.padding };
  }
  const row = document.querySelector('.nk-join-wrap .nk-join-row');
  if (row) { const cs = getComputedStyle(row); out.row = { display: cs.display, gridTemplateColumns: cs.gridTemplateColumns }; }
  const sel = document.querySelector('.nk-join-wrap select');
  if (sel) { const cs = getComputedStyle(sel); out.select = { border: cs.border, background: cs.backgroundColor }; }
  // list linked css files
  out.css = [...document.querySelectorAll('link[rel=stylesheet]')].map(l => l.href).filter(h => h.includes('_nk'));
  return out;
});
console.log(JSON.stringify(data, null, 2));
await browser.close();
