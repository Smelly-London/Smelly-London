//Last updated in March 2017
//Leaflet map

var radius = d3.scale.sqrt().domain([1, 20]).range([10, 15])
var smell_colors = d3.scale.category20();

var highlightColor = '#a9fcff';
var selectedColor = '#f442dc';

var boroughToMoh;
var borough_outlines;
var leaflet_json = null
/*
 * processes one jason at a time and saves in the variables above. 
 *after getting all three jsons, calls makeFilterMap().
 */
function initMap() {
    $.getJSON("data/moh_smell_category_borough_json.json",function(boroughToMohFromServer){
        boroughToMoh = boroughToMohFromServer;
        $.getJSON("data/london_districts_latlong_with_centroids.json",function(borough_outlines_data){
            borough_outlines = borough_outlines_data;
            $.getJSON("data/leaflet_markers.json", function(raw_data){
                leaflet_json = raw_data;
                makeFilteredMap();                
            });
        });
    });
}

/*
 * every control changes these variables.
 */
var selected_year = 1956;
var selected_filter = null;
var selected_borough = null;

/*
 * filtering the data
 */
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
/*
 * one layer for every year and every borough.
 */
var year_layers;
var borough_layers;

/*
 * This funtion does everything else but should not. Can be improved.
 */
function makeFilteredMap() {
    var data = get_filtered_leaflet_data(selected_filter);
    ////////////// Map Parameters //////////////
    $("#map").remove();
    $("#map-and-controls").prepend("<div id=map></div>");

    var centreLatitude = 51.5;
    var centreLongitude = -0.12;
    var initialZoom = 10;

    map = L.map('map', {
        zoomControl:true,
        maxZoom: 12,
        minZoom: 8,
    }).setView([centreLatitude, centreLongitude], initialZoom);

    var darkMap = L.tileLayer("").addTo(map);
    // getting data to transform current borough to MOH
    
/*
 * white outlines. this is constant so this does not change. So can be avoided repeating.
 */
    L.geoJson(borough_outlines, {
      style: function(feature){
        return {
            color: "white",
            weight: 1,
            fillColor: "black",
            fillOpacity: 0,
        };
      },
      onEachFeature: function(feature, layer) {
        layer.on("click", function(){
            selected_borough = feature.properties.name;
            select_borough();
            update_sidebar();
        })
      }
    }).addTo(map);
/*
 * Create borough layers
 */
    year_layers = new L.layerGroup();
    borough_layers = [];

    for(var borough_outline of borough_outlines.features) {
        var myLayer = L.geoJSON();
        myLayer.addData(borough_outline, {
          style: function(feature){
            return {
                color: "white",
                weight: 1,
                fillColor: "green", // not really green #3388ff
                fillOpacity: 1 };
            }
        });
        myLayer.name = borough_outline.properties.name;
        borough_layers.push(myLayer);
    }
/*
 * Create year layers and tooltips.
 */
    for (var d of data) {
        for(var s of d.smells) {
            s.style = {
                fillStyle: smell_colors(s.name),
                strokeStyle: "black",
                lineWidth: 0
            }
        }

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
          selected_borough = d.location_name;
          select_borough()
          update_sidebar();
        })

        marker.bindPopup(tooltipContent());

        year_layers.addLayer(marker);
    }

    select_year( $("#slider").slider("value") );
    select_borough();
}


/*
 * Creating a smell dropdown. Everytime select a filter, initialises the map again. Unnecessary so can be improved.
 */
$(function(){
    $("select").change(function() {
        selected_filter = $("select").val();
        if(selected_filter === "all smells") {
            selected_filter = null;
            makeFilteredMap();
        } else {
            makeFilteredMap();
        }        
    });  
});

/*
 *Year slider.
 */
  $(function() {
    var handle = $( "#custom-handle" );
    $( "#slider" ).slider({
      create: function() {
        handle.text( $( this ).slider( "value" ) );
      },
      slide: function( event, ui ) {
        handle.text( ui.value );
        select_year(ui.value);
        selected_year = ui.value;
        update_sidebar();
      },
      min:1848,
      max:1973,
      value:1956
    });
  } );

/*
 * Selecting the right year layer and display.
 */
function select_year(selected_year) {
    var layers = year_layers._layers;
    for(var i in layers) {
        var layer = layers[i];
        var layer_year = parseInt( layer.data.formatted_year.substr(0,4) );
        map.removeLayer(layer);
        if(layer_year === selected_year) {
            map.addLayer(layers[i]);
        }
    }
}
/*
 * Selecting and highlighting the borough. 
 * How can I unclick?
 */

function select_borough() {
    for(var b of borough_layers) {
        if(b.name === selected_borough) {
            map.addLayer(b);
        } else {
            map.removeLayer(b);
        }
    }
}

/*
 * Updating the side content bar.
 */
function update_sidebar() {
    if(selected_borough === null) {
        return;
    }

    $('#map-info').css('opacity', '0.9');
    $('#map-info').html(function(){
        var title = selected_borough + ' ' + selected_year;
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
                var color = smell_colors(smell.cat)
                var header_content = "Smell: "+smell.cat;
                header_content += "<span class='color_legend' style='background-color:"+color+";'></span>"
                if (selected_filter === smell.cat) {
                    sidebarContent +=
                        "<h2 class='highlighted'>"+header_content+"</h2>";
                } else {
                    sidebarContent +=
                        "<h2>"+header_content+"</h2>";
                        ;
                }
                sidebarContent += "<p>Reported "+smell.count+" times</p>"
            };
        }
        return sidebarContent;
    });
}
