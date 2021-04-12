"""
    ftp上传下载demo
"""

# coding: utf-8
from ftplib import FTP
import time
import tarfile
import os
# !/usr/bin/python
# -*- coding: utf-8 -*-

from ftplib import FTP


def ftpconnect(host, username, password):
    ftp = FTP()
    # ftp.set_debuglevel(2)
    ftp.connect(host, 21)
    ftp.login(username, password)
    return ftp


# 从ftp下载文件
def downloadfile(ftp, remotepath, localpath):
    bufsize = 1024
    fp = open(localpath, 'wb')
    ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)
    ftp.set_debuglevel(0)
    fp.close()


# 从本地上传文件到ftp
def uploadfile(ftp, localpath, remotepath):
    bufsize = 1024
    # print(ftp.cwd('/'))
    # remotepath = os.path.join('/home/km/', remotepath)
    # print(remotepath)
    fp = open(localpath, 'rb+')
    ftp.storbinary('STOR ' + remotepath, fp, bufsize)
    ftp.set_debuglevel(0)
    fp.close()


if __name__ == "__main__":
    ftp = ftpconnect("43.5.169.242", "test1", "test1")
    ftp.dir()
    ftp.nlst()
    try:
        ftp.mkd('c')
        ftp.mkd('c/b')
    except Exception as e:
        print(e)
    uploadfile(ftp, "13.jpg", "c/b/13.jpg")

    ftp.quit()
