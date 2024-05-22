(function ($) {
	"use strict";

	/*------ Sticky menu start ------*/
	var $window = $(window);
	
	/*------ daily deals carousel active start ------*/
	$('.product-deal-carousel--2').slick({
		autoplay: true,
		autoplaySpeed: 3000,
		dots: true,
		fade: false,
		speed: 1000,
		slidesToShow: 2,
		adaptiveHeight: false,
		responsive: [{
			breakpoint: 992,
			settings: {
				slidesToShow: 1
			}
		}]
	});
	/*------ daily deals carousel active end ------*/

	/*-------- prodct details slider active start --------*/
    $('.product-large-slider').slick({
        fade: true,
        arrows: false,
        asNavFor: '.pro-nav'
    });


	


  

}(jQuery));