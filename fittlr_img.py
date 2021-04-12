"""
根据文件名筛选图片
"""

import os


# windows
# 创建文件夹 md 路径\文件名
# 复制 copy 路径\文件名
def get_img_list(file_dir, my_cf, right_dir, error_dir):
    for root, dirs, files in os.walk(file_dir):
        # print(root)  # 当前目录路径
        # print(dirs)  # 当前路径下所有子目录
        # print(files)  # 当前路径下所有非目录子文件
        for file in files:
            # 提取置信度
            cf = file.split('cfds')[1][:4]
            img_dir = '{}\\{}'.format(file_dir, file)
            if float(cf) >= my_cf:
                print('筛选出一条：{}'.format(file))
                os.system('copy {} {}'.format(img_dir, right_dir))
            else:
                print('过滤：{}'.format(file))
                os.system('copy {} {}'.format(img_dir, error_dir))


if __name__ == '__main__':
    my_cf = 0.7  # 自定义置信度
    file_dir = 'E:\\to方彬，筛选后的数据\image'  # 主文件目录
    right_dir = '{}\\{}'.format(file_dir, my_cf)  # 以自定义的置信度为目录，高于的提取到此目录下
    os.mkdir(right_dir)
    error_dir = '{}\\{}\\{}_error'.format(file_dir, my_cf, my_cf)  # 以自定义的置信度为目录，低于的的提取到此目录下
    os.mkdir(error_dir)
    get_img_list(file_dir, my_cf, right_dir, error_dir)
