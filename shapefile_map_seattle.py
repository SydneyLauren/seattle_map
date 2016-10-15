from __future__ import division
import pandas as pd
import numpy as np
from matplotlib.patches import Polygon
import matplotlib
from matplotlib.collections import PatchCollection
from mpl_toolkits.basemap import Basemap
from shapely.geometry import Point, Polygon, MultiPoint, MultiPolygon
import fiona
from descartes import PolygonPatch
import matplotlib.pyplot as plt


def parse_shapes(shapefilepath):
    '''
    INPUT: path to directory containing shape file
    OUTPUT: coordinates of the shapes to plot

    Takes a shape file (.shp) and return coordinates for plotting'''

    shp = fiona.open(shapefilepath+'.shp')
    coords = shp.bounds
    shp.close
    return coords


def plot_initializer(coordinates):
    '''
    INPUT: coordinates for a set of shapes
    OUTPUT: plot handle and basemap object

    Takes coordinates for a set of shapes and initializes a basemap figure'''

    w, h = coordinates[2] - coordinates[0], coordinates[3] - coordinates[1]
    extra = 0.01

    figwidth = 8
    fig = plt.figure(figsize=(figwidth, figwidth*h/w))
    ax = fig.add_subplot(111, axisbg='w', frame_on=False)
    m = Basemap(
        projection='tmerc', ellps='WGS84',
        lon_0=np.mean([coordinates[0], coordinates[2]]),
        lat_0=np.mean([coordinates[1], coordinates[3]]),
        llcrnrlon=coordinates[0] - extra * w,
        llcrnrlat=coordinates[1] - (extra * h),
        urcrnrlon=coordinates[2] + extra * w,
        urcrnrlat=coordinates[3] + (extra * h),
        resolution='i',  suppress_ticks=True)
    return m, ax


def make_shape_dataframe(m, shapefilename):
    '''
    INPUT: basemape object and shape file name
    OUTPUT: dataframe of shapes

    Takes a basemap object shape file and returns a dataframe of polygons that will plot on the basemap'''

    _out = m.readshapefile(shapefilename, name='seattle', drawbounds=False, color='none', zorder=2)
    # set up a map dataframe for shape outlines
    df = pd.DataFrame({
        'poly': [Polygon(points) for points in m.seattle],
    })
    return df


def plot_shapes(df_map, ax):
    '''
    INPUT: dataframe of polygons and plot handle
    OUTPUT: None

    Takes a dataframe of polygons and plot handle and adds patches to plot'''
    pc = PatchCollection(df_map['patches'], match_original=True)
    ax.add_collection(pc)


''' Plot Seattle Shorelines '''
shore_shapefilename = 'Shorelines/WGS84/Shorelines'
coords = parse_shapes(shore_shapefilename)  # Read in neighborhood shape file
m, ax = plot_initializer(coords)  # Initialize the plot, this only needs to be done once
df_shore = make_shape_dataframe(m, shore_shapefilename)  # get dataframe for plotting
df_shore['patches'] = df_shore['poly'].map(lambda x: PolygonPatch(x, ec='b',  # draw the parks as green patches
                                           lw=.8, facecolor='b', alpha=.5, zorder=4))
plot_shapes(df_shore, ax)  # add to the plot

''' Plot Seattle Neighborhoods '''
hood_shapefilename = 'Neighborhoods/WGS84/Neighborhoods'
df_map = make_shape_dataframe(m, hood_shapefilename)  # get neighborhood dataframe for plotting
df_map['patches'] = df_map['poly'].map(lambda x: PolygonPatch(x, ec='#111111',  # draw neighborhoods with grey outlines
                                       lw=.8, facecolor='w', alpha=1., zorder=4))
plot_shapes(df_map, ax)

''' Plot Seattle Parks '''
park_shapefilename = 'City of Seattle Parks/WGS84/City_of_Seattle_Parks'
df_map_park = make_shape_dataframe(m, park_shapefilename)  # get dataframe for plotting
df_map_park['patches'] = df_map_park['poly'].map(lambda x: PolygonPatch(x, ec='g',  # draw the parks as green patches
                                                 lw=.8, facecolor='g', alpha=.5, zorder=4))
plot_shapes(df_map_park, ax)  # add parks to the plot


''' Draw the map '''
m.drawmapboundary()
plt.show()
plt.savefig('seattle_map.png')
