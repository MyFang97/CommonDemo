# encoding:utf8
import os
import psutil
# import datetime
# import requests
# import chardet
# import json


def clean_image():
    print('== CLEAN UP FILES ==')
    image_dic = '/home/nvidia/image'
    face_big = '/home/nvidia/image/face/big/'
    face_small = '/home/nvidia/image/face/small/'
    plate_big = '/home/nvidia/image/plate/big/'
    plate_small = '/home/nvidia/image/plate/small/'
    rtn = psutil.disk_usage(image_dic)
    print(rtn.percent)
    if rtn.percent > 0:
        print('执行')
        try:
            suCmd('rm -fr ' + plate_big + '* ')
            suCmd('rm -fr ' + plate_small + '* ')
            # suCmd('rm -fr ' + config.path_plate + 'pass/* ')
            suCmd('rm -fr ' + face_big + '* ')
            suCmd('rm -fr ' + face_small + '* ')
            # suCmd('rm -fr ' + config.path_face + 'pass/* ')
            print('ok')
        except Exception as e:
            print(e)


def suCmd(command):
    sudoPassword = 'nvidia'
    rtn = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
    print(str(command) + "==>" + str(rtn))

clean_image()