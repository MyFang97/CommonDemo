"""
自动更新
"""

import ftplib
import sys
import os
import models
import logging
import datetime
import requests
import sqlite3
import time


def get_server_version():  # 读取服务器版本信息
    # 需要新增version接口，返回版本号
    url = "http://120.92.107.97:8001/api/version"
    data = requests.get(url)
    res = data.json()['result']
    print('远程版本：{}'.format(res))
    logging.info('远程版本：{}'.format(res))
    return res


def get_local_version():  # 读取本地版本信息
    # 从model中获取
    res = {}
    try:
        conn = sqlite3.connect("/home/nvidia/hylink/engine.db")
        cursor = conn.cursor()
        sql = """select CONF_VALUE from T_B_CONFIG where CONF_KEY= ?"""
        cursor.execute(sql, ('version',))
        result = cursor.fetchone()
        print(result[0])
        print(type(result))
        conn.close()
        res['result'] = result[0]
        print('本地版本:{}'.format(result[0]))
        return result[0]
    except Exception as e:
        # res['result'] = str(e)
        print(e)
        return str(0)

    # return json.dumps(res)
    # 部署版
    # version = models.ConfigThread.query_version()
    # print(version)
    # logging.info('本地版本', version)
    # return version


local_version = get_local_version()
new_version = get_server_version()


# 检查版本
def check_version():
    result = {}
    if local_version < new_version:
        logging.info('需要更新(local_version:{},new_version:{})'.format(
            local_version, new_version))
        print('需要更新(local_version:{},new_version:{})'.format(
            local_version, new_version))
        result['code'] = 0
        result['msg'] = '当前版本:{},檢查到新版本:{}'.format(local_version, new_version)
    else:
        result['code'] = 1000
        result['msg'] = '当前版本:{},已經是最新版本！'.format(local_version)
    return result


class myFtp:
    ftp = ftplib.FTP()

    def __init__(self, host):
        self.ftp.connect(host)

    def Login(self, user, passwd):
        self.ftp.login(user, passwd)
        print(self.ftp.welcome)

    def DownLoadFile(self, LocalFile, RemoteFile):  # 下载当个文件
        file_handler = open(LocalFile, 'wb')
        print(file_handler)
        # self.ftp.retrbinary("RETR %s" % (RemoteFile), file_handler.write)#接收服务器上文件并写入本地文件
        self.ftp.retrbinary('RETR ' + RemoteFile, file_handler.write)
        file_handler.close()
        return True

    def DownLoadFileTree(self, LocalDir, RemoteDir):  # 下载整个目录下的文件
        print("remoteDir:", RemoteDir)
        if not os.path.exists(LocalDir):
            os.makedirs(LocalDir)
        self.ftp.cwd(RemoteDir)
        RemoteNames = self.ftp.nlst()
        print("RemoteNames", RemoteNames)
        for file in RemoteNames:
            Local = os.path.join(LocalDir, file)
            print(self.ftp.nlst(file))
            if file.find(".") == -1:
                if not os.path.exists(Local):
                    os.makedirs(Local)
                self.DownLoadFileTree(Local, file)
            else:
                self.DownLoadFile(Local, file)
        self.ftp.cwd("..")
        return

    def close(self):
        self.ftp.quit()


def run(new_name):
    host_ip = '129.204.162.56'
    remote_path = '/home/ubuntu/hylink'
    local_path = '/home/nvidia/hylink'
    remote_file = '/home/ubuntu/hylink{}.zip'.format(new_version)  # 服务器上新版文件路径
    local_file = '/home/nvidia/hylink{}.zip'.format(new_version)  # 下载文件本地存储路径
    username = 'ubuntu'
    password = 'FANGbin1997'
    status = check_version()
    result = {}
    print(status)
    if not status:
        result['code'] = 1000
        result['msg'] = '已經是最新版本'
        print('已經是最新版本')
        return result

    # 判断新版本zip文件在本地是否存在，不存在则下载
    if not os.path.isfile(local_file):
        print('开始连接ftp下载')
        ftp = myFtp(host_ip)
        try:
            ftp.Login(username, password)
        except Exception as e:
            logging.info('连接错误:{}'.format(e))
            print('连接错误:{}'.format(e))
            result['code'] = 1001
            result['msg'] = '网络连接错误，退出更新！'
            return result
        print('开始更新')
        # 从目标目录下载到本地目录
        print('下载zip源文件中')
        try:
            ftp.DownLoadFile(local_file, remote_file)
        except Exception as e:
            result['code'] = 1002
            result['msg'] = '下载更新文件失败：{}，请联系后台管理员！'.format(e)
            print('下载失败：{}'.format(e))
            ftp.close()
            return result
        ftp.close()
        print('下载完成')

    # 把原hylink文件重命名
    cmd = "mv /home/nvidia/hylink {}".format(new_name)
    os.system(cmd)
    logging.info('重命名后的备份文件new_name:', new_name)

    # 下载完成后解压,
    print('进入解压程序')
    try:
        os.system('cd /home/nvidia/image')
        os.system('unzip -o -d /home/nvidia/ {}'.format(local_file))
        # 解压后删除压缩包,(因为盒子空间不足)
        # os.system('rm {}'.format(local_file))
        # 更新本地数据库和版本信息
        print('更新engine.db文件')
        os.system('cp {}/engine.db {}'.format(new_name, local_path))
        # models.ConfigThread.update_param('version',str(get_server_version()))
        print('更新数据库版本')
        conn = sqlite3.connect("/home/nvidia/hylink/engine.db")
        cursor = conn.cursor()
        sql = """UPDATE T_B_CONFIG SET CONF_VALUE = ? WHERE CONF_KEY = 'version'"""
        res = cursor.execute(sql, (new_version,))
        print('更新db版本成功', res)
        conn.commit()
        conn.close()
    except Exception as e:
        result['code'] = 1003
        result['msg'] = '解压更新失败'
    logging.info("ok!更新完成")
    print('ok!更新完成')
    result['code'] = 0
    result['msg'] = 'ok!更新完成,请重启完成更新！'
    return result


# 测试
if __name__ == '__main__':
    # 更新前把hylink文件夹重命名的文件
    strtime = str(int(time.time()))
    new_name = "/home/nvidia/hylink-{}".format(strtime)
    res = run(new_name)
    print('更新结果：{}'.format(res))
    if res['code'] == 0:
        # 更新完成，删除备份的原文件夹
        print('更新完成，删除备份的原文件夹')
        os.system('sudo rm -r {}'.format(new_name))
    elif res['code'] == 1003:
        # 解压出现错误，回退原版本
        print('出现错误，回退原版本')
        os.system('mv {} /home/nvidia/hylink'.format(new_name))
