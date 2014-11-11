/* Project specific Javascript goes here. */

$(document).ready (function () {

	$('#id_from_date').datepicker({
    	weekStart: 1,
    	format: "yyyy-mm-dd",
	});

	$('#id_to_date').datepicker({
    	weekStart: 1,
    	format: "yyyy-mm-dd",
	});

	// $(function() {
	//   var loc = window.location.href; // returns the full URL
	//   if(/dashboard/.test(loc)) {
	//     $('#navbar').removeClass('visible-xs');
	//     $('#left-sidebar').remove();
	//   }
	// });

	$('#id_categories').selectize({
   		placeholder: 'Selecciona una categoria'
   	});
	
});



