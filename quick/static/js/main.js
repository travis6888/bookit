/**
 * Created by Travis on 8/17/14.
 */
$(document).ready(function () {

    // Gets all the matched events
    $('.eventBtn').on('click', function () {
        $.ajax({
            url: '/match/',
            dataType: 'html',
            type: 'GET',
            success: function (reponse) {
                console.log(reponse);
                $('.events').html(reponse);
            },
            error: function (error) {
                console.log(error);
            }
        });
    });

    // Posts the picked event to users google calendar
    $('.bookit').on('click', function () {
        var event_id = $(this).data('id');
        var eventInfo = JSON.stringify(event_id);
        $(this).hide();
        $(this).siblings('.bookedBtn').show();

        $.ajax({
            url: '/post_event/',
            type: 'POST',
            dataType: 'json',
            data: eventInfo,
            success: function (response) {
                console.log(response);


            },
            error: function (response) {

            }


        })
    });

    // Allows the user to invite their friends through email
    $('.inviteSubmit').on('click', function () {
        var friendsEmail = $('.friendEmail').val();
        var friendsEmail2 = JSON.stringify(friendsEmail);
        $.ajax({
            url: '/invite_friends/',
            type: "POST",
            dataType: "json",
            data: friendsEmail2,
            success: function (response) {
                console.log(response);
            },
            error: function (response) {
                console.log(response);

            }

        })
    });

    // Lets people say who referred them to the service when signing up
    $('.friendSubmit').on('click', function () {
        var referrer = $('.friend').val();
        console.log(referrer);
        $('.friend').val('');
        referrer = JSON.stringify(referrer);
        $.ajax({
            url: '/add_friend/',
            type: 'POST',
            dataType: 'html',
            data: referrer,
            success: function (response) {
                console.log(response)
            },
            error: function (response) {
                console.log(response)
            }
        })
    });


    // Lets the user see more events
    $('.seeMore').on('click', function () {
        $(this).text(function (i, text) {
            return text === "More Events" ? "Less Info" : "More Events";
        });
        $(this).parent().parent().siblings('.extra-events').toggle()
    });

    // Lets user see all of the events on a google map
    $('.mapEvents').on('click', function () {
        $('.event-content').toggle('slow');
        $('.map-container').height(600).slideToggle(0, function () {
            google.maps.event.trigger(map, "resize");
        });

    });


    // Redirects to loading page, where the matched events will be pulled
    $('.loadEvents').on('click', function () {
        window.location.replace("/loading/");
    });

    // User can create a profile with zipcode and interests
    $('.profileCreateBtn').on('click', function () {
        $.ajax({
            url: '/profile/',
            dataType: 'json',
            type: "GET",
            success: function (response) {
                console.log(response)
            },
            error: function (response) {
                console.log(response)
            }

        });
    });
});