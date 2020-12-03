"""
This file tests projection from ERSI:102100 to EPSR:4326 using ArcGIS.

The entire file works, and pyproj is much faster than than ArcGIS. The only thing to do now is to use multiprocessing in Python to make the entire thing faster.

However, note that PyProj reverses the order so that it is in latitude longitude.
"""

import os
import time

import pyproj
import numpy as np

# ArcGIS imports
import arcgis.gis as arcgis
import arcgis.geometry as arcgeo


def convert_with_GIS(input_geometry):
    gis = arcgis.GIS()

    time_start = time.time()
    output_geometry = arcgeo.project(geometries=input_geometry, in_sr=3857, out_sr=4326)
    time_end = time.time()
    print(output_geometry)
    print("Entire operation took {} seconds.".format(time_end - time_start))


def convert_with_pyproj(input_geometry):
    output_geometry = list()
    time_start = time.time()
    transformer = pyproj.Transformer.from_crs("epsg:3857", "epsg:4326")
    for i in range(len(input_geometry)):
        (x_proj, y_proj) = transformer.transform(
            input_geometry[i]["x"], input_geometry[i]["y"]
        )
        output_geometry.append((x_proj, y_proj))
    time_end = time.time()
    print(output_geometry)
    print("Entire operation took {} seconds.".format(time_end - time_start))


if __name__ == "__main__":
    input_geometry = [
        {"x": -11870815.520399999, "y": 4174578.855800003},
        {"x": -11877970.1406, "y": 4180379.3342999965},
    ]
    convert_with_GIS(input_geometry)
    print("\n")
    convert_with_pyproj(input_geometry)
