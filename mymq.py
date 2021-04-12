"""
    activeMq
"""
import stomp

# from cs_police import logger
"""
2020-12-28 11:55:42,442 - stomp.py - INFO - Attempting connection to host 43.5.18.2, port 61616
2020-12-28 11:55:42,448 - stomp.py - INFO - Established connection to host 43.5.18.2, port 61616
2020-12-28 11:55:42,453 - stomp.py - INFO - Starting receiver loop
2020-12-28 11:55:42,454 - stomp.py - WARNING - Unknown response frame type: '�activemq' (frame length was 10)
2020-12-28 11:55:42,454 - stomp.py - WARNING - Unknown response frame type: '' (frame length was 1)
2020-12-28 11:55:42,455 - stomp.py - WARNING - Unknown response frame type: '�' (frame length was 1)
2020-12-28 11:55:42,455 - stomp.py - WARNING - Unknown response frame type: '	' (frame length was 1)
2020-12-28 11:55:42,456 - stomp.py - WARNING - Unknown response frame type: 'maxframesize�������' (frame length was 22)
2020-12-28 11:55:42,456 - stomp.py - WARNING - Unknown response frame type: '	cachesize' (frame length was 11)
2020-12-28 11:55:42,457 - stomp.py - WARNING - Unknown response frame type: '' (frame length was 1)
2020-12-28 11:55:42,457 - stomp.py - WARNING - Unknown response frame type: 'cacheenabled' (frame length was 15)
2020-12-28 11:55:42,458 - stomp.py - WARNING - Unknown response frame type: 'sizeprefixdisabled' (frame length was 20)
2020-12-28 11:55:42,458 - stomp.py - WARNING - Unknown response frame type: ' maxinactivitydurationinitaldelay' (frame length was 34)
2020-12-28 11:55:42,459 - stomp.py - WARNING - Unknown response frame type: ''' (frame length was 2)
2020-12-28 11:55:42,459 - stomp.py - WARNING - Unknown response frame type: 'tcpnodelayenabled' (frame length was 20)
2020-12-28 11:55:42,460 - stomp.py - WARNING - Unknown response frame type: 'maxinactivityduration' (frame length was 23)
2020-12-28 11:55:42,460 - stomp.py - WARNING - Unknown response frame type: 'u0' (frame length was 2)
2020-12-28 11:55:42,461 - stomp.py - WARNING - Unknown response frame type: 'tightencodingenabled' (frame length was 23)
2020-12-28 11:55:42,463 - stomp.py - INFO - Sending frame: 'CONNECT'
2020-12-28 11:55:42,472 - stomp.py - INFO - Receiver loop ended

Process finished with exit code -1

"""


class MyMq:

    def __init__(self):
        try:
            self.conn = stomp.Connection10([("120.92.107.97", 61613)], auto_content_length=False)
            # self.conn.start()
            self.conn.connect('admin', 'admin')
            print('mq2连接上了')
        except Exception as e:
            # # logger.info('mq2连接失败：{}'.format(e))
            # self.conn = stomp.Connection10([("43.5.18.3", 61616)], auto_content_length=False)
            # # self.conn.start()
            # self.conn.connect('cshiatmp', 'cshiatmp')
            print('mq3连接上了')
            print('连接失败')

    def send_to_wf_topic(self, wf_msg):
        print('开始发送：{}'.format(wf_msg))
        try:
            self.conn.send('/topic/test1', wf_msg)
            # logger.info('发送成功')
            # logger.info('发送成功')
            print('发送成功')
            return 1
        except Exception as e:
            print('错误')
            # logger.info('错误')
            # logger.info(e)
            return 0

    def send_to_kk_topic(self, kk_msg):
        try:
            # print('开始连接')
            # conn = stomp.Connection10([("43.5.18.2", 61616)])
            # # conn.start()
            # conn.connect('cshiatmp', 'cshiatmp')
            # print('开始发送卡口数据')
            self.conn.send('/topic/HIATMP.HISENSE.PASS.PASSINF', kk_msg)
            print('发送卡口数据成功')
            # logger.info('发送卡口数据成功')
            return 1
        except Exception as e:
            print('发送卡口数据失败{}'.format(e))
            # logger.warning('发送卡口数据失败{}'.format(e))
            # logging.error(f"send message with activemq failed, error is:{e}")
            return 0

    def close(self):
        self.conn.disconnect()


kk_data = """VMKS,2.4,0099,103df1f248b611eb9e75f3886d352d64,02,鄂A788DG,99,630001307000,湘江路与高冲路交叉路口,2,430106000000010140,,,2020-12-26 15:52:24,430100000000,,ftp://test1:test1@43.5.169.242:21/20201227/1545/20201226_155224125_imageMix.jpg,,,,,01,,,20201228 10:40:37,,,,0,0,0,0,0,0,0"""

mymq = MyMq()
mymq.send_to_kk_topic(kk_data)
