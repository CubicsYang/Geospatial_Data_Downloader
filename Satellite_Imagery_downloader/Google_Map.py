import math
import os
import requests
import warnings
from tqdm import tqdm
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import Utils.coord_transformer as ct
warnings.filterwarnings("ignore")
from multiprocessing import Pool
import numpy as np
import cv2 as cv

class Google_Map_downloader:
    def __init__(self,  map_type='satellite', output_dir=r'output'):
        self.map_type = map_type
        self.output_dir = output_dir
        if map_type == 'satellite':
            self.base_url = 'http://0pn.cn/maps/vt?lyrs=s'
        else:
            print("Invalid map type, please choose 'satellite'")
            return
    
    def get_tile(self, x, y,zoom=16):
        url = f"{self.base_url}&x={x}&y={y}&z={zoom}"
        try:
            response = requests.get(url, stream=True, verify=False)
            save_path = os.path.join(self.output_dir, str(zoom), str(x), f'{y}.png')
            if not os.path.exists(os.path.join(self.output_dir, str(zoom), str(x))):
                os.makedirs(os.path.join(self.output_dir, str(zoom), str(x)))
            with open(save_path, 'wb') as out_file:
                out_file.write(response.content)
        except:
            print(f"Failed to download image, url: {url}")
            return

    def get_tiles(self, x1, y1, x2, y2, zoom=16, max_workers=4):
        pool = Pool(max_workers)
        total = self._calculate_tile_count(x1, x2, y1, y2)
        with tqdm(total=total) as pbar: # Use tqdm to show progress bar
                for x in range(x1, x2 + 1):
                    for y in range(y1, y2 + 1):
                        pool.apply_async(self.get_tile, args=(x, y, zoom), callback=self._update_pbar(pbar))
                        # pbar.update(1)
                pool.close()
                pool.join()
                
    def _calculate_tile_count(self, x1, x2, y1, y2):
        total = (x2-x1+1) * (y2-y1+1)
        return total
    
    def _update_pbar(self, pbar):
        pbar.update(1)

    def _merge_projection_tiles(self, x1, y1, x2, y2, zoom=16):
        try:
            rows = []
            for x in range(x1, x2 + 1):
                row = []
                for y in range(y1, y2 + 1):
                    image_path = os.path.join(self.output_dir, str(zoom), str(x), f'{y}.png')
                    row.append(cv.imread(image_path))
                rows.append(row)
            rows = np.array(rows)
            img = np.hstack([np.vstack(row) for row in rows])
            cv.imwrite(os.path.join(self.output_dir, f'Google_Satellite_{zoom}.png'), img)
        except Exception as e:
            print(f"Failed to merge tiles: {e}")
            return
        try:
            # left, top = ct.CoordTransformer.xyz2lonlat(x1, y1, zoom)
            # right, bottom = ct.CoordTransformer.xyz2lonlat(x2, y2, zoom)
            # print(f"left: {left}, top: {top}, right: {right}, bottom: {bottom}")
            ct.ProjectionDefiner('epsg:4326', os.path.join(self.output_dir, f'Google_Satellite_{zoom}.png'), os.path.join(self.output_dir, f'Google_Satellite_{zoom}.tif'), x1, y1, x2+1, y2+1,zoom=zoom).define_projection()
        except Exception as e:
            print(f"Failed to define projection: {e}")
            return

    def download_google_satellite(self, left, top, right, bottom, zoom=16, max_workers=4,merge=True):
        x1, y1 = ct.CoordTransformer.lonlat2xyz(left, top, zoom)
        x2, y2 = ct.CoordTransformer.lonlat2xyz(right, bottom, zoom)

        self.get_tiles(x1, y1, x2, y2, zoom, max_workers)
        if merge:
            self._merge_projection_tiles(x1, y1, x2, y2, zoom)
        print("Download completed")


if __name__ == "__main__":
    google_map_downloader = Google_Map_downloader()
    left, top = 14.35, 50.1
    right, bottom = 14.6, 50
    # google_map_downloader.get_tile(413299,260257,19)
    google_map_downloader.download_google_satellite(left, top, right, bottom, zoom=12, max_workers=4, merge=True)