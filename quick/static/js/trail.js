/**
 * Created by Travis on 8/13/14.
 */
$(document).ready( function(){
//    $.ajax({
//        url: 'https://outdoor-data-api.herokuapp.com/api.json?api_key=e65652575b4c95b8d78fae0621bf7428',
//        type: "GET",
//        dataType: 'jsonp',
//        success: function(response){
//            console.log(response);
//        },
//        error: function(error){
//            console.log(error);
//        }
//    });
//    $.ajax({
//        url: 'https://outdoor-data-api.herokuapp.com/api.json?api_key=e65652575b4c95b8d78fae0621bf7428&q[city_eq]=San+Jose&q[activities_activity_type_name_cont]=biking&q[radius]=30',
//        type: "GET",
//        dataType: 'jsonp',
//        success: function(response){
//            console.log(response);
//        },
//        error: function(error){
//            console.log(error);
//        }
//    });
//
//
    $.ajax({
        url: 'http://api.eventful.com/json/events/search?app_key=pXS5JztFCZDmbxbG&keywords=startup&location=San+Francisco&date=Future&page_size=30&sort_order=popularity',
        type: "GET",
        dataType: 'jsonp',
        success: function(response){
            console.log(response);
        },
        error: function(error){
            console.log(error);
        }
    });

//    $.ajax({
//        url: 'http://api.eventful.com/json/categories/list?app_key=pXS5JztFCZDmbxbG',
//        type: "GET",
//        dataType: 'jsonp',
//        success: function(response){
//            console.log(response);
//        },
//        error: function(error){
//            console.log(error);
//        }
//    });

});
