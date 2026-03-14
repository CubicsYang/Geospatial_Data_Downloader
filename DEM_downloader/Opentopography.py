import requests
import os
import sys
from tqdm import tqdm

class OpenTopographyDownloader:
    """
    A class to download Digital Elevation Models (DEMs) from OpenTopography.
    Attributes:
    -----------
    dem_type : str
        The type of DEM to download ('globaldem' or 'usgsdem').
    datasetName_list : list
        List of available datasets for the specified DEM type.
    base_url : str
        Base URL for the OpenTopography API.
    session : requests.Session
        Session object for making HTTP requests.
    api_key : str
        API key for accessing the OpenTopography API.
    output_dir : str
        Directory to save the downloaded DEM files.
    Methods:
    --------
    __init__(self, api_key='demoapikeyot2022', dem_type='globaldem', output_dir=r'output'):
        Initializes the downloader with the specified API key, DEM type, and output directory.
    get_datasetName_list(self):
        Returns the list of available datasets for the specified DEM type.
    file_format_extension_mappping(self, format):
        Maps the specified file format to its corresponding file extension.
    download_global_DEM(self, south, north, west, east, format='GTiff', datasetName='COP30'):
        Downloads a global DEM for the specified bounding box and dataset name.
    download_usgs_DEM(self, south, north, west, east, format='GTiff', datasetName='USGS10m'):
        Downloads a USGS DEM for the specified bounding box and dataset name.
    download_global_DEMs(self, south, north, west, east, format='GTiff', datasetNames=['COP30', 'SRTMGL1', 'SRTMGL3']):
        Downloads multiple global DEMs for the specified bounding box and dataset names.
    download_usgs_DEMs(self, south, north, west, east, format='GTiff', datasetNames=['USGS30m', 'USGS10m', 'USGS1m']):
        Downloads multiple USGS DEMs for the specified bounding box and dataset names.
    """
    
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
        
    def get_dataset_name_list(self):
        if self.dem_type == 'globaldem':
            return self.datasetName_list
        elif self.dem_type == 'usgsdem':
            return self.datasetName_list
        else:
            print("Invalid DEM type, please choose 'globaldem' or 'usgsdem'")
            return []

    # Backward-compatible alias
    def get_datasetName_list(self):
        return self.get_dataset_name_list()
    
    def file_format_extension_mapping(self, output_format):
        if output_format == 'GTiff':
            return 'tif'
        elif output_format == 'HFA':
            return 'img'
        elif output_format == 'AAIGrid':
            return 'asc'
    
    # Backward-compatible alias (keeps original typo)
    def file_format_extension_mappping(self, format):
        return self.file_format_extension_mapping(format)
        
    def download_global_dem(self, south, north, west, east, output_format='GTiff', dataset_name='COP30'):
        if dataset_name not in self.datasetName_list:
            print(f"DEM type {dataset_name} not supported")
            return
        else:
            url = f"{self.base_url}?demtype={dataset_name}&south={south}&north={north}&west={west}&east={east}&outputFormat={output_format}&API_Key={self.api_key}"
            try:
                response = self.session.get(url, stream=True)
                if response.status_code == 200:
                    file_extension = self.file_format_extension_mapping(output_format)
                    filename = f"{dataset_name}_{south}_{north}_{west}_{east}.{file_extension}"
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

    # Backward-compatible alias
    def download_global_DEM(self, south, north, west, east, format='GTiff', datasetName='COP30'):
        self.download_global_dem(south, north, west, east, output_format=format, dataset_name=datasetName)

    def download_usgs_dem(self, south, north, west, east, output_format='GTiff', dataset_name='USGS10m'):
        if dataset_name not in self.datasetName_list:
            print(f"Dataset name {dataset_name} not supported")
            return
        else:
            url = f"{self.base_url}?datasetName={dataset_name}&south={south}&north={north}&west={west}&east={east}&outputFormat={output_format}&API_Key={self.api_key}"
            response = self.session.get(url, stream=True)
            if response.status_code == 200:
                file_extension = self.file_format_extension_mapping(output_format)
                filename = f"{dataset_name}_{south}_{north}_{west}_{east}.{file_extension}"
                output_path = os.path.join(self.output_dir, filename)
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                print(f"Downloaded DEM to {output_path}")
            else:
                print(f"Failed to download DEM, status code: {response.status_code}, error message: {status_code_error_message(response.status_code)}")
                print(response.text)

    # Backward-compatible alias
    def download_usgs_DEM(self, south, north, west, east, format='GTiff', datasetName='USGS10m'):
        self.download_usgs_dem(south, north, west, east, output_format=format, dataset_name=datasetName)
            
    def download_global_dems(self, south, north, west, east, output_format='GTiff', dataset_names=['COP30', 'SRTMGL1', 'SRTMGL3']):
        for dataset_name in tqdm(dataset_names):
            if dataset_name not in self.datasetName_list:
                print(f"DEM type {dataset_name} not supported")
            else:
                url = f"{self.base_url}?demtype={dataset_name}&south={south}&north={north}&west={west}&east={east}&outputFormat={output_format}&API_Key={self.api_key}"
                try:
                    response = self.session.get(url, stream=True)
                    if response.status_code == 200:
                        file_extension = self.file_format_extension_mapping(output_format)
                        filename = f"{dataset_name}_{south}_{north}_{west}_{east}.{file_extension}"
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

    # Backward-compatible alias
    def download_global_DEMs(self, south, north, west, east, format='GTiff', datasetNames=['COP30', 'SRTMGL1', 'SRTMGL3']):
        self.download_global_dems(south, north, west, east, output_format=format, dataset_names=datasetNames)

    def download_usgs_dems(self, south, north, west, east, output_format='GTiff', dataset_names=['USGS30m', 'USGS10m', 'USGS1m']):
        for dataset_name in tqdm(dataset_names):
            if dataset_name not in self.datasetName_list:
                print(f"Dataset name {dataset_name} not supported")
            else:
                try:
                    url = f"{self.base_url}?datasetName={dataset_name}&south={south}&north={north}&west={west}&east={east}&outputFormat={output_format}&API_Key={self.api_key}"
                    response = self.session.get(url, stream=True)
                    if response.status_code == 200:
                        file_extension = self.file_format_extension_mapping(output_format)
                        filename = f"{dataset_name}_{south}_{north}_{west}_{east}.{file_extension}"
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

    # Backward-compatible alias
    def download_usgs_DEMs(self, south, north, west, east, format='GTiff', datasetNames=['USGS30m', 'USGS10m', 'USGS1m']):
        self.download_usgs_dems(south, north, west, east, output_format=format, dataset_names=datasetNames)
                    
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
    globaldem_downloader = OpenTopographyDownloader(dem_type='globaldem')
    globaldem_downloader.download_global_dems(south, north, west, east)
    globaldem_downloader.download_global_dem(south, north, west, east, dataset_name='SRTMGL1')
    south, north, west, east = 40.234, 40.24, -105.234, -105.223
    Your_API_Key = 'Your_API_Key'
    usgsdem_downloader = OpenTopographyDownloader(dem_type='usgsdem',api_key=f'{Your_API_Key}')
    usgsdem_downloader.download_usgs_dems(south, north, west, east)
    usgsdem_downloader.download_usgs_dem(south, north, west, east, dataset_name='USGS10m')


# Backward-compatible class alias
Opentopography_downloader = OpenTopographyDownloader
    