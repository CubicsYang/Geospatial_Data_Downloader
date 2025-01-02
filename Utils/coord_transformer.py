from pyproj import Proj, transform
import math
import os
import sys

## Class to transform coordinates between different coordinate systems
class CoordProjector:
    """
    A class used to project coordinates from one coordinate reference system (CRS) to another.
    Attributes
    ----------
    proj_from : pyproj.Proj
        The source coordinate reference system in EPSG format.
    proj_to : pyproj.Proj
        The target coordinate reference system in EPSG format.
    Methods
    -------
    transform_coords(x, y)
        Transforms coordinates from the source CRS to the target CRS.
    round_coords(lon, lat, decimals=0)
        Rounds the transformed coordinates to a specified number of decimal places.
    """

    def __init__(self, proj_from='epsg:3857', proj_to='epsg:4326'):
        if not proj_from.startswith('epsg:'):
            raise ValueError("proj_from must be in EPSG format, e.g. 'epsg:3857'")
        else:
            self.proj_from = Proj(proj_from)
            self.proj_to = Proj(proj_to)
        
    def transform_coords(self, x, y):
        lon, lat = transform(self.proj_from, self.proj_to, x, y)
        return lon, lat

    def round_coords(self, lon, lat, decimals=0):
        lon_rounded = round(lon, decimals)
        lat_rounded = round(lat, decimals)
        return lon_rounded, lat_rounded

## Class to transform coordinates between web tile index and lon/lat
class CoordTransformer:
    """
    A class used to transform geographic coordinates.

    Methods
    -------
    lonlat2xyz(lon, lat, zoom)
        Converts longitude and latitude to tile x, y coordinates at a given zoom level.

    xyz2lonlat(x, y, zoom)
        Converts tile x, y coordinates at a given zoom level to longitude and latitude.
    """

    def __init__(self):
        self.transformer = CoordProjector()

    def lonlat2xyz(lon, lat, zoom):
        n = math.pow(2, zoom)
        x = ((lon + 180) / 360) * n
        y = (1 - (math.log(math.tan(math.radians(lat)) + (1 / math.cos(math.radians(lat)))) / math.pi)) / 2 * n
        return int(x), int(y)

    def xyz2lonlat(x, y, zoom):
        n = math.pow(2, zoom)
        lon = x / n * 360.0 - 180.0
        lat = math.atan(math.sinh(math.pi * (1 - 2 * y / n)))
        lat = lat * 180.0 / math.pi
        return lon, lat

class ProjectionDefiner:
    """
    A class to define the projection of a geospatial dataset using GDAL.
    Attributes:
    -----------
    proj_to : str
        The target projection in EPSG format (e.g., 'epsg:4326').
    input_file : str
        The path to the input file.
    output_file : str
        The path to the output file.
    left : float
        The longitude of the left boundary.
    top : float
        The latitude of the top boundary.
    right : float
        The longitude of the right boundary.
    bottom : float
        The latitude of the bottom boundary.
    Methods:
    --------
    define_projection():
        Defines the projection of the input file and saves it to the output file.
    """
    
    def __init__(self, proj_to, input_file, output_file, x1, y1, x2, y2,zoom):
        self.proj_to = proj_to 
        self.input_file = input_file
        self.output_file = output_file
        self.left = CoordTransformer.xyz2lonlat(x1, y1, zoom)[0]
        self.top = CoordTransformer.xyz2lonlat(x1, y1, zoom)[1]
        self.right = CoordTransformer.xyz2lonlat(x2, y2, zoom)[0]
        self.bottom = CoordTransformer.xyz2lonlat(x2, y2, zoom)[1]
        
    def define_projection(self):
        if not self.proj_to.lower().startswith('epsg:'):
            raise ValueError("proj_to must be in EPSG format, e.g. 'epsg:4326'")
        else:
            try:
                os.system(f"gdal_translate -of GTiff -a_srs EPSG:4326 -a_ullr {self.left} {self.top} {self.right} {self.bottom} {self.input_file} {self.output_file}")
            except Exception as e:
                print(f"Failed to define projection: {e}")
                return
            
        
    
# Example usage
if __name__ == "__main__":
    transformer = CoordProjector()
    x, y = 500000, 5000000  # Example coordinates in EPSG:3857
    lon, lat = transformer.transform_coords(x, y)
    print(f"Transformed coordinates: Longitude: {lon}, Latitude: {lat}")
    lon_rounded, lat_rounded = transformer.round_coords(lon, lat, 2)
    print(f"Rounded coordinates: Longitude: {lon_rounded}, Latitude: {lat_rounded}")