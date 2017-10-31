var map;
var service;
var infowindow;
var location;
var latlng = {};
var markers = [];
var $select = $('#searchSelection');

function initialize() {
    var url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + "{{start.city}}" + '&key=AIzaSyCU3lP4pg-iFEcdIFpwGKDLKpaR6kbEC6Q';
    $.get(url,function(res){
        latlng = {lat: res.results[0].geometry.location.lat, lng: res.results[0].geometry.location.lng}
        var pyrmont = new google.maps.LatLng(latlng.lat, latlng.lng);

        map = new google.maps.Map(document.getElementById('map'), {
            center: pyrmont,
            zoom: 13
        });

        infowindow = new google.maps.InfoWindow();
        var service = new google.maps.places.PlacesService(map);

        var button = document.getElementById('addMeal')

        google.maps.event.addDomListener(button, 'click', function() {
            deleteMarkers();
            var meal = $('#meal').val();
            if(meal == '-'){
                meal = $('#meal_alt').val();
            }
            service.textSearch({
                query: meal + "+Restuarant",
                location: pyrmont,
                radius: 2000,
                minPriceLevel: $('#minPrice').val(),
            }, callback);
        });
    })
}

function callback(results, status) {
    $select.empty();
    if (status == google.maps.places.PlacesServiceStatus.OK) {
        for (var i = 0; i < results.length; i++) {
            createMarker(results[i]);
            var $option = $('<option/>').attr("value", results[i].name).text(results[i].name);
            $select.append($option);
        }
    }
}
function createMarker(place) {
    var placeLoc = place.geometry.location;
    var marker = new google.maps.Marker({
        map: map,
        position: place.geometry.location
    });

    markers.push(marker);
    google.maps.event.addListener(marker, 'click', function() {
        infowindow.setContent(place.name);
        infowindow.open(map, this);
    });
 }

 function setMapOnAll(map) {
     for (var i = 0; i < markers.length; i++) {
         markers[i].setMap(map);
     }
 }

 function clearMarkers(){
     setMapOnAll(null);
 }
 function deleteMarkers(){
     clearMarkers();
     markers=[];
 }
