from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from message_port_app.models import Message
from .serializers import MessageSerializer
from rest_framework.decorators import detail_route
import os
from django.conf import settings
from django.http import HttpResponse
from rest_framework.decorators import api_view

@api_view(['GET'])
def api_root(request, format=None):
    """
    The entry endpoint of our API.
    """
    return Response({
        'users': '123',
    })

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @detail_route(methods=['post'])
    def lock_message(self, request):
        # print('lock_message')
        # model = MLModel.objects.get(pk=pk)
        # model.deploy()
        return Response(status.HTTP_200_OK)

    @detail_route(methods=['get'])
    def get_config(self, request):
        # model = MLModel.objects.get(pk=pk)
        # config = model.config
        return Response(data='{}', status=status.HTTP_200_OK)


