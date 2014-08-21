/**
 * Created by Travis on 8/19/14.
 */
$(document).ready(function(){
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

        }).complete(function(){
    $.when(
      $.ajax({
           url: "/meetup_api/",
           type: "GET",
           dataType: "json",
           success: function(response){
               console.log(response);
           },
           error: function(response){
               console.log(response);

           }
       }),
       $.ajax({
           url: "/trail_api/",
           type: "GET",
           dataType: "json",
           success: function(response){
               console.log(response);

           },
           error: function(response){
               console.log(response);

           }
       }),
       $.ajax({
           url: "/eventbrite_api/",
           type: "GET",
           dataType: "json",
           success: function(response){
               console.log(response);

           },
           error: function(response){
               console.log(response);
           }
       })
    ).then(function(){
        window.location.replace("/match/");
    });
        });
    calendar = function(){
         $('.loadingText').html("<h3> Getting Your Free Times</h3>");
        setTimeout(function(){
            eventbrite();

        },
        4000)
    };
    eventbrite = function(){
        $('.loadingText').html("<h3> Loading Events from EventBrite</h3>");
        setTimeout(function(){
            meetup();

        },
        4000)
    };
    meetup = function(){
        $('.loadingText').html("<h3> Loading Events from Meetup</h3>");
        setTimeout(function(){
            trail();

        },
        4000)
    };
    trail = function(){
        $('.loadingText').html("<h3> Loading Outdoor Events</h3>");

    };
    calendar();
});