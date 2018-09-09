from rest_framework import status
from rest_framework import viewsets

from hard_port.arduino_client import ArduinoClient
from message_port_app.etherium.eth_worker import EthWorker
from message_port_app.models import Message
from .serializers import MessageSerializer
from rest_framework.decorators import detail_route
from rest_framework.decorators import action
from rest_framework.response import Response
import json
import os
from django.conf import settings
from django.http import HttpResponse
from rest_framework.decorators import api_view

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @action(methods=['put'], detail=True)
    def create_eth_bargain(self, request, pk=None):
        user = self.get_object()
        serializer = MessageSerializer(data=request.data)
        print('request.data '+ str(request.data))
        if serializer.is_valid():
            print('request.data is valid' )
            instance = request.data
            print('instance ' + str(instance))
            if (instance['type'] == Message.FROM_USER_MESSAGE):
                message_text = instance['text']
                data = json.loads(message_text)
                if data['theme'] == 'NEW_BARGAIN':
                    bargain_id = data['bargain_id']
                    yahsik_address = EthWorker.save_bargain_id_and_gen_addr(bargain_id)
                    return Response({'box_address': yahsik_address})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def unlock_message(self, request, pk=None):
        ArduinoClient.init()
        ArduinoClient.unlock()
        return Response(status.HTTP_200_OK)