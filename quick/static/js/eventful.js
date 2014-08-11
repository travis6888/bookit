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
        url: 'https://www.eventbriteapi.com/v3/events/?city=Denver&token=VMJ33HPKLUJ3INR7ASCM',
        type: 'GET',
        dataType: 'json',
       success: function(movie_response) {
            console.log(movie_response);

        },
        error: function(error_response) {
            console.log(error_response);
        }
    });
