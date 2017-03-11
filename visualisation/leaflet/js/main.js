//Last updated in March 2017

var radius = d3.scale.sqrt().domain([1, 20]).range([20, 40])

var highlightColor = '#a9fcff';
var selectedColor = '#f442dc';

// For interactive map
var disableClusterZoomLevel = 8;
var markerOpacity = 0.35;

function initMap() {
	$.getJSON("data/leaflet_markers.json", makeMap);
}

var leaflet_json = null
function makeMap(raw_data) {
    leaflet_json = raw_data;
    makeFilteredMap(null);
}    


function get_filtered_leaflet_data(filter) {
    var raw_data = leaflet_json;
    if(filter === null) {
        return raw_data;
    }
    var data = [];
    for(var data_item of raw_data) {
        var filtered_item = {
            smells: [],
            centroid_lon: data_item.centroid_lon,
            centroid_lat: data_item.centroid_lat,
            total_smells_location_year: 0,
            formatted_year: data_item.formatted_year,
            location_name: data_item.location_name,
            moh: data_item.moh
        };
        for(var smell of data_item.smells) {
            if(smell.name === filter) {
                filtered_item.smells.push(smell);
                filtered_item.total_smells_location_year += smell.value;
            }
        }
        if(filtered_item.total_smells_location_year) {
            data.push(filtered_item);
        }
    }
    return data;
}

function makeFilteredMap(filter) {
    var data = get_filtered_leaflet_data(filter);
    ////////////// Map Parameters //////////////
    $("#map").remove();
    $("#map-and-controls").prepend("<div id=map></div>");

    var centreLatitude = 51.5;
    var centreLongitude = -0.12;
    var initialZoom = 10;

    var map = L.map('map', {
        zoomControl:true,
        maxZoom: 12,
        minZoom: 8,
    }).setView([centreLatitude, centreLongitude], initialZoom);


    // add basemap url here
    var mbUrl = ''

    var darkMap = L.tileLayer(mbUrl).addTo(map);
    // getting data to transform current borough to MOH
    var boroughToMoh = {}
    $.getJSON("data/moh_smell_category_borough_json.json",function(boroughToMohFromServer){
        boroughToMoh = boroughToMohFromServer;
    });
    $.getJSON("data/london_districts_latlong_with_centroids.json",function(borough_outlines){
        boroughLayer = L.geoJson( borough_outlines, {
          style: function(feature){
            return {
                color: "white",
                weight: 1,
                fillColor: 'none',
                fillOpacity: 0 };
            }
        }).addTo(map);
    });

    allmarkers = new L.layerGroup();

    for (var d of data) {

        var marker = L.piechartMarker(new L.LatLng(d.centroid_lat, d.centroid_lon), {
            radius: radius(d.total_smells_location_year),
            data: d.smells,
            time: d.formatted_year
            
        });

        var tooltipContentDiv;
        function tooltipContent(){
            tooltipContentDiv = '<h2 id="tooltipContentDiv" class="tooltipTitle">Borough: '+d.location_name+'</h2>'+
                                '<p id="tooltipContentDiv" class="tooltipDescription">Records: '+ d.total_smells_location_year+'</p>';

            return tooltipContentDiv;
        }

        marker.data = d;

        marker.on('click', function(e){
          var d = e.target.data;
            $('#map-info').css('opacity', '0.9');
            $('#map-info').html(function(){
                var title = d.location_name + ' ' + d.formatted_year.substr(0, 4);
                var sidebarContent = '<h1 id="tooltipContentDiv">'+title+'</h1>';
                var mohs = boroughToMoh[title]

                    // notes: smells per authority
                    for (var mohName in mohs) {
                        var moh = mohs[mohName];

                        sidebarContent +=
                        '<p>' +
                          '<a href="http://wellcomelibrary.org/item/'+moh.bID+'" target="_blank">'+
                          mohName+
                          '</a>' +
                        '</p>';
                        for (var smell of moh.smells) {
                            sidebarContent +=
                                "<h2>Smell: "+smell.cat+"</h2>"+
                                "<p>Reported "+smell.count+" times</p>";

                        };
                    }
                return sidebarContent;
            });
        })

        marker.bindPopup(tooltipContent());

        allmarkers.addLayer(marker);
    }

    // Animation - time slider
    sliderControl = L.control.sliderControl({
        position: "topright",
        layer: allmarkers,
        timeStrLength: 4,
        follow: 3 // displays markers only at specific timestamp
    });
    //Make sure to add the slider to the map ;-)
    map.addControl(sliderControl);
    // Initialize the slider
    sliderControl.startSlider();

    // Define base map layers
    var baseMaps = {
        "All": allmarkers
    };

    // Add controls
    L.control.layers(
        baseMaps, null, {collapsed:false, position:"bottomleft"}
    ).addTo(map);

    // Add legend title
    $('.leaflet-control-layers-expanded').prepend('<h3>Layers</h3>');

}

$(function(){
    $("select").change(function() {
        var selected_filter = $("select").val();
        console.log("changing selection to", selected_filter);
        if(selected_filter === "all smells") {
             makeFilteredMap(null);
        } else {
            makeFilteredMap(selected_filter);
        }        
    });  
});
