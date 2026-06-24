/**
 * extract-tokens.mjs — 레퍼런스 URL → design-tokens.json 초안 (입력 파이프라인 P4)
 * ---------------------------------------------------------------------------
 * 비코더가 색상코드를 직접 입력하지 않게, 레퍼런스 사이트의 computed style 에서
 * 색·폰트·타입스케일을 자동 추출해 design-tokens.json(=example-tokens.json 포맷) 초안을 만든다.
 *
 * ⚠️ 추출값은 **초안**이다. 휴리스틱이라 primary/accent 매핑은 사람/에이전트가 검토·보정.
 *    spacing 은 사이트마다 불규칙해 자동 추정 대신 표준 스케일을 둔다(직접 조정).
 *
 * [사용]
 *   npm i -D playwright && npx playwright install chromium
 *   node extract-tokens.mjs --url https://레퍼런스 --client 몰ID --out tokens.json
 *
 * 데스크톱 UA 고정. 아무것도 안 고친다 — 읽기·추출만.
 */
import { writeFileSync } from 'node:fs';

const argv = process.argv.slice(2);
const arg = (f, d) => { const i = argv.indexOf(f); return i >= 0 && argv[i + 1] ? argv[i + 1] : d; };
const url = arg('--url');
const client = arg('--client', 'unknown');
const out = arg('--out');
if (!url) { console.error('사용법: node extract-tokens.mjs --url <레퍼런스URL> [--client 몰ID] [--out tokens.json]'); process.exit(2); }

let chromium;
try { ({ chromium } = await import('playwright')); }
catch { console.error('\n⚠️ Playwright 미설치: npm i -D playwright && npx playwright install chromium\n'); process.exit(3); }

const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1440, height: 960 }, isMobile: false });
const page = await ctx.newPage();
await page.goto(url, { waitUntil: 'networkidle', timeout: 45000 });
await page.waitForTimeout(800);

const raw = await page.evaluate(() => {
  const lum = (r, g, b) => 0.2126 * r + 0.7152 * g + 0.0722 * b;
  const sat = (r, g, b) => { const mx = Math.max(r, g, b), mn = Math.min(r, g, b); return mx === 0 ? 0 : (mx - mn) / mx; };
  const parse = (s) => { const m = (s || '').match(/(\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?/); return m ? [+m[1], +m[2], +m[3], m[4] === undefined ? 1 : +m[4]] : null; };
  const hex = (c) => '#' + c.slice(0, 3).map((n) => n.toString(16).padStart(2, '0')).join('').toUpperCase();

  const bgArea = {}, textCnt = {};
  const els = Array.prototype.slice.call(document.querySelectorAll('body *')).slice(0, 4000);
  els.forEach((el) => {
    const cs = getComputedStyle(el), r = el.getBoundingClientRect();
    const bg = parse(cs.backgroundColor), tc = parse(cs.color);
    if (bg && bg[3] > 0.5) { const k = hex(bg); bgArea[k] = (bgArea[k] || 0) + Math.max(0, r.width) * Math.max(0, r.height); }
    if (tc && tc[3] > 0.5 && (el.textContent || '').trim().length > 1) { const k = hex(tc); textCnt[k] = (textCnt[k] || 0) + 1; }
  });

  // accent = 링크/버튼에서 가장 채도 높은 색
  let accent = null, accentSat = 0.25;
  Array.prototype.slice.call(document.querySelectorAll('a, button, [class*=btn], [class*=button]')).slice(0, 400).forEach((el) => {
    const cs = getComputedStyle(el);
    [parse(cs.color), parse(cs.backgroundColor), parse(cs.borderColor)].forEach((c) => {
      if (c && c[3] > 0.5) { const s = sat(c[0], c[1], c[2]); if (s > accentSat) { accentSat = s; accent = hex(c); } }
    });
  });

  const fontOf = (sel) => { const e = document.querySelector(sel); if (!e) return null; const c = getComputedStyle(e); return { family: (c.fontFamily || '').split(',')[0].replace(/['"]/g, '').trim(), weight: +c.fontWeight || 400, size: c.fontSize, 'line-height': c.lineHeight === 'normal' ? 1.4 : +(parseFloat(c.lineHeight) / parseFloat(c.fontSize)).toFixed(2), 'letter-spacing': c.letterSpacing === 'normal' ? '0' : c.letterSpacing }; };
  const bodyFont = (getComputedStyle(document.body).fontFamily || '').split(',')[0].replace(/['"]/g, '').trim();

  return {
    bgRanked: Object.entries(bgArea).sort((a, b) => b[1] - a[1]).map((x) => x[0]).slice(0, 6),
    textRanked: Object.entries(textCnt).sort((a, b) => b[1] - a[1]).map((x) => x[0]).slice(0, 6),
    accent,
    bodyFont,
    type: { heading: fontOf('h1') || fontOf('h2'), subhead: fontOf('h3') || fontOf('h2'), body: fontOf('p') || fontOf('body'), button: fontOf('button, [class*=btn]'), lum: lum },
    _lumNote: 1
  };
});
await browser.close();

// 휴리스틱 매핑 (초안)
const darkest = [...raw.textRanked, ...raw.bgRanked].filter(Boolean)
  .sort((a, b) => { const p = (h) => { const n = parseInt(h.slice(1), 16); return ((n >> 16) & 255) + ((n >> 8) & 255) + (n & 255); }; return p(a) - p(b); });
const lightestBg = [...raw.bgRanked].sort((a, b) => { const p = (h) => parseInt(h.slice(1), 16); return p(b) - p(a); })[0] || '#FFFFFF';

const tokens = {
  client,
  source: 'url',
  site_url: url,
  extracted_at: new Date().toISOString().slice(0, 10),
  version: '1.0.0',
  _draft: '휴리스틱 자동추출 — primary/accent/background 매핑은 검토·보정 필요',
  colors: {
    primary: darkest[0] || '#1A1A1A',
    accent: raw.accent || '#C8A97E',
    background: lightestBg,
    surface: '#FFFFFF',
    text: raw.textRanked[0] || '#1A1A1A',
    'text-sub': raw.textRanked[1] || '#666666',
    border: '#E5E5E5'
  },
  _candidates: { backgrounds: raw.bgRanked, texts: raw.textRanked, accent: raw.accent },
  typography: {
    'font-family': raw.bodyFont || 'Pretendard',
    'note': 'NOOKITOKKI 표준은 Pretendard — 레퍼 폰트는 참고용, 클라 지시 없으면 Pretendard 유지',
    heading: raw.type.heading || { weight: 700, size: '32px', 'line-height': 1.3 },
    subhead: raw.type.subhead || { weight: 600, size: '20px', 'line-height': 1.4 },
    body: raw.type.body || { weight: 400, size: '15px', 'line-height': 1.6 },
    button: raw.type.button || { weight: 600, size: '14px', 'line-height': 1.2 }
  },
  spacing: { xs: '4px', sm: '8px', md: '16px', lg: '24px', xl: '40px', '2xl': '64px', '3xl': '96px', _note: '표준 스케일(자동추출 아님) — 필요시 조정' }
};

const json = JSON.stringify(tokens, null, 2);
if (out) { writeFileSync(out, json, 'utf8'); console.log('저장:', out); }
console.log(json);
console.log('\n⚠️ 초안입니다. colors.primary/accent/background 와 폰트를 레퍼런스와 대조해 보정하세요.');
