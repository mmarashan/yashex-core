#!/usr/bin/env python

# Внешний клиентский цикл - читает core и генерирует внешние события
# Работает не в Докере!
import time

from client.rest_client import CoreClient, CloudClient
import json

from client.screen import ScreenFace

from hard_port.arduino_client import ArduinoClient

lb=ScreenFace('SberSmartHome')

def read_message():
    ArduinoClient.init()
    result = ArduinoClient.read()
    print('Read message: ' + result)
    return result

def get_state():
    message = read_message()
    text = json.loads(message)
    state = text.get('state')
    print('State: '+state)
    return state

def read_fire_sensor_state():
    state = get_state()
    if state == 'ok':
        lb.set_text('Ты в безопасности','green')
    if state == 'fire':
        lb.set_text('Внимание! Сработал датчик дыма!','red')
    return state

def alert():
    CloudClient().fire_allert()

def main():
    while True:
        time.sleep(3)
        fire_sensor_state = read_fire_sensor_state()
        if fire_sensor_state == 'fire':
            print('Fire!')
            alert()
        else:
            pass

if __name__ == "__main__":
    main()