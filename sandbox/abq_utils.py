import pyproj
import shapely
import numpy as np
import pandas as pd
from tqdm import tqdm
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
