/**
 * Created by travis6888 on 2/4/15.
 */
$(document).ready(function () {







    // Loading page has text that tells the user what is happening, changes every 5 seconds.
    var calendar = function () {
        $('.loadingText').html("<h3> Getting Your Free Times</h3>");
        setTimeout(function () {
                profile();
                matching();

            },
            4000)
    };
    var matching = function () {
        $('.loadingText').html("<h3> Matching user Free Times to your Free Times</h3>");
        setTimeout(function () {
                finish();

            },
            4000)
    };
    var finish = function () {
        $('.loadingText').html("<h3> Thank you for partnering with BookIt!</h3>");
        setTimeout(function () {

            mysuccess();
            },
            4000)
    };


    calendar();


// Pulls the free time from user google calendar
    var profile = function() {
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
       })
   };

    var mysuccess = function () {
        // When 3 ajax calls are done, redirects to page with the results
        window.location.replace("/business_match/")
    };





});