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

	$('#id_categories').selectize({
   		placeholder: 'Selecciona una categoria'
   	});
	
});



