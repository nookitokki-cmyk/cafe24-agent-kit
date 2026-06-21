/*!
 * nk-diagnose-overrides.js — 카페24 base CSS 오버라이드 자가진단 (콘솔용)
 * --------------------------------------------------------------------------
 * "카페24 기본 스타일이 우리 nk- 스킨을 이기는" 문제를 라이브 화면에서 자동으로 찾아
 * "졌다/이겼다 + 원인 + 처방"을 표로 보여준다. 아무것도 고치지 않는다 — 진단만.
 *
 * [비코더 사용법]
 *  1) 라이브 쇼핑몰을 크롬에서 연다 (예: https://{몰ID}.cafe24.com) — 메인/상품목록/상세/장바구니 각각
 *  2) F12 → "Console(콘솔)" 탭 → 이 파일 전체 복사·붙여넣기 → Enter
 *  3) ❌(졌다) 항목의 "처방"을 검토 후 custom.css 에 #nk-skinN 스코프로 적용
 *  ─ 모바일도: F12 좌상단 폰 아이콘으로 375px → 새로고침 → 다시 실행 (PC·모바일 따로!)
 *  ─ 페이지마다 잡히는 게 다르다 (메인=헤더/배너, 상세=수량칸/구매버튼, 목록=상품카드 …) → 주요 페이지 다 돌려라
 *
 * [점검 범위] (대표님 요청 — 상품명·가격뿐 아니라 "틀어질 만한 변수 전부")
 *   A. 스킨 스코프(#nk-skinN) 유무
 *   B. 전역 골격: body·#container·#contents·section·.inner·헤더/푸터 폭 일치
 *   C. base 기본값 통째 스캔: 굴림/돋움 폰트 · 빨간 가격 · 골드(#d0ac88) · 파란 링크 · 기울임(italic) · 회색 테이블
 *   D. 영역별 폰트 스윕: 헤더메뉴·푸터·검색·상품명·가격·설명·PDP·장바구니·게시판·회원폼
 *   E. 헤더: 로고 중앙쏠림·GNB·아이콘 오프셋·유틸바·헤더높이 변수
 *   F. PLP: 그리드 폭·리스트마커·아이콘박스
 *   G. PDP: 수량칸·구매영역 폭·infoArea·아코디언·상세이미지
 *   H. 폼: select caret·input 높이·체크박스·버튼 색/모서리
 *   I. EZ 인라인 style="" (외부 CSS 로 못 이기는 것)
 *
 * [원리] base 가 이기는 건 "먼저 로드돼서"가 아니라 명시도/!important 때문.
 *   처방은 원본 수정이 아니라 #nk-skinN 스코프로 명시도를 올려 이기는 것. (EZ 인라인만 !important)
 *
 * 출처: brain/docs/CAFE24-SMARTDESIGN-AGENT.md §6·§9 / references/traps.json
 */
(function () {
  'use strict';

  // ---- 도우미 --------------------------------------------------------------
  var $  = function (s, r) { try { return (r || document).querySelector(s); } catch (e) { return null; } };
  var $$ = function (s, r) { try { return Array.prototype.slice.call((r || document).querySelectorAll(s)); } catch (e) { return []; } };
  var gcs = function (el) { return el ? getComputedStyle(el) : null; };
  var px  = function (v) { var n = parseFloat(v); return isNaN(n) ? 0 : n; };
  var rectW = function (el) { return el ? el.getBoundingClientRect().width : 0; };
  var isMobile = window.matchMedia && window.matchMedia('(max-width: 768px)').matches;

  function rgbOf(s) { var m = (s || '').match(/(\d+)[,\s]+(\d+)[,\s]+(\d+)/); return m ? [+m[1], +m[2], +m[3]] : null; }
  function reddish(c) { return c && c[0] > 140 && c[1] < 95 && c[2] < 95; }              // 빨간 가격
  function bluish(c)  { return c && c[2] > 130 && c[0] < 100 && c[1] < 150 && c[2] - c[0] > 50; } // 파란 링크
  function gold(c)    { return c && Math.abs(c[0] - 208) < 30 && Math.abs(c[1] - 172) < 30 && Math.abs(c[2] - 136) < 30; } // EZ 기본 골드 #d0ac88
  function goodFont(ff) { return /pretendard|bricolage|marcellus|apple sd gothic|noto sans kr/i.test(ff || ''); }
  function baseFont(ff) { return /gulim|굴림|dotum|돋움|batang|바탕|gungsuh|궁서/i.test(ff || ''); }
  function shortSel(el) {
    if (!el) return '';
    var c = (el.className && typeof el.className === 'string') ? el.className.trim().split(/\s+/).slice(0, 2) : [];
    return c.length ? '.' + c.join('.') : el.tagName.toLowerCase();
  }

  // ---- 스킨 스코프 ---------------------------------------------------------
  var bodyId = document.body && document.body.id ? document.body.id : '';
  var SKIN = /^nk-skin/i.test(bodyId) ? '#' + bodyId
           : ($('[id^="nk-skin"]') ? '#' + $('[id^="nk-skin"]').id : null);
  var S = SKIN || '#nk-skinN';

  var findings = [];
  function add(sev, id, area, symptom, evidence, fix) {
    findings.push({ sev: sev, id: id, area: area, symptom: symptom, evidence: evidence, fix: fix });
  }
  var seen = {}; // 같은 id 중복 억제
  function addOnce(sev, id, area, symptom, evidence, fix) { if (seen[id]) return; seen[id] = 1; add(sev, id, area, symptom, evidence, fix); }

  // =========================================================================
  // A. 스코프
  // =========================================================================
  if (!SKIN) {
    add('❌', 'S1', '스코프', 'body 에 #nk-skinN 스코프 ID 가 없음 — base 를 이길 힘 자체가 약함',
        'document.body.id = "' + (bodyId || '(빈값)') + '"',
        'layout.html <body> 에 id="nk-skin{번호}" + 모든 커스텀 CSS 를 그 스코프로 감쌀 것');
  }

  // F3) 토큰 미로드 (번들 지연) — 다른 진단의 신뢰도에 영향
  (function () {
    var v = (gcs(document.documentElement).getPropertyValue('--nk-theme') || '').trim();
    if (!v) add('🟡', 'F3', '배포', '디자인 토큰(--nk-theme)이 비어 있음 — 번들이 아직 안 왔거나 토큰 미정의',
                '--nk-theme = (빈값)',
                '하드리로드(Ctrl/Cmd+Shift+R) 후 5~10분 대기 재확인. 계속 비면 custom.css :root 토큰 정의 확인');
  })();

  // =========================================================================
  // A-2. ★ 작업 방식 판별 (HTML 네이티브 vs EZ 엎기) — 가장 먼저
  // =========================================================================
  var ezTheme = (document.body && document.body.getAttribute) ? document.body.getAttribute('data-ez-theme') : null;
  var dataEzCount = $$('[data-ez]').length;
  var themeCssLoaded = false;
  try {
    themeCssLoaded = Array.prototype.slice.call(document.styleSheets).some(function (s) { return /sub_theme|add_theme|add_layout/i.test(s.href || ''); });
  } catch (e) {}
  var hasEZST = !!window.EZST;
  var IS_EZ = !!(ezTheme || dataEzCount > 0 || themeCssLoaded || hasEZST);
  var METHOD = IS_EZ ? 'EZ-on-legacy (B)' : 'HTML-native (A)';

  if (IS_EZ) {
    add('⚠️', 'EZ-METHOD', '방식', 'EZ 엎기(EZ-on-legacy) 방식으로 판별됨 — EZ 전용 함정·후처리 적용',
        'data-ez-theme=' + (ezTheme || '?') + ', [data-ez] ' + dataEzCount + '개, 테마CSS=' + themeCssLoaded + ', EZST=' + hasEZST,
        '워크플로우 07/08 + strip(data-ez 제거). skin-method-detect.md 분기 B 참조');
    if (ezTheme) {
      add('⚠️', 'EZ-BODY-THEME', '방식/전역', 'body.theme(' + ezTheme + ')가 EZ 테마 색·폰트(#d0ac88 등)를 상시 주입 — base가 이김',
          'document.body.dataset.ezTheme=' + ezTheme,
          'strip(data-ez 제거) 또는 body' + S + '{} 토큰 재정의 + 테마CSS 차단. (#d0ac88 출처 = EZ theme01 WARM)');
    }
    if (themeCssLoaded) {
      add('⚠️', 'EZ-THEME-LATELOAD', '방식/전역', 'sub_theme/add_theme CSS가 </body> 직전 late-load → 우리 CSS보다 나중 → 로드순서로 못 이김',
          '테마 CSS 로드됨',
          '로드순서 의존 금지 → ' + S + ' ID 스코프로 명시도로 이길 것 (EZ-2)');
    }
    if (dataEzCount > 0) {
      add('🟡', 'EZ-RESIDUE', '방식', 'data-ez 잔존 ' + dataEzCount + '개 — strip 미완료(우리식 자유편집 어려움)',
          '[data-ez] ' + dataEzCount + '개',
          'strip_ez.py 로 data-ez 제거 → HTML-clean (목표 0). 단 ez/ez-module·smart-banner 시스템 파일은 보존');
    }
  }

  // =========================================================================
  // B. 전역 골격
  // =========================================================================
  // F10) body max-width 좌측 쏠림
  (function () {
    var c = gcs(document.body);
    if (c && c.maxWidth !== 'none' && px(c.maxWidth) > 0) {
      add('❌', 'F10', '전역/골격', 'body 에 max-width 가 박혀 전체가 좌측으로 쏠림 (좌측 쏠림이면 1순위 용의자)',
          'body max-width=' + c.maxWidth,
          'body' + S + '{max-width:none!important; margin-left:auto!important; margin-right:auto!important}');
    }
  })();

  // F27) #contents 풀폭 아님
  (function () {
    var el = $('#contents') || $('#container #contents');
    if (el) {
      var c = gcs(el), w = rectW(el), p = el.parentElement ? rectW(el.parentElement) : window.innerWidth;
      var ratio = p ? w / p : 1;
      if (ratio < 0.97 && c.marginLeft === c.marginRight) {
        add('⚠️', 'F27', '전역/골격', '#contents 가 부모 폭을 못 채워 좌우 흰 gap (EZ MO 92% / max-width 캡)',
            Math.round(ratio * 100) + '% of parent' + (c.maxWidth !== 'none' ? ', max-width=' + c.maxWidth : ''),
            S + ' #container #contents{width:100%!important; max-width:none!important}');
      }
    }
  })();

  // 헤더/푸터 .inner 폭 ≠ 본문 폭 (헤더가 본문보다 넓거나 좁음)
  (function () {
    var hi = $('#header .inner'), ci = $('#container.inner') || $('#contents .inner') || $('#contents');
    if (hi && ci) {
      var wh = rectW(hi), wc = rectW(ci);
      if (wh && wc && Math.abs(wh - wc) > 24) {
        add('⚠️', 'INNER-W', '전역/골격', '헤더 폭과 본문 폭이 달라 큰 화면에서 헤더가 본문을 넘거나 좁음',
            '#header .inner ' + Math.round(wh) + 'px vs 본문 ' + Math.round(wc) + 'px',
            S + ' #container.inner, body' + S + ' #header .inner, body' + S + ' #footer .inner{max-width:var(--nk-container,1440px)!important; width:100%!important; margin:0 auto; box-sizing:border-box}');
      }
    }
  })();

  // F6) .inner 이중 패딩
  (function () {
    var cont = $('#container'), inner = $('#container .inner') || $('#contents .inner');
    if (cont && inner) {
      var cp = px(gcs(cont).paddingLeft), ip = px(gcs(inner).paddingLeft);
      if (cp >= 30 && ip >= 30) {
        add('⚠️', 'F6', '전역/골격', '#container 와 내부 .inner 가 좌우 패딩을 이중으로 먹어 폭이 좁아짐',
            'container ' + cp + 'px + inner ' + ip + 'px',
            S + ' #container.inner #contents .inner{max-width:100%!important; padding-left:0!important; padding-right:0!important} /* .ec-base-help .inner 등 콘텐츠 박스는 패딩 복원 */');
      }
    }
  })();

  // F1) 전역 section 120px margin
  (function () {
    var s = $$('section').slice(0, 40).filter(function (e) { var c = gcs(e); return px(c.marginTop) >= 100 || px(c.marginBottom) >= 100; })[0];
    if (s) { var c = gcs(s);
      add('🟡', 'F1', '전역/골격', '전역 section 규칙(margin:120px)이 풀블리드 섹션에 큰 빈공간을 만듦',
          'section margin ' + c.marginTop + '/' + c.marginBottom,
          S + ' .nk-full{margin:0!important}  /* 풀블리드에만 */');
    }
  })();

  // F2) overflow-x:hidden 이 sticky 무력화
  (function () {
    var h = gcs(document.documentElement).overflowX, b = gcs(document.body).overflowX;
    if ((h === 'hidden' || b === 'hidden') && ($('.infoArea') || $('[class*="sticky"]'))) {
      add('🟡', 'F2', '전역/골격', 'html/body overflow-x:hidden 이 스크롤 컨테이너를 만들어 sticky(상세 우측 구매영역 등) 무력화 가능',
          'overflow-x html=' + h + ', body=' + b,
          'html,body{overflow-x:clip!important}  /* hidden→clip: 가로넘침은 막되 sticky 유지 */');
    }
  })();

  // =========================================================================
  // C. base 기본값 통째 스캔 (★ 나열 안 한 변수까지 잡는 그물)
  // =========================================================================
  var sampled = $$('a,strong,em,i,span,p,h1,h2,h3,h4,td,th,li,button').slice(0, 600);
  var redPrice = null, goldEl = null, blueLink = null, italicEl = null, baseFontEl = null, grayTable = null;
  sampled.forEach(function (el) {
    var c = gcs(el);
    if (!redPrice && (/price|cost|won/i.test(el.className) || (el.parentElement && /price/i.test(el.parentElement.className))) && reddish(rgbOf(c.color))) redPrice = el;
    if (!goldEl && (gold(rgbOf(c.color)) || gold(rgbOf(c.backgroundColor)) || gold(rgbOf(c.borderTopColor)))) goldEl = el;
    if (!blueLink && el.tagName === 'A' && bluish(rgbOf(c.color))) blueLink = el;
    if (!italicEl && c.fontStyle && c.fontStyle.indexOf('italic') === 0) italicEl = el;
    if (!baseFontEl && baseFont(c.fontFamily)) baseFontEl = el;
  });
  $$('table').slice(0, 20).forEach(function (t) {
    if (grayTable) return;
    var c = rgbOf(gcs(t).borderTopColor) || rgbOf(gcs(t).borderColor);
    if (c && c[0] > 200 && c[1] > 200 && c[2] > 200 && Math.abs(c[0] - c[1]) < 12 && px(gcs(t).borderTopWidth) > 0) grayTable = t;
  });

  if (redPrice) add('⚠️', 'PRICE-RED', '가격', '가격이 base 기본 빨간색으로 표시됨 (디자인 토큰 색 아님)',
      shortSel(redPrice) + ' color=' + gcs(redPrice).color,
      S + ' .xans-product-listitem .price strong, ' + S + ' .price{color:var(--nk-font,#1a1a1a)!important}');
  if (goldEl) add('⚠️', 'F9', '전역', 'EZ 기본 골드(#d0ac88)가 잔존 — css/module 2차 base 레이어 토큰화 누락 의심',
      shortSel(goldEl) + ' 에 골드색',
      'css/module + layout/basic/css 양쪽 토큰화. ' + S + ' {해당셀렉터}{color/background:var(--nk-theme)}');
  if (blueLink) add('🟡', 'LINK-BLUE', '전역', '링크(a)가 base 기본 파란색 — 톤 불일치',
      shortSel(blueLink) + ' color=' + gcs(blueLink).color,
      S + ' a{color:var(--nk-font,#1a1a1a)} ' + S + ' a:hover{text-decoration:underline}');
  if (italicEl) add('⚠️', 'ITALIC', '전역', 'italic(기울임)이 적용된 요소 발견 — 누끼토끼 규칙상 italic 금지',
      shortSel(italicEl) + ' font-style=italic',
      S + ' em, ' + S + ' i, ' + S + ' [style*="italic"]{font-style:normal!important; font-weight:700}');
  if (baseFontEl) add('⚠️', 'BASEFONT', '전역', 'base/EZ 기본 폰트(굴림/돋움)가 우리 폰트를 이김',
      shortSel(baseFontEl) + ' font=' + gcs(baseFontEl).fontFamily,
      S + ' {해당영역}{font-family:"Pretendard",-apple-system,"Apple SD Gothic Neo",sans-serif!important}');
  if (grayTable) add('🟡', 'TABLE-GRAY', '전역', '테이블 테두리가 base 기본 회색 — 토큰 미적용',
      'table border=' + gcs(grayTable).borderTopColor,
      S + ' table{border-color:var(--nk-line,#e0e0e0)!important} ' + S + ' th{background:var(--nk-bg2)}');

  // =========================================================================
  // D. 영역별 폰트 스윕 (헤더~회원폼)
  // =========================================================================
  [
    ['헤더 메뉴', '#header .menu, .xans-layout-gnb, [class*="gnb"], #header .top_category'],
    ['검색창', '#header input[type="text"], .xans-layout-searchheader input'],
    ['푸터', '#footer, .xans-layout-footer'],
    ['상품명', '.xans-product-listitem .name, [class*="prd"] .name'],
    ['상품 설명', '.xans-product-listitem .description'],
    ['상품 상세', '.xans-product-detail, .nk-pdp'],
    ['장바구니', '.xans-order-orderbasketlist, [class*="basket"]'],
    ['게시판', '.xans-board-listitem, .xans-board-detail'],
    ['회원/로그인', '.xans-member-login, .xans-member-agreement, .myshopArea']
  ].forEach(function (row) {
    var el = $(row[1]);
    if (!el) return;
    var ff = gcs(el).fontFamily;
    if (!goodFont(ff)) {
      add('🟡', 'FONT', row[0], row[0] + ' 폰트가 우리 폰트가 아님',
          'font=' + ff,
          S + ' ' + shortSel(el) + '{font-family:"Pretendard",-apple-system,"Apple SD Gothic Neo",sans-serif!important}');
    }
  });

  // =========================================================================
  // E. 헤더
  // =========================================================================
  (function () { // F7 로고 중앙/고정폭 (실측: .xans-layout-logotop{width:800px;text-align:center})
    var logo = $('.xans-layout-logotop') || $('#header [class*="logo"]') || $('.xans-layout-logo');
    if (logo) { var c = gcs(logo);
      if (c.textAlign === 'center' || (c.width !== 'auto' && px(c.width) >= 400))
        add('⚠️', 'F7', '헤더', '로고가 base(logotop.css)에 의해 가운데/고정폭으로 강제됨',
            '로고 ' + (c.textAlign === 'center' ? 'text-align:center' : 'width:' + c.width),
            S + ' #header .xans-layout-logotop, ' + S + ' #header [class*="logo"]{width:auto!important; margin:0 auto 0 0!important; text-align:left!important}');
    }
  })();
  (function () { // 헤더 우측 아이콘 오프셋 (부모 static)
    var box = $('#header .top_nav_box') || $('#header [class*="nav_box"]');
    var icon = $('#header .top_mypage') || $('#header [class*="mypage"]') || $('#header [class*="icon"]');
    if (box && icon && gcs(box).position === 'static' && gcs(icon).position === 'absolute') {
      add('🟡', 'HD-ICON', '헤더', '헤더 우측 아이콘이 absolute 인데 부모가 static → 컨테이너 패딩만큼 밖으로 빠짐',
          shortSel(box) + ' position:static',
          S + ' #header .top_nav_box{position:relative!important}');
    }
  })();
  (function () { // 유틸바 toparea
    var t = $('#header .toparea');
    if (t && gcs(t).display !== 'none') {
      add('🟡', 'TOPAREA', '헤더', '상단 유틸바(.toparea)가 살아있음 — 미니멀 헤더면 제거 대상(헤더 높이↑)',
          '.toparea display=' + gcs(t).display,
          S + ' #header .toparea{display:none!important}  /* + --nk-header-h 축소·#container padding-top 재정합 */');
    }
  })();

  // =========================================================================
  // F. PLP
  // =========================================================================
  (function () { // F13 그리드 25%
    var el = $('.nk-prd-grid > .nk-prd') || $('.xans-product-listitem li[style*="25"]');
    if (el) { var w = gcs(el).width;
      if (/%$/.test(w) && px(w) <= 30)
        add('⚠️', 'F13', 'PLP', '상품 그리드 카드가 base width:25% 주입으로 쪼그라듦',
            'item width=' + w, S + ' .nk-prd-grid > .nk-prd{width:100%; min-width:0; max-width:100%; float:none} ' + S + ' .nk-prd-grid img{display:block}');
    }
  })();
  (function () { // 리스트 마커
    var li = $('.xans-product-listitem li');
    if (li) { var c = gcs(li);
      if (c.listStyleType !== 'none' && px(c.marginLeft) + px(c.paddingLeft) > 0 && c.listStyleType !== 'outside')
        addOnce('🟡', 'LIST-MARK', 'PLP', '상품 목록 ul/li 에 base 리스트 마커/여백 잔존',
            'li list-style=' + c.listStyleType,
            S + ' .xans-product-listitem ul, ' + S + ' .xans-product-listitem li{list-style:none!important; margin:0!important; padding:0!important}');
    }
  })();
  (function () { // 아이콘박스 검정 띠
    var box = $('.prdList__item .icon__box') || $('.icon__box');
    if (box) { var bg = rgbOf(gcs(box).backgroundColor); var c = gcs(box);
      if (bg && (c.backgroundColor.indexOf('rgba') === 0) && px(c.width) > 200)
        add('🟡', 'ICONBOX', 'PLP', '상품카드 아이콘박스가 base 검정 반투명 띠로 전폭 깔림',
            shortSel(box) + ' bg=' + c.backgroundColor,
            S + ' .icon__box{background:none!important; width:auto!important; height:auto!important; padding:0!important}');
    }
  })();

  // =========================================================================
  // G. PDP
  // =========================================================================
  (function () { // F18 infoArea margin-left
    var el = $('.infoArea');
    if (el && px(gcs(el).marginLeft) >= 80)
      add('⚠️', 'F18', 'PDP', '상세 .infoArea 에 base margin-left(100px)가 남아 우측 구매영역이 잘림',
          '.infoArea margin-left=' + gcs(el).marginLeft, S + ' .nk-pdp .infoArea{margin:0!important; padding-left:0!important}');
  })();
  (function () { // 수량칸 높이
    var el = $('.xans-product-detail .quantity input[type="text"]') || $('.quantity input[type="text"]');
    if (el && px(gcs(el).height) > 44)
      add('🟡', 'QTY', 'PDP', '수량 입력칸 높이가 base 상속으로 부풀어짐',
          'quantity input height=' + gcs(el).height, S + ' .xans-product-detail .quantity input[type=text]{height:30px; line-height:28px; padding:0; text-align:center}');
  })();
  (function () { // detail_guide flex
    var el = $('#prdInfo .detail_guide') || $('.detail_guide');
    if (el && gcs(el).display === 'flex')
      add('🟡', 'F16', 'PDP', '상세 안내 아코디언(.detail_guide)이 base flex 2열 배치로 상단 어긋남',
          '.detail_guide display:flex', S + ' #prdInfo .detail_guide{display:block} ' + S + ' #prdInfo .detail_guide > .ec-base-fold{width:100%}');
  })();
  (function () { // 상세 이미지 overflow
    var el = $('.xans-product-detail img');
    if (el && gcs(el).maxWidth === 'none')
      addOnce('🟡', 'DETAIL-IMG', 'PDP', '상세 이미지에 max-width 제한 없음 → 모바일에서 넘침 가능',
          '.xans-product-detail img max-width=none', S + ' .xans-product-detail img{max-width:100%!important; height:auto!important}');
  })();

  // =========================================================================
  // H. 폼
  // =========================================================================
  (function () { // F20 select caret
    var el = $('select');
    if (el && px(gcs(el).paddingRight) < 28)
      add('🟡', 'F20', '폼', 'select 우측 caret 자리 부족 → 긴 옵션 텍스트와 겹칠 수 있음',
          'select padding-right=' + gcs(el).paddingRight, S + ' select{padding:0 36px 0 14px; appearance:none; background-image:url(SVG-caret); background-position:right 14px center; background-size:11px 7px}');
  })();
  (function () { // input 과도 높이
    var el = $('input[type="text"], input[type="password"]');
    if (el && px(gcs(el).height) > 52)
      add('🟡', 'INPUT-H', '폼', '입력칸 높이가 base 상속으로 과도하게 큼',
          'input height=' + gcs(el).height, S + ' input[type=text], ' + S + ' input[type=password], ' + S + ' textarea{height:40px; padding:10px 14px; line-height:20px; border:1px solid var(--nk-line)}');
  })();
  (function () { // 체크박스 accent
    var el = $('input[type="checkbox"], input[type="radio"]');
    if (el) { var ac = gcs(el).accentColor;
      if (!ac || ac === 'auto')
        add('🟡', 'ACCENT', '폼', '체크박스/라디오가 base 기본 색 (브랜드 accent 미적용)',
            'accent-color=' + ac, S + ' input[type=checkbox], ' + S + ' input[type=radio]{accent-color:var(--nk-theme)}');
    }
  })();
  (function () { // 버튼 색 (골드/파랑/회색 base)
    var el = $('.btnSubmit, .btnSubmitFix, .ec-base-button button, button[class*="btn"]');
    if (el) { var c = rgbOf(gcs(el).backgroundColor);
      if (gold(c) || bluish(c))
        add('⚠️', 'BTN-COLOR', '폼', '구매/제출 버튼이 base 기본색(골드/파랑) — 브랜드 색 아님',
            shortSel(el) + ' bg=' + gcs(el).backgroundColor, S + ' .btnSubmit, ' + S + ' .btnSubmitFix{background:var(--nk-accent)!important; border-radius:var(--nk-radius)}');
    }
  })();

  // =========================================================================
  // I. EZ 인라인 style=""
  // =========================================================================
  (function () {
    var inl = $$('[style]').filter(function (el) { return /font|color|margin|padding|width|background/i.test(el.getAttribute('style') || ''); });
    if (inl.length) {
      var sample = inl.slice(0, 3).map(function (el) { return el.tagName.toLowerCase() + '[style="' + (el.getAttribute('style') || '').slice(0, 40) + '…"]'; }).join(' | ');
      add('⚠️', 'EZ-INLINE', 'EZ 인라인', 'EZ 가 박은 인라인 style="" ' + inl.length + '곳 (외부 CSS 가 명시도로 못 이김 → !important 필요)',
          sample, '해당 요소를 .xans-* 부모로 좁혀 ' + S + ' .xans-… {…!important}. snippets/css/nk-ez-override.css 참고');
    }
  })();

  // =========================================================================
  // 출력
  // =========================================================================
  var report = {
    url: location.href,
    method: METHOD,
    viewport: (isMobile ? 'MOBILE' : 'PC') + ' (' + window.innerWidth + 'px)',
    skinScope: SKIN || '(없음 — S1)',
    count: findings.length,
    findings: findings,
    ts: new Date().toISOString()
  };
  var ord = { '❌': 0, '⚠️': 1, '🟡': 2 };
  findings.sort(function (a, b) { return (ord[a.sev] || 9) - (ord[b.sev] || 9); });

  console.log('%c🔎 nk-진단: base 오버라이드 점검', 'font-size:14px;font-weight:700;color:#1a1a1a');
  console.log('%c방식: ' + report.method + ' · ' + report.viewport + ' · 스코프 ' + report.skinScope + ' · 발견 ' + findings.length + '건', 'color:#666');
  if (!findings.length) {
    console.log('%c✅ 이 페이지·뷰포트에서 눈에 띄는 base 충돌이 안 보입니다. (다른 페이지·모바일도 실행 권장)', 'color:#137333;font-weight:600');
  } else {
    try { console.table(findings.map(function (f) { return { '심각도': f.sev, 'ID': f.id, '영역': f.area, '증상': f.symptom }; })); } catch (e) {}
    console.groupCollapsed('%c📋 처방 상세 (펼치기)', 'font-weight:700');
    findings.forEach(function (f, i) {
      console.log('%c' + (i + 1) + '. [' + f.sev + ' ' + f.id + '] ' + f.area + ' — ' + f.symptom, 'font-weight:700;color:#1a1a1a');
      console.log('   근거: ' + f.evidence);
      console.log('%c   처방: ' + f.fix, 'color:#1a73e8');
    });
    console.groupEnd();
  }
  console.log('%c원리: base 가 이기는 건 명시도/!important 때문. 원본 수정 말고 ' + report.skinScope + ' 스코프로 이길 것.', 'color:#999');

  window.__NK_DIAG__ = report;
  return report;
})();
