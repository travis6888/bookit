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
    });
    $('.inviteSubmit').on('click', function(){
        var friendsEmail = $('.friendEmail').val();
        console.log(friendsEmail)
        friendsEmail2 = JSON.stringify(friendsEmail);
        $.ajax({
            url: '/invite_friends/',
            type: "POST",
            dataType: "json",
            data: friendsEmail2,
            success: function(response){
                console.log(response);
            },
            error: function(response){
                console.log(response);

            }

        })
    });

    $('.friendSubmit').on('click', function(){
        var referrer = $('.friend').val();
        console.log(referrer);
        $('.friend').val('');
        referrer = JSON.stringify(referrer);
        $.ajax({
            url: '/add_friend/',
            type: 'POST',
            dataType: 'html',
            data: referrer,
            success: function(response){
                console.log(response)
            },
            error: function(response){
                console.log(response)
            }
        })
    });


    $('.seeMore').on('click', function(){
       $(this).text(function(i,text){
                        return text === "More Events" ? "Less Info" : "More Events";
                    });
       $(this).parent().parent().siblings('.extra-events').toggle()
    });

    $('.mapEvents').on('click', function(){
        $('.event-content').toggle('slow');
        $('.map-container').height(600).slideToggle(0, function(){
            google.maps.event.trigger(map, "resize")
        });

    });



    $('.loadEvents').on('click', function() {
        window.location.replace("/loading/");
    });

    $('.profileCreateBtn').on('click', function(){
        $.ajax({
            url: '/profile/',
            dataType: 'json',
            type: "GET",
            success: function(response){
                console.log(response)
            },
            error: function(response){
                console.log(response)
            }

        });
    });
});