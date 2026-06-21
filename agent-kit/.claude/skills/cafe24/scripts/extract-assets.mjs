/**
 * extract-assets.mjs — 레퍼런스 URL → 이미지 인벤토리 (입력 파이프라인 P3)
 * ---------------------------------------------------------------------------
 * cafe24-ez 가 <img src> 만 훑어 CSS background-image 로 들어간 히어로/배너를 통째로
 * 놓치던 문제(P3) 해결. <img src/srcset/data-src> + <picture> + computed background-image
 * + <video poster> 까지 전부 수집해 인벤토리 JSON 을 만든다.
 *
 * [사용]
 *   npm i -D playwright && npx playwright install chromium
 *   node extract-assets.mjs --url https://레퍼런스 --out assets.json
 *
 * 데스크톱 UA 고정. 읽기·수집만 (다운로드 안 함 — URL 목록만).
 */
import { writeFileSync } from 'node:fs';

const argv = process.argv.slice(2);
const arg = (f, d) => { const i = argv.indexOf(f); return i >= 0 && argv[i + 1] ? argv[i + 1] : d; };
const url = arg('--url');
const out = arg('--out');
if (!url) { console.error('사용법: node extract-assets.mjs --url <레퍼런스URL> [--out assets.json]'); process.exit(2); }

let chromium;
try { ({ chromium } = await import('playwright')); }
catch { console.error('\n⚠️ Playwright 미설치: npm i -D playwright && npx playwright install chromium\n'); process.exit(3); }

const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1440, height: 960 }, isMobile: false });
const page = await ctx.newPage();
await page.goto(url, { waitUntil: 'networkidle', timeout: 45000 });
await page.waitForTimeout(1000); // lazy-load 트리거 위해 스크롤
await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise((r) => setTimeout(r, 120)); } window.scrollTo(0, 0); });
await page.waitForTimeout(500);

const assets = await page.evaluate((pageUrl) => {
  const abs = (u) => { try { return new URL(u, pageUrl).href; } catch (e) { return u; } };
  const found = [];
  const push = (src, kind, el) => {
    if (!src || /^data:|^javascript:/.test(src)) return;
    const r = el ? el.getBoundingClientRect() : { width: 0, height: 0, top: 0 };
    found.push({ url: abs(src.trim()), kind, w: Math.round(r.width), h: Math.round(r.height), top: Math.round(r.top + window.scrollY) });
  };

  // <img src / srcset / data-src / data-original>
  document.querySelectorAll('img').forEach((el) => {
    push(el.currentSrc || el.getAttribute('src'), 'img', el);
    ['data-src', 'data-original', 'data-lazy'].forEach((a) => el.getAttribute(a) && push(el.getAttribute(a), 'img-lazy', el));
    (el.getAttribute('srcset') || '').split(',').forEach((s) => { const u = s.trim().split(/\s+/)[0]; if (u) push(u, 'img-srcset', el); });
  });
  // <picture><source srcset>
  document.querySelectorAll('picture source').forEach((el) => (el.getAttribute('srcset') || '').split(',').forEach((s) => { const u = s.trim().split(/\s+/)[0]; if (u) push(u, 'picture', el); }));
  // <video poster>
  document.querySelectorAll('video[poster]').forEach((el) => push(el.getAttribute('poster'), 'video-poster', el));
  // computed background-image (★ 히어로/배너 단골)
  Array.prototype.slice.call(document.querySelectorAll('body *')).slice(0, 4000).forEach((el) => {
    const bg = getComputedStyle(el).backgroundImage;
    if (bg && bg !== 'none') { const m = bg.match(/url\(["']?([^"')]+)["']?\)/g); if (m) m.forEach((one) => { const u = one.replace(/url\(["']?|["']?\)/g, ''); push(u, 'background', el); }); }
  });
  return found;
}, url);
await browser.close();

// dedupe + 히어로 후보 표시 (상단 + 큰 면적)
const seen = new Set();
const uniq = assets.filter((a) => { if (seen.has(a.url + a.kind)) return false; seen.add(a.url + a.kind); return true; });
uniq.forEach((a) => { a.heroCandidate = (a.top < 900 && a.w >= 600 && a.h >= 200) || (a.kind === 'background' && a.top < 900 && a.w >= 800); });

const report = {
  site_url: url,
  extracted_at: new Date().toISOString().slice(0, 10),
  total: uniq.length,
  byKind: uniq.reduce((m, a) => { m[a.kind] = (m[a.kind] || 0) + 1; return m; }, {}),
  heroCandidates: uniq.filter((a) => a.heroCandidate),
  all: uniq
};
const json = JSON.stringify(report, null, 2);
if (out) { writeFileSync(out, json, 'utf8'); console.log('저장:', out); }
console.log(`이미지 ${report.total}개 (종류: ${JSON.stringify(report.byKind)}) · 히어로 후보 ${report.heroCandidates.length}개`);
report.heroCandidates.forEach((a) => console.log(`  ★ ${a.kind} ${a.w}x${a.h} @top${a.top}  ${a.url}`));
console.log('\n★ background-image/srcset/picture 까지 수집됨 — <img src>만 보던 P3 한계 해소.');
if (!out) console.log('(전체 목록은 --out assets.json 으로 저장)');
