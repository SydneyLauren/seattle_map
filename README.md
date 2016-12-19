## Plot a map of Seattle in Python
##### This code plots shape files for the city of Seattle using matplotlib's Basemap toolkit in Python.
  
<img src="images/python.png" height="45">
<img src="images/matplotlib.png" height="45">

The general process is as follows:
* Download shape files for the city of Seattle data.seattle.gov
* Read the shape files and parse them into coordinates using fiona
* Initialize a basemap object
* Record shapes in a dataframe and convert to polygon patches using descartes PolygonPatch
* Plot the polygons

![](seattle_map.png)
