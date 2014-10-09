/* Project specific Javascript goes here. */

$(document).ready (function () {

	$(function() {
	  var loc = window.location.href; // returns the full URL
	  if(/dashboard/.test(loc)) {
	    $('#navbar').removeClass('visible-xs');
	    $('#left-sidebar').remove();
	  }
	});
	
});



