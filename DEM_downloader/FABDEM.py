import requests
import os
import sys
from tqdm import tqdm
import geopandas as gpd
import Utils.download_util as download_util

class FABDEM_downloader:
    
    def __init__(self, output_dir=r'output'):
        self.base_url = 'https://data.bris.ac.uk/datasets/s5hqmjcdj8yo2ibzi9b4ew3sn/'
        self.session = requests.Session()
        self.output_dir = output_dir
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        try:
            # read FABDEM_v1-2_tiles
            self.tile_gdf = gpd.read_file('../Assets/FABDEM_v1-2_tiles.geojson')
        except Exception as e:
            print(f'An exception occurred: {e}')
            sys.exit(1)

    
    def download_FABDEM(self, south, north, west, east):
        # create a bounding box from the input coordinates
        download_bbox = gpd.GeoDataFrame(geometry=[gpd.geoseries.box(west, south, east, north)], crs='EPSG:4326')
        # find the tiles that intersect with the bounding box
        intersecting_tiles = gpd.overlay(self.tile_gdf, download_bbox, how='intersection')
        tiles_zip_names = intersecting_tiles['zipfile_name'].values
        for tile_zip_name in tqdm(tiles_zip_names):
            url = f"{self.base_url}{tile_zip_name}"
            output_path = os.path.join(self.output_dir, tile_zip_name)
            download_util.download_file(url, output_path)
