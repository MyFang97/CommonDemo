import os
import time

# 服务器定时重启
def timed_reboot(timed):
    time.sleep(timed)
    cmd = "reboot"
    password = "aaeon"
    os.system('echo %s|sudo -S %s' % (password, cmd))


timed_reboot(3)
