# nk-cafe24-reset.css 사용 가이드

> 카페24 기본 디자인(base CSS)이 깔아놓은 **함정 7종을 한 번에 무력화**하는 휴대용 CSS.
> base를 직접 못 고치는 **운영 몰**에서 "덮어쓰기(override)"로 쓴다.
> 파일: `snippets/css/nk-cafe24-reset.css` (약 18KB, 10개 섹션)

---

## 1. 한 줄 정리

카페24는 모든 몰에 똑같은 함정(고정폭·가짜선·a밑줄·상품 회색테두리·카페24 파란색·옛날 폼버튼·푸터 고정폭)을 깐다.
이 파일 **하나를 켜면** 그 함정들이 일괄 중화된다. 페이지마다 셀렉터 찾아 막는 "두더지잡기"를 끝낸다.

## 2. 언제 쓰나 / 언제 안 쓰나

| 상황 | reset 사용 |
|---|---|
| base 소스를 못 고치는 **운영 중인 몰** (덮어쓰기만 가능) | ✅ 이 파일 |
| base 소스를 직접 고칠 수 있음 (`#nk-skinN` 토큰화) | `nk-ez-override.css` 쪽 |
| 손 안 댈 페이지 (게시판·주문 등 기본 그대로 둘 곳) | ❌ 그 페이지엔 `nk-skin` 안 붙임 |

## 3. 적용 3단계 (이게 "실행" 방법)

> CSS는 프로그램처럼 실행되는 게 아니라 **불러와지면 적용**된다. 단, 이 파일은 **opt-in**이라
> ① 파일 로드 + ② `<body class="nk-skin">` **둘 다** 맞아야 켜진다.

```
1단계 — 업로드
   nk-cafe24-reset.css 를 몰 스킨에 올린다 (SFTP)
   예) /_nk/css/nk-cafe24-reset.css

2단계 — 제일 먼저 로드  ★맨 위 (다른 CSS보다 먼저)
   custom.css(또는 _nk 메인 CSS) 최상단에:
   <!--@css(/_nk/css/nk-cafe24-reset.css)-->
   → 그 다음 줄부터 클라 색·폰트·레이아웃을 얹는다

3단계 — body에 스위치 ON
   <body id="main" class="nk-skin">
   (이 클래스가 붙은 페이지에만 중화 적용 → 나머지는 base 그대로 = 안전)
```

## 4. 색은 변수로 위임 (강제 안 함)

reset은 **레이아웃·가짜선·옛날 버튼·강제 폰트만 원위치**시키고, **색은 강제하지 않는다.**
카페24 기본 파란색만 `--nk-point` 변수로 빼놨다 → 브랜드색으로 덮으면 끝:

```css
:root { --nk-point: #여기에브랜드색; }   /* 클라 CSS에 한 줄 */
```

## 5. ⚠️ 안 먹을 때 (가장 흔한 함정)

카페24 base는 `body#main` + `!important`로 거는 경우가 많아 **힘(명시도)이 reset보다 셀 수 있다.**
일부 줄이 안 먹으면 클라 CSS에서 **id를 같이 붙여** 한 번 더 감싼다:

```css
body#main.nk-skin { ... }   /* id로 base의 힘을 맞받음 */
```

## 6. 이 파일이 막는 함정 (10개 섹션)

| § | 막는 것 |
|---|---|
| 1 | 전역 골격 — 고정폭·min-width·overflow·헤더/푸터 강제 배경 |
| 2 | 태그 reset 역중화 — a 밑줄·검정색, img 정렬, 강제 폰트(돋움/Verdana) |
| 3 | 폼 컨트롤 — 옛날 PNG 화살표·체크박스·라디오 → 순수 CSS(이미지 0) |
| 4 | 공통 컴포넌트(.ec-base-*) — 탭·페이지네이션·버튼·테이블·툴팁 |
| 5 | 카페24 파란색(#008bcc) → `--nk-point` 위임 |
| 6 | 가상요소 가짜선 — 헤더/푸터/박스 ::before·::after 선 |
| 7 | 상품 진열 — 회색테두리·고정폭·가운데정렬 |
| 8 | 푸터 모듈 — float·고정폭·고정높이 |
| 9 | 고정폭 팝업·레이어 — 모바일 화면 이탈 방지 |
| 10 | gif/png 옛날 불릿·아이콘(echosting 이미지) |

## 7. 헷갈리는 3형제 구분

| 파일 | 용도 |
|---|---|
| `nk-cafe24-reset.css` | **(이 파일)** base 함정 범용 중화 — 운영 몰 덮어쓰기, `body.nk-skin` opt-in |
| `nk-ez-override.css` | base 소스를 고칠 수 있을 때 `#nk-skinN` 토큰화 보완 |
| `nk-reset.css` | 일반적인 CSS 초기화(범용) |

## 8. 새 클라 작업 시 (정석)

reset만 믿지 말 것. 클라마다 base가 조금씩 다르다(maison/기본스킨 등).
**Step 0: base 전수 스캔**으로 그 클라 base를 기계가 훑어 reset 미커버 잔존을 `brain/docs/BASE-CSS-MAP.md`에 보강한다.
→ 함정은 "사람이 발견"하지 말고 "기계가 스캔". (상세: `brain/docs/CAFE24-SMARTDESIGN-AGENT.md` STEP 2)

## 9. 적용 체크리스트

- [ ] `nk-cafe24-reset.css` SFTP 업로드 (`/_nk/css/`)
- [ ] custom.css **맨 위**에서 `@css`로 먼저 로드
- [ ] 커스텀할 페이지 `<body>`에 `class="nk-skin"`
- [ ] 브랜드색 `--nk-point` 지정
- [ ] 안 먹는 줄은 `body#main.nk-skin`으로 재감싸기
- [ ] 새 클라면 Step 0 base 전수 스캔 1회
- [ ] 라이브 `?v=N` → PC + 모바일 스크린샷 확인
