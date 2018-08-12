import serial.tools.list_ports
import time
import sys
import glob

class ArduinoClient():
    serial_port = None

    @staticmethod
    def get_arduino_serial():
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

    @staticmethod
    def init():
        if ArduinoClient.serial_port is None:
            ArduinoClient.serial_port = ArduinoClient.get_arduino_serial()
            print('INIT ARDUINO CONNECTION')
        # sudo chown maxim /dev/ttyACM0
        # sudo ln - s /dev/ttyACM0 /dev/ttyACM0

    @staticmethod
    def read(byte_count):
        i = 0
        text = ''
        end_message_symbol='}'
        current_symbol = ''
        while (current_symbol != end_message_symbol):
            current_symbol = ArduinoClient.serial_port.read().decode("utf-8")
            print('Read symbol : '+current_symbol)
            text = text+current_symbol
            i = i + 1
        return text

    @staticmethod
    def write(str):
        ArduinoClient.serial_port.write(str.encode())