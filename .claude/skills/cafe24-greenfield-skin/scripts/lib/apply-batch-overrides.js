/** Apply per-mall URL overrides (plpCateNo, batch URL replacements). */
function applyBatchOverrides(batches, overrides = {}) {
  const cate = overrides.plpCateNo;
  if (!cate) return batches;

  const mapUrl = (u) =>
    typeof u === 'string' ? u.replace(/cate_no=\d+/g, `cate_no=${cate}`) : u;

  const out = {};
  for (const [key, urls] of Object.entries(batches)) {
    out[key] = urls.map(mapUrl);
  }
  return out;
}

function resolveUltraqaPages(defaultPages, overrides = {}) {
  const pageOverrides = overrides.ultraqaPages || {};
  return defaultPages.map(([name, url]) => [name, pageOverrides[name] || url]);
}

module.exports = { applyBatchOverrides, resolveUltraqaPages };
