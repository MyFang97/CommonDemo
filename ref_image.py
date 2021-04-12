"""
图片添加防伪码等信息水印
"""
import hashlib
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter


def get_md5(img):
    file = open(img, "rb")
    m2 = hashlib.md5()
    m2.update(file.read())
    return m2.hexdigest()


# print(get_md5('D:\Desktop\通用代码合集\\12.jpeg'))
