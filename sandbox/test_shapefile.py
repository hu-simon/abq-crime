"""
This Python file tests converting the coordinates in a shape file (.shp) from EPSG:4269 to EPSG:4326. 
"""

import os
import time
import glob

import shapely
import pandas as pd
from tqdm import tqdm

import geopandas as gpd

if __name__ == "__main__":
    # Load the shapefile.
    shapefile = gpd.read_file(
        "/Users/administrator/Documents/Projects/abq_crime/shapefiles/zipcodes/zipcodes.shp"
    )

    # Extract the coordinates for each of the Polygons.
    geometries = shapefile["geometry"]
    zipcode_polygons = list()

    for idx in tqdm(range(len(geometries))):
        if type(geometries[idx]) == shapely.geometry.multipolygon.MultiPolygon:
            for poly in geometries[idx]:
                zipcode_polygons.append(poly.exterior.coords[:])
        else:
            zipcode_polygons.append(geometries[idx].exterior.coords[:])

