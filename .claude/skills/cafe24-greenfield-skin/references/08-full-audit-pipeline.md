# Phase A–G 전수 감사

```
자동 스캔 PASS = 1차. 완료 = A→G + visual + 로그인 수동.
```

| 단계 | 도구 | PASS |
|------|------|------|
| A | grep preflight / ultraqa preflight | #008bcc·italic 0 |
| B | `04-html-css-parity.md` | nk HTML ↔ CSS 정합 |
| C | `_stock-scan-tier.js` | violations=0 |
| D | `_*-interaction-scan.js` | click-test |
| E | `_ultraqa-wave4-sweep.js` | overflow·{$ 0 |
| F | visual-verdict / qa-checker | 핵심 URL |
| G | 로그인 URL 수동 | myshop · modify 등 |

**실행** (몰ID 치환):

```powershell
cd agent-kit/clients/{몰}/04_design/shots/wave4
$env:CAFE24_BASE="https://{몰}.cafe24.com"
node _stock-scan-tier.js --tier page --batch default
node _ultraqa-wave4-sweep.js
```

페이지 에이전트 작업 **전부** 끝난 뒤 G8만 수행.
