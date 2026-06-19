# 에이전트 키트 로드맵 — 추가 도구·문서

> 초보 에이전트가 ecudemo393674→400786 수준에 도달하기 위해 키트에 넣을 항목.

---

## 이미 있는 것

| 항목 | 위치 |
|------|------|
| 레퍼런스 인입 | `workflows/05-reference-intake.md`, `/레퍼런스인입` |
| 실측 우선 | `workflows/04-measure-first.md` |
| verify-loop | `workflows/06-verify-loop.md` |
| 함정 postmortem | `docs/common-pitfalls.md` |
| 관리자 검증 규칙 | `rules/cafe24-admin-verify.md` |

---

## work/ 에서 검증된 스크립트 (템플릿)

`work/scripts/ref393674-score-*.py`

- `plp`, `pdp`, `basket`, `member`, `board`, `page`, `header`
- 패턴: Playwright + `getComputedStyle` + PASS≥90 + `sys.exit(1)`

새 몰: REF/TGT URL·셀렉터만 교체.

---

## 추가 예정·권장

| 도구 | 설명 |
|------|------|
| **page-type classifier** | URL·DOM → `plp-full` / `pdp-full` / `narrow` JSON (`layout.js` 와 동기) |
| **layout measure sheet** | 타입별 container·padding·grid CSV 템플릿 (`04-measure-first` 확장) |
| **FTP upload helper** | `mcp/backends/cafe24_ftp.py` `open_remote`; Windows `MSYS_NO_PATHCONV=1` |
| **optimizer cache wait** | 업로드 후 2~5분·`?v=` — `03-reference-renewal` §7 룰을 스크립트 exit 메시지에 포함 |

---

## 품질 게이트 (권장)

1. 인입표 승인
2. Phase별 score ≥ 90
3. `verify-loop.md` 로그
4. header dropdown·search PC/MO 실측 (`ref393674-score-header.py`)
