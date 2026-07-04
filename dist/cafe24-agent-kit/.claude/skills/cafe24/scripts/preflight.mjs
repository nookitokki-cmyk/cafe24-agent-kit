/**
 * preflight.mjs — 카페24 base 오버라이드 자동 진단 (Playwright 래퍼)
 * ---------------------------------------------------------------------------
 * diagnose-overrides.js 를 라이브 페이지에 자동 주입해 PC + 모바일 둘 다 점검하고
 * JSON 리포트를 출력한다. 에이전트(또는 CI)의 "라이브 검증" 단계에서 호출.
 * diagnose-overrides.js 는 단일 정본 엔진 — 여기서 끌어다 주입만 한다 (로직 중복 X).
 *
 * [사람이 직접 쓸 때]
 *   1) 한 번만:  npm i -D playwright && npx playwright install chromium
 *   2) 실행:     node preflight.mjs https://{몰ID}.cafe24.com
 *                node preflight.mjs https://{몰ID}.cafe24.com --out report.json
 *                node preflight.mjs https://{몰ID}.cafe24.com /product/detail.html?...
 *   ─ 여러 URL 을 공백으로 나열하면 전부 점검한다.
 *   ─ 각 URL 을 PC(1280) + 모바일(375) 두 뷰포트로 자동 검사.
 *
 * [에이전트가 쓸 때]
 *   비코더 대표님 환경엔 Playwright MCP 가 이미 있으므로, 설치 없이 MCP 로
 *   diagnose-overrides.js 를 page.evaluate 주입해도 동일 결과를 얻는다.
 *   (이 파일은 설치형 폴백 + CI 게이트용)
 *
 * 종료코드: high 심각도 발견 시 1 (게이트에서 실패 처리 가능), 아니면 0.
 * 아무것도 고치지 않는다 — 진단만.
 */

import { readFileSync } from 'node:fs';
import { writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ENGINE = join(__dirname, 'diagnose-overrides.js');

// ---- 인자 파싱 -------------------------------------------------------------
const argv = process.argv.slice(2);
let outPath = null;
const urls = [];
for (let i = 0; i < argv.length; i++) {
  if (argv[i] === '--out') { outPath = argv[++i]; continue; }
  if (argv[i].startsWith('http')) urls.push(argv[i]);
}
if (!urls.length) {
  console.error('사용법: node preflight.mjs <url> [url2 ...] [--out report.json]');
  console.error('예시:   node preflight.mjs https://demo-brand.cafe24.com');
  process.exit(2);
}

// ---- Playwright 로드 (없으면 친절히 안내) ----------------------------------
let chromium;
try {
  ({ chromium } = await import('playwright'));
} catch {
  console.error('\n⚠️  Playwright 가 설치돼 있지 않습니다.');
  console.error('    설치:  npm i -D playwright && npx playwright install chromium');
  console.error('    (또는 에이전트가 Playwright MCP 로 diagnose-overrides.js 를 주입해도 됩니다)\n');
  process.exit(3);
}

const engineSrc = readFileSync(ENGINE, 'utf8');
const VIEWPORTS = [
  { name: 'PC', width: 1280, height: 900, isMobile: false },
  // 카페24: 모바일 UA는 별도 모바일 스킨(/sde_design/mobile)을 띄움 → PC 반응형 스킨이 안 잡힘.
  // 데스크톱 UA + 좁은 뷰포트로 검증한다 (capture-pair.mjs 와 동일 규칙). [2026-06-22 실증 보정]
  { name: 'MOBILE', width: 375, height: 812, isMobile: false }
];

const results = [];
const browser = await chromium.launch();

for (const url of urls) {
  for (const vp of VIEWPORTS) {
    const ctx = await browser.newContext({
      viewport: { width: vp.width, height: vp.height },
      isMobile: vp.isMobile,
      userAgent: vp.isMobile
        ? 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148'
        : undefined
    });
    const page = await ctx.newPage();
    let report;
    try {
      await page.goto(url, { waitUntil: 'networkidle', timeout: 45000 });
      // diagnose-overrides.js 는 IIFE 라 마지막 return 값이 안 잡힘 → window.__NK_DIAG__ 로 회수
      await page.evaluate(engineSrc);
      report = await page.evaluate(() => window.__NK_DIAG__ || null);
    } catch (e) {
      report = { url, viewport: vp.name, error: String(e), findings: [], count: 0 };
    }
    report = report || { url, viewport: vp.name, findings: [], count: 0 };
    report.viewportName = vp.name;
    report.targetUrl = url;
    results.push(report);
    await ctx.close();
  }
}
await browser.close();

// ---- 요약 출력 -------------------------------------------------------------
let highCount = 0;
console.log('\n══════════ nk preflight — base 오버라이드 진단 ══════════');
for (const r of results) {
  const hi = (r.findings || []).filter((f) => f.sev === '❌').length;
  highCount += hi;
  console.log(`\n▶ ${r.targetUrl}  [${r.viewportName}]  발견 ${r.count || 0}건` + (r.error ? `  (오류: ${r.error})` : ''));
  (r.findings || []).forEach((f) => {
    console.log(`   ${f.sev} ${f.id} · ${f.area} — ${f.symptom}`);
    console.log(`      처방: ${f.fix}`);
  });
}
console.log('\n────────────────────────────────────────────────────────');
console.log(`총 ${results.length}개 화면 점검 · ❌(high) ${highCount}건`);

const out = { generatedAt: new Date().toISOString(), screens: results, highCount };
if (outPath) {
  writeFileSync(outPath, JSON.stringify(out, null, 2), 'utf8');
  console.log(`리포트 저장: ${outPath}`);
}

process.exit(highCount > 0 ? 1 : 0);
