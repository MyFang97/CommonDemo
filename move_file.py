# author_='Fang';
# date: 2021/6/7 18:17
"""
    移动cl下载的MP4文件
"""
import os
import random
import shutil

mydir = 'D:\\\\myVideo'  # test的文件路径
# todir = 'D:\\myVideo\\'
todir = 'E:\\方彬交接\\x'
video_to_dir = todir + '\\video\\'
photo_to_dir = todir + '\\photo\\'
xl_to_dir = todir + '\\xltd\\'


def moveFile():
    """
    移动picture和video到指定文件夹
    :return:
    """
    if not os.path.exists(video_to_dir):
        os.mkdir(video_to_dir)
    if not os.path.exists(photo_to_dir):
        os.mkdir(photo_to_dir)
    for root, dirs, files in os.walk(mydir):
        for file in files:
            if '.mp4' in file:  # 只查找mp4文件
                print("mp4:" + os.path.join(root, file))
                if not os.path.exists(os.path.join(video_to_dir, file)):
                    shutil.move(os.path.join(root, file), video_to_dir)
                else:
                    new_name = file + str(random.randint(100, 999)) + "_.mp4"
                    shutil.move(os.path.join(root, file), video_to_dir + new_name)
            elif '.jpg' in file or '.png' in file:
                print("jpg:" + os.path.join(root, file))
                if not os.path.exists(os.path.join(photo_to_dir, file)):
                    shutil.move(os.path.join(root, file), photo_to_dir)
                else:
                    new_name = file + str(random.randint(1000, 9999)) + "_.jpg"
                    shutil.move(os.path.join(root, file), photo_to_dir + new_name)


# print(os.listdir(to_dir))

# 未下载完成的转移到xl目录
def selectXltd():
    """
    移动xltd文件
    :return:
    """
    if not os.path.exists(xl_to_dir):
        os.mkdir(xl_to_dir)
    for root, dirs, files in os.walk(video_to_dir):
        for file in files:
            if ".xltd" in file:
                print(file)
                shutil.move(os.path.join(root, file), xl_to_dir)
    for root, dirs, files in os.walk(photo_to_dir):
        for file in files:
            if ".xltd" in file:
                print(file)
                shutil.move(os.path.join(root, file), xl_to_dir)


if __name__ == '__main__':
    moveFile()
    # selectXltd()
