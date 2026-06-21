# scripts/ — 자가진단 도구 (base 오버라이드 점검)

카페24 **기본(base) CSS·구조가 우리 `nk-` 스킨을 이기는** 문제를 *자동으로 찾아* "졌다/이겼다 + 원인 + 처방"을 알려주는 도구 모음입니다. **아무것도 고치지 않습니다 — 진단만 합니다.** (수정은 검토 후 사람이/에이전트가 `#nk-skinN` 스코프로 적용)

| 파일 | 누가 | 무엇 |
|---|---|---|
| `diagnose-overrides.js` | **비코더용** (설치 0) | 라이브 화면 F12 콘솔에 붙여넣으면 진단표 + **방식(HTML/EZ) 자동판정** 출력 |
| `preflight.mjs` | 자동화/CI용 | Playwright 로 PC+모바일 자동 점검 → JSON 리포트 (override 축) |
| `capture-pair.mjs` | 자동화/CI용 | 레퍼런스 vs 결과 스크린샷 4장(PC+모바일) 캡처 → qa-checker visual 축 입력. **★ 데스크톱 UA 고정**(카페24 모바일 스킨 회피) |
| `../references/traps.json` | 엔진 데이터 정본 | 함정 47종(증상·탐지·처방, `method` 축). 위 진단이 이걸 미러/참조 |
| `../references/accuracy-gate.md` | 합격 계약 | "정확" = visual+override+rule 3축 게이트 정의 |

---

## 1. 비코더 빠른 사용 — `diagnose-overrides.js`

> "헤더 글씨가 왜 가운데로 가지?", "상품명·가격 간격이 왜 이래?", "내 CSS 가 왜 안 먹지?" 싶을 때

1. 라이브 쇼핑몰을 **크롬**에서 연다 (예: `https://{몰ID}.cafe24.com`)
2. **F12** → 상단 **Console(콘솔)** 탭
3. `diagnose-overrides.js` **전체 복사 → 콘솔에 붙여넣기 → Enter**
4. 표에서 **❌(졌다)** 항목의 **처방**을 검토 후 `custom.css` 에 적용
5. **모바일도** 보려면: F12 좌상단 **폰 아이콘**으로 화면을 375px 로 만들고 **새로고침** 후 다시 실행
   - ⚠️ PC·모바일은 **따로** 봐야 합니다. 한쪽만 정상이면 "미완료".

**무엇을 점검하나**
1. 스킨 스코프(`#nk-skinN`) 유무 — 없으면 base 를 이길 힘 자체가 약함
2. 전역 골격(`#container`·`#contents`·`header`·`footer`·`section`·`.inner`)이 base 에 졌는지
3. EZ 에디터가 박은 **인라인 `style=""`** (외부 CSS 로는 못 이김)
4. base 폰트(굴림/돋움)가 우리 Pretendard/Bricolage 를 이기는지
5. 알려진 함정 F1~F32 자동 매칭

---

## 2. 자동화/CI 사용 — `preflight.mjs`

```bash
# 한 번만 (설치)
npm i -D playwright && npx playwright install chromium

# 실행 — URL 을 PC(1280) + 모바일(375) 두 뷰포트로 자동 점검
node preflight.mjs https://{몰ID}.cafe24.com
node preflight.mjs https://{몰ID}.cafe24.com /product/detail.html?...  --out report.json
```

- 여러 URL 을 공백으로 나열하면 전부 점검합니다.
- **종료코드**: `❌(high)` 발견 시 `1` (게이트에서 실패 처리), 없으면 `0`.
- 에이전트는 설치 없이 **Playwright MCP** 로 `diagnose-overrides.js` 를 `page.evaluate` 주입해도 동일 결과를 얻습니다.

---

## 3. 두 개의 눈 (정적 + 런타임)

이 도구는 **런타임(화면)** 진단입니다 — "실제로 졌는지"를 봅니다.
**정적(파일)** 진단 — "어느 base 파일·줄이 범인인지" — 은 에이전트가 SFTP 로
`/layout/basic/css/`·`/css/module/`·`ec-base-*.css`·`logotop.css`·`category.css` 를
읽어서 대조합니다. `traps.json` 의 `detectable: "static|network|manual"` 항목이 그 영역입니다.

> **원리 한 줄**: base 가 이기는 건 "먼저 로드돼서"가 아니라 **명시도/`!important`** 때문.
> 처방은 원본 수정이 아니라 `#nk-skinN` 스코프로 우리 명시도를 올려 이기는 것. (EZ 인라인만 `!important`)

산문 원본: `brain/docs/CAFE24-SMARTDESIGN-AGENT.md` §6 · `02_막혔을때/함정-INDEX.md`
