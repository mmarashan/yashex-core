import os
from arduino_client import ArduinoClient
import time

os.chmod("../media/", 0o777)
f = open("../media/guru99.txt", "a+")
print('Try to init')
ArduinoClient.init()
time.sleep(5)
print('Try to unlock')
ArduinoClient.unlock()
time.sleep(5)
print('Try to sayState')
result = ArduinoClient.read()
print(str(result))
f.write(str(result))