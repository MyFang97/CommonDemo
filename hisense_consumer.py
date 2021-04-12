# -*-coding:utf-8-*-
import stomp

__listener_name = 'SampleListener'
__topic_name1 = '/topic/FirstTopic'
__topic_name2 = '/topic/SecondTopic'
__host = '127.0.0.1'
__port = 61613
__user = 'manbuzhe'
__password = '20180725'


class SampleListener(object):

    def on_message(self, headers, message):
        print('每5秒发送一次')
        print('headers: %s' % headers['destination'])
        print('message: %s\n' % message)


## 从主题接收消息
def receive_from_topic():
    conn = stomp.Connection10([(__host, __port)])
    conn.set_listener(__listener_name, SampleListener())
    conn.start()
    conn.connect(__user, __password, wait=True)
    conn.subscribe(__topic_name1)
    conn.subscribe(__topic_name2)
    while True:
        pass
    conn.disconnect()


if __name__ == '__main__':
    receive_from_topic()
