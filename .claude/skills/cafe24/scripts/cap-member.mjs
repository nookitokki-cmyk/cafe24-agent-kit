/**
 * cap-member.mjs — ecudemo402307 회원 폼(login/join/modify) PC+MO 캡처
 * modify.html 은 로그인 필요 → 동일 컨텍스트에서 선(先)로그인 후 캡처.
 *   node cap-member.mjs --out <dir> --tag <before|after> --v <verParam> --id test1111 --pw "..."
 */
import { mkdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { chromium } from 'playwright';

const argv = process.argv.slice(2);
const arg = (f, d) => { const i = argv.indexOf(f); return i >= 0 && argv[i + 1] ? argv[i + 1] : d; };
const outDir = resolve(arg('--out', './shots'));
const tag = arg('--tag', 'shot');
const ver = arg('--v', '');
const ID = arg('--id', 'test1111');
const PW = arg('--pw', '');
const base = 'https://ecudemo402307.cafe24.com';
const q = ver ? `?v=${ver}` : '';

mkdirSync(outDir, { recursive: true });

const VPS = [
  { tag: 'pc', width: 1440, height: 960 },
  { tag: 'mo', width: 390, height: 844 },
];

const PAGES = [
  { name: 'login', url: `${base}/member/login.html${q}`, auth: false },
  { name: 'join', url: `${base}/member/join.html${q}`, auth: false },
  { name: 'modify', url: `${base}/member/modify.html${q}`, auth: true },
];

const browser = await chromium.launch();
const saved = [];

async function settle(page) {
  await page.evaluate(async () => {
    const h = document.body.scrollHeight;
    for (let y = 0; y < h; y += 700) { window.scrollTo(0, y); await new Promise((r) => setTimeout(r, 120)); }
    window.scrollTo(0, 0);
  });
  await page.waitForTimeout(700);
}

for (const vp of VPS) {
  const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height }, isMobile: false });
  // 로그인 1회 (auth 페이지용)
  let loggedIn = false;
  const login = async (page) => {
    if (loggedIn) return true;
    await page.goto(`${base}/member/login.html`, { waitUntil: 'networkidle', timeout: 45000 });
    try {
      await page.fill('#member_id, input[name="member_id"]', ID, { timeout: 8000 });
      await page.fill('#member_passwd, input[name="member_passwd"]', PW, { timeout: 8000 });
      await Promise.all([
        page.waitForNavigation({ waitUntil: 'networkidle', timeout: 20000 }).catch(() => {}),
        page.click('.nk-btn-login, a.btnSubmit, input[type="submit"], button[type="submit"], .btnLogin', { timeout: 8000 }).catch(async () => {
          await page.press('#member_passwd, input[name="member_passwd"]', 'Enter');
        }),
      ]);
      loggedIn = true;
      return true;
    } catch (e) { return false; }
  };

  for (const p of PAGES) {
    const page = await ctx.newPage();
    const file = `${outDir}/${p.name}_${tag}_${vp.tag}.png`;
    try {
      if (p.auth) {
        const ok = await login(page);
        if (!ok) throw new Error('login failed');
      }
      const resp = await page.goto(p.url, { waitUntil: 'networkidle', timeout: 45000 });
      await settle(page);
      const finalUrl = page.url();
      await page.screenshot({ path: file, fullPage: true });
      saved.push({ p: p.name, vp: vp.tag, file, ok: true, status: resp && resp.status(), finalUrl });
    } catch (e) {
      saved.push({ p: p.name, vp: vp.tag, file, ok: false, err: String(e) });
    }
    await page.close();
  }
  await ctx.close();
}
await browser.close();

console.log('\n══════ cap-member ' + tag + ' ══════');
for (const s of saved) console.log(`  ${s.ok ? 'OK' : 'XX'} ${s.p}/${s.vp}  ${s.file}${s.status ? ' ['+s.status+']' : ''}${s.finalUrl ? ' -> '+s.finalUrl : ''}${s.err ? '  ('+s.err+')' : ''}`);
process.exit(saved.some((s) => !s.ok) ? 1 : 0);
