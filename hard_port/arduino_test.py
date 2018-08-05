import os
from arduino_client import ArduinoClient

os.chmod("../media/", 0o777)
f = open("../media/guru99.txt", "a+")
arduino_client = ArduinoClient()
arduino_client.init()
i=0
while(i<20):
    result = arduino_client.read()
    print(str(result))
    f.write(str(result))
    i=i+1