# author_='Fang';
# date: 2021/4/12 15:57
"""
图片拼接
"""
import os
from os import listdir
from PIL import Image


def pinjie(im_list, out_img):
    """
    传入要拼接的图片列表、输出图片路径
    :param im_list:
    :param out_img:
    :return:
    """
    # 图片转化为相同的尺寸
    ims = []
    for i in im_list:
        new_img = Image.open(i).resize((1280, 1280), Image.BILINEAR)
        ims.append(new_img)
    # 单幅图像尺寸
    width, height = ims[0].size
    # 创建空白长图
    result = Image.new(ims[0].mode, (width, height * len(ims)))
    # 拼接图片
    for i, im in enumerate(ims):
        result.paste(im, box=(0, i * height))
    # 保存图片
    result.save(out_img)


if __name__ == '__main__':
    # pinjie(["123.jpg", "123.jpg", "123.jpg"], "121a.jpg")
    os.remove("121a.jpg")
