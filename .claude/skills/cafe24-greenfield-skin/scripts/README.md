# Wave4 audit scripts (cafe24-greenfield-skin)

ecudemo402307 검증본을 **몰ID 파라미터화**해 승격한 Playwright 스캐너입니다.

## 전제

- **키트 루트** (`cafe24-kit-작업본`)에서 실행 — `mcp/server.py`·`node_modules/playwright` 필요
- `npm install` 은 키트 루트에 이미 있음 (`playwright` devDependency)
- 로그인 배치: `CAFE24_TEST_PW` 또는 `mcp/config/sftp_{몰ID}.json` password

## 빠른 실행

```powershell
cd C:\nookitokki\cafe24-kit-작업본

# 4-tier page scan + UltraQA (기본)
node .claude/skills/cafe24-greenfield-skin/scripts/run-audit.js --mall-id ecudemo402307

# 4-tier만 (batch 지정)
node .claude/skills/cafe24-greenfield-skin/scripts/stock-scan-tier.js --mall-id ecudemo402307 --tier module --batch board

# UltraQA만
node .claude/skills/cafe24-greenfield-skin/scripts/ultraqa-wave4-sweep.js --mall-id ecudemo402307

# Interaction (타입별)
node .claude/skills/cafe24-greenfield-skin/scripts/interaction/main.js --mall-id ecudemo402307

# 전체 (tier + ultraqa + interaction 5종)
node .claude/skills/cafe24-greenfield-skin/scripts/run-audit.js --mall-id ecudemo402307 --steps tier,ultraqa,interaction
```

## 출력 위치

리포트는 **항상** `agent-kit/clients/{몰ID}/04_design/shots/wave4/` 에 저장됩니다.

| 스크립트 | 리포트 파일 |
|----------|-------------|
| stock-scan-tier | `_stock-scan-tier-{batch}-{tier}-report.json` |
| ultraqa | `_ultraqa-wave4-report.json` |
| interaction/* | `_*-interaction-scan-report.json` |

## 몰별 URL 오버라이드

`clients/{몰ID}/04_design/audit-overrides.json` (템플릿: `templates/audit-overrides.example.json`)

```json
{
  "plpCateNo": 24,
  "loginId": "test1111",
  "ultraqaPages": {
    "pdp": "/product/샘플상품-2/10/category/1/display/1/"
  }
}
```

- `plpCateNo` — batch URL의 `cate_no=` 일괄 치환
- `ultraqaPages` — UltraQA·PDP interaction URL 키별 override

## 환경 변수

| 변수 | 용도 |
|------|------|
| `CAFE24_MALL_ID` | `--mall-id` 대체 |
| `CAFE24_BASE` | 라이브 URL override |
| `CAFE24_OUT_DIR` | 리포트 출력 폴더 override |
| `CAFE24_TEST_PW` | 로그인 스캔 비밀번호 |

## 레거시 경로

클라이언트 `04_design/shots/wave4/_*.js` 는 **검증 스냅샷**으로 유지 가능. 신규 몰·재검토는 이 `scripts/` 폴더를 SSOT로 사용하세요.
