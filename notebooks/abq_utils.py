import os
import time

import pyproj
import shapely
import numpy as np
import pandas as pd

import geopandas as gpd

import matplotlib.pyplot as plt


def change_bar_width(ax, new_width):
    """Changes the width of the bars in a bar plot.
    
    Parameters
    ----------
    ax : matplotlib.Axes instance
        The axes used to set the new patch widths.
    new_width : double > 0
        The new width of the bars.

    Returns
    -------
    None

    """
    for patch in ax.patches:
        current_width = patch.get_width()
        diff = current_width - new_width
        patch.set_width(new_width)
        patch.set_x(patch.get_x() + diff * 0.5)


def plot_percentages_bar(barplot):
    """Plots percentages on top of the bars on a barplot.
    
    Parameters
    ----------
    barplot : matplotlib.container.BarContainer instance
        Matplotlib barplot used for obtaining percentages and anchoring text.

    Returns
    -------
    None

    """
    for bar in barplot:
        height = bar.get_height()
        height_percent = height * 100
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            "{:.2f}%".format(height_percent),
            ha="center",
            va="bottom",
            fontsize=15,
        )


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


def test_membership(coords, zipcodes_polygons):
    """Tests membership of a point in a shapely Polygon.

    Parameters
    ----------
    coords : tuple (int, int)
        Tuple containing the (x, y) coordinates of the point to check.
    zipcodes_polygons : list of shapely.geometry.Polygon instances
        List containing the shapely Polygons to check membership.

    Returns
    -------
    idx : int
        The index of the Polygon that contains the point. Returns -1 if the index cannot be found.
    
    """
    point = shapely.geometry.Point(coords[0], coords[1])
    for idx in range(len(zipcodes_polygons)):
        if zipcodes_polygons[idx].contains(point):
            return idx
    return -1
