#!/usr/bin/env node
/**
 * check-binding.mjs — 재마크업 "바인딩 보존" 정적 검사 (accuracy-gate §5 제안 축 구현)
 *
 * 재마크업한 _nk/inc/*.html 이 카페24 보존대상(module= · 반복단위 · input name · {$action_*}
 * · 로그인분기 · data-ez)을 유지했는지 정적(grep/regex)으로 검사한다.
 * qa-checker 환각과 무관한 규칙 기반이라 신뢰 가능. 라이브 무접근, 파일만 읽는다.
 *
 * 사용:
 *   node check-binding.mjs --new _nk/inc/header.html [--orig layout/basic/header.html] [--ez] [--json]
 *   node check-binding.mjs --new _nk/inc/            (폴더 = *.html 전수)
 *
 * 종료코드: 0 = PASS(blocking 0), 1 = NEEDS_WORK
 *
 * [검증필요] "정의 밖 변수"(모듈이 제공하지 않는 {$변수}) 검사는 모듈별 제공변수 표가
 * 있어야 정확하다(현재 kit엔 회원 모듈만 상세). 여기선 미구현 → 사람 검토로 남긴다.
 */
import { readFileSync, readdirSync, statSync, existsSync } from "node:fs";
import { join, dirname, basename } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const opt = (k) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : null; };
const has = (k) => args.includes(k);
const NEW = opt("--new"); const ORIG = opt("--orig");
const EZ = has("--ez"); const JSON_OUT = has("--json");
if (!NEW) { console.error("사용: node check-binding.mjs --new <file|dir> [--orig <file>] [--ez] [--json]"); process.exit(2); }

// 모듈 등급 로드 (module-safety.json) — 등급표에 있으면 그 등급을 '우선'한다(레이아웃 오탐 방지)
let gradeMap = new Map();
try {
  const safety = JSON.parse(readFileSync(join(HERE, "../references/module-safety.json"), "utf8"));
  for (const m of safety.modules || []) gradeMap.set(m.module_family, String(m.grade));
} catch { /* 없으면 이름패턴으로 대체 */ }
const RED_RE = /(option|action|addcart|basket|order|payment|delivery|coupon|estimate|attend|myshop|member|login|join|find|address|refund|receipt|adult|cert|agree)/i;
// 등급표에 있으면 그 등급만 신뢰(Layout_* 는 ✅). 없을 때만 이름패턴 fallback.
const isRed = (mod) => {
  const fam = mod.replace(/_\d+$/, "");
  if (gradeMap.has(fam)) return gradeMap.get(fam).startsWith("🔴");
  return RED_RE.test(mod);
};

const rd = (p) => readFileSync(p, "utf8");
const modulesOf = (t) => [...t.matchAll(/module="([^"]+)"/g)].map((m) => m[1]);
const anchorCount = (t) => (t.match(/id="anchorBoxId_/g) || []).length;

function checkFile(newPath) {
  const t = rd(newPath);
  const findings = []; // {level:'blocking'|'warn'|'verify', msg}
  const mods = modulesOf(t);

  // 1) 원본 대비 사라진 module= 래퍼
  if (ORIG && existsSync(ORIG)) {
    const om = new Set(modulesOf(rd(ORIG)));
    const nm = new Set(mods);
    for (const m of om) if (!nm.has(m)) findings.push({ level: "blocking", msg: `module="${m}" 래퍼가 원본에 있었는데 사라짐(데이터 출력 중단 위험)` });
  }
  // 2) product_list* 반복단위 anchorBoxId 2개 미만
  if (mods.some((m) => /product_list/i.test(m))) {
    const a = anchorCount(t);
    if (a < 2) findings.push({ level: "blocking", msg: `상품목록 모듈인데 anchorBoxId 반복단위 ${a}개(<2) → 상품 1개만 출력될 위험(module-remarkup §4)` });
  }
  // 3) 🔴 모듈인데 input name / {$action_*} 흔적 0
  const redMods = mods.filter(isRed);
  if (redMods.length) {
    const hasName = /name="[^"]+"/.test(t);
    const hasAction = /\{\$action_[^}]+\}/.test(t);
    if (!hasName && !hasAction)
      findings.push({ level: ORIG ? "blocking" : "warn", msg: `🔴 거래/폼 모듈(${redMods.slice(0,3).join(", ")}) 포함인데 input name·{$action_*} 흔적 0 → 재마크업 시 폼/결제 바인딩 누락 의심(오버라이드 권장)` });
    findings.push({ level: "verify", msg: `🔴 모듈 ${redMods.length}종 — 라이브 결제/폼 시나리오 실증 검증 필요[검증필요]` });
  }
  // 4) 로그인 분기
  if (ORIG && existsSync(ORIG)) {
    const o = rd(ORIG);
    for (const br of ["Layout_statelogoff", "Layout_statelogon"])
      if (o.includes(br) && !t.includes(br)) findings.push({ level: "blocking", msg: `로그인 분기 ${br} 가 원본에 있었는데 사라짐` });
  }
  // 5) EZ data-ez
  if (EZ) {
    const nEz = (t.match(/data-ez/g) || []).length;
    if (ORIG && existsSync(ORIG)) {
      const oEz = (rd(ORIG).match(/data-ez/g) || []).length;
      if (oEz > 0 && nEz === 0) findings.push({ level: "warn", msg: `EZ 스킨인데 data-ez 속성 전부 소실(원본 ${oEz}개) → EZ 편집 연동 깨질 수 있음` });
    } else if (nEz === 0) findings.push({ level: "verify", msg: "EZ(--ez)인데 data-ez 0개 — 원본(--orig) 대조 필요[검증필요]" });
  }
  return { file: newPath, modules: mods.length, anchor: anchorCount(t), findings };
}

// 대상 수집
let targets = [];
const st = statSync(NEW);
if (st.isDirectory()) {
  const walk = (d) => readdirSync(d).forEach((n) => { const p = join(d, n); statSync(p).isDirectory() ? walk(p) : (p.endsWith(".html") && targets.push(p)); });
  walk(NEW);
} else targets = [NEW];

const results = targets.map(checkFile);
const blocking = results.flatMap((r) => r.findings.filter((f) => f.level === "blocking"));
const warn = results.flatMap((r) => r.findings.filter((f) => f.level === "warn"));
const verify = results.flatMap((r) => r.findings.filter((f) => f.level === "verify"));
const verdict = blocking.length === 0 ? "PASS" : "NEEDS_WORK";

if (JSON_OUT) {
  console.log(JSON.stringify({ verdict, blocking: blocking.length, warn: warn.length, verify: verify.length, results }, null, 1));
} else {
  console.log(`\n=== 바인딩 보존 검사: ${verdict} (파일 ${targets.length}) ===`);
  console.log(`  blocking ${blocking.length} · warn ${warn.length} · 검증필요 ${verify.length}\n`);
  for (const r of results) {
    if (!r.findings.length) continue;
    console.log(`[${r.file}] 모듈 ${r.modules}·anchor ${r.anchor}`);
    for (const f of r.findings) console.log(`   ${f.level === "blocking" ? "❌" : f.level === "warn" ? "⚠️ " : "🔍"} ${f.msg}`);
  }
  console.log("\n※ [검증필요]: 모듈별 제공변수 표 부재로 '정의 밖 변수' 검사는 미구현 — 사람 검토.");
}
process.exit(verdict === "PASS" ? 0 : 1);
