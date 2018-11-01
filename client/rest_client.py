#!/usr/bin/env python

import requests
import logging
import json

logging.basicConfig(level=logging.DEBUG)


def _cloud_url(path):
    cloud_url = 'http://192.168.1.1'
    return cloud_url + path

def _core_url(path):
    cloud_url = 'http://127.0.0.1:8000/api'
    return cloud_url + path

class CoreClient:
    @staticmethod
    def get_last_message():
        headers = {'Accept': '*/*',
                   'Content-Type':'application/json'}
        #data = {'count': '10'}
        response = requests.get(_core_url('/messages/0/last_message/'), headers = headers, data = None)
        return response

class CloudClient:
    @staticmethod
    def fire_allert():
        headers = {'Accept': '*/*',
                   'Content-Type':'application/json'}
        data = {'address': 'Shipilovskaya 32k1'}
        response = requests.get(_cloud_url('/house/device-status/'), headers = headers, data = data)
        return response

if __name__ == "__main__":


    response = CoreClient.get_last_message()
    if response.status_code == 200:
        print('Последие сообщения получены')
        print(response.json())
        text = json.loads(response.json())['text']
        state = text.get('state')
        print(state)