#!/usr/bin/env python

# Внешний клиентский цикл - читает core и генерирует внешние события
# Работает не в Докере!
import time

from rest_client import CoreClient, CloudClient
import json

from screen import ScreenFace

lb=ScreenFace('SberSmartHome')


#не работал докер, запускаем автономно без core
def get_fire_sensor_state():
    try:
        response = CoreClient.get_last_message()
        if response.status_code == 200:
            text = json.loads(response.json())['text']
            state = text.get('state')
            if state == 'ok':
                lb.set_text('Ты в безопасности','green')
            return state
    except Exception:
        print('Нет соединения с Core')
        lb.set_text('Установливаю соединение с Core', 'gray')

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