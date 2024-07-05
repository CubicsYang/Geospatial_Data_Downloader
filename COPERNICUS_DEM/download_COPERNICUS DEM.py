import os

savePath = "./Data"
resolutions = 30  # 90


def cmd_init(lon, lat):
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
        str(resolutions), str(int(resolutions / 3)), str(c_lat), str(c_lon), savePath)
    return cmd


def get_remote_file(lon, lat):
    """Get Copernicus Dem by lon and lat

    Args:
        lon (number): lontitude
        lat (number): latitude
    """
    lon = int(lon)
    lat = int(lat)
    cmd = cmd_init(lon, lat)
    try:
        res = os.popen(cmd)
        output_str = res.read()  # 获得输出字符串
        print(output_str)
    except:
        print('An exception occurred')


def get_remote_file_batch(lon_min, lon_max, lat_min, lat_max):
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
            cmd = cmd_init(lon, lat)
            try:
                res = os.popen(cmd)
                output_str = res.read()  # 获得输出字符串
                print(output_str)
            except:
                print('An exception occurred')


if __name__ == "__main__":
    # get_remote_file(39,1)
    get_remote_file_batch(-180, 180, -90, 90)
    # get_remote_file_batch(-9,9,-90,90)
