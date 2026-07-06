# _nk/inc 재마크업 안전 골격 스니펫

> 카페24 **모듈 재마크업 방법론**(`references/module-remarkup.md`)의 실행 부품.
> 이 골격을 스킨의 `/_nk/inc/`에 올리고 `layout.html`의 `@import` 경로를 교체해 쓴다.
> **구조(div/클래스/배치)는 내 맘대로, `<!-- ★보존 -->` 표시된 줄은 그대로 이식.**

## 파일
- `header.html` — 헤더 재마크업 골격 (Layout_* 모듈 보존 + nk 구조)
- `footer.html` — 푸터 재마크업 골격
- `product-list.html` — 상품목록 골격 (anchorBoxId 반복단위 보존 예시)

## 이식 체크리스트 (재마크업 후 반드시 확인)
- [ ] 모든 `module="..."` 래퍼가 살아 있는가
- [ ] 그 모듈이 **제공하는 `{$변수}`만** 썼는가 (정의 밖 변수 X)  `[공식: 모듈별 변수 고정]`
- [ ] 반복 블록 `id="anchorBoxId_{$...}"` `<li>` 를 **2개 이상** 유지했는가  `[반복 깨짐 방지]`
- [ ] 필수 `input name="..."` / `onclick="{$action_*}"` 를 이식했는가  `[거래·폼]`
- [ ] 로그인 분기 `Layout_statelogoff/logon` 유지
- [ ] (EZ 스킨) `data-ez-*` 유지
- [ ] `layout.html` @import 를 `/_nk/inc/*`로 교체 + 원본 `_nk/_backup_*` 보존
- [ ] 🔴 거래 모듈(장바구니/주문/결제/옵션)은 재마크업 대신 오버라이드했는가 (`module-safety.json`)

> ⚠️ 아래 골격의 모듈명·변수는 **대표 예시**다. 실제 모듈 ID/제공 변수는 몰의 스킨 소스와 `references/modules.md`·`variables.md`로 확인할 것. 불확실하면 `[검증필요]`.
