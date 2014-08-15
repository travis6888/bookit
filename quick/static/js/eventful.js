/**
 * Created by Travis on 8/9/14.
 */

//eventful api call works well
$.ajax({
        url: 'http://api.eventful.com/json/events/search?app_key=pXS5JztFCZDmbxbG&keywords=music&location=San+Francisco&date=Future',
        type: 'GET',
        dataType: 'jsonp',
       success: function(movie_response) {
            console.log(movie_response);

        },
        error: function(error_response) {
            console.log(error_response);
        }
    });



//eventbrite api call works
$.ajax({
        url: 'https://www.eventbriteapi.com/v3/events/search/?popular=on&sort_by=date&location.within=25mi&location.latitude=37.790964500000000000&location.longitude=-122.401688400000010000&token=VMJ33HPKLUJ3INR7ASCM',
        type: 'GET',
        dataType: 'json',
       success: function(response) {
            console.log(response);
           var eventbriteArray = response.events;
        },
        error: function(error_response) {
            console.log(error_response);
        }
    });


