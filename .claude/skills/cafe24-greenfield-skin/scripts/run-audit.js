#!/usr/bin/env node
/**
 * Wave4 audit orchestrator — runs stock-scan-tier + ultraqa + optional interaction.
 *
 * Usage:
 *   node run-audit.js --mall-id ecudemo402307
 *   node run-audit.js --mall-id ecudemo402307 --steps tier,ultraqa,interaction
 *   node run-audit.js --mall-id ecudemo402307 --tier page --batch default
 */
const { spawnSync } = require('child_process');
const path = require('path');
const { resolveConfig } = require('./lib/resolve-config');

const SCRIPTS = path.resolve(__dirname);

function parseArgs(argv) {
  const mallIdx = argv.indexOf('--mall-id');
  const stepsIdx = argv.indexOf('--steps');
  const tierIdx = argv.indexOf('--tier');
  const batchIdx = argv.indexOf('--batch');
  const interactionIdx = argv.indexOf('--interaction');
  return {
    mallId: mallIdx >= 0 ? argv[mallIdx + 1] : null,
    steps: stepsIdx >= 0 ? argv[stepsIdx + 1].split(',').map((s) => s.trim()) : ['tier', 'ultraqa'],
    tier: tierIdx >= 0 ? argv[tierIdx + 1] : 'page',
    batch: batchIdx >= 0 ? argv[batchIdx + 1] : 'default',
    interaction: interactionIdx >= 0 ? argv[interactionIdx + 1] : null,
    passthrough: argv,
  };
}

function runNode(script, extraArgs, env) {
  const rel = path.relative(process.cwd(), script);
  const target = rel.startsWith('..') ? script : rel;
  console.log('\n>> node', target, extraArgs.join(' '));
  const r = spawnSync(process.execPath, [script, ...extraArgs], {
    stdio: 'inherit',
    env: { ...process.env, ...env },
    cwd: path.dirname(script),
  });
  if (r.status !== 0) {
    console.error('FAIL:', script);
    process.exit(r.status || 1);
  }
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const cfg = resolveConfig(process.argv.slice(2));
  const env = {
    CAFE24_MALL_ID: cfg.mallId,
    CAFE24_BASE: cfg.base,
    CAFE24_OUT_DIR: cfg.wave4OutDir,
  };
  const mallFlag = ['--mall-id', cfg.mallId];

  console.log('Wave4 audit:', cfg.mallId, '→', cfg.wave4OutDir);

  if (args.steps.includes('tier')) {
    runNode(
      path.join(SCRIPTS, 'stock-scan-tier.js'),
      [...mallFlag, '--tier', args.tier, '--batch', args.batch],
      env
    );
  }

  if (args.steps.includes('ultraqa')) {
    runNode(path.join(SCRIPTS, 'ultraqa-wave4-sweep.js'), mallFlag, env);
  }

  if (args.steps.includes('interaction') || args.interaction) {
    const types = args.interaction
      ? args.interaction.split(',').map((s) => s.trim())
      : ['main', 'plp', 'pdp', 'auth', 'board'];
    for (const t of types) {
      const script = path.join(SCRIPTS, 'interaction', `${t}.js`);
      runNode(script, mallFlag, env);
    }
  }

  console.log('\nWave4 audit complete. Reports →', cfg.wave4OutDir);
}

main();
