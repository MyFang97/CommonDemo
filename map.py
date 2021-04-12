import requests
import json
import math
from tran import tr

# url = 'https://api.mapabc.com/as/rgeo?ak=ec85d3648154874552835438ac6a02b2&callback=IMAP.Geocoder.location&location=116.46794,40.01213&pois=1'


headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'api.mapabc.com',
    # Referer: https://api.mapabc.com/jsmap/1.0/demo/apidemos/geocode/regeocode.htm
    # ' Sec-Fetch-Dest': 'script',
    # 'Sec-Fetch-Mode': 'no-cors',
    # 'Sec-Fetch-Site': 'same-origin',
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
}


# 高德坐标转换
def gps_to_gd(lon, lat):
    lon = '%.6f' % lon
    lat = '%.6f' % lat
    url = 'https://restapi.amap.com/v3/assistant/coordinate/convert'
    gd_params = {
        'key': '845c7057e8b5f06e0f6bb2fe8956d039',
        'coordsys': 'gps',
        'locations': '{},{}'.format(lon, lat)
    }

    requests.packages.urllib3.disable_warnings()
    response = requests.get(url=url, params=gd_params, verify=False)
    res = response.json()
    return res['locations'].split(',')[0], res['locations'].split(',')[1]


def run(lon, lat):
    url = 'https://api.mapabc.com/as/rgeo'
    params = {
        'ak': 'ec85d3648154874552835438ac6a02b2',
        # 'callback': 'IMAP.Geocoder.location',
        # 'location': '116,40.01213',
        'location': '{},{}'.format(lon, lat),
        # 'pois': 1
    }
    requests.packages.urllib3.disable_warnings()
    response = requests.post(url=url, params=params, verify=False)
    a = response.json()
    return a['result'][0]['formatted_address']


def gdrun(lon, lat):
    url = 'https://restapi.amap.com/v3/geocode/regeo'
    gd_params = {
        'key': '845c7057e8b5f06e0f6bb2fe8956d039',
        'location': '{},{}'.format(lon, lat)
    }
    requests.packages.urllib3.disable_warnings()
    response = requests.post(url=url, params=gd_params, verify=False)
    res = response.json()
    return res['regeocode']['formatted_address']


# run(114.21873305555556, 22.7261375, url)
# 除法gps 114.21873305555556 22.7261375 街道：广东省深圳市龙岗区黄阁路附近

lon = 11412.67439 / 100
lat = 2243.34095 / 100
# print('初始', lon, lat)
div_lon = 114 + 12.67439 / 60
div_lat = 22 + 43.34095 / 60
# print("除法 lon lat", lon, lat)  # 广东省深圳市龙岗区黄阁路附近
# lon, lat = 114.20833, 22.72556
gc_lon, gc_lat = tr.wg84_to_gcj02(div_lon, div_lat)  # 广东省深圳市龙岗区愉龙路附近
# print('gc转换后坐标：{},{}'.format(gc_lon, gc_lat))
# 初始 114.12674390000001 22.433409499999996

gdlon, gdlat = gps_to_gd(div_lon, div_lat)  # 广东省深圳市龙岗区愉龙路附近
# print('gd地址', div_lon, div_lat)
# 初始坐标除法后转高德接口
# run(lon, lat)
# print(gdrun(114.216739,22.719733)) # 正确公司地址
# print('高德api:高德地址',gdrun(gdlon,gdlat)) # 广东省深圳市龙岗区龙城街道愉龙路万科金色沁园
# print('高德api:除法地址',gdrun(div_lon,div_lat)) # 除法地址 广东省深圳市龙岗区龙城街道黄阁坑新秀新村家乐园家居建材广场
# print('高德api:gc地址',gdrun(gc_lon,gc_lat)) # 广东省深圳市龙岗区龙城街道愉龙路万科金色沁园

# print('本地api:高德地址',run(gdlon,gdlat)) # 广东省深圳市龙岗区愉龙路附近
# print('本地api:除法地址',run(div_lon,div_lat)) # 广东省深圳市龙岗区黄阁路附近
# print('本地api:gc地址',run(gc_lon,gc_lat)) # 广东省深圳市龙岗区愉龙路附近
# print(run(114.19891, 22.71749))

#城邦大道
# 114.197690833,22.7211151667
gc_lon, gc_lat = tr.wg84_to_gcj02(114.197690833,22.7211151667)
gd_lon, gd_lat = gps_to_gd(114.197690833,22.7211151667)
print(gdrun(gc_lon, gc_lat))
print(run(gc_lon,gc_lat))
print(gdrun(gd_lon, gd_lat)) # 广东省东莞市凤岗镇城邦大道益田·大运城邦
print(run(gd_lon,gd_lat)) # 城邦大道附近