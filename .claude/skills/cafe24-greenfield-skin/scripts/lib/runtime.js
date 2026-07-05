const path = require('path');
const { resolveConfig } = require('./resolve-config');

/** Bootstrap BASE + OUT for interaction scanners. */
function boot(argv, reportBasename) {
  const cfg = resolveConfig(argv);
  return {
    cfg,
    BASE: cfg.base,
    OUT: path.join(cfg.wave4OutDir, reportBasename),
  };
}

module.exports = { boot };
