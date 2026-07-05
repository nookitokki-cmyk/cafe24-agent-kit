/*
 * nk-cart-app.js — 카트 JS 재구축 엔진 (재사용)
 * [검증됨 2026-07-06 · 프로토타입]
 *
 * 원리: 카페24 원본 장바구니(#nk-src, 화면 밖 배치)를 그대로 두고,
 *       그 안 데이터(상품명·가격·수량·총액)를 JS로 읽어 커스텀 UI(#nk-cart-app)를 새로 그린다.
 *       커스텀 버튼은 "숨긴 원본의 진짜 버튼을 대신 클릭"해 기능을 연결한다(프록시).
 *       → 표를 안 뜯으므로 주문이 안 깨지고, 겉모습은 100% 커스텀.
 *
 * ★ 안전 규칙(오늘 삽질로 확정):
 *   1) #nk-src 는 visibility:hidden 금지! (숨긴 요소는 클릭 안 됨) → position:absolute; left:-99999px 로만 숨긴다.
 *   2) 주문 링크는 a[link-order] 첫 번째가 아니라 '전체상품주문' 텍스트로 정확히 골라야 함(스토어픽업 링크 오선택 주의).
 *   3) 수량 변경/삭제/주문은 원본 <a> 를 .click() 프록시. 카페24가 페이지를 리로드하면 이 스크립트가 다시 그린다.
 *
 * ⚠️ [프로토타입] 검증됨: 단순 상품 렌더 + 전체상품주문 라우팅.
 *    하드닝 필요: 옵션 상품·품절·배송그룹 여러 개·수량 동기화 정밀도.
 *
 * 사용: basket-app-skeleton.html 참고. `<!--@js(/_nk/js/nk-cart-app.js)-->` 로 로드하거나 인라인.
 */
(function () {
  function T(el) { return el ? (el.textContent || "").replace(/\s+/g, " ").trim() : ""; }
  // 원(₩) 금액 추출
  function won(s) { var m = (s || "").match(/[0-9][0-9,]*\s*원/); return m ? m[0].replace(/\s/g, "") : ""; }

  function build() {
    var src = document.getElementById("nk-src");        // 숨긴 카페24 원본 카트
    var app = document.getElementById("nk-cart-app");    // 커스텀 UI가 그려질 곳
    if (!src || !app) return;

    // 상품 줄 = 수량 입력(.ec-base-qty)과 이름(.name)이 있는 <tr>
    var rows = [].slice.call(src.querySelectorAll("tr")).filter(function (tr) {
      return tr.querySelector(".ec-base-qty") && (tr.querySelector(".name") || tr.querySelector("strong.name"));
    });

    if (!rows.length) {
      app.innerHTML = '<div class="nkc__empty"><p>장바구니가 비어 있습니다.</p><a href="/product/list.html">쇼핑하러 가기</a></div>';
      return;
    }

    // 1) 상품 카드 그리기 (원본에서 이름·이미지·수량·가격 읽기)
    var list = '<div class="nkc__list">';
    rows.forEach(function (tr, i) {
      var name = T(tr.querySelector(".name") || tr.querySelector("strong"));
      var im = tr.querySelector("img"); var img = im ? im.src : "";
      var qi = tr.querySelector(".ec-base-qty input"); var q = qi ? qi.value : "1";
      var price = won(T(tr));
      list += '<div class="nkc__item" data-i="' + i + '">' +
        '<div class="nkc__thumb"><img src="' + img + '" alt=""></div>' +
        '<div class="nkc__info"><p class="nkc__name">' + name + '</p>' +
        '<div class="nkc__qty"><button class="nkc__m" data-a="down">−</button><span class="nkc__q">' + q + '</span><button class="nkc__m" data-a="up">+</button></div></div>' +
        '<div class="nkc__r"><p class="nkc__price">' + price + '</p><button class="nkc__del">삭제</button></div>' +
        '</div>';
    });
    list += "</div>";

    // 2) 합계: 원본에서 가장 큰 콤마금액 = 결제예정금액(근사)
    var amts = (T(src).match(/[0-9]{1,3}(?:,[0-9]{3})+원/g) || []);
    var total = amts.length ? amts.reduce(function (a, b) {
      return parseInt(a.replace(/[^0-9]/g, "")) >= parseInt(b.replace(/[^0-9]/g, "")) ? a : b;
    }) : "";

    // 3) 주문 링크: '전체상품주문' 텍스트로 정확히 선택 (★첫 번째 아님)
    var _lk = [].slice.call(src.querySelectorAll("a[link-order]"));
    var oa = _lk.filter(function (a) { return /전체상품주문/.test(a.textContent); })[0] || _lk[0];

    var summary = '<aside class="nkc__summary"><div class="nkc__srow"><span>결제예정금액</span><strong>' + total + '</strong></div>' +
      '<button class="nkc__order">전체상품주문</button>' +
      '<a class="nkc__cont" href="/product/list.html">쇼핑 계속하기</a></aside>';

    app.innerHTML = '<div class="nkc"><div class="nkc__main">' + list + '</div>' + summary + '</div>';

    // 4) 배선 연결: 커스텀 버튼 → 숨긴 원본 클릭(프록시)
    app.querySelectorAll(".nkc__item").forEach(function (card) {
      var tr = rows[+card.getAttribute("data-i")];
      var qa = tr.querySelectorAll(".ec-base-qty a");  // [0]=증가, [1]=감소
      card.querySelectorAll(".nkc__m").forEach(function (b) {
        b.onclick = function () { var a = b.getAttribute("data-a") === "up" ? qa[0] : qa[1]; if (a) a.click(); };
      });
      card.querySelector(".nkc__del").onclick = function () {
        var d = [].slice.call(tr.querySelectorAll("a")).filter(function (a) { return /삭제/.test(a.textContent); })[0];
        if (d) d.click();
      };
    });
    var ob = app.querySelector(".nkc__order");
    if (ob) ob.onclick = function () { if (oa) oa.click(); };
  }

  // 카페24 카트 JS가 초기화된 뒤 실행
  if (document.readyState === "complete") setTimeout(build, 500);
  else window.addEventListener("load", function () { setTimeout(build, 500); });
})();
