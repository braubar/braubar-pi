import time

from helper.steckdose import Steckdose

s = Steckdose()
a = s.switch(Steckdose.PLUG_1,Steckdose.ON)
print(a)
a = s.switch(Steckdose.PLUG_1,Steckdose.OFF)
print(a)
print(s.status)
time.sleep(1)
s.logout()
s.switch(Steckdose.PLUG_2,Steckdose.OFF)
print(s.status)

