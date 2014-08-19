$(document).ready(function(){


    var geocoder;

    var map;
    var locationArray = [];
//
//    $.ajax({
//        url: '/get_locations/',
//        type: 'GET',
//        dataType: 'json',
//        success: function(response){
//            console.log(response)
//        },
//        error: function (response) {
//            console.log(response)
//        }
//    });

//    $('#searchBtn').on('click',function codeAddress(){
//        var sAddress = document.getElementById('searchVal').value;
//
//        geocoder.geocode({'address': sAddress}, function(results, status) {
//            if (status == google.maps.GeocoderStatus.OK){
//                map.setCenter(results[0].geometry.location);
//                console.log(results);
//                for(i=0; i<locationArray.length; i++){
//                    var markers = [];
//                    var infowindows = [];
//
//                    var content = "<h2>"+locationArray[i].title+"</h2><p>"+locationArray[i].description+"</p><p><a href='/view_project/"+locationArray[i].id+"'>See More</a></p>";
//                    var infowindow = new google.maps.InfoWindow({
//                        content: content
//                    });
//
//                    var marker = new google.maps.Marker({
//                        map: map,
//                        position: new google.maps.LatLng(locationArray[i].lat,locationArray[i].lng),
//                        title: locationArray[i].title,
//                        infowindow: infowindow
//                    });
//
//                    infowindows.push(infowindow);
//
//
//                    google.maps.event.addListener(marker, 'click', function(){
//                        this.infowindow.open(map, this);
//                    });
//
//                    markers.push(marker);
//
//
//                }
//
//            }
//            else{
//
//                alert("Geocode was not successful because: " + status);
//            }
//
//        });
//    });


    function initialize() {
        var mapOptions = {
            zoom: 12,
            center: new google.maps.LatLng(37.7833, -122.4167)
        };
        map = new google.maps.Map(document.getElementById('map-canvas'),
            mapOptions);
        geocoder = new google.maps.Geocoder();
    }


    google.maps.event.addDomListener(window, 'load', initialize);
});