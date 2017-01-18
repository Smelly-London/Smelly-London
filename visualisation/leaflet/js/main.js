//Code modified from Wellcome Trust Women's Work project: https://github.com/wellcometrust/womens-work/tree/master/visualisations/map

////////////////////////////////////////////////////////////////

var highlightColor = '#a9fcff';
var selectedColor = '#f442dc';

// For interactive map
var disableClusterZoomLevel = 8;
var markerOpacity = 0.35;

function initMap() {
	$.getJSON("/data/leaflet_markers.json", makeMap);
}

function makeMap(data) {
    ////////////// Map Parameters //////////////
    var centreLatitude = 51.5;
    var centreLongitude = 0.12;
    var initialZoom = 10;


    var map = L.map('map', {
        zoomControl:true,
        maxZoom: 21,
        minZoom: 2,
    }).setView([centreLatitude, centreLongitude], initialZoom);


    // add basemap url here
    var mbUrl = ''

    var darkMap = L.tileLayer(mbUrl).addTo(map);
    $.getJSON("/data/london_districts_latlong_with_centroids.json",function(borough_outlines){
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

    radiusScale = d3.scale.sqrt().domain([1, 20]).range([20, 40])
    //numbersmellsradiusScale = d3.scale.sqrt().domain([1, 20]).range([0, 20])

    function radius(total_number_smells){
        return radiusScale(total_number_smells)
    }

    allmarkers = new L.layerGroup();

    for (var i=0; i<data.length; i++) {
        var d = data[i];
        d.centroid_lat = parseFloat(d.centroid_lat);
        d.centroid_lon = parseFloat(d.centroid_lon);

        var marker = L.piechartMarker(new L.LatLng(d.centroid_lat, d.centroid_lon), {
            radius: radius(d.total_smells_location_year),
            data: d.smells,
            time: d.formatted_year
            //color: highlightColor,
            //fillOpacity: markerOpacity,
        });

        var tooltipContentDiv;
        function tooltipContent(){
            tooltipContentDiv = '<h2 id="tooltipContentDiv">Borough: '+d.location_name+'</h2>'+
                                '<p id="tooltipContentDiv">Records: '+ d.total_smells_location_year+'</p>';

            return tooltipContentDiv;
        }

        marker.data = d

        marker.on('click', function(e){
            // marker.setStyle({color:'blue'})
            e.target.setStyle({color:selectedColor})
            $('.infoWindow').css('opacity', '0.9');
            $('.infoWindow').css('height', 'auto');
            $('.infoWindow').html(function(){
                sidebarContent = '<h1 id="tooltipContentDiv">'+e.target.data.key+'</h1>';

                for (var m=0; m< e.target.data.values.length; m++) {
                    sidebarContent +=
                                    "<h2>REPORT #"+ (m + 1) +"</h2>"+
                                    "<p>Location "+e.target.data.values[m].location_name+"</p>"+
                                    '<p id="years">'+ e.target.data.values[m].year +'</p>'+
                                    //"<p><a href='"+ e.target.data.values[m].source_url +"' target='_blank'>Link to report</a></p>"+
                                    //"<p>"+e.target.data.values[m].contextText+"</p>"+
                                    '<hr>';

                };
                return sidebarContent;
            });
        })

        marker.on('popupclose', function(e){
            e.target.setStyle({color:highlightColor})
        })
        marker.bindPopup(tooltipContent());

        allmarkers.addLayer(marker);
    }
    // map.addLayer(allmarkers); // It's the slider showing them

    // Animation - time slider
	    sliderControl = L.control.sliderControl({
        position: "topright",
        layer: allmarkers,
        follow: 3 // displays markers only at specific timestamp
    });

    //Make sure to add the slider to the map ;-)
    map.addControl(sliderControl);
    // Initialize the slider
    sliderControl.startSlider();


    // Infowindow
    var infoContainer = L.Control.extend({
        options: {
            position: 'topright',
        },
        onAdd: function (map) {
            // create the control container with a particular class name
            var infoContainer = L.DomUtil.create('div', 'infoWindow');
            return infoContainer;
        }
    });
    map.addControl(new infoContainer());

    // Define base map layers
    var baseMaps = {
        "All": allmarkers
    };

    layer_names = ["All"];
    layer_urls = [allmarkers];

    var overlayMaps = {};
    for (i=0; i<layer_names.length; i++) {
        var layer_name = layer_names[i];
        var overlayLayer = layer_urls[i];
        overlayDiv = ('<span style="width: 10px; ' +
        'height: 10px; -moz-border-radius: 5px; -webkit-border-radius: 5px; border-radius: 5px; border: 1px solid #FFF; float: left; margin-right: 0px; margin-left: 0px;' +
        'margin-top: 3px;"></span>' + layer_name);
        overlayMaps[overlayDiv] = overlayLayer;
    }

    // Add controls
    L.control.layers(
        baseMaps, null, {collapsed:false, position:"bottomleft"}
    ).addTo(map);

    // Add legend title
    jQuery(function($){$('.leaflet-control-layers-expanded').prepend(
        '<h3 style="color:white"; margin-top:0px !important>' + 'Layers' + '</h3>');
    });

}
