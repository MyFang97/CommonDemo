import requests

# lon = '105.142197'
# lat = '30.124857'
# url = 'http://51.205.21.43:25001/as/rgeo?ak=ec85d3648154874552835438ac6a02b2&location=%s,%s&pois=1' % (lon, lat)
# response = requests.get(url)
# print(response)
# print(response.json())
# print(response.json()['result'][0]['formatted_address'])
url = 'https://ccn.91p52.com//m3u8/420024/420024.m3u8?st=RypWjLSG-HplNCxGLauhAg&e=1609006906&f=44b1xX0vq7I7GzSq6PPKZhSvLiz/d9TQQ8n9oAwVClRFfMnFJLecm0GYDbnA/peFFhTU55SX5rtCr/JUPIsLXICA2O5hlmyaCW0c'
head_url = 'https://ccn.91p52.com//m3u8/420024/4200240.ts'
ts_text = requests.get(url).text
print(ts_text)