# author_='Fang';
# date: 2021/6/2 18:02
"""
    恩杠ftp上传
"""
import requests

url = "http://192.168.1.11:80/Login.cgi"
headers = {
    "Cookie": "usrname=admin&amp; password=admin&amp",
    "Accept-Encoding": "gzip, deflate",
    "Referer": "http://192.168.1.11/config.html"

}
data = {"Header":
            {"Action": "Request", "Method": "SetFtpConfig", "Session": ""},
        "Param":
            {"FtpEnable": 1, "FtpSeverAddr": "192.168.1.122", "FtpServerPort": 2221, "UsrName": "admin",
             "PassWord": "123456", "FtpDir": "/BJJC001CP11"}
        }
response = requests.post(url=url, headers=headers, data=data)
print(response)
print(response.status_code)
