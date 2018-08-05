import serial.tools.list_ports
import time
import sys
import glob

class ArduinoClient():
    serial_port = None

    def get_arduino_serial(self):
        ports = list(serial.tools.list_ports.comports())
        print(ports)

        for p in ports:
            #print(p[1])
            #if "Arduino" in p[1]:
            if p[1]:
                ser = serial.Serial(p[0], 9600, dsrdtr=False, timeout=2.0, rtscts=True, xonxoff=False)
                return ser
            else:
                print("No Arduino Device was found connected to the computer")

    def init(self):
        self.serial_port = self.get_arduino_serial()
        # sudo chown maxim /dev/ttyACM0
        # sudo ln - s /dev/ttyACM0 /dev/ ttyUSB0

    def read(self, byte_count):
        i = 0
        text = ''
        while (i < byte_count):
            text = text+self.serial_port.read().decode("utf-8")
            i = i + 1
        return text

    def write(self, str):
        self.serial_port.write(str)