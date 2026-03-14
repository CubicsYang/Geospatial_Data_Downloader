import os
import subprocess

class CopernicusDEMDownloader:
    def __init__(self, output_dir=r"output", resolution=30, save_path=None, resolutions=None):
        if save_path is not None:
            output_dir = save_path
        if resolutions is not None:
            resolution = resolutions

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        if not self.check_aws_cli():
            raise EnvironmentError("Please install AWS CLI first")
        else:
            self.output_dir = output_dir
            self.resolution = int(resolution)
            # Backward-compatible attributes
            self.save_path = self.output_dir
            self.resolutions = self.resolution
            print("AWS CLI is installed")

    def check_aws_cli(self):
        try:
            res = subprocess.run(["aws", "--version"], check=False, capture_output=True, text=True)
            output_str = (res.stdout or "") + (res.stderr or "")
            return "aws-cli" in output_str
        except Exception as e:
            print(f'An exception occurred: {e}')
            return False
    
    def cmd_init(self, lon, lat):
        s_lon = str(abs(lon))
        s_lat = str(abs(lat))
        if abs(lon) < 10:
            s_lon = "00" + str(abs(lon))
        elif abs(lon) < 100:
            s_lon = "0" + str(abs(lon))
        if abs(lat) < 10:
            s_lat = "0" + str(abs(lat))
        if lon < 0:
            c_lon = "W" + str(s_lon)
        else:
            c_lon = "E" + str(s_lon)
        if lat < 0:
            c_lat = "S" + str(s_lat)
        else:
            c_lat = "N" + str(s_lat)
        cmd = "aws s3 cp --no-sign-request" + " s3://copernicus-dem-{0}m/Copernicus_DSM_COG_{1}_{2}_00_{3}_00_DEM/ {4} --recursive".format(
            str(self.resolution), str(int(self.resolution / 3)), str(c_lat), str(c_lon), self.output_dir)
        return cmd

    def download_tile(self, lon, lat):
        """Get Copernicus Dem by lon and lat

        Args:
            lon (number): longitude
            lat (number): latitude
        """
        lon = int(lon)
        lat = int(lat)
        cmd = self.cmd_init(lon, lat)
        try:
            res = os.popen(cmd)
            output_str = res.read()  # 获得输出字符串
            print(output_str)
        except Exception as e:
            print(f'An exception occurred: {e}')

    def download_extent(self, lon_min, lon_max, lat_min, lat_max):
        """Get Copernicus Dems by extent 

        Args:
            lon_min (number): 
            lon_max (number): 
            lat_min (number): 
            lat_max (number):
        """
        lon_min = int(lon_min)
        lon_max = int(lon_max)
        lat_min = int(lat_min)
        lat_max = int(lat_max)
        for lon in range(lon_min, lon_max + 1):
            for lat in range(lat_min, lat_max + 1):
                cmd = self.cmd_init(lon, lat)
                try:
                    res = os.popen(cmd)
                    output_str = res.read()  # 获得输出字符串
                    print(output_str)
                except Exception as e:
                    print(f'An exception occurred: {e}')

    # Backward-compatible aliases
    def get_remote_file(self, lon, lat):
        self.download_tile(lon, lat)

    def get_remote_file_batch(self, lon_min, lon_max, lat_min, lat_max):
        self.download_extent(lon_min, lon_max, lat_min, lat_max)

if __name__ == "__main__":
    downloader = CopernicusDEMDownloader()
    # downloader.get_remote_file(39, 1)
    downloader.download_extent(-180, 180, -90, 90)
    # downloader.get_remote_file_batch(-9, 9, -90, 90)
