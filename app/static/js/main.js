/* Author:
	Sam Sherwood
	Optiem LLC
*/
// Prepare
(function (window, undefined) {

	// Heading off IE7 specific behavior; giving the entire site a vertical scrolling experience.
	var siteLinks = $('.ie7 a[href^="?"]');

	/*siteLinks.each(function (index, siteLink) {
	var url = $(siteLink).attr('href');
	$(siteLink).attr('href', url.replace('?page=', '#'));
	});

	$(siteLinks).on('click', function (event) {
	event.preventDefault();
	$(window).scrollTo($(this).attr('href'), slideTime);
	});*/

	if ($(siteLinks).length > 0) {
		$(window).scroll(function (event) {
			var siteNav = $('header nav');
			window.log($(window).scrollTop());

			if ($(window).scrollTop() >= 50 && !$(siteNav).hasClass('pinned')) {
				$(siteNav).animate({
					top: 0
				});

				$(siteNav).addClass('pinned');
			} else if ($(window).scrollTop() < 50 && $(siteNav).hasClass('pinned')) {
				$(siteNav).removeClass('pinned');
				$(siteNav).animate({
					top: 110
				});
			}
		});
	}
	//End IE7 re-engineering

	var History = window.History; // Note: We are using a capital H instead of a lower h

	var siteTitle = 'Kauffman Foundation | ';
	var slideTime = 1000;

	var pane = $('#pane');

	if ($('html').hasClass('ie7')) {
		pane = $(window);
	}

	pane.css({
		width: pane.width() + 'px'
	});

	function pageInit() {
		window.log('Starting Page Initiation');
		var margin = adjustMargins();
		window.log(margin);
		adjustScroll(margin);

		$('article').fadeIn(1000);

		$(window).off('statechange');
		$(window).on('statechange', function (event) {
			//alert('changing state');
			window.log('state changed', History.getState());
			urlState = History.getState().data.page;
			adjustScroll(margin);
			activeState(urlState);
		});
	}

	function adjustScroll(margin) {
		//window.log('Adjusting Scroll');
		var urlState = History.getState().data.page;
		//alert('URL state: ' + urlState);
		if (urlState) {
			//alert('adjusting scroll to: ' + urlState);

			$(pane).scrollTo('#' + urlState, slideTime, { offset: -margin });

			googleEvent('Page Interaction', 'Scroll To', urlState);
		}
	}

	function adjustMargins() {

		if ($('html').hasClass('ie7')) {
			return 0;
		}

		//alert('bird is the word');
		var documentWidth = $(window).width();
		//alert(documentWidth);
		var itemWidth = $('article:first-child').width();
		//alert(documentWidth - itemWidth);

		var margin = (documentWidth - itemWidth) / 2;
		//alert(margin);

		var elements = $('#main article');

		//$('#main').css('paddingLeft', margin);
		//$('#main').css('paddingRight', margin);

		elements.css('marginLeft', margin);
		elements.css('marginRight', margin);

		$('#main').css('width', elements.length * (margin * 2 + 900));

		return margin;
	}

	//Navigation Scrolling
	function navigationScroll() {
		var jumpLinks = $('a[href^="?"]');

		jumpLinks.each(function (index) {
			$(this).off('click');
			$(this).on('click', function (event) {
				event.preventDefault();
				History.pushState({ page: $(this).attr('href').replace('?page=', '') }, siteTitle + $(this).attr('alt'), $(this).attr('href'));
				/*$('#pane').scrollTo($(this).attr('href').replace('?page=', '#'), slideTime, { offset: -margin });
				googleEvent('Page Interaction', 'Scroll To', $(this).attr('href').replace('?page=', '#'));
				History.pushState(null, siteTitle + $(this).attr('alt'), $(this).attr('href'));
				activeState($(this).attr('href').replace('?page=', ''));
				return false;*/
			});
		});
	}


	//Track the active item and update it's respective navigation item with an active class.
	function activeState(currentSection) {
		var pageElements = $('li, article');

		if (currentSection == "" || typeof currentSection == 'undefined') {
			currentSection = "home";
		}

		//Strip out trailing numbers to group sections and their children
		currentPage = currentSection;
		window.log('current section: ', currentSection);
		currentSection = currentSection.replace(/[0-9]/g, '');
		//window.log('Current Section is', currentSection);

		pageElements.removeClass('active');
		$('*[id="' + currentPage + '"]').addClass('active');
		$('*[href*="' + currentSection + '"]').parent().addClass('active');

	}

	function factDialogue() {
		var factLinks = $('p.button');

		factLinks.on('click', function (event) {
			var fact = $(this).parent();
			if (fact.hasClass('open')) {
				fact.animate({
					top: 600 + 'px'
				}).toggleClass('open');
				$(this).text('Did You Know');
			} else {
				fact.animate({
					top: 580 - fact.height() + 'px'
				}).toggleClass('open');
				$(this).text(' ');
			}
		});
	}


	//Check for Document Ready state and start scripts
	$(document).ready(function () {
		//alert('document ready!');
		pageInit();
		factDialogue();
		navigationScroll();
		externalLinks();
		$(window).resize(function () {
			pageInit();
		});

	});

})(window);