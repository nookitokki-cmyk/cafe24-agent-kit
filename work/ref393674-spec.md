# ref393674 (maeve) 1:1 구현 계획표

> 레퍼런스: https://ecudemo393674.cafe24.com/  
> 대상 몰: https://ecudemo400786.cafe24.com/ (워크플로우 03 검증용)  
> 분석 소스: live HTML + MorenvyBanner_AreaData + optimizer user CSS 실측

## 섹션 계획

| 섹션 | 레퍼런스 실측 | 대상 파일 | 난이도 | 순서 |
|---|---|---|---|---|
| 토큰/베이스 | body 13px Bricolage / #222 / lh1.6 | `_ref393674/css/tokens.css`, `base.css` | 하 | 1 |
| 헤더 | fixed 50px lh / Menu 70px / GNB gap 20px / logo Marcellus 31px(모바일 23px) | `layout/basic/header.html` + `_ref393674/css/header.css` | 중 | 2 |
| 히어로 | 100vh vertical swiper / pagination 세로 0.5px white / box left 20 bottom 20 | `_ref393674/inc/hero.html`, `hero.css`, `hero.js` | 중 | 3 |
| 팝업(텍스트) | fixed right 30 bottom 30 / 12px / NOTICE | `_ref393674/inc/popup-text.html`, `popup.css` | 하 | 4 |
| 푸터 | flex 4열 Legal·Menu·SNS·© / company 11.5px #999 | `layout/basic/footer.html` + `_ref393674/css/footer.css` | 하 | 5 |

## 레퍼런스에 없는 것 (홈)

- 메인진열(product_listmain) 없음
- 팝업(이미지) area 4346 bannerList 빈 배열 → 미구현

## 히어로 슬라이드 (Morenvy 배너 JSON)

1. **Women** — `e655c017ad9ba73ef6c5cbd8a8323845.jpg` / tit Women / Discover your true style…
2. **Men** — `620c0b9a4f1cb56b6aea2f1a28d61155.jpg` / tit Men / Redefine your everyday style…

## 한계

- Morenvy 배너 관리자 설정은 FTP로 복제 불가 → 정적 HTML+레퍼런스 CDN 이미지 사용
- EZ 스킨 잔재(서브페이지)는 홈 1:1 검증 후 별도 격차표
