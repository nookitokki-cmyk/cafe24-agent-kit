/**
 * capture-pair.mjs — 레퍼런스 vs 결과 스크린샷 쌍 캡처 (visual-diff 입력 생성)
 * ---------------------------------------------------------------------------
 * accuracy-gate.md 의 visual 축(qa-checker)이 비교할 4장을 만든다:
 *   {레퍼런스, 결과} × {PC, 모바일폭}
 *
 * ★ 카페24 핵심 규칙: 모바일도 **데스크톱 UA + 좁은 뷰포트**로 캡처한다.
 *   모바일 UA(에뮬레이션)를 쓰면 카페24가 *별도 모바일 스킨(sde_design/mobile)* 을 띄워
 *   우리 반응형 PC 스킨이 안 나온다 (handover 규칙). → isMobile:false 고정, UA 미변경.
 *
 * [사람이 직접]
 *   npm i -D playwright && npx playwright install chromium   # 한 번만
 *   node capture-pair.mjs --ref https://레퍼런스 --result https://결과 --out ./shots --name home
 *   → ./shots/home_ref_pc.png, home_ref_mobile.png, home_result_pc.png, home_result_mobile.png
 *
 * [에이전트] Playwright MCP 가 있으면 설치 없이 동일 캡처 가능(이 파일은 설치형 폴백).
 *
 * 아무것도 안 고친다 — 캡처만.
 */

import { mkdirSync } from 'node:fs';
import { resolve } from 'node:path';

// ---- 인자 ------------------------------------------------------------------
const argv = process.argv.slice(2);
function arg(flag, def) { const i = argv.indexOf(flag); return i >= 0 && argv[i + 1] ? argv[i + 1] : def; }
const refUrl = arg('--ref');
const resultUrl = arg('--result');
const outDir = resolve(arg('--out', './shots'));
const name = arg('--name', 'page');

if (!refUrl && !resultUrl) {
  console.error('사용법: node capture-pair.mjs --ref <레퍼런스URL> --result <결과URL> [--out ./shots] [--name home]');
  console.error('  (--ref 또는 --result 중 하나만 줘도 됨)');
  process.exit(2);
}

let chromium;
try { ({ chromium } = await import('playwright')); }
catch {
  console.error('\n⚠️  Playwright 미설치: npm i -D playwright && npx playwright install chromium');
  console.error('   (또는 에이전트가 Playwright MCP 로 캡처 — 데스크톱 UA·뷰포트 1440/390 고정)\n');
  process.exit(3);
}

mkdirSync(outDir, { recursive: true });

// ★ 데스크톱 UA 고정. 모바일은 뷰포트 폭만 좁힘 (isMobile:false)
const VIEWPORTS = [
  { tag: 'pc', width: 1440, height: 960 },
  { tag: 'mobile', width: 390, height: 844 }  // 데스크톱 UA + 좁은 폭 = 반응형 모바일 (카페24 별도 스킨 회피)
];
const TARGETS = [];
if (refUrl) TARGETS.push({ role: 'ref', url: refUrl });
if (resultUrl) TARGETS.push({ role: 'result', url: resultUrl });

const browser = await chromium.launch();
const saved = [];
for (const t of TARGETS) {
  for (const vp of VIEWPORTS) {
    const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height }, isMobile: false }); // UA·isMobile 손대지 않음
    const page = await ctx.newPage();
    const file = `${outDir}/${name}_${t.role}_${vp.tag}.png`;
    try {
      await page.goto(t.url, { waitUntil: 'networkidle', timeout: 45000 });
      await page.waitForTimeout(800); // lazy 이미지·폰트 안착
      await page.screenshot({ path: file, fullPage: true });
      saved.push({ role: t.role, vp: vp.tag, file, ok: true });
    } catch (e) {
      saved.push({ role: t.role, vp: vp.tag, file, ok: false, err: String(e) });
    }
    await ctx.close();
  }
}
await browser.close();

console.log('\n══════ capture-pair (데스크톱 UA · PC 1440 / 모바일 390) ══════');
for (const s of saved) console.log(`  ${s.ok ? '✅' : '❌'} ${s.role}/${s.vp}  ${s.file}${s.err ? '  (' + s.err + ')' : ''}`);
console.log('\nqa-checker 에 전달: 레퍼(ref) vs 결과(result) PC·모바일 4장을 시각 비교 → accuracy-gate visual 축');
process.exit(saved.some((s) => !s.ok) ? 1 : 0);
