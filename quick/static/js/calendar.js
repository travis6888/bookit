/**
 * Created by Travis on 8/11/14.
 */

$(document).ready(function(){
    $.ajax({
        url:'https://www.googleapis.com/calendar/v3/users/me/calendarList?',
        type: 'GET',
        dataType: 'jsonp',
        success: function(response){
            console.log(response);
        },
        error: function(error){
            console.log(error);
        }

    })

});