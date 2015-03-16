

$(document).ready(function() {

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


	// Activates change profile picture

	$('#id_picture').change(
	    function(){
	         $(this).closest('form').trigger('submit');
	    });
 
   var picture = $("#id_user_pic");
 
   $(picture).click(function(e){
      e.preventDefault();
      $('#id_picture').trigger('click');
   });

   // controls dashboard create event button


   $( "#event-form-btn" ).click(function() {
	  $( "#event-form" ).slideToggle( 500, "linear" );
	});

   // controls dashboard add user button


   $( "#add-new-user-btn" ).click(function() {
	  $( "#add-new-user-form" ).slideToggle( 500, "linear" );
	});

	// controls dashboard show event description


   $( ".show-description" ).click(function() {
	  $( this ).parents('tr').next().slideToggle();
	});

   // add class to change password form

   $('#id_new_password1, #id_new_password2').addClass('form-control');


  //password change
   var password_change = $('#password-change');
     password_change.click(function(event){
       event.preventDefault();
         $.ajax({
           url: '/accounts/password_change/',
           data: $('#password-change-form').serialize(),
           type: "POST",
           success:
           function(result){
             //if result.is_changed is true activate message
             //telling the user the password has been changed
             if(result.is_changed){
               if(!$('#change_success_message').hasClass('hidden')){
                 $('#change_success_message').addClass('hidden');
                 }
                 $('#change_success_message').removeClass('hidden');
               }else{
                 //else it should display
                 if(!$('#change_success_message').hasClass('hidden')){
                   $('#change_success_message').addClass('hidden');
                   }
                   $('#change_error_message').html(result.reasons).removeClass('hidden');
                 }
               },
           error:
           function(){
             $('#change_error_message').val('Estamos experimentando problemas con el servidor. Intentelo luego.').show();
             }
             });
                  });

    var users = $('.user');

    users.click(function(event){
      event.preventDefault();
      
      var user_deletion = confirm("Estas seguro que deseas borrar este evento?");

      var id = this.dataset.id;
      if( user_deletion==true){
      $.ajax({
        url: '/accounts/dashboard_userdeletion/'+ id + '/',
        type: "POST",
        data: {csrfmiddlewaretoken: csrf_token},
        success:
          function(result){
            if( result.is_deleted == true){
              var user = document.querySelector('#user-' + id);
              user.parentNode.removeChild(user);
            }else{
            alert('El usuario no pudo ser eliminado, trate mas tarde');
            }
          },
        error:
          function(){
            console.log('error');
          }
      });
      }else{
      return false;
      }
    });

});
