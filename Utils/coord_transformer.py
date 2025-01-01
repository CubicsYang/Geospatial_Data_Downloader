from pyproj import Proj, transform
import math

## Class to transform coordinates between different coordinate systems
class CoordTransformer:

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

# Example usage
if __name__ == "__main__":
    transformer = CoordTransformer()
    x, y = 500000, 5000000  # Example coordinates in EPSG:3857
    lon, lat = transformer.transform_coords(x, y)
    print(f"Transformed coordinates: Longitude: {lon}, Latitude: {lat}")
    lon_rounded, lat_rounded = transformer.round_coords(lon, lat, 2)
    print(f"Rounded coordinates: Longitude: {lon_rounded}, Latitude: {lat_rounded}")