import pandas as pd
from streetlevel import streetview
import os
import math

class Google_SVI_downloader:
    def __init__(self):
        pass
    
    def download_panorama(self, pano, path, zoom=1):
        """Download panorama image

        Args:
            pano (pano): pano object
            path (str): path to save the image
            zoom (int): zoom level
        """
        path = os.path.join(path, f"{pano.id}.jpg")
        streetview.download_panorama(pano, path, zoom=zoom) 
        return 
        
    def find_panorama(self, lat, lon):
        """Find panorama by lat and lon

        Args:
            lat (number): latitude
            lon (number): longitude

        Returns:
            pano: pano object
        """
        try:
            pano = streetview.find_panorama(lat, lon)
            return pano
        except Exception as e:
            print(f"Error finding panorama: {e}")
            return None
    
    def find_panorama_batch(self, lons, lats):
        """Find panorama by lons and lats

        Args:
            lons (list): list of longitude
            lats (list): list of latitude

        Returns:
            list: list of pano object
        """
        if len(lons) != len(lats):
            raise ValueError("Length of lons and lats should be the same")
        else:
            # create a csv file to store the metadata
            panos_info = [streetview.find_panorama(lat, lon) for lon, lat in zip(lons, lats)]
            metadata = []
            if len(panos_info) > 0:
                # create a csv file to store the metadata
                for pano in panos_info:
                    if pano:
                        metadata.append({
                            'pid': str(pano.id),
                            'lat': pano.lat,
                            'lng': pano.lon,
                            'heading': pano.heading,
                            'yaw': pano.yaw,
                            'pitch': pano.pitch,
                            'date': pano.date,
                            'location': str(pano.address[-1])})
                    else:
                        metadata.append({
                            'pid': None,
                            'lat': None,
                            'lng': None,
                            'heading': None,
                            'yaw': None,
                            'pitch': None,
                            'date': None,
                            'location': None})
                metadata = pd.DataFrame(metadata)
                # save the metadata to a csv file
                metadata.to_csv("panos_metadata.csv", index=False)
                return panos_info
            else:
                raise ValueError("No panorama found")    
        
    
    def download_panorama_batch(self, panos, path, zoom=1):
        """Download panorama image batch
        
        """
        for pano in panos:
            if pano:
                self.download_panorama(pano, path, zoom=zoom)
            else:
                continue
        return
    
    
