/**
 * Created by Travis on 8/19/14.
 */
$(document).ready(function(){
    mysuccess =function(){
        // When 3 ajax calls are done, redirects to page with the results
        window.location.replace("/match/")};
    myfailure = function(){
        // When 3 ajax calls are done, redirects to page with the results
        window.location.replace("/match/")};
    // Pulls the free time from user google calendar
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
//      Three Ajax calls that tell server to pull event data in the backend
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
       });
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
       });
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
       });
    }).complete(function(){
        myfailure();
        mysuccess();
    });


    // Loading page has text that tells the user what is happening, changes every 5 seconds.
    calendar = function(){
         $('.loadingText').html("<h3> Getting Your Free Times</h3>");
        setTimeout(function(){
            eventbrite();

        },
        5000)
    };
    eventbrite = function(){
        $('.loadingText').html("<h3> Loading Events from EventBrite</h3>");
        setTimeout(function(){
            meetup();

        },
        5000)
    };
    meetup = function(){
        $('.loadingText').html("<h3> Loading Events from Meetup</h3>");
        setTimeout(function(){
            trail();

        },
        5000)
    };
    trail = function(){
        $('.loadingText').html("<h3> Loading Outdoor Events</h3>");

    };
    calendar();
});