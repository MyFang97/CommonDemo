"""
    常用方法合集
"""
import base64
import os
import datetime
import time
import psutil


def getImgB64(imageUrl):
    """
    获取图片base64编码
    :param imageUrl: 图片路径
    :return:
    """
    # img_path = 'face.jpg'
    img = os.path.join('/home/ubuntu/HFAI', imageUrl)
    f_img = open(imageUrl, 'rb')  # 二进制方式打开图文件
    ls_f = base64.b64encode(f_img.read())  # 读取文件内容，转换为base64编码
    f_img.close()
    # print('ls_f:{}'.format(ls_f))
    return ls_f


# 获取当前格式化时间
def get_str_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]


# 定期自动清理image文件夹
def auto_clear():
    image = "/home/nvidia/image"
    rtn = psutil.disk_usage("/")
    while True:
        if rtn.percent > 85:
            # 清理七天之前创建的所有类型的文件
            os.system('sudo find ' + image + ' -ctime +7 -name "*.*" -delete')
            time.sleep(10 * 24 * 60 * 60)  # 清理之后，10天之后再次查询
        time.sleep(3 * 24 * 60 * 60)  # 没有清理之前三天查一次



