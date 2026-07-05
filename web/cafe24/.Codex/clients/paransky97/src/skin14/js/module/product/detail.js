function removePagingArea(oTarget)
{
    if ($(oTarget).length < 1 && (oTarget != '#prdReview' || oTarget != '#prdQna')) return;

    if ($(oTarget).css('display') == 'block') {
        if (oTarget == '#prdReview') {
            var record = $('.xans-record-', '.xans-product-review').first();
            if (record.length < 1 || record.is(':not(:visible)')) {
                $('.xans-product-reviewpaging').remove();
             }
         } else if (oTarget == '#prdQnA') {
            var record = $('.xans-record-', '.xans-product-qna').first();
            if (record.length < 1 || record.is(':not(:visible)')) {
                $('.xans-product-qnapaging').remove();
            }
         }
     }
}

$(function() {

    $('#actionCartClone, #actionWishClone, #actionBuyClone, #actionWishSoldoutClone').off().on('click', function() {
        try {
            var id = $(this).attr('id').replace(/Clone/g, '');
            if (typeof(id) !== 'undefined') $('#' + id).trigger('click');
            else return false;
        } catch(e) {
            return false;
        }
    });

    function productDetailOrigin(){
        var imgChk = $('#prdDetailContent').find('img').length;
        if(imgChk <= 0){
            $('#prdDetailBtn').remove();
        }
    }
    productDetailOrigin();

    // Add Image
    var oTarget = $('.xans-product-mobileimage ul li');
    var oAppend = oTarget.first().children('p').clone();

    oTarget.slice(1).each(function() {
        this.innerHTML = '<p class="thumbnail">' + oAppend.html() + this.innerHTML + '</p>';
        if ($(this).children('p').children('img').length > 1) {
            $(this).children('p').children('img').first().remove();
        }
    });
});


/** 아키테이블_JS 210519 **/
jQuery(document).ready(function() {

	/* 상세 관련상품 */
	if (jQuery('.xans-product-relation').val() != undefined) {	//관련상품 모듈 있을떄만 실행(없으면 주문서페이지에서 오류) -정환
		var relation_slide = new Swiper('.relation_slide', {
			slidesPerView: 4,
			spaceBetween: 20,
			observer: true,
			observeParents: true,
			watchOverflow: 'true', // 스와이프가 한개일때 버튼 라인 비활성
			speed:700,
			navigation: {
				nextEl: '.swiper-next-relation',
				prevEl: '.swiper-prev-relation',
			},
			pagination: {
				el: '.swiper-pagination-relation',
				clickable: true,
			},
			autoplay: {
				delay: 5000,
				disableOnInteraction: false,
			},
			breakpoints: {
				768: {
					slidesPerView: 2,
					spaceBetween: 10,
				},
			}
		});
	}

	/* 할인율 없을시 상품명길이 수정 */
	setTimeout(function(){
		jQuery(".sale_box").each(function(){
			jQuery(".xans-product-detail .headingArea").addClass('sale_on');
		});
	},500)

	/* 상품상세 탭 고정 */
	jQuery(window).scroll(function() {
		var header_height = jQuery('#header .top_nav_box').innerHeight();
		var jh_offset = jQuery('.tabProduct_box').offset();
		if ((jQuery(document).scrollTop() + header_height) >= jh_offset.top ) {
			jQuery('#tabProduct').addClass('tab_fixed');
			jQuery('#tabProduct').css('top',header_height + 1);
		} else {
			jQuery('#tabProduct').removeClass('tab_fixed');
		}
	});

    // 상품상세 탭 이벤트
    $('#tabProduct a').click(function(e){
		var header_height = jQuery('#header .top_nav_box').innerHeight();
        var oTarget = $(this).attr('href');
		var offset = $('.xans-product-additional').offset(); //선택한 태그의 위치를 반환
		$('html').animate({scrollTop : offset.top - header_height}, 400);
        $(this).parent('li').addClass('selected').siblings().removeClass('selected');
        $('#tabProduct a').each(function(){
            var oSiblings = $(this).attr('href');
            if (oTarget != oSiblings) {
                $(oSiblings).hide();
            } else {
                $(oTarget).show();
            }
        });
        removePagingArea(oTarget);
        if(e) e.preventDefault();
    });
});