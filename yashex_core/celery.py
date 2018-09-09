# quick_publisher/celery.py
import os
from celery import Celery
import time

from ddns.ddns_sender import DdnsSetter
from hard_port.arduino_client import ArduinoClient
from message_port_app.etherium.eth_worker import EthWorker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yashex_core.settings')

celery_app = Celery('yashex_core')
celery_app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
celery_app.autodiscover_tasks()

# run celery periodic task with yashik listening
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls every 10 seconds.
    print('setup_periodic_celety_tasks')
    sender.add_periodic_task(600.0, read_yashik_message.s(None), name='set_ddns_url')
    sender.add_periodic_task(60.0, read_yashik_message.s(None), name='read_yashik_message')
    sender.add_periodic_task(10.0, read_yashik_message.s(None), name='check_bargains_status')

@celery_app.task
def read_yashik_message(args):
    ArduinoClient.init()
    time.sleep(10)
    result = ArduinoClient.read()
    #import re
    #result = re.split(r',', result)[0]
    print('Read from arduino : ' + result)
    from message_port_app.models import Message
    if result != '':
        print('Create message : ' + result)
        Message.create_message('arduino', '-', result, Message.FROM_YASHIK_MESSAGE)
        EthWorker.init_contract()
        print("OK init ETHContract")
        EthWorker.addHistoryItem(result)

@celery_app.task
def set_ddns_url(args):
    ddns_setter = DdnsSetter()
    ddns_setter.set_ddns_url()

@celery_app.task
def check_bargains_status(args):
    EthWorker.init_contract()
    print("check_bargains_status: OK init ETHContract")
    contract_state = EthWorker.getBargainStateById()
    print("check_bargains_status contract_state :" + str(contract_state))
    if (contract_state == 'True'):
        ArduinoClient.unlock()