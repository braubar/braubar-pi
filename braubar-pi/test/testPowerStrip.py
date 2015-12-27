import time

from helper.powerstrip import PowerStrip

s = PowerStrip()

s.fetch_status()

# a = s.switch(PowerStrip.PLUG_1, PowerStrip.ON)
# print(a)
# a = s.switch(PowerStrip.PLUG_1, PowerStrip.OFF)
# print(a)
# print(s.status)
# time.sleep(1)
# s.logout()
# s.switch(PowerStrip.PLUG_2, PowerStrip.OFF)
# print(s.status)
