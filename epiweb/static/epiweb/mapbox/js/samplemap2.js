var map = L.mapbox.map('map', 'examples.map-20v6611k')
    .setView([37.9, -77], 6);

var geoJson = [{
    type: 'Feature',
    geometry: {
        type: 'Point',
        coordinates: [-77, 37.9]
    },
    properties: {
        title: 'Marker One',
        // http://mapbox.com/developers/simplestyle/
        'marker-color': '#CC0033'
    }
},
{
    type: 'Feature',
    geometry: {
        type: 'Point',
        coordinates: [-78, 36.5]
    },
    properties: {
        title: 'Marker Two',
        'marker-color': '#0099ff'
    }
}];

map.markerLayer.setGeoJSON(geoJson);

function resetColors() {
    for (var i = 0; i < geoJson.length; i++) {
        geoJson[i].properties['marker-color'] = geoJson[i].properties['old-color'] ||
            geoJson[i].properties['marker-color'];
    }
    map.markerLayer.setGeoJSON(geoJson);
}

map.markerLayer.on('click',function(e) {
    resetColors();
    e.layer.feature.properties['old-color'] = e.layer.feature.properties['marker-color'];
    e.layer.feature.properties['marker-color'] = '#000';
    map.markerLayer.setGeoJSON(geoJson);
});

map.on('click', resetColors);