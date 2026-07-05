import { mkdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { chromium } from 'playwright';
const outDir = resolve(process.argv[2] || './shots');
mkdirSync(outDir, { recursive: true });
const PAGES = [
  { name: 'ref401949_form', url: 'https://ecudemo401949.cafe24.com/omc_skill_%EC%A0%84%EC%B2%B4%EB%AA%A9%EB%A1%9D.html' },
  { name: 'ref401788_join', url: 'https://ecudemo401788.cafe24.com/member/join.html' },
  { name: 'ref401788_login', url: 'https://ecudemo401788.cafe24.com/member/login.html' },
];
const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1440, height: 960 }, isMobile: false });
for (const p of PAGES) {
  const page = await ctx.newPage();
  try {
    await page.goto(p.url, { waitUntil: 'networkidle', timeout: 45000 });
    await page.waitForTimeout(900);
    await page.screenshot({ path: `${outDir}/${p.name}.png`, fullPage: true });
    console.log('OK', p.name, page.url());
  } catch (e) { console.log('XX', p.name, String(e)); }
  await page.close();
}
await browser.close();
