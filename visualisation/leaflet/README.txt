The code for this visualisation is based on that created for different projects:

---- Wellcome Trust project, Women's Work: https://github.com/wellcometrust/womens-work/tree/master/visualisations/map See this repository for the original code. 

---- Leaflet piechart project: https://github.com/sashakavun/leaflet-piechart See this repository for the original code.



###### Viewing the map.#######
To run the code locally on a Unix system, download the repository then navigate to the data directory. 

Run the following scripts using python3:

python3 generate_leaflet_data.py

then

python3 generate_leaflet_markers.py

Navigate up one level to the git directory and run:

python -m SimpleHTTPServer

and open http://localhost:8000/visualisation/leaflet/ in a browser to view the map.



Updated 24/1//16.
 
