/**
 * Created by Travis on 8/19/14.
 */
$(document).ready(function(){
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
    eventbrite();
});