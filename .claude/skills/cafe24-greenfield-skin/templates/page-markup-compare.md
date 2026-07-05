# 3단 마크업 비교 — {몰ID} / {페이지} / {모듈 또는 섹션}

> **승인 전 코드 작성 금지.** 목표 구조 = `design.md` + `component-gallery.html` (외부 DS 참조 없음).

**담당**: {URL} · `{소스 경로}` · queue §{N}

---

## 비교표

| # | 유닛 | 현재 마크업 (요약) | 목표 구조 (gallery/design) | 재구성안 (NK) | L1 유지 항목 |
|---|------|-------------------|---------------------------|---------------|-------------|
| 1 | 예: `member_login` | `ec-base-box` + `table` | `nk-login-box` (gallery §폼) | `div.nk-login-box > ...` | `{$form.*}` · login btn onclick |
| 2 | | | | | |
| 3 | | | | | |

## 섹션·모듈 트리 (재구성안)

```
body.nk-skin
└─ .nk-{page}
   ├─ .nk-{page}__head
   └─ [module="..."]
      └─ (NK inner — ec-base 제거)
```

## L1 Binding 체크 (재구성 전 확인)

- [ ] module 목록 동일
- [ ] {$변수} 목록 동일
- [ ] anchorBoxId ×≥2 (해당 모듈)
- [ ] form field name/id 목록 동일

## 사용자 승인

- [ ] **승인** — Step B 착수 OK
- [ ] **수정 요청** — {메모}
- [ ] **보류**

승인자: __________ · 일자: __________
