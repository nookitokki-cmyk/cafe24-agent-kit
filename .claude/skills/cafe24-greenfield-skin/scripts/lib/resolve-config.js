// Mall-agnostic paths for Wave4 audit scripts (cafe24-greenfield-skin)
const fs = require('fs');
const path = require('path');

const SCRIPTS_DIR = path.resolve(__dirname, '..');
const SKILL_DIR = path.resolve(SCRIPTS_DIR, '..');

function findKitRoot(start) {
  let dir = path.resolve(start);
  for (let i = 0; i < 12; i++) {
    if (fs.existsSync(path.join(dir, 'mcp', 'server.py'))) return dir;
    const parent = path.dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  return null;
}

function parseMallId(argv) {
  const idx = argv.indexOf('--mall-id');
  if (idx >= 0 && argv[idx + 1]) return argv[idx + 1];
  return null;
}

function loadOverrides(clientRoot) {
  const p = path.join(clientRoot, '04_design', 'audit-overrides.json');
  if (!fs.existsSync(p)) return {};
  try {
    return JSON.parse(fs.readFileSync(p, 'utf8'));
  } catch (e) {
    throw new Error(`audit-overrides.json parse fail: ${e.message}`);
  }
}

function loadPassword(sftpConfigPath) {
  if (process.env.CAFE24_TEST_PW) return process.env.CAFE24_TEST_PW;
  try {
    if (fs.existsSync(sftpConfigPath)) {
      const cfg = JSON.parse(fs.readFileSync(sftpConfigPath, 'utf8'));
      if (cfg.password) return cfg.password;
    }
  } catch (_) { /* ignore */ }
  return '';
}

/**
 * @param {string[]} [argv] CLI args after node script name
 */
function resolveConfig(argv = process.argv.slice(2)) {
  const mallId = process.env.CAFE24_MALL_ID || parseMallId(argv);
  if (!mallId) {
    throw new Error(
      'CAFE24_MALL_ID env or --mall-id {몰ID} required (e.g. ecudemo402307)'
    );
  }

  const kitRoot =
    process.env.CAFE24_KIT_ROOT ||
    findKitRoot(process.cwd()) ||
    findKitRoot(SKILL_DIR) ||
    path.resolve(SKILL_DIR, '../../..');

  const clientRoot = path.join(kitRoot, 'agent-kit', 'clients', mallId);
  if (!fs.existsSync(clientRoot)) {
    throw new Error(`Client folder not found: ${clientRoot}`);
  }

  const overrides = loadOverrides(clientRoot);
  const wave4OutDir =
    process.env.CAFE24_OUT_DIR ||
    path.join(clientRoot, '04_design', 'shots', 'wave4');

  fs.mkdirSync(wave4OutDir, { recursive: true });

  const cssDir = path.join(clientRoot, 'src', '_nk', 'css');
  const base =
    process.env.CAFE24_BASE ||
    overrides.base ||
    `https://${mallId}.cafe24.com`;
  const sftpConfigPath = path.join(kitRoot, 'mcp', 'config', `sftp_${mallId}.json`);

  return {
    mallId,
    kitRoot,
    clientRoot,
    wave4OutDir,
    cssDir,
    base,
    overrides,
    loginId: overrides.loginId || process.env.CAFE24_TEST_ID || 'test1111',
    sftpConfigPath,
    loadPassword: () => loadPassword(sftpConfigPath),
    scriptsDir: SCRIPTS_DIR,
  };
}

module.exports = { resolveConfig, findKitRoot, loadOverrides, loadPassword };
