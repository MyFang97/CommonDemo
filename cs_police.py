"""
    长沙交警支队数据对接

1、目录
    /home/test1
    /home/test2
    /home/test3
2、获取目录里的文件列表 eg:['20201212','20201213']
3、排序列表，取最大值也就是最近一天的值。如果值与当天日期相同，则执行后续逻辑
"""
import os
import threading
import time
import re
import glob
import sqlite3
from lxml import etree
import uuid
import stomp
import logging
import shutil


# def get_dev(path):
#     files = os.listdir(path)  # 获得当前 硬盘目录中的所有文件夹
#     print(files)  # [test1、test2、test3]
#     for i in files:  # 逐个文件遍历
#         if (os.path.isdir(os.path.join(basepath, i))):  # 判断当前是一个文件夹'''
#             if i not in dev_list:
#                 dev_list.append(os.path.join(basepath, i))
#     dev_list.sort()
#     # time.sleep(300)  # 300s检测一次是否有新设备 现在就先三个设备吧


def get_data():
    # for num in range(len(dev_list)):
    # 设备编号
    sbbh = '6'
    sbbh1 = '7'
    sbbh2 = '8'
    # ftp账号密码
    ftp_accont, ftp_passwd = 'test1', 'test1'
    ftp_accont1, ftp_passwd1 = 'test2', 'test2'
    ftp_accont2, ftp_passwd2 = 'test3', 'test3'
    t1 = threading.Thread(target=upload_data,
                          args=('D:\\Desktop\\csjj\\test1', sbbh, ftp_accont,
                                ftp_passwd))  # eg:dev_list[0]='D:\\Desktop\\csjj\\test1'
    t1.start()
    # t2 = threading.Thread(target=upload_data, args=(
    #     'D:\\Desktop\\csjj\\test2', sbbh1, ftp_accont1, ftp_passwd1))  # eg:dev_list[0]=D:\\Desktop\\csjj\\test2
    # t2.start()
    # t3 = threading.Thread(target=upload_data, args=(
    #     'D:\\Desktop\\csjj\\test3', sbbh2, ftp_accont2, ftp_passwd2))  # eg:dev_list[0]=D:\\Desktop\\csjj\\test3
    # t3.start()


def upload_data(path, sbbh, ftp_accont, ftp_passwd):
    # 设备分线程
    # eg:datefile = 20201212 = date_files[-1]

    date_files = []
    dev = path.split('\\')[-1]
    print('dev', dev)
    while True:
        # eg:path='D:\\Desktop\\csjj\\test1'
        # 连接数据库和海信端，循环获取目录
        try:
            my_slqite = MySqlite()
            # mymq = MyMq()
        except Exception as e:
            print(e)
            time.sleep(10)
            continue
        for date_file in os.listdir(path):  # eg:datefile = 20201212
            date_files.append(date_file)
        date_files.sort()
        if date_files == []:
            continue
        print(date_files[-1])  # eg:date_files[-1] = 20201218
        now_time = time.strftime("%Y%m%d", time.localtime())
        if date_files[-1] == '20201218':  # 正式环境下应该改为now_time
            res = my_slqite.select_sqlite(date_files[-1], dev)
            for file in os.listdir(os.path.join(path, date_files[-1])):
                if file[-4:] == '.xml':
                    """
                        已经找到xml文件，查看数据库有没有插入过，没有就将文件插入到数据库，解析xml文件，组织上传数据
                        注意：sqlite查询返回的是列表套元组，比对需要注意
                    """
                    tup_file = (file,)
                    if tup_file in res:
                        continue
                    # 解析xml文件，组织上传数据，新建方法parse_xml,send_to_hx
                    xml_file_path = os.path.join(path, date_files[-1], file)
                    # xml_file_path D:\Desktop\csjj\test1\20201218\湖南省长沙市岳麓区银盆南路_违法停车_湘AZ5Y23_20201217_165731781_plate.xml
                    print('xml_file_path', xml_file_path)
                    try:
                        RoadName, Time, PlateNo, Image1, AVI, TrackMode, GPS = parse_xml(xml_file_path)
                        # 处理图片路径
                        Image1_name = Image1.split('\\')[-1]
                        new_Image1_name = Image1_name.split('_')[-3] + '_' + Image1_name.split('_')[-2] + '_' + \
                                          Image1_name.split('_')[-1]
                        shutil.copy(os.path.join(path, date_files[-1], Image1_name),
                                    os.path.join(path, date_files[-1], new_Image1_name))
                        # 处理视频路径
                        AVI_name = AVI.split('\\')[-1]
                        new_AVI_name = AVI_name.split('_')[-3] + '_' + AVI_name.split('_')[-2] + '_' + \
                                       AVI_name.split('_')[-1]
                        shutil.copy(os.path.join(path, date_files[-1], AVI_name),
                                    os.path.join(path, date_files[-1], new_AVI_name))
                        # 发送逻辑
                        send_Image = 'ftp://{}:{}@{}:21/{}/{}'.format(ftp_accont, ftp_passwd, '43.5.169.242',
                                                                      date_files[-1], new_Image1_name)
                        send_AVI = 'ftp://{}:{}@{}:21/{}/{}'.format(ftp_accont, ftp_passwd, '43.5.169.242',
                                                                    date_files[-1], new_AVI_name)
                        print('send_Image', send_Image)
                        msg = final_data(sbbh, RoadName, Time, PlateNo, send_Image, send_AVI, TrackMode, GPS)
                        # mymq.send_to_topic(msg)
                    except Exception as e:
                        print(e)
                    else:
                        my_slqite.insert_sqlite(file, date_files[-1], dev)
            print('ok')
            break
        # time.sleep(30)


def parse_xml(xml_path):
    getxml = GetXML()
    getxml.Read(xml_path)
    RoadName = getxml.Find('RoadName').get('value')
    Time = getxml.Find('Time').get('value')
    PlateNo = getxml.Find('PlateNo').get('value')
    Image1 = getxml.Find('Image1').get('value')
    AVI = getxml.Find('AVI').get('value')
    TrackMode = getxml.Find('TrackMode').get('value')
    GPS = getxml.Find('GPS').get('value')
    # print(RoadName, Time, PlateNo, Image1, AVI, GPS)
    return RoadName, Time, PlateNo, Image1, AVI, TrackMode, GPS


def final_data(sbbh, RoadName, Time, PlateNo, Image1, AVI, TrackMode, GPS):
    # 010010001
    # 2020-12-17 16:57:31 781  [:-4]
    # 湘AZ5Y23
    # D:\\result\192.168.12.250\20201217\湖南省长沙市岳麓区银盆南路_违法停车_湘AZ5Y23_20201217_165731781_imageMix.jpg
    # D:\\result\192.168.12.250\20201217\湖南省长沙市岳麓区银盆南路_违法停车_湘AZ5Y23_20201217_165731781_plate.avi
    # 违法停车
    # 湖南省长沙市岳麓区银盆南路
    pass
    csbh = '0099'  # 厂商编号
    wfdm = '13441'  # 违法代码
    ddbh = ''  # 采集点编号
    cjdd = ''
    cjjgdm = '430106000000'  # 采集机关代码
    jh = ''
    uid = str(uuid.uuid1())
    suid = ''.join(uid.split('-'))
    Time = Time[:-4]
    now_time = time.strftime("%Y%m%d %H:%M:%S", time.localtime())
    msg = "ILLEGAL01,2.6,{},{},9-其他,99,{},{},{},{},{},{},05,2,{},,{},,,{},,{},,,{},0,".format(csbh, suid, PlateNo,
                                                                                              Time,
                                                                                              wfdm, ddbh, GPS, cjjgdm,
                                                                                              sbbh,
                                                                                              Image1, jh, AVI,
                                                                                              now_time)
    # print(msg)
    logger.info('组织好的数据：{}'.format(msg))
    return msg
    # ILLEGAL01,2.6,0099,cea6528645f511ebb5fcabcfb6a891ab,9-其他,99,湘AF149S,2020-12-18 17:39:12,13441,,湖南省长沙市岳麓区银盆南路,430106000000,05,2,6,,ftp://test1:test1@43.5.169.242:21/20201218/20201218_173912281_imageMix.jpg,,,,,ftp://test1:test1@43.5.169.242:21/20201218/20201218_173912281_plate.avi,,,20201224 22:39:20,0,


class MyMq:
    def __init__(self):
        try:
            self.conn = stomp.Connection10([("43.5.18.2", 61616)], auto_content_length=False)
            self.conn.start()
            self.conn.connect()
            logger.info('mq2连接上了')
        except Exception as e:
            self.conn = stomp.Connection10([("43.5.18.3", 61616)], auto_content_length=False)
            self.conn.start()
            self.conn.connect()
            logger.info('mq3连接上了')

    def send_to_topic(msg):
        logger.info('开始发送：{}'.format(msg))
        conn.send('/topic/HIATMP.HISENSE.ILLEGAL', msg)
        logger.info('发送成功')

    def close(self):
        self.conn.disconnect()


class MySqlite:
    def __init__(self):
        self.conn = sqlite3.connect("csjj.db")
        self.cursor = self.conn.cursor()

    def select_sqlite(self, dir, dev):
        # sql = """INSERT T_B_CONFIG SET CONF_VALUE = ? WHERE CONF_KEY = 'version'"""
        sql = """SELECT TRAN_FILE FROM TRAN WHERE TRAN_DIR=? AND TRAN_DEV=?"""
        res = self.cursor.execute(sql, (dir, dev))
        res = self.cursor.fetchall()
        # print('db查询成功', res)
        self.conn.commit()
        # conn.close()
        return res

    def insert_sqlite(self, file, dir, dev):
        # sql = """INSERT T_B_CONFIG SET CONF_VALUE = ? WHERE CONF_KEY = 'version'"""
        sql = """INSERT INTO TRAN (TRAN_FILE,TRAN_DIR,TRAN_DEV) VALUES (?,?,?)"""
        res = self.cursor.execute(sql, (file, dir, dev))
        # print('db插入成功', res)
        self.conn.commit()
        # conn.close()


class GetXML:
    '提供读取XML文件和读取值得一些方法'

    def __init__(self):
        pass

    def Read(self, xmlfilename):
        '将XML文件解析为树,并且得到根节点'
        # tree = ET.parse(xmlfilename)
        tree = etree.parse(xmlfilename)
        self.root = tree.getroot()
        return self.root

    def Iter(self):
        '递归迭代xml文件中所有节点（包含子节点，以及子节点的子节点）'
        return self.root.iter()

    def FindAll(self, tag):
        '查找节点为tag的所有直接子元素'
        # 直接子元素的意思：只会查找当前节点的子节点那一级目录
        return self.root.findall(tag)

    def Find(self, tag):
        '查找第一个节点为tag的直接子元素'
        return self.root.find(tag)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    get_data()
    # 改split('/')
    # 改基础路径
