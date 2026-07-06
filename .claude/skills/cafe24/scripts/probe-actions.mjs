import { chromium } from 'playwright';
const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1440, height: 960 }, isMobile: false });
const page = await ctx.newPage();
await page.goto('https://ecudemo402307.cafe24.com/member/join.html', { waitUntil: 'networkidle', timeout: 45000 });
const d = await page.evaluate(() => {
  const a = document.querySelector('.nk-join-actions');
  if (!a) return { none: true };
  const p = a.parentElement;
  const btn = a.querySelector('.nk-mbr-btn');
  return {
    actions: { w: a.getBoundingClientRect().width, display: getComputedStyle(a).display, maxWidth: getComputedStyle(a).maxWidth },
    parent: { tag: p.tagName, cls: p.className, display: getComputedStyle(p).display, flexDir: getComputedStyle(p).flexDirection },
    btn: btn ? { w: btn.getBoundingClientRect().width, display: getComputedStyle(btn).display, width: getComputedStyle(btn).width } : null,
  };
});
console.log(JSON.stringify(d, null, 2));
await browser.close();
