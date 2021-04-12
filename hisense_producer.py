import stomp

def send_to_topic(msg):
    try:
        conn = stomp.Connection10([(localhost, 61613)],auto_content_length=False)
        conn.start()
        conn.connect()
        conn.send('/topic/xxxx', msg)
        conn.disconnect()
        return 1
    except Exception as e:
        # logging.error(f"send message with activemq failed, error is:{e}")
        return 0
