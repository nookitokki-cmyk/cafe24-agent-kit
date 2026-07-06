const fs = require('fs');
const path = require('path');

const HIGH_PATTERNS = [
  /:\s*#008bcc\b/i,
  /:\s*#009ffa\b/i,
  /font-family:\s*굴림/i,
  /font-style:\s*italic/i,
];

function grepPreflightHigh(cssDir) {
  const hits = [];
  if (!fs.existsSync(cssDir)) {
    return { pass: true, hits: [], count: 0, note: 'css dir missing: ' + cssDir };
  }
  for (const f of fs.readdirSync(cssDir).filter((x) => x.endsWith('.css'))) {
    const text = fs.readFileSync(path.join(cssDir, f), 'utf8');
    const lines = text.split('\n');
    let inBlockComment = false;
    lines.forEach((line, i) => {
      const trimmed = line.trim();
      if (trimmed.startsWith('/*')) inBlockComment = true;
      if (inBlockComment) {
        if (trimmed.includes('*/')) inBlockComment = false;
        return;
      }
      if (trimmed.startsWith('//') || trimmed.startsWith('*') || trimmed.startsWith('/*')) return;
      for (const pat of HIGH_PATTERNS) {
        if (pat.test(line) && !line.includes('var(--nk-')) {
          hits.push({ file: f, line: i + 1, snippet: line.trim().slice(0, 120) });
        }
      }
    });
  }
  return { pass: hits.length === 0, hits: hits.slice(0, 20), count: hits.length };
}

module.exports = { grepPreflightHigh };
