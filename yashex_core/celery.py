# quick_publisher/celery.py
import os
from celery import Celery

from hard_port.arduino_client import ArduinoClient

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yashex_core.settings')

celery_app = Celery('yashex_core')
celery_app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
celery_app.autodiscover_tasks()

# run celery periodic task with yashik liste
# ning
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls every 10 seconds.
    print('setup_periodic_celety_tasks')
    sender.add_periodic_task(10.0, read_yashik_message.s(None), name='read_yashik_message')

@celery_app.task
def read_yashik_message(args):
    ArduinoClient.init()
    ArduinoClient.write('sayState\n')
    result = ArduinoClient.read(100)
    #import re
    #result = re.split(r',', result)[0]
    print('Read from arduino : ' + result)

    from message_port_app.models import Message
    Message.create_message('arduino', '-', result, Message.FROM_YASHIK_MESSAGE)