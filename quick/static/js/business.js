/**
 * Created by travis6888 on 2/4/15.
 */
$(document).ready(function () {


   $('.businessGetTimes').on('click', function(){
       window.location.replace("/loading_business/");
   });




    // Loading page has text that tells the user what is happening, changes every 5 seconds.
    calendar = function () {
        $('.loadingText').html("<h3> Getting Your Free Times</h3>");
        setTimeout(function () {
                matching();

            },
            4000)
    };
    matching = function () {
        $('.loadingText').html("<h3> Matching user Free Times to your Free Times</h3>");
        setTimeout(function () {
                finish();

            },
            4000)
    };
    finish = function () {
        $('.loadingText').html("<h3> Thank you for partnering with BookIt!</h3>");
        setTimeout(function () {


            },
            4000)
    };


    calendar();









});