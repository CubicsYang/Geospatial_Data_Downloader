import sys
import os
import Google_Map as gm
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import Utils.coord_transformer as ct

if __name__ == "__main__":
    transformer = ct.CoordTransformer()
    google_map_downloader = gm.Google_Map_downloader()
    left, top = 14.35, 50.1
    right, bottom = 14.6, 50
    google_map_downloader.download_google_satellite(left, top, right, bottom, zoom=12, max_workers=4, merge=True)
