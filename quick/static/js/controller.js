/**
 * Created by Travis on 8/9/14.
 */
map.controller('eventController', function($scope, $http){
    $scope.events =[];
    $http({
        method:'jsonp',
        url:'https://www.eventbriteapi.com/v3/events/',
        params:{
            token: 'VMJ33HPKLUJ3INR7ASCM',
            q:'startup',
            venue: 'San Francisco',

//            page_limit: '20'
//            ,callback: 'JSON_CALLBACK'
        }
    }).success(function (data) {
            console.log(data);
        }).error(function (error) {
            console.log(error)
        }).then(function (promise) {
        for (var i=0; i<promise.data.length; i++){
            console.log(promise);
            $scope.events.push(promise.data[i])

        }
    });

});

map.controller('eventController', function ($scope, $http) {
    $scope.search = function (searched, city) {
        $scope.events2 = [];


        $http({
            method: 'jsonp',
            url: 'https://www.eventbrite.com/json/event_search?&app_key=VMJ33HPKLUJ3INR7ASCM',
            params: {

                keywords: searched,
                category: 'conferences',
                city: city
//            ,venue: 'San Francisco'

//            page_limit: '20'
            ,callback: 'JSON_CALLBACK'
            }
        }).success(function (data) {
            console.log(data);
        }).error(function (error) {
            console.log(error)
        }).then(function (promise) {
            for (var i = 0; i < promise.data.events.length; i++) {
                console.log(promise.data.events[i]);
                $scope.events2.push(promise.data.events[i]);



            }
        });
    }
});
//angular.module('appMaps', ['google-maps'])


//map.controller('eventController', function ($scope, $http, EventService) {
//
//    $scope.search = function (searched, city) {
//        $scope.eventslist = [];
//        longitudelist =[];
//        latitudelist =[];
//
//        $http({
//            methond: 'jsonp',
//            url: 'https://www.eventbriteapi.com/v3/events/search/',
//            params: {
//                token: 'VMJ33HPKLUJ3INR7ASCM',
//                q: searched + '&' + city,
//                popular: true
//
//
//            }
//        }).success(function (data) {
//            console.log(data);
//        }).error(function (error) {
//            console.log(error)
//        }).then(function (promise) {
//            for (var i = 0; i < promise.data.events.length; i++) {
//                console.log(promise.data.events[i].category);
////                console.log(promise.data.events[i].venue.latitude);
////                console.log(promise.data.events[i].venue.longitude);
//
//                $scope.eventslist.push(promise.data.events[i]);
//                latitudelist.push(promise.data.events[i].venue.latitude);
//                longitudelist.push(promise.data.events[i].venue.longitude);
//
//
//
//            }
//            console.log(latitudelist);
//            $scope.map = {center: {latitude: 37.89, longitude: -121.89 }, zoom: 4 };
//            $scope.options = {scrollwheel: false};
//            for(var j =0; j< latitudelist.length; j++){
//            $scope.markers = {
//                id: [j],
//                coords: {
//                    latitude: latitudelist[j],
//                    longitude: longitudelist[j]
//                }
//            }
//
//            }
//});
//
////            EventService.events = $scope.eventList;
////            EventService.longitude = longitudelist;
////            EventService.latitude = latitudelist;
//
//
//    }
//});

map.controller('mainCtrl', function ($scope, $log, EventService) {
    $scope.mapped = function () {
        $scope.map = {center: {latitude: 37.89, longitude: -121.89 }, zoom: 4 };
        $scope.options = {scrollwheel: false};

        var eventslst = EventService.events;
        var longitudelst = EventService.longitude;
        var latitudelst = EventService.latitude;
        console.log(latitudelst);
        console.log(longitudelst);
        for (var i = 0; i < latitudelst.length; i++) {
            $scope.markers = {
                id: [i],
                coords: {
                    latitude: latitudelst[i],
                    longitude: longitudelst[i]
                }
            }

        }
    }
});


map.factory('EventService', function () {
    return{
        events: [],
        longitude:[],
        latitude:[]

    }
});