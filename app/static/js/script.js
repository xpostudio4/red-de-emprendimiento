

$(document).ready(function() {

	$(function() {
		if ($('#cover').length > 0) {
			$('#navbar').addClass('hidden-md hidden-lg');
		}
	});
	

	$( "#cover" ).each(function(){
        var $this = $(this);
        $this.css({'min-height':($(window).height())+'px'});
 
        // Recalculate on window resize
        $(window).resize(function(){
            $this.css({'min-height':($(window).height())+'px'});
        });
    });


	// Learn more button scroll
 
	$("#scroll").click(function() {
	    $('html, body').animate({
	        scrollTop: $("#categories-scroll").offset().top
	   		}, 1000);
		});

	// controls category slideLeftMine animation

	$(window).scroll(function() {
		$('.category-left').each(function(){
		var imagePos = $(this).offset().top;

		var topOfWindow = $(window).scrollTop();
			if (imagePos < topOfWindow+800) {
				$(this).addClass("slideLeftX");
			}
		});
	});

	// controls category slideRightMine animation

	$(window).scroll(function() {
		$('.category-right').each(function(){
		var imagePos = $(this).offset().top;

		var topOfWindow = $(window).scrollTop();
			if (imagePos < topOfWindow+800) {
				$(this).addClass("slideRightX");
			}
		});
	});

	// controls category slideUpMine animation

	$(window).scroll(function() {
		$('.category-up').each(function(){
		var imagePos = $(this).offset().top;

		var topOfWindow = $(window).scrollTop();
			if (imagePos < topOfWindow+800) {
				$(this).addClass("slideUpX");
			}
		});
	});

	// controls inspire page animation

	$('.company img, .company .btn-success').hover(
		function() {
		$(this).addClass("pulse");
	}, function() {
		$(this).removeClass("pulse");
	});

});