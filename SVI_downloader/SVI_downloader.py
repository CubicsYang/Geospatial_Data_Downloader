import Google_SVI_downloader as gsvi
import os
import math
import pandas as pd

if __name__ == "__main__":
    downloader = gsvi.Google_SVI_downloader()
    # Download panorama
    pano = downloader.find_panorama(40.758895, -73.985131)
    downloader.download_panorama(pano, os.path.join(os.path.dirname(__file__), 'panoramas'), zoom=1)
    # Download panorama batch
    lons = [-73.985131, -73.985131]
    lats = [40.758895, 40.758895]
    panos = downloader.find_panorama_batch(lons, lats)
    for pano in panos:
        downloader.download_panorama(pano, os.path.join(os.path.dirname(__file__), 'panoramas'), zoom=1)
    # Download panorama by csv
    # df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'panoramas.csv'))
    # for index, row in df.iterrows():
    #     pano = downloader.find_panorama(row['lat'], row['lon'])
    #     downloader.download_panorama(pano, os.path.join(os.path.dirname(__file__), 'panoramas'), zoom=1)
    # # Download panorama by csv batch
    # df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'panoramas.csv'))
    # lons = df['lon'].tolist()
    # lats = df['lat'].tolist()
    # panos = downloader.find_panorama_batch(lons, lats)
    # for pano in panos:
    #     downloader.download_panorama(pano, os.path.join(os.path.dirname(__file__), 'panoramas'), zoom=1)
    # print("Download finished")