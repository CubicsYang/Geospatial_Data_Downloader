import sys
import os
import Opentopography as ot
import Copernicus
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import Utils.coord_transformer as ct

if __name__ == "__main__":
    transformer = ct.CoordTransformer()
    # x, y = 500000, 5000000  # Example coordinates in EPSG:3857
    # lon, lat = transformer.transform_coords(x, y)
    # print(f"Transformed coordinates: Longitude: {lon}, Latitude: {lat}")
    # lon_rounded, lat_rounded = transformer.round_coords(lon, lat, 2)
    # print(f"Rounded coordinates: Longitude: {lon_rounded}, Latitude: {lat_rounded}")
    south, north, west, east = 50, 50.1, 14.35, 14.6
    globaldem_downloader = ot.Opentopography_downloader(dem_type='globaldem')
    globaldem_downloader.download_global_DEMs(south, north, west, east)
    globaldem_downloader.download_global_DEM(south, north, west, east, datasetName='SRTMGL1')
    south, north, west, east = 40.234, 40.24, -105.234, -105.223
    Your_API_Key = 'Your_API_Key'
    usgsdem_downloader = ot.Opentopography_downloader(dem_type='usgsdem',api_key=f'{Your_API_Key}')
    usgsdem_downloader.download_usgs_DEMs(south, north, west, east)
    usgsdem_downloader.download_usgs_DEM(south, north, west, east, datasetName='USGS10m')