from hard_port.serial import serialposix
from hard_port.serial.tools import list_ports_linux

class ArduinoClient():
    serial_port = None

    @staticmethod
    def get_arduino_serial():
        ports = list(list_ports_linux.comports())
        print(ports)

        for p in ports:
            if p[1]:
                print('Arduino on port : ' + p[1])
                ser = serialposix.Serial(p[0], 9600, timeout=0.01)
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
    def write(str):
        ArduinoClient.serial_port.write(str.encode())

    @staticmethod
    def unlock():
        ArduinoClient.write('unlock\n')

    @staticmethod
    def lock():
        ArduinoClient.write('lock\n')

    @staticmethod
    def read():
        ArduinoClient.write('sayState\n')
        i = 0
        text = ''
        end_message_symbol='}'
        current_symbol = ''
        while current_symbol != end_message_symbol:
            current_symbol = ArduinoClient.serial_port.read().decode("utf-8")
            text = text+current_symbol
            print('Read symbol : ' + current_symbol)
            i = i + 1
        return text