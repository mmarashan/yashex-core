from django.db import models
from django.utils import timezone

# Create your models here.
class Message(models.Model):
    sender_address = models.TextField()
    reciever_address = models.TextField()
    text = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)

    FROM_YASHIK_MESSAGE = 'FROM_YASHIK_MESSAGE'
    FROM_USER_MESSAGE = 'FROM_USER_MESSAGE'

    MESSAGE_TYPES = (
        (FROM_YASHIK_MESSAGE, 'Сообщение от ящика'),
        (FROM_USER_MESSAGE, 'Сообщение от пользователя')
    )

    type = models.CharField(max_length=64, choices=MESSAGE_TYPES, null=True, blank=True)


    def __str__(self):
        return '{}-{}-{}'.format(self.sender_address, self.type, self.text)

    def create_message(sender_address, reciever_address, text, type):
        arduino_message = Message.objects.create()
        arduino_message.sender_address = sender_address
        arduino_message.sender_address = reciever_address
        arduino_message.text = text
        arduino_message.type = type
        arduino_message.save()
        print("Add new message from "+ sender_address + ' : '+text)