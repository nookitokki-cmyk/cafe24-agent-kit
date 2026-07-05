# Module 계약 체크리스트 (code-reviewer 전용)

> blank-slate **L1 Binding** 위반 여부만 본다. 디자인 품질·grep은 별도 라운드.

## PASS 조건 — 전항목 ✓

### A. module 속성

- [ ] 모든 `module="..."` 태그 **존재·이름·개수** 변경 전과 동일 (의도적 추가/삭제 없음)
- [ ] module 설정변수 주석 블록 보존 (줄바꿈·`$` 설정 그대로)

### B. 치환 변수

- [ ] `{$variable}` 이름 변경·삭제 없음
- [ ] 변수가 **module 밖**으로 새로 노출되지 않음 (module 밖 텍스트는 하드코딩만)

### C. anchorBoxId / 상품 반복

- [ ] `product_list*` · `product_ListItem` 등: anchorBoxId 패턴 **≥2 블록** 나란히 유지
- [ ] `{$product_no}` 등 반복 단위 훼손 없음

### D. Form / 액션

- [ ] `input`/`select`/`textarea` `name`·`id` 보존
- [ ] `action`·`method`·`onclick`·카페24 JS hook 속성 보존

### E. EZ (해당 파일만)

- [ ] `data-ez-*` · `<ez-prop>` · `<ez-var>` 삭제 없음 (header/footer/layout EZ 잔존 시)

### F. 금지 패턴 (inner에 재유입)

- [ ] module 안에 `ec-base-*` 클래스 **신규 잔존 0** (의도적 stock 호환 래퍼 제외 — 주석 사유 필수)
- [ ] 인라인 `style=""` 0

## FAIL 시

- 위반 항목 파일·줄 단위로 보고
- 수정은 **L2 inner만** — L1 복구 우선
