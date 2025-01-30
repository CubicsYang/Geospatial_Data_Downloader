# Geospatial_Data_Downloader
A simple python script to download geospatial data from the internet. These scripts are designed to download data from the following sources:
- DEM
  - [COPERNICUS DEM](https://panda.copernicus.eu/panda)
  - [DCM](https://download.geoservice.dlr.de/TDM30_DCM/)
  - [SRTM](https://earthexplorer.usgs.gov/)
  - [AW3D30](https://www.eorc.jaxa.jp/ALOS/en/aw3d30/index.htm)
  - [SRTM15Plus](https://www.cgiar-csi.org/data/srtm-90m-digital-elevation-database-v4-1)
  - [NASADEM](https://lpdaac.usgs.gov/products/nasadem_hgtv001/)
  - [EU_DTM](https://land.copernicus.eu/imagery-in-situ/eu-dem/eu-dem-v1.1?tab=download)
  - [GEDI_L3](https://lpdaac.usgs.gov/products/gedi02_bv001/)
  - [GEBCO](https://www.gebco.net/)
- Land Use/Land Cover
  - [GLC_FCS30](https://data.casearth.cn/en/sdo/detail/64d0950d08415d6cdb033018)
- Satellite Imagery
  - [Google Map Tiles](https://www.google.com/maps)
# Example usage
## Download single-source DEM
```python
# using Opentopography.py
south, north, west, east = 50, 50.1, 14.35, 14.6
globaldem_downloader = Opentopography_downloader(dem_type='globaldem')
#'SRTMGL1', 'SRTMGL3', 'SRTMGL1_E', 'AW3D30', 'AW3D30_E', 'SRTM15Plus', 'NASADEM', 'COP30','COP90', 'EU_DTM', 'GEDI_L3', 'GEBCOIceTopo', 'GEBCOSubIceTopo'
globaldem_downloader.download_global_DEM(south, north, west, east, datasetName='SRTMGL1')
```
## Download multi-source DEM
```python
# using Opentopography.py
south, north, west, east = 50, 50.1, 14.35, 14.6
#['SRTMGL1', 'SRTMGL3', 'SRTMGL1_E', 'AW3D30', 'AW3D30_E', 'SRTM15Plus', 'NASADEM', 'COP30','COP90', 'EU_DTM', 'GEDI_L3', 'GEBCOIceTopo', 'GEBCOSubIceTopo']
globaldem_downloader = Opentopography_downloader(dem_type='globaldem')
globaldem_downloader.download_global_DEMs(south, north, west, east)
```
## Download USGS DEM
```python
# using Opentopography.py
south, north, west, east = 40.234, 40.24, -105.234, -105.223

Your_API_Key = 'Your_API_Key'
usgsdem_downloader = Opentopography_downloader(dem_type='usgsdem',api_key=f'{Your_API_Key}')
# batch download
# ['USGS30m', 'USGS10m', 'USGS1m']
usgsdem_downloader.download_usgs_DEMs(south, north, west, east)
# single download
# 'USGS30m', 'USGS10m', 'USGS1m'
usgsdem_downloader.download_usgs_DEM(south, north, west, east, datasetName='USGS10m')
```
## Download Google Map Tiles
```python
# using GoogleMap.py
left, top = 14.35, 50.1
right, bottom = 14.6, 50
google_map_downloader.download_google_satellite(left, top, right, bottom, zoom=12, max_workers=4, merge=True)
```
# Acknowledgement
Thanks for the following sources for providing the data:
- [OpenTopography](https://opentopography.org/)
- [Google Map](https://www.google.com/maps)