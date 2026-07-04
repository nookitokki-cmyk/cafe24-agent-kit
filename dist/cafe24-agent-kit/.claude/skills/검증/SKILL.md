---
name: 검증
description: run_preflight·score 자기검증 핑퐁 (F34 등 해석)
---

사용자가 `/검증` 을 요청했습니다. **한 번에 질문 하나.**

## Q1. 몰 ID

「검증할 **몰 ID**는? (`--mall-id` / `CAFE24_MALL_ID`)」

## Q2. 검증 범위

「**전체 9종** (`check=all`) 인가요, **단일 페이지** (header/plp/pdp/…) 인가요?」

| check | 의미 |
|-------|------|
| `all` | 9종 순차 (~2분) |
| `header` | 헤더·검색 |
| `mobile_full` | MO 390 — **MOBILE_WEB=false** 필요 |
| `plp` / `pdp` / … | 해당 페이지 |

MCP: `run_preflight(check="...", mall_id="...")`

## Q3. 결과 해석

| 결과 | 조치 |
|------|------|
| `pass: true`, score 100 | ✅ 완료 |
| F34 / MOBILE_WEB | 관리자 **모바일 디자인 OFF** → 재실행 |
| score &lt; 100 | `01_작업하기/workflows/06-verify-loop.md` · 해당 score 스크립트 |
| `mall_id_applied_to_scripts: false` | 키트 v2.0.0 이하 — v2.0.1+ 배포본 사용 |

터미널 (단일):

```bash
cd work/scripts
python ref393674-score-header.py --mall-id {몰ID}
```

## 완료

```
[검증 완료]
- 몰: {몰ID}
- check: {name}
- pass: {true|false}
- 다음: 06-verify-loop 또는 /디자인수정
```
