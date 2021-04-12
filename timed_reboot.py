import os
import time


def timed_reboot(timed):
    time.sleep(timed)
    cmd = "reboot"
    password = "aaeon"
    os.system('echo %s|sudo -S %s' % (password, cmd))


timed_reboot(3)
