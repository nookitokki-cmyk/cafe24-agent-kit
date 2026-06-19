# 잔여 작업 체크리스트 (REMAINING-WORK)



> **갱신:** 2026-06-20  

> **목적:** agent-kit 파일럿·MVP 진행 중 열린 항목을 한곳에 모음.  

> **수용 기준 상세:** [`TEMPLATE-PILOT-ACCEPTANCE.md`](TEMPLATE-PILOT-ACCEPTANCE.md)  

> **배포:** **v2.2.0 shipped** — GitHub Release `v2.2.0` · [`DISTRIBUTION-KIT.md`](DISTRIBUTION-KIT.md) §7



---



## v1 shipped / v2 shipped



| | 상태 |

|---|------|

| **v1** `run_preflight(check=all)` MVP + dist kit | ✅ shipped 2026-06-19 |

| **v2.2** 온보딩 명령·diagnose·smoke 5/9·GitHub Release | ✅ shipped 2026-06-20 |



**v2 완료 항목:**



- [x] MOBILE_WEB auto-probe — `ref393674-score-mobile-full.py` `fetch_mobile_web()` 라이브 소스 검사

- [x] smoke 9/9 live default — `smoke_test.py` 토큰 있으면 `SMOKE_PREFLIGHT_ALL` 기본 1

- [x] `score_mall.py` — `CAFE24_MALL_ID` / `--mall-id` / `--ref-base` / `--tgt-base`

- [x] **9/9 score 스크립트** `parse_mall_config` — ecudemo400786 9/9 PASS 검증 (2026-06-19)

- [x] `run_preflight` mall_id + env — `server.py` `CAFE24_MALL_ID` 전달, `mall_id_applied_to_scripts: true`

- [x] dist **v2.2.0** — onboarding commands, `kit_tools.py`, GitHub Release channel

## B+. v2.2 shipped (2026-06-20)

- [x] `/키트시작` `/새클라이언트` `/MCP연결` + 검증 명령 4종
- [x] MCP `diagnose_kit_setup` · `scaffold_client` · `get_kit_guides` kit_version
- [x] smoke **5/9 partial exit 0** (config 없음)
- [x] GitHub `nookitokki-cmyk/cafe24-agent-kit` · `kit-update --from-github`



**v2.1+ 잔여:**



- [ ] paransky97 workflow 08 end-to-end



---



## A. 파일럿 합격 전 (blocking)



- [x] **07 doc cleanup** — Phase 0-C/0-D 분리, mermaid·Phase 1 decision tree, ez-on-legacy 표 정렬 (2026-06-19)

- [x] **ecudemo400786: 9/9 score scripts = 100** — closeout 재실측 **9/9 PASS** (mobile-full logoW fix → 100, 2026-06-19; sprint batch 재확인)

- [x] **MOBILE_WEB=false** verified on ecudemo — 라이브 소스 `CAFE24.MOBILE_WEB=false` (2026-06-19 closeout; 관리자 설정은 retrospective Phase A 기록)

- [x] **`clients/ecudemo400786/.workflow.md`** — Phase A/B/C retrospective 기록 + 사용자 「예」 placeholder (2026-06-19)

- [x] **파일럿 PASS 선언** — A 섹션 전항 ✅ · [`TEMPLATE-PILOT-ACCEPTANCE.md`](TEMPLATE-PILOT-ACCEPTANCE.md) §5 (2026-06-19 sprint)



---



## B. 키트 MVP (post-pilot or parallel)



- [x] **run_preflight full** (Phase 2) — 9 check 타입 + `check=all` batch + F34/MOBILE_WEB 안내 (`mcp/server.py`, 2026-06-19)

- [x] **run_preflight stub** — `mcp/server.py` header 등 단일 check + smoke (2026-06-19, [템플릿 파일럿](ea387518-b862-4c23-b2e6-cee95e66d94c))

- [x] **thin AGENTS.md** at `cafe24-agent-workspace` root — MCP 이름 + `get_kit_guides` 1줄 (2026-06-19)

- [x] **OneDrive agent-kit deprecated note / sync warning** in README — 경로 이중화·동기화 함정 안내 (2026-06-19)

- [x] **v2 dist shipped** — `dist/cafe24-agent-kit/VERSION` = v2.0.0; `score_mall.py` + 9/9 score scripts `parse_mall_config` (2026-06-19)



---



## C. v2 + 신규 템플릿 파일럿 A (after v1 ship)



- [x] **v2 run_preflight** — mall_id env·metadata, 9/9 score `score_mall.py`, MOBILE_WEB auto-probe, smoke 9/9 default, dist v2.0.0 ([`DISTRIBUTION-KIT.md`](DISTRIBUTION-KIT.md) §5)

- [ ] **paransky97** ([paransky97.cafe24.com](https://paransky97.cafe24.com/)) 또는 신규 몰로 워크플로우 **08** end-to-end (HTML skin → EZ FTP overlay → **Phase C strip**) — 조사 완료: [`PARANSKY97-EZ-INVESTIGATION.md`](PARANSKY97-EZ-INVESTIGATION.md)



> **레퍼런스·전략:** [`EZ-STRATEGY.md`](EZ-STRATEGY.md) — strip 기본, ecudemo400786 스킵은 파일럿 예외만.



---



## D. 완료됨 (checked)



- [x] **get_kit_guides** — MCP 부트스트랩, `next_read` 08(실행)→07(배경) 라우팅 힌트

- [x] **F35 / F36** — common-pitfalls, F-index, 07 Phase 0-D·08 이름 주의

- [x] **08 workflow** — 3단계 핑퐁, 07 Phase 0-D canonical 링크

- [x] **smoke 9/9** — `mcp/smoke_test.py` (도구 10종 incl. `run_preflight`; v2 default batch)

- [x] **psmux/tmux 3.3.6** — winget 설치; **터미널 재시작** 후 `tmux -V` ([psmux 설치](331e6510-7ec5-48d7-8a80-9025bb43f79b))

- [x] **TEMPLATE-PILOT-ACCEPTANCE.md** — 파일럿 수용 기준 문서화

- [x] **REMAINING-WORK-CHECKLIST.md** — 본 문서



---



## 빠른 검증 명령



```bash

cd work/scripts

for f in ref393674-score-*.py; do

  python "$f" | python -c "import sys,json; d=json.load(sys.stdin); print(d.get('total_score'), d.get('pass'), '$f')"

done

```



**MCP batch (Phase 2):** Cursor MCP `run_preflight` with `check=all` — 9종 순차 실행, `total_passed/9` + `f34_message` (F34).



```bash

cd mcp && python smoke_test.py                    # v2: token 있으면 9/9 batch 기본 (~15min)

SMOKE_PREFLIGHT_ALL=0 python smoke_test.py        # fast smoke (도구·API만)

```



**합격 선언:** A 섹션 전항 ✅ → [`TEMPLATE-PILOT-ACCEPTANCE.md`](TEMPLATE-PILOT-ACCEPTANCE.md) §5 체크리스트.

