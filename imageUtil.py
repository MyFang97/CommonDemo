# encoding:utf8

'''
图片水印添加
'''
import cv2
import numpy as np
from PIL import ImageFont, Image, ImageDraw
import hashlib
import os

'''
imgPath  原始图片
destPath 生成图片
length   延伸的长度
'''


def expand(imgPath, destPath, length):
    image = cv2.imread(imgPath)
    h, w, c = image.shape
    img = np.zeros((length, w, 3), np.uint8)
    img.fill(0)
    addText = np.vstack([image, img])
    cv2.imwrite(destPath, addText)


'''
imgPath  原始图片
destPath 生成图片
x
y
text   文字
color  文字颜色
size   文字大小
'''


def writeText(imgPath, destPath, sbbh,text1, text2, text3, color, size):
    image = cv2.imread(imgPath)

    h, w, c = image.shape  # shape返回的是一个tuple元组，第一个元素表示图像的高度，第二个表示图像的宽度

    font = ImageFont.truetype("../simhei.ttf", size, encoding="utf-8")  # 参数1：字体文件路径，参数2：字体大小

    cv2img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # cv2和PIL中颜色的hex码的储存顺序不同
    pilimg = Image.fromarray(cv2img)
    draw = ImageDraw.Draw(pilimg)  # 图片上打印
    draw.text((10, h - 150), sbbh, color, font=font)  # 参数1：打印坐标，参数2：文本，参数3：字体颜色，参数4：字体
    draw.text((10, h - 120), text1, color, font=font)  # 参数1：打印坐标，参数2：文本，参数3：字体颜色，参数4：字体
    draw.text((10, h - 90), text2, color, font=font)  # 参数1：打印坐标，参数2：文本，参数3：字体颜色，参数4：字体
    draw.text((10, h - 60), text3, color, font=font)  # 参数1：打印坐标，参数2：文本，参数3：字体颜色，参数4：字体
    # draw.text((w, h), text, color, font=font)  # 参数1：打印坐标，参数2：文本，参数3：字体颜色，参数4：字体
    cv2charimg = cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)
    cv2.imwrite(destPath, cv2charimg)


def get_md5(img):
    file = open(img, "rb")
    m2 = hashlib.md5()
    m2.update(file.read())
    return m2.hexdigest()


def draw_image(imgPath, destPath, sbbh, text1, text2, text3):
    # print(get_md5(imgPath))
    expand(imgPath, destPath, 150)
    writeText(destPath, destPath, sbbh, text1, text2, text3, (255, 0, 0), 30)
    # print(get_md5(destPath))


def imgToMd5(imgPath):
    image = cv2.imread(imgPath)
    zuoshangx = 53
    zuoshangy = 74
    youxiax = 614
    youxiay = 177
    md5 = '6ac3fdf409314419aee1a57bbf62d072'
    [dirname, filename] = os.path.split(imgPath)
    cut = image[zuoshangy:youxiay, zuoshangx:youxiax]
    ft = ImageFont.truetype("simhei.ttf", 30, encoding="utf-8")  # 参数1：字体文件路径，参数2：字体大小
    cvimg = paint(cut, 12, 53, md5, ft)
    cv2.imwrite(dirname + '/cc.jpg', cvimg)
    fd = np.array(Image.open(dirname + '/cc.jpg'))
    fmd5 = hashlib.md5(fd)
    os.remove(dirname + '/cc.jpg')
    fmd5 = fmd5.hexdigest()
    return fmd5


def paint(img, x, y, content, ft):
    cv2img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # cv2和PIL中颜色的hex码的储存顺序不同
    pilimg = Image.fromarray(cv2img)
    draw = ImageDraw.Draw(pilimg)  # 图片上打印
    draw.text((x, y), content, (255, 0, 0), font=ft)
    cvimg = cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)
    return cvimg


if __name__ == '__main__':
    # expand("12.jpeg", "12.jpeg", 200)
    # writeText("12.jpeg", "12.jpeg", u"我是水印文字", (255, 0, 0), 40)
    # md5 = imgToMd5("1.jpg")
    draw_image("123.jpg", "1.jpg", "设备编号", "我是水印文字1", "我是水印文字2", "我是水印文字3")
    # 调用方法
    # md5 = imgToMd5("1.jpg")
