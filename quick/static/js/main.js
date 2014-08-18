/**
 * Created by Travis on 8/17/14.
 */
$(document).ready(function(){
   $('.profileBtn').on('click', function(){
       $.ajax({
           url: "/meetup_api/",
           type: "GET",
           dataType: "json",
           success: function(response){
               console.log(response.data);
               $('.meetup').append("<h3>done</h3>")
           },
           error: function(response){
               console.log(response);
              $('.meetup').append("<h3>nope</h3>")

           }
       });
       $.ajax({
           url: "/trail_api/",
           type: "GET",
           dataType: "json",
           success: function(response){
               console.log(response.data);
               $('.trail').append("<h3>done</h3>")

           },
           error: function(response){
               console.log(response);
                              $('.trail').append("<h3>nope</h3>")

           }
       });
       $.ajax({
           url: "/api_test/",
           type: "GET",
           dataType: "json",
           success: function(response){
               console.log(response.data);
           $('.eventbrite').append("<h3>done</h3>")

           },
           error: function(response){
               console.log(response);
                          $('.eventbrite').append("<h3>nope</h3>")

           }
       });
   });
//    $('.carousel').carousel();

});