"""
    计算nx算法错误率
"""
import os

all_num = 0
error_num = 0
dir_num = 0
list_no_num = []


def run(file_dir):
    global all_num
    global error_num, dir_num, list_no_num
    for img_dir in os.listdir(file_dir):
        try:
            dir_num += 1
            print(img_dir)
            all = img_dir.split('z')[1].split('c')[0]
            error = img_dir.split('c')[-1]
            print(all)
            print(error)
            all_num += int(all)
            error_num += int(error)
        except Exception as e:
            list_no_num.append(img_dir)
    # for root, dirs, files in os.walk(file_dir):
    # print(root)  # 当前目录路径
    # print(dirs)  # 当前路径下所有子目录
    # print(files)  # 当前路径下所有非目录子文件
    # for img_dir in dirs:
    #     try:
    #         dir_num += 1
    #         print(img_dir)
    #         all = img_dir.split('z')[1].split('c')[0]
    #         error = img_dir.split('c')[-1]
    #         print(all)
    #         print(error)
    #         all_num += int(all)
    #         error_num += int(error)
    #     except Exception as e:
    #         list_no_num.append(img_dir)


run('F:\\nx0106')
print('文件夹总数', dir_num)
print('图片总数', all_num)
print('错误数', error_num)
print('错误率', error_num / all_num)
print(list_no_num)
"""
文件夹总数 1494
图片总数 9373
错误数 974
错误率 0.1039155019737544
['粤B92550', '粤BDZ93D-zz3c3', '粤BFA9925-zz9c0', '粤BJDM1603']
"""
