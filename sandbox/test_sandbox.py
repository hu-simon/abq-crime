import time

import pyproj
import shapely
import pandas as pd
form tqdm import tqdm

import geopandas as gpd

# Utility functions.
def convert_coordinates(coordinates, transformer=None):
    """Converts coordinates from the EPSG:2258 standard to the EPSG:4326 standard.

    Parameters
    ----------
    coordinates : tuple (int, int)
        Tuple containing the coordinates in the EPSG:2258 standard.
    transformer : pyproj.transformer.Transformer instance
        Instance of a pyproj transformer used for converting the coordinates, by default None. If no transformer is specified, then the default transformer that converts EPSG:2258 to EPSG:4326 is used.

    Returns
    -------
    trans_coordinates : tuple (int, int)
        Tuple containing the coordinates in the EPSG:4326 standard.

    """
    if transformer is None:
        transformer = pyproj.Transformer.from_crs("epsg:2258", "epsg:4326")

    trans_coordinates = transformer.transform(coordinates[0], coordinates[1])

    return trans_coordinates

def batch_convert_coordinates(coord_list, transformer=None):
    """Converts a batch of coordinates from the EPSG:2258 standard to the EPSG:4326 standard.

    Parameters
    ----------
    coord_list : list of tuples (int, int)
        List containing tuples containing the coordinates in the EPSG:2258 standard.
    transformer : pyproj.transformer.Transformer instance
        Instance of a pyproj transformer used for converting the coordinates, by default None. If no transformer is specified, then the default transformer that converts EPSG:2258 to EPSG:4326 is used.

    Returns
    -------
    trans_coord_list : list of tuples (int, int)
        List containing tuples of coordinates in the EPSG:4326 standard.

    """
    if transformer is None:
        transformer = pyproj.Transformer.from_crs("epsg:2258", "epsg:4326")

    trans_coord_list = list()
    for coord in coord_list:
        trans_coord_list.append(convert_coordinates(coord, transformer=transformer))

    return trans_coord_list

if __name__ == "__main__":

    # Load the zipcode file.
    shapefile_path = "/Users/administrator/Documents/Projects/abq_crime/shapefiles/zipcodes/zipcodes.shp"
    zipcodes_shapefile = gpd.read_file(shapefile_path)

    # Keep only the relevant columns.
    keep_columns = ["ZIPCODE", "geometry"]
    zipcodes_shapefile = zipcodes_shapefile[keep_columns]

    # Create duplicate entries for the zip codes that contain separared convex sets.
    multipolygon_indices = [type(entry) == shapely.geometry.multipolygon.MultiPolygon for entry in zipcodes_shapefile["geometry"]]
    multipolygon_indices = [idx for idx, x in enumerate(multipolygon_indices) if x == True]

    # For the indices above, create new entries at the end of the DataFrame containing the zipcode and geometry.
    for indices in multipolygon_indices:
             
