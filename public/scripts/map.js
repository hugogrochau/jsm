var map;

function initialize() {
    var mapOptions = {
        zoom: 8,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    map = new google.maps.Map(document.getElementById('map-canvas'),
                            mapOptions);

    if (navigator.geolocation) {

        navigator.geolocation.getCurrentPosition(function(position) {

            var pos = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);

            map.setCenter(pos);
        });
    }
}

google.maps.event.addDomListener(window, 'load', initialize);