# author_='Fang';
# date: 2021/4/13 12:52
"""
cv2生产者
"""
# import cv2
# import time
#
# if __name__ == "__main__":
#     frameDict = dict()
#     ## 读取rtsp视频流并显示
#     # cap = cv2.VideoCapture("rtsp://192.168.xx.xxx:8554/live1.h264")
#     ## 读取usb-came 0（/dev/video0）
#     cap = cv2.VideoCapture(0)
#     while cap.isOpened():
#         (ret, frame) = cap.read()
#         print(frame.shape[0], frame.shape[1], frame.shape[2])
#         cv2.imshow("frame", frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
# cv2.destroyWindow("frame")
# cap.release()

import threading
import os
import cv2
import gc
import time
from multiprocessing import Process, Manager
import redis

disVideo2frameDict = dict()


def getDisPhotoDict():
    # disRtspUrl = models.DeviceThread().selectBeforeMid()["deviceRtspUrl"]
    # disRtspUrl = "rtsp://admin:admin@192.168.1.14:554/c=0&s=0"
    disRtspUrl = 0
    cap = cv2.VideoCapture(disRtspUrl)
    while True:
        rval, frame = cap.read()
        nowTime = int(time.time())
        print("nowTime" + str(nowTime))
        disVideo2frameDict[nowTime] = frame
        cv2.imshow("frame", frame)

        cv2.waitKey(1)
        time.sleep(1)


def delDisPhotoDict():
    while True:
        # global disVideo2frameDict
        disDictKeys = disVideo2frameDict.keys()
        for key in disDictKeys:
            if int(time.time()) - int(key) >= 60:
                print("删除" + disVideo2frameDict[key])
                del disVideo2frameDict[key]
        time.sleep(5)


def printKey():
    while True:
        # print(disVideo2frameDict)
        print(disVideo2frameDict.keys())
        time.sleep(2)


if __name__ == '__main__':
    threading.Thread(target=getDisPhotoDict).start()
    threading.Thread(target=delDisPhotoDict).start()
    threading.Thread(target=printKey).start()

