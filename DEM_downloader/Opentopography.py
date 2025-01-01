import requests
import os
import sys
from tqdm import tqdm

class Opentopography_downloader:
    
    def __init__(self, api_key='demoapikeyot2022', dem_type='globaldem', output_dir=r'output'):
        self.dem_type = dem_type
        if dem_type == 'globaldem':
            datasetName_list = ['SRTMGL1', 'SRTMGL3', 'SRTMGL1_E', 'AW3D30', 'AW3D30_E', 'SRTM15Plus', 'NASADEM', 'COP30','COP90', 'EU_DTM', 'GEDI_L3', 'GEBCOIceTopo', 'GEBCOSubIceTopo']
            self.datasetName_list = datasetName_list
            self.base_url = 'https://portal.opentopography.org/API/globaldem'
        elif dem_type == 'usgsdem':
            datasetName_list = ['USGS30m', 'USGS10m', 'USGS1m']
            self.datasetName_list = datasetName_list
            self.base_url = 'https://portal.opentopography.org/API/usgsdem'
        else:
            print("Invalid DEM type, please choose 'globaldem' or 'usgsdem'")
            return
        self.session = requests.Session()
        self.api_key = api_key
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
    def get_datasetName_list(self):
        if self.dem_type == 'globaldem':
            return self.datasetName_list
        elif self.dem_type == 'usgsdem':
            return self.datasetName_list
        else:
            print("Invalid DEM type, please choose 'globaldem' or 'usgsdem'")
            return []
    
    def file_format_extension_mappping(self, format):
        if format == 'GTiff':
            return 'tif'
        elif format == 'HFA':
            return 'img'
        elif format == 'AAIGrid':
            return 'asc'
        
    def download_global_DEM(self, south, north, west, east, format='GTiff', datasetName='COP30'):
        if datasetName not in self.datasetName_list:
            print(f"DEM type {datasetName} not supported")
            return
        else:
            url = f"{self.base_url}?demtype={datasetName}&south={south}&north={north}&west={west}&east={east}&outputFormat={format}&API_Key={self.api_key}"
            try:
                response = self.session.get(url)
                if response.status_code == 200:
                    file_extension = self.file_format_extension_mappping(format)
                    filename = f"{datasetName}_{south}_{north}_{west}_{east}.{file_extension}"
                    output_path = os.path.join(self.output_dir, filename)
                    with open(output_path, 'wb') as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)
                    print(f"Downloaded DEM to {output_path}")
                else:
                    print(f"Failed to download DEM, status code: {response.status_code}, error message: {status_code_error_message(response.status_code)}")
                    print(response.text)
            except Exception as e:
                print(f"Failed to download DEM: {e}")

    def download_usgs_DEM(self, south, north, west, east, format='GTiff', datasetName='USGS10m'):
        if datasetName not in self.datasetName_list:
            print(f"Dataset name {datasetName} not supported")
            return
        else:
            url = f"{self.base_url}?datasetName={datasetName}&south={south}&north={north}&west={west}&east={east}&outputFormat={format}&API_Key={self.api_key}"
            response = self.session.get(url, stream=True)
            if response.status_code == 200:
                file_extension = self.file_format_extension_mappping(format)
                filename = f"{datasetName}_{south}_{north}_{west}_{east}.{file_extension}"
                output_path = os.path.join(self.output_dir, filename)
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                print(f"Downloaded DEM to {output_path}")
            else:
                print(f"Failed to download DEM, status code: {response.status_code}, error message: {status_code_error_message(response.status_code)}")
                print(response.text)
            print(f"Failed to download DEM, status code: {response.status_code}")
            
    def download_global_DEMs(self, south, north, west, east, format='GTiff', datasetNames=['COP30', 'SRTMGL1', 'SRTMGL3']):
        for datasetName in tqdm(datasetNames):
            if datasetName not in self.datasetName_list:
                print(f"DEM type {datasetName} not supported")
            else:
                url = f"{self.base_url}?demtype={datasetName}&south={south}&north={north}&west={west}&east={east}&outputFormat={format}&API_Key={self.api_key}"
                try:
                    response = self.session.get(url, stream=True)
                    if response.status_code == 200:
                        file_extension = self.file_format_extension_mappping(format)
                        filename = f"{datasetName}_{south}_{north}_{west}_{east}.{file_extension}"
                        output_path = os.path.join(self.output_dir, filename)
                        with open(output_path, 'wb') as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)
                        print(f"Downloaded DEM to {output_path}")
                    else:
                        print(f"Failed to download DEM, status code: {response.status_code}, error message: {status_code_error_message(response.status_code)}")
                        print(response.text)
                except Exception as e:
                    print(f"Failed to download DEM: {e}")

    def download_usgs_DEMs(self, south, north, west, east, format='GTiff', datasetNames=['USGS30m', 'USGS10m', 'USGS1m']):
        for datasetName in tqdm(datasetNames):
            if datasetName not in self.datasetName_list:
                print(f"Dataset name {datasetName} not supported")
            else:
                try:
                    url = f"{self.base_url}?datasetName={datasetName}&south={south}&north={north}&west={west}&east={east}&outputFormat={format}&API_Key={self.api_key}"
                    response = self.session.get(url, stream=True)
                    if response.status_code == 200:
                        file_extension = self.file_format_extension_mappping(format)
                        filename = f"{datasetName}_{south}_{north}_{west}_{east}.{file_extension}"
                        output_path = os.path.join(self.output_dir, filename)
                        with open(output_path, 'wb') as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)
                        print(f"Downloaded DEM to {output_path}")
                    else:
                        print(f"Failed to download DEM, status code: {response.status_code}, error message: {status_code_error_message(response.status_code)}")
                        print(response.text)
                except Exception as e:
                    print(f"Failed to download DEM: {e}")
                    
def status_code_error_message(status_code):
    if status_code == 400:
        return "Invalid request, please check the request parameters"
    elif status_code == 401:
        return "Unauthorized, please check the API key"
    elif status_code == 500:
        return "Internal server error"
    elif status_code == 204:
        return "No content"
    else:
        return "Unknown error"

if __name__ == "__main__":
    south, north, west, east = 50, 50.1, 14.35, 14.6
    globaldem_downloader = Opentopography_downloader(dem_type='globaldem')
    globaldem_downloader.download_global_DEMs(south, north, west, east)
    globaldem_downloader.download_global_DEM(south, north, west, east, datasetName='SRTMGL1')
    south, north, west, east = 40.234, 40.24, -105.234, -105.223
    Your_API_Key = 'Your_API_Key'
    usgsdem_downloader = Opentopography_downloader(dem_type='usgsdem',api_key=f'{Your_API_Key}')
    usgsdem_downloader.download_usgs_DEMs(south, north, west, east)
    usgsdem_downloader.download_usgs_DEM(south, north, west, east, datasetName='USGS10m')
    