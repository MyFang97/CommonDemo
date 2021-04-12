# encoding: utf-8
import base64
import datetime
import json
import logging
import threading
import time
import uuid

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Column, String, create_engine, Integer, MetaData, Table, desc, Float, not_, and_

print(__name__)

Base = declarative_base()

# 初始化数据库连接:
engine = create_engine('sqlite:///engine.db')


# def __repr__(self):
# 	return "<User(name='%s', fullname='%s', password='%s')>" % (
# 			self.name, self.fullname, self.password)


class FaceRecord(Base):
    # 表的名字:
    __tablename__ = 'T_B_FACE_RECORD'

    # 表的结构:
    ID = Column(Integer, primary_key=True, autoincrement=True)
    FR_IMAGEURL = Column(String(500))
    FR_DEVICE_NUMBER = Column(Integer)
    FR_BIG_IMAGEURL = Column(String(500))
    FR_LAT = Column(String(100))
    FR_LNG = Column(String(100))
    ISDEL = Column(Integer)
    CREATE_TIME = Column(String(100))


class FaceBlack(Base):
    # 表的名字:
    __tablename__ = 'T_B_FACE_BLACK'

    # 表的结构:
    ID = Column(Integer, primary_key=True, autoincrement=True)
    FB_IMAGEURL = Column(String(500))
    FB_NAME = Column(String(100))
    FB_AGE = Column(Integer)
    FB_SEX = Column(Integer)
    FB_ZJ_NUM = Column(String(100))
    FB_NOTE = Column(String(100))
    FB_PHONE = Column(String(100))
    FACEFT_128 = Column(String(5000))
    ISDEL = Column(Integer)
    CREATE_TIME = Column(String(100))
    FB_LOCALIMAGEURL = Column(String(500))  # 本地图片


class FaceWarning(Base):
    # 表的名字:
    __tablename__ = 'T_B_FACE_WARNING'

    # 表的结构:
    ID = Column(Integer, primary_key=True, autoincrement=True)
    FRID = Column(Integer)
    FW_FBZJNUM = Column(Integer)
    ISDEL = Column(Integer)
    CREATE_TIME = Column(String(100))
    CONTRAST = Column(Float)


class PlateRecord(Base):
    # 表的名字:
    __tablename__ = 'T_B_PLATE_RECORD'

    # 表的结构:
    ID = Column(Integer, primary_key=True, autoincrement=True)
    PR_IMAGEURL = Column(String(500))
    PR_BIG_IMAGEURL = Column(String(500))
    PR_NUMBER = Column(String(500))
    PR_COLOR = Column(String(100))
    PR_LOGO = Column(String(100))
    PR_DEVICE_NUMBER = Column(String(100))
    PR_LAT = Column(String(100))
    PR_LNG = Column(String(100))
    ISDEL = Column(Integer)
    CREATE_TIME = Column(String(100))


class PlateBlack(Base):
    # 表的名字:
    __tablename__ = 'T_B_PLATE_BLACK'

    # 表的结构:
    ID = Column(Integer, primary_key=True, autoincrement=True)
    PB_NUMBER = Column(String(500))
    PB_LOGO = Column(String(100))
    PB_COLOR = Column(String(100))
    PB_OWNER_NAME = Column(String(100))
    PB_OWNER_PHONE = Column(String(100))
    PB_NOTE = Column(String(100))
    ISDEL = Column(Integer)
    CREATE_TIME = Column(String(100))
    ISONLINE = Column(Integer)


class PlateWarning(Base):
    # 表的名字:
    __tablename__ = 'T_B_PLATE_WARNING'

    # 表的结构:
    ID = Column(Integer, primary_key=True, autoincrement=True)
    PRID = Column(Integer)
    PW_PBNUMBER = Column(Integer)
    ISDEL = Column(Integer)
    CREATE_TIME = Column(String(100))


class Config(Base):
    # 表的名字:
    __tablename__ = 'T_B_CONFIG'

    # 表的结构:
    CONF_ID = Column(Integer, primary_key=True, autoincrement=True)
    CONF_KEY = Column(String(100))
    CONF_VALUE = Column(String(100))
    CONF_TYPE = Column(String(100))


class Device(Base):
    # 表的名字:
    __tablename__ = 'T_B_DEVICE'

    # 表的结构:
    DEVICE_ID = Column(Integer, primary_key=True, autoincrement=True)
    DEVICE_IP = Column(String(100))
    DEVICE_NAME = Column(String(100))
    DEVICE_PUID = Column(String(100))
    DEVICE_ZDY_POSITION = Column(String(100))
    DEVICE_RTSP_MAIN = Column(String(250))
    DEVICE_TYPE = Column(Integer)
    DEVICE_CLASS = Column(String(100))
    DEVICE_POSITION = Column(Integer)


# 创建DBSession类型:
session_factory = sessionmaker(bind=engine)
DBSession = scoped_session(session_factory)
###之前上面两段代码中出现过的东西就不再声明了###
# 这就是为什么表类一定要继承Base，因为Base会通过一些方法来通过引擎初始化数据库结构。不继承Base自然就没有办法和数据库发生联系了。
Base.metadata.create_all(engine)
session = DBSession()


class ConfigThread(threading.Thread):

    def update_param(self, key, value):
        session = DBSession()
        session.query(Config).filter(Config.CONF_KEY == key).update({Config.CONF_VALUE: value})
        session.commit()
        session.close()

    def query_version(self):
        session = DBSession()
        config = session.query(Config).filter(Config.CONF_KEY == 'version').all()
        cfg = {}
        if config[0] != None:
            cfg['id'] = config[0].CONF_ID
            cfg['key'] = config[0].CONF_KEY
            cfg['value'] = config[0].CONF_VALUE
        else:
            pass
        session.close()
        return cfg['value']

    def select_param(self, key):
        session = DBSession()
        config = session.query(Config).filter(Config.CONF_KEY == key).all()

        cfg = {}
        if config[0] != None:
            cfg['id'] = config[0].CONF_ID
            cfg['key'] = config[0].CONF_KEY
            cfg['value'] = config[0].CONF_VALUE
        else:
            pass
        session.close()
        return cfg

    def select_param(self, type, key):
        session = DBSession()
        config = session.query(Config).filter(and_(Config.CONF_TYPE == type, Config.CONF_KEY == key)).all()

        cfg = None
        if config[0] != None:
            cfg = config[0].CONF_VALUE
        else:
            pass
        session.close()
        return cfg

    def select_param_by_type(self, type):
        session = DBSession()
        config = session.query(Config).filter(Config.CONF_TYPE == type).all()

        cfg = {}
        for item in config:
            cfg[item.CONF_KEY] = item.CONF_VALUE
        else:
            pass
        session.close()
        return cfg


class DeviceThread(threading.Thread):
    def insert(self, strDeviceIp, strDevicePuid, strRtspMain, nType, nPosition, strDeviceName, strZdyPosition,
               strDeviceClass):
        session = DBSession()
        device = Device(
            DEVICE_IP=strDeviceIp,
            DEVICE_PUID=strDevicePuid,
            DEVICE_NAME=strDeviceName,
            DEVICE_CLASS=strDeviceClass,
            DEVICE_RTSP_MAIN=strRtspMain,
            DEVICE_TYPE=nType,
            DEVICE_POSITION=nPosition,
            DEVICE_ZDY_POSITION=strZdyPosition,
        )
        session.add(device)
        session.commit()
        session.close()

    def modify(self, Cid, strDeviceIp, strDevicePuid, strRtspMain, nType, nPosition, strDeviceName, strZdyPosition,
               strDeviceClass):
        session = DBSession()

        result = session.query(Device).filter_by(DEVICE_ID=Cid).first()
        if result != None:
            result.DEVICE_IP = strDeviceIp
            result.DEVICE_PUID = strDevicePuid
            result.DEVICE_RTSP_MAIN = strRtspMain
            result.DEVICE_TYPE = nType
            result.DEVICE_POSITION = nPosition
            result.DEVICE_NAME = strDeviceName
            result.DEVICE_CLASS = strDeviceClass
            result.DEVICE_ZDY_POSITION = strZdyPosition
            session.commit()
        session.close()

    def select_by_class(self, strDeviceClass):
        '''
        yt: 云台
        cj: 采集
        '''
        session = DBSession()
        devices = session.query(Device).filter(Device.DEVICE_CLASS == strDeviceClass).order_by(Device.DEVICE_ID).all()
        result = []
        for device in devices:
            if device != None:
                dev = {}
                dev['id'] = device.DEVICE_ID
                dev['ip'] = device.DEVICE_IP
                dev['puid'] = device.DEVICE_PUID
                dev['rtsp_main'] = device.DEVICE_RTSP_MAIN
                dev['zdyPosition'] = device.DEVICE_ZDY_POSITION
                dev['devName'] = device.DEVICE_NAME
                dev['type'] = device.DEVICE_TYPE
                dev['position'] = device.DEVICE_POSITION
                result.append(dev)
        session.close()
        return result

    def delete_by_id(self, id):
        session = DBSession()
        session.query(Device).filter(
            Device.DEVICE_ID == id).delete()
        session.commit()
        session.close()

    def select_by_class(self, strDeviceClass):
        '''
        yt: 云台
        cj: 采集
        '''
        session = DBSession()
        devices = session.query(Device).filter(Device.DEVICE_CLASS == strDeviceClass).order_by(Device.DEVICE_ID).all()
        result = []
        for device in devices:
            if device != None:
                dev = {}
                dev['id'] = device.DEVICE_ID
                dev['ip'] = device.DEVICE_IP
                dev['puid'] = device.DEVICE_PUID
                dev['rtsp_main'] = device.DEVICE_RTSP_MAIN
                dev['zdyPosition'] = device.DEVICE_ZDY_POSITION
                dev['devName'] = device.DEVICE_NAME
                dev['type'] = device.DEVICE_TYPE
                dev['position'] = device.DEVICE_POSITION
                result.append(dev)
        session.close()
        return result

    def select_ip_by_puid(self, puid):
        session = DBSession()
        devices = session.query(Device).filter_by(DEVICE_PUID=puid).order_by(Device.DEVICE_ID).all()
        result = {}
        if len(devices) > 1:
            return -1
        for device in devices:
            if device != None:
                result = device.DEVICE_IP
        session.close()
        return result


'''
人脸记录类
'''


class FaceRecordThread(threading.Thread):
    '''
     人脸记录新增
     '''

    def insert(self, imageUrl, bigImageUrl, deviceId):
        session = DBSession()
        new_state = FaceRecord(
            FR_IMAGEURL=imageUrl,
            FR_BIG_IMAGEURL=bigImageUrl,
            FR_DEVICE_NUMBER=deviceId,
            CREATE_TIME=getNowTime(),
            ISDEL=0
        )
        session.add(new_state)
        session.commit()
        fRId = new_state.ID
        session.close()
        return str(fRId)

    '''
     人脸记录查询(分页查询)
     '''

    def faceSelectInfo(self, pageIndex=None, pageSize=None, deviceNum=None, startTime=None, endTime=None):
        session = DBSession()
        result = session.query(FaceRecord.FR_BIG_IMAGEURL,
                               FaceRecord.FR_IMAGEURL,
                               FaceRecord.FR_DEVICE_NUMBER,
                               FaceRecord.CREATE_TIME,
                               FaceRecord.FR_LAT,
                               FaceRecord.FR_LNG)
        if deviceNum:
            result = result.filter(FaceRecord.FR_DEVICE_NUMBER == deviceNum)
        if startTime:
            result = result.filter(FaceRecord.CREATE_TIME >= startTime)
        if endTime:
            result = result.filter(FaceRecord.CREATE_TIME <= endTime)
        data = result.order_by(FaceRecord.CREATE_TIME.desc()).limit(pageSize).offset(
            (int(pageIndex) - 1) * int(pageSize))
        arry = []
        for row in data:
            facerecord = {}
            facerecord["frBigImageUrl"] = row[0]
            facerecord["frImageUrl"] = row[1]
            facerecord["frDeviceNumber"] = row[2]
            facerecord["createTime"] = row[3]
            facerecord["frLat"] = row[4]
            facerecord["frLng"] = row[5]
            arry.append(facerecord)
        print
        len(arry)
        session.close()
        return arry

    def selectFaceById(self, id):
        session = DBSession()
        data = session.query(FaceRecord).filter(FaceRecord.ID == id).first()
        resultData = {}

        if data != None:
            resultData['fbId'] = data.ID
            resultData['frBigImageurl'] = data.FR_BIG_IMAGEURL
            resultData['deviceNumber'] = data.FR_DEVICE_NUMBER
            resultData['createTime'] = data.CREATE_TIME
        else:
            resultData = None
        session.close()
        return resultData


class PlateRecordThread(threading.Thread):
    def insertPlate(self, smallImage, bigImage, deviceNum):
        session = DBSession()
        plateRecord = PlateRecord(CREATE_TIME=getNowTime(),
                                  PR_IMAGEURL=smallImage,
                                  PR_BIG_IMAGEURL=bigImage,
                                  PR_NUMBER=deviceNum,
                                  PR_COLOR="",
                                  PR_LOGO="",
                                  PR_DEVICE_NUMBER=deviceNum,
                                  PR_LAT="",
                                  PR_LNG="",
                                  ISDEL=2
                                  )
        session.add(plateRecord)
        session.commit()
        prid = plateRecord.ID
        session.close()
        return str(prid)

    '''
     车牌记录新增
    '''

    def insertPlateInfo(self, smallImage, bigImage, plateNum, deviceNum, gpsData):
        session = DBSession()
        plateRecord = PlateRecord(PR_IMAGEURL=smallImage.decode('utf-8'),
                                  PR_BIG_IMAGEURL=bigImage.decode('utf-8'),
                                  PR_NUMBER=plateNum.decode('utf-8'),
                                  PR_DEVICE_NUMBER=deviceNum.decode('utf-8'),
                                  PR_LAT=str(gpsData['lat']).decode('utf-8'),
                                  PR_LNG=str(gpsData['lon']).decode('utf-8'),
                                  PR_IMAGE_ISUPLOAD=0,
                                  CREATE_TIME=getNowTime(),
                                  UUID=getUUID(),
                                  ISDEL=0)
        session.add(plateRecord)
        session.commit()
        session.close()

    '''
     获取车牌记录(分页查询)
     '''

    def plateSelectInfo(self, pageIndex=None, pageSize=None, deviceNum=None, startTime=None, endTime=None,
                        plateNum=None):
        session = DBSession()
        result = session.query(PlateRecord.PR_BIG_IMAGEURL,
                               PlateRecord.PR_IMAGEURL,
                               PlateRecord.PR_DEVICE_NUMBER,
                               PlateRecord.CREATE_TIME,
                               PlateRecord.PR_LAT,
                               PlateRecord.PR_LNG,
                               PlateRecord.PR_NUMBER)
        if deviceNum:
            result = result.filter(PlateRecord.PR_DEVICE_NUMBER == deviceNum)
        if startTime:
            result = result.filter(PlateRecord.CREATE_TIME >= startTime)
        if endTime:
            result = result.filter(PlateRecord.CREATE_TIME <= endTime)
        if plateNum:
            result = result.filter(PlateRecord.PR_NUMBER.like('%' + plateNum + '%'))
        data = result.order_by(PlateRecord.CREATE_TIME.desc()).limit(pageSize).offset(
            (int(pageIndex) - 1) * int(pageSize))
        arry = []
        for row in data:
            platerecord = {}
            platerecord["prBigimageUrl"] = row[0]
            platerecord["prImageUrl"] = row[1]
            platerecord["prDeviceNumber"] = row[2]
            platerecord["createTime"] = row[3]
            platerecord["prLat"] = row[4]
            platerecord["prLng"] = row[5]
            platerecord["prNumber"] = row[6]
            arry.append(platerecord)
        print
        len(arry)
        session.close()
        return arry

    def plateSelectById(self, id):
        session = DBSession()
        result = session.query(PlateRecord.PR_BIG_IMAGEURL,
                               PlateRecord.PR_IMAGEURL,
                               PlateRecord.PR_DEVICE_NUMBER,
                               PlateRecord.CREATE_TIME,
                               PlateRecord.PR_LAT,
                               PlateRecord.PR_LNG,
                               PlateRecord.PR_NUMBER)
        if id:
            result = result.filter(PlateRecord.ID == id).first()
            platerecord = {}
            platerecord["prBigimageUrl"] = result[0]
            platerecord["prImageUrl"] = result[1]
            platerecord["prDeviceNumber"] = result[2]
            platerecord["createTime"] = result[3]
            platerecord["prLat"] = result[4]
            platerecord["prLng"] = result[5]
            platerecord["prNumber"] = result[6]

        session.close()
        return platerecord


'''
人脸黑名单类
'''


class FaceBlackThread(threading.Thread):
    '''
    获取人脸黑名单记录(分页查询)
    '''

    def selectAllPage(self, pageSize=None, pageIndex=None, name=None, phone=None):
        session = DBSession()
        result = session.query(FaceBlack)
        if name:
            result = result.filter(FaceBlack.FB_NAME.like('%' + name + '%'))
        if phone:
            result = result.filter(FaceBlack.FB_PHONE.like('%' + phone + '%'))

        result = result.filter(not_(FaceBlack.FB_LOCALIMAGEURL == None))
        data = result.limit(pageSize).offset((int(pageIndex) - 1) * int(pageSize))
        resultList = []
        for faceblack in data:
            resultData = {}
            resultData['id'] = faceblack.ID
            resultData['fbImageUrl'] = faceblack.FB_LOCALIMAGEURL
            resultData['fbName'] = faceblack.FB_NAME
            resultData['fbAge'] = faceblack.FB_AGE
            resultData['fbSex'] = faceblack.FB_SEX
            resultData['fbZjNum'] = faceblack.FB_ZJ_NUM
            resultData['fbPhone'] = faceblack.FB_PHONE
            resultData['fbNote'] = faceblack.FB_NOTE
            # resultData['fbWebId'] = faceblack.FB_WEBID
            resultList.append(resultData)
        print
        len(resultList)
        session.close()
        return resultList

    '''
     翟
     2020 04 27
     获取人脸黑名单全部数据
     '''

    def selectData(self):
        session = DBSession()
        dataList = session.query(FaceBlack)
        dataList = dataList.filter(FaceBlack.FB_LOCALIMAGEURL.isnot(None))
        dataList = dataList.group_by(FaceBlack.FB_ZJ_NUM).all()
        imgList = []
        for faceblack in dataList:
            resultData = {}
            resultData['fbId'] = faceblack.ID
            # if did.isOnline == 0:
            resultData['fbImageUrl'] = faceblack.FB_LOCALIMAGEURL
            # else:
            #     resultData['fbImageUrl'] = faceblack.FB_IMAGEURL
            # resultData['fbImageUrl'] = faceblack.FB_IMAGEURL
            resultData['fbName'] = faceblack.FB_NAME
            resultData['fbAge'] = faceblack.FB_AGE
            resultData['fbSex'] = faceblack.FB_SEX
            resultData['fbZjNum'] = faceblack.FB_ZJ_NUM
            resultData['fbPhone'] = faceblack.FB_PHONE
            resultData['fbNote'] = faceblack.FB_NOTE
            resultData['faceft128'] = faceblack.FACEFT_128
            # resultData['fbWebId'] = faceblack.FB_WEBID
            imgList.append(resultData)
        session.close()
        return imgList

    '''
    增加单个人脸黑名单
    '''

    def insertOneBlack(self, faceBlack):
        session = DBSession()
        age = 0
        name = None
        fbNote = None
        fbImageurl = ''
        sex = 1
        phone = None
        zjNum = None
        # name = base64.b64decode()
        if 'fbZjNum' in faceBlack:
            zjNum = faceBlack['fbZjNum']
        if 'fbName' in faceBlack:
            name = faceBlack['fbName']
        if 'fbNote' in faceBlack:
            fbNote = faceBlack['fbNote']
        if 'fbAge' in faceBlack:
            age = faceBlack['fbAge']
        if 'fbImageurl' in faceBlack:
            fbImageurl = faceBlack['fbImageurl']
        if 'fbSex' in faceBlack:
            sex = faceBlack['fbSex']
        if 'fbPhone' in faceBlack:
            phone = faceBlack['fbPhone']
        if 'faceft128' in faceBlack:
            faceft128 = faceBlack['faceft128']
        faceBlackParams = FaceBlack(FB_IMAGEURL=None, FB_NAME=name,
                                    FB_AGE=age, FB_SEX=sex, FB_ZJ_NUM=zjNum,
                                    FB_PHONE=phone, FB_NOTE=fbNote, ISDEL=0, FACEFT_128=faceft128,
                                    FB_LOCALIMAGEURL=fbImageurl)
        session.add(faceBlackParams)
        session.commit()
        # faceBlackParams.FB_WEBID = faceBlackParams.id
        session.commit()
        session.close()

        '''
        修改
        '''

    def updateFaceBlack(self, faceInfo):
        session = DBSession()
        if faceInfo != None:
            fbId = faceInfo['fbId']
            result = session.query(FaceBlack).filter_by(ID=fbId).first()
            if result != None:
                if 'fbImageUrl' in faceInfo and faceInfo['fbImageUrl'] != None:
                    result.FB_IMAGEURL = faceInfo['fbImageUrl']
                if 'faceft128' in faceInfo and faceInfo['faceft128'] != None:
                    result.faceft128 = faceInfo['faceft128']
                if 'fbName' in faceInfo and faceInfo['fbName'] != None:
                    result.FB_NAME = faceInfo['fbName']
                    print(result.FB_NAME)
                if 'fbAge' in faceInfo and faceInfo['fbAge'] != None:
                    result.FB_AGE = faceInfo['fbAge']
                if 'fbSex' in faceInfo and faceInfo['fbSex'] != None:
                    result.FB_SEX = faceInfo['fbSex']
                if 'fbZjNum' in faceInfo and faceInfo['fbZjNum'] != None:
                    result.FB_ZJ_NUM = faceInfo['fbZjNum']
                if 'fbPhone' in faceInfo and faceInfo['fbPhone'] != None:
                    result.FB_PHONE = faceInfo['fbPhone']
                if 'fbNote' in faceInfo and faceInfo['fbNote'] != None:
                    result.FB_NOTE = faceInfo['fbNote'].decode('utf8')
            session.commit()
        session.close()

    '''
    删除
    '''

    def deleteFaceBlackInfo(self, fbId):
        session = DBSession()
        session.query(FaceBlack).filter_by(ID=fbId).delete(synchronize_session=False)
        session.commit()
        session.close()


'''
车牌黑名单类
'''


class PlateBlackThread(threading.Thread):

    def selectAllPage(self, pageSize=None, pageIndex=None, name=None, phone=None, carNum=None, carFlag=None):
        session = DBSession()
        result = session.query(PlateBlack)
        if name:
            result = result.filter(PlateBlack.PB_OWNER_NAME.like('%' + name + '%'))
        if phone:
            result = result.filter(PlateBlack.PB_OWNER_PHONE.like('%' + phone + '%'))
        if carNum:
            result = result.filter(PlateBlack.PB_NUMBER.like('%' + carNum + '%'))
        if carFlag:
            result = result.filter(PlateBlack.PB_LOGO.like('%' + carFlag + '%'))

        dataList = result.filter(PlateBlack.ISONLINE == 1).limit(pageSize).offset((int(pageIndex) - 1) * int(pageSize))
        resultList = []
        for plateBlack in dataList:
            resultData = {}
            resultData['id'] = plateBlack.ID
            resultData['pbNumber'] = plateBlack.PB_NUMBER
            resultData['pbLogo'] = plateBlack.PB_LOGO
            resultData['pbOwnerName'] = plateBlack.PB_OWNER_NAME
            resultData['pbOwnerPhone'] = plateBlack.PB_OWNER_PHONE
            resultData['pbNote'] = plateBlack.PB_NOTE
            resultData['createTime'] = plateBlack.CREATE_TIME
            # resultData['pbWebId'] = plateBlack.PB_WEBID
            resultList.append(resultData)
        print
        len(resultList)
        session.close()
        return resultList

    def insertPlateBlackInfo(self, plateBlack):
        session = DBSession()
        if plateBlack != None:
            vbNumber = None
            vbLogo = None
            vbColor = None
            vbOwnerName = None
            vbOwnerPhone = None
            vbNote = None
            if 'vbNumber' in plateBlack and plateBlack['vbNumber'] != None:
                vbNumber = plateBlack['vbNumber'].decode('utf8')
            if 'vbLogo' in plateBlack and plateBlack['vbLogo'] != None:
                vbLogo = plateBlack['vbLogo'].decode('utf8')
            if 'vbColor' in plateBlack and plateBlack['vbColor'] != None:
                vbColor = plateBlack['vbColor'].decode('utf8')
            if 'vbOwnerName' in plateBlack and plateBlack['vbOwnerName'] != None:
                vbOwnerName = plateBlack['vbOwnerName']
            if 'vbOwnerPhone' in plateBlack and plateBlack['vbOwnerPhone'] != None:
                vbOwnerPhone = plateBlack['vbOwnerPhone']
            if 'vbNote' in plateBlack and plateBlack['vbNote'] != None:
                vbNote = plateBlack['vbNote'].decode('utf8')
            plateParams = PlateBlack(PB_NUMBER=vbNumber, PB_LOGO=vbLogo, PB_COLOR=vbColor, PB_OWNER_NAME=vbOwnerName,
                                     PB_OWNER_PHONE=vbOwnerPhone, PB_NOTE=vbNote, ISDEL=0, ISONLINE=0)
            session.add(plateParams)
            session.commit()
            # plateParams.PB_WEBID = plateParams.PB_ID
            session.commit()
        session.close()

    def selectAll(self):
        session = DBSession()
        result = session.query(PlateBlack)
        resultList = []
        for plateBlack in result:
            resultData = {}
            resultData['pbId'] = plateBlack.ID
            resultData['pbNumber'] = plateBlack.PB_NUMBER
            resultData['pbLogo'] = plateBlack.PB_LOGO
            resultData['pbOwnerName'] = plateBlack.PB_OWNER_NAME
            resultData['pbOwnerPhone'] = plateBlack.PB_OWNER_PHONE
            resultData['pbNote'] = plateBlack.PB_NOTE
            resultData['createTime'] = plateBlack.CREATE_TIME
            # resultData['pbWebId'] = plateBlack.PB_WEBID
            resultList.append(resultData)
        print
        len(resultList)
        session.close()
        return resultList

    def updatePlateBlack(self, plateBlack):
        session = DBSession()
        if plateBlack != None:
            vbId = plateBlack['vbId']
            result = session.query(PlateBlack).filter_by(ID=vbId).first()
            if result != None:
                if 'vbNumber' in plateBlack and plateBlack['vbNumber'] != None:
                    result.PB_NUMBER = plateBlack['vbNumber'].decode('utf8')
                if 'vbLogo' in plateBlack and plateBlack['vbLogo'] != None:
                    result.PB_LOGO = plateBlack['vbLogo'].decode('utf8')
                if 'vbColor' in plateBlack and plateBlack['vbColor'] != None:
                    result.PB_COLOR = plateBlack['vbColor'].decode('utf8')
                if 'vbOwnerName' in plateBlack and plateBlack['vbOwnerName'] != None:
                    result.PB_OWNER_NAME = plateBlack['vbOwnerName']
                if 'vbOwnerPhone' in plateBlack and plateBlack['vbOwnerPhone'] != None:
                    result.PB_OWNER_PHONE = plateBlack['vbOwnerPhone']
                if 'vbNote' in plateBlack and plateBlack['vbNote'] != None:
                    result.PB_NOTE = plateBlack['vbNote'].decode('utf8')
            session.commit()
        session.close()

    def deletePlateBlackInfo(self, vbId):
        session = DBSession()
        session.query(PlateBlack).filter_by(ID=vbId).delete(synchronize_session=False)
        session.commit()
        session.close()

    def deletePlateBlack(self):
        session = DBSession()
        session.query(PlateBlack).filter(PlateBlack.ISONLINE == 1).delete(synchronize_session=False)
        session.commit()
        session.close()


class FaceWarningThread(threading.Thread):
    '''
    人脸预警添加
    '''

    def insert(self, frid, rbzjnum, contrast):
        session = DBSession()
        new_state = FaceWarning(FRID=frid, FW_FBZJNUM=rbzjnum, CREATE_TIME=getNowTime(), ISDEL=0,
                                CONTRAST=contrast)
        session.add(new_state)
        session.commit()
        fwId = new_state.ID
        session.close()
        return fwId

    def select(self, startTime, endTime):
        session = DBSession()
        result = session.query(FaceWarning.CREATE_TIME,
                               FaceRecord.FR_IMAGEURL,
                               FaceRecord.FR_BIG_IMAGEURL,
                               FaceRecord.FR_DEVICE_NUMBER,
                               FaceBlack.FB_NAME,
                               FaceBlack.FB_AGE,
                               FaceBlack.FB_SEX,
                               FaceBlack.FB_ZJ_NUM,
                               FaceBlack.FB_IMAGEURL,
                               FaceBlack.FB_PHONE,
                               FaceBlack.FB_NOTE,
                               FaceBlack.FB_LOCALIMAGEURL,
                               # Device.DEVICE_NAME,
                               FaceRecord.FR_LAT,
                               FaceRecord.FR_LNG,
                               FaceWarning.CONTRAST).filter(FaceWarning.FRID == FaceRecord.ID,
                                                            FaceWarning.FW_FBZJNUM == FaceBlack.FB_ZJ_NUM,
                                                            FaceWarning.CREATE_TIME.between(startTime,
                                                                                            endTime)
                                                            # Device.DEVICE_NUMBER == FaceRecord.FR_DEVICE_NUMBER
                                                            ).group_by(
            FaceRecord.ID).order_by(
            FaceWarning.CREATE_TIME.desc())
        print
        result
        arr = []
        for row in result:
            face = {}
            face['createTime'] = row.CREATE_TIME
            face['frImageUrl'] = row.FR_IMAGEURL
            face['frBigImageUrl'] = row.FR_BIG_IMAGEURL
            face['frDeviceNumber'] = row.FR_DEVICE_NUMBER
            face['fbName'] = row.FB_NAME
            face['fbAge'] = row.FB_AGE
            face['fbSex'] = row.FB_SEX
            face['fbZjNum'] = row.FB_ZJ_NUM
            face['fbImageUrl'] = row.FB_LOCALIMAGEURL
            face['fbNote'] = row.FB_NOTE
            face['fbPhone'] = row.FB_PHONE
            # face['fDeviceName'] = row.DEVICE_NAME
            face['frLat'] = row.FR_LAT
            face['frLng'] = row.FR_LNG
            if row.CONTRAST > 0.7:
                face['contrast'] = 100
            elif row.CONTRAST < 0.4:
                face['contrast'] = 60
            else:
                face['contrast'] = row.CONTRAST
            arr.append(face)
        # print arr
        session.close()
        return arr

    def selects(self, startTime=None, endTime=None, pageSize=None, pageIndex=None, name=None, phone=None):
        session = DBSession()
        result = session.query(FaceWarning.CREATE_TIME,
                               FaceRecord.FR_IMAGEURL,
                               FaceRecord.FR_BIG_IMAGEURL,
                               FaceRecord.FR_DEVICE_NUMBER,
                               FaceBlack.FB_NAME,
                               FaceBlack.FB_AGE,
                               FaceBlack.FB_SEX,
                               FaceBlack.FB_ZJ_NUM,
                               FaceBlack.FB_IMAGEURL,
                               FaceBlack.FB_PHONE,
                               FaceBlack.FB_NOTE,
                               FaceBlack.FB_LOCALIMAGEURL,
                               # Device.DEVICE_NAME,
                               FaceRecord.FR_LAT,
                               FaceRecord.FR_LNG,
                               FaceWarning.CONTRAST)
        if startTime:  # !=None and startTime != ''
            result = result.filter(FaceWarning.CREATE_TIME >= startTime)  # .order_by(FaceWarning.CREATE_TIME.desc())
        if endTime:  # !=None and endTime != ''
            result = result.filter(FaceWarning.CREATE_TIME <= endTime)  # .order_by(FaceWarning.CREATE_TIME.asc())
        if name:  # !=None and name != ''
            result = result.filter(FaceBlack.FB_NAME.like('%' + name + '%'))
        if phone:  # !=None and phone != ''
            result = result.filter(FaceBlack.FB_PHONE.like('%' + phone + '%'))

        data = result.filter(FaceWarning.FRID == FaceRecord.ID, FaceWarning.FW_FBZJNUM == FaceBlack.FB_ZJ_NUM
                             # Device.DEVICE_NUMBER == FaceRecord.FR_DEVICE_NUMBER
                             ).group_by(FaceRecord.ID).order_by(
            FaceWarning.CREATE_TIME.desc()).limit(pageSize).offset((int(pageIndex) - 1) * int(pageSize))
        print(data)
        arr = []
        for row in data:
            face = {}
            face['createTime'] = row.CREATE_TIME
            face['frImageUrl'] = row.FR_IMAGEURL
            face['frBigImageUrl'] = row.FR_BIG_IMAGEURL
            face['frDeviceNumber'] = row.FR_DEVICE_NUMBER
            face['fbName'] = row.FB_NAME
            face['fbAge'] = row.FB_AGE
            face['fbSex'] = row.FB_SEX
            face['fbZjNum'] = row.FB_ZJ_NUM
            face['fbImageUrl'] = row.FB_IMAGEURL
            face['fbNote'] = row.FB_NOTE
            face['fbPhone'] = row.FB_PHONE
            face['fDeviceName'] = row.DEVICE_NAME
            face['frLat'] = row.FR_LAT
            face['frLng'] = row.FR_LNG
            if row.CONTRAST > 0.7:
                face['contrast'] = 100
            elif row.CONTRAST < 0.4:
                face['contrast'] = 60
            else:
                face['contrast'] = row.CONTRAST
            arr.append(face)
        # print arr
        session.close()
        return arr

    def getCurrectTimeWarnCount(self, startTime, endTime):
        session = DBSession()
        count = session.query(FaceWarning).filter(FaceWarning.FW_FBZJNUM == FaceBlack.FB_ZJ_NUM,
                                                  # FaceRecord.FR_DEVICE_NUMBER == Device.DEVICE_NUMBER,
                                                  FaceWarning.FRID == FaceRecord.ID,
                                                  FaceWarning.CREATE_TIME.between(startTime, endTime),
                                                  ).group_by(
            FaceRecord.ID).count()
        session.close()
        return count


class PlateWarningThread(threading.Thread):
    '''
    车牌预警添加
    '''

    def insert(self, prid, pbnumber):
        session = DBSession()
        # pbnumber = unicode(pbnumber, "utf-8")
        pbnumber = pbnumber
        new_state = PlateWarning(PRID=prid, PW_PBNUMBER=pbnumber, CREATE_TIME=getNowTime(), ISDEL=0)
        session.add(new_state)
        session.commit()
        session.close()

    '''
    预警
    '''

    def select(self, startTime, endTime):
        session = DBSession()
        result = session.query(PlateWarning.CREATE_TIME,
                               PlateRecord.PR_IMAGEURL,
                               PlateRecord.PR_BIG_IMAGEURL,
                               PlateRecord.PR_NUMBER,
                               PlateRecord.PR_COLOR,
                               PlateRecord.PR_DEVICE_NUMBER,
                               PlateRecord.PR_LOGO,
                               PlateRecord.PR_LAT,
                               PlateRecord.PR_LNG,
                               PlateBlack.PB_NOTE,
                               PlateBlack.PB_OWNER_NAME,
                               PlateBlack.PB_OWNER_PHONE
                               # Device.DEVICE_NAME
                               ).filter(PlateWarning.PW_PBNUMBER == PlateBlack.PB_NUMBER,
                                        PlateWarning.CREATE_TIME.between(startTime, endTime),
                                        # Device.DEVICE_NUMBER == PlateRecord.PR_DEVICE_NUMBER,
                                        PlateBlack.ISONLINE == 1).order_by(
            PlateWarning.CREATE_TIME.desc()).limit(5)
        print(result)
        arry = []
        for row in result:
            plate = {}
            plate["createTime"] = row.CREATE_TIME
            plate["prImageUrl"] = row.PR_IMAGEURL
            plate["prBigImageUrl"] = row.PR_BIG_IMAGEURL
            plate["prNumber"] = row.PR_NUMBER
            plate["prColor"] = row.PR_COLOR
            plate["prDeviceNumber"] = row.PR_DEVICE_NUMBER
            plate["prLogo"] = row.PR_LOGO
            plate["pbNote"] = row.PB_NOTE
            # plate["pDeviceName"] = row.DEVICE_NAME
            plate["pbOwnerName"] = row.PB_OWNER_NAME.decode('utf8')
            plate["pbOwnerPhone"] = row.PB_OWNER_PHONE
            plate["prLat"] = row.PR_LAT
            plate["prLng"] = row.PR_LNG
            arry.append(plate)
        # print('-----------------------------')
        # print(json.dumps(arry))
        # print('-----------------------------')
        session.close()
        return arry

    def selects(self, startTime=None, endTime=None, pageSize=None, pageIndex=None, name=None, phone=None):
        session = DBSession()
        result = session.query(PlateWarning.CREATE_TIME,
                               PlateRecord.PR_IMAGEURL,
                               PlateRecord.PR_BIG_IMAGEURL,
                               PlateRecord.PR_NUMBER,
                               PlateRecord.PR_COLOR,
                               PlateRecord.PR_DEVICE_NUMBER,
                               PlateRecord.PR_LOGO,
                               PlateRecord.PR_LAT,
                               PlateRecord.PR_LNG,
                               PlateBlack.PB_NOTE,
                               PlateBlack.PB_OWNER_NAME,
                               PlateBlack.PB_OWNER_PHONE)
        if startTime:
            result = result.filter(PlateWarning.CREATE_TIME >= startTime)
        if endTime:
            result = result.filter(PlateWarning.CREATE_TIME <= endTime)
        if name:
            result = result.filter(PlateBlack.PB_OWNER_NAME.like('%' + name + '%'))
        if phone:
            result = result.filter(PlateBlack.PB_OWNER_PHONE.like('%' + phone + '%'))
        data = result.filter(PlateWarning.PW_PBNUMBER == PlateBlack.PB_NUMBER,
                             # Device.DEVICE_NUMBER == PlateRecord.PR_DEVICE_NUMBER,
                             ).order_by(
            PlateWarning.CREATE_TIME.desc()).limit(pageSize).offset((int(pageIndex) - 1) * int(pageSize))
        arry = []
        for row in data:
            plate = {}
            plate["createTime"] = row.CREATE_TIME
            plate["prImageUrl"] = row.PR_IMAGEURL
            plate["prBigImageUrl"] = row.PR_BIG_IMAGEURL
            plate["prNumber"] = row.PR_NUMBER
            plate["prColor"] = row.PR_COLOR
            plate["prDeviceNumber"] = row.PR_DEVICE_NUMBER
            plate["prLogo"] = row.PR_LOGO
            plate["pbNote"] = row.PB_NOTE
            # plate["pDeviceName"] = row.DEVICE_NAME
            plate["pbOwnerName"] = row.PB_OWNER_NAME
            plate["pbOwnerPhone"] = row.PB_OWNER_PHONE
            plate["prLat"] = row.PR_LAT
            plate["prLng"] = row.PR_LNG
            arry.append(plate)
        # print('-----------------------------')
        # print(json.dumps(arry))
        # print('-----------------------------')
        session.close()
        return arry

    def getCurrectTimeCount(self, startTime, endTime):
        session = DBSession()
        count = session.query(PlateWarning).filter(PlateWarning.PW_PBNUMBER == PlateBlack.PB_NUMBER,
                                                   # PlateRecord.PR_DEVICE_NUMBER == Device.DEVICE_NUMBER,
                                                   # PlateRecord.PR_ID == PlateWarning.PW_PRID,
                                                   PlateWarning.CREATE_TIME.between(startTime, endTime),
                                                   PlateBlack.ISONLINE == 1).count()
        print(str(count))
        # print('-----------------------------')
        # print(json.dumps(arry))
        # print('-----------------------------')
        session.close()
        return count


def getNowTime():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def getUUID():
    return str(uuid.uuid1())
