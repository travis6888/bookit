/**
 * Created by Travis on 8/17/14.
 */
$(document).ready(function(){

    $('.eventBtn').on('click', function(){
        $.ajax({
            url: '/match/',
            dataType: 'html',
            type: 'GET',
            success: function(reponse){
                console.log(reponse);
                $('.events').html(reponse);
            },
            error: function(error){
                console.log(error);
            }
        })
    });

/// Closes the sidebar menu
    $("#menu-close").click(function(e) {
        e.preventDefault();
        $("#sidebar-wrapper").toggleClass("active");
    });

    // Opens the sidebar menu
    $("#menu-toggle").click(function(e) {
        e.preventDefault();
        $("#sidebar-wrapper").toggleClass("active");
    });


    $('.bookit').on('click', function(){
        var event_id = $(this).data('id');
        var eventInfo = JSON.stringify(event_id);
        $(this).hide();
        $(this).siblings('.bookedBtn').show();

        $.ajax({
            url: '/post_event/',
            type: 'POST',
            dataType: 'json',
            data: eventInfo,
            success: function(response){
                console.log(response);


            },
            error: function(response){

            }


        })
    })


});