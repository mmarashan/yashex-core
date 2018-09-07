from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from message_port_app.models import Message
from .serializers import MessageSerializer
from rest_framework.decorators import detail_route
import os
from django.conf import settings
from django.http import HttpResponse


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(created_by=self.request.user)

    @detail_route(methods=['post'])
    def lock_message(self, request):
        print('lock_message')
        model = MLModel.objects.get(pk=pk)
        model.deploy()
        return Response(status.HTTP_200_OK)

    @detail_route(methods=['post'],  permission_classes=[ModelPermission])
    def remove_image(self, request, pk=None, project_pk=None):
        model = MLModel.objects.get(pk=pk)
        model.interrupt_deploy()
        return Response(status.HTTP_200_OK)

    @detail_route(methods=['get'],  permission_classes=[ModelPermission])
    def get_method_params(self, request, pk=None, project_pk=None):
        model = MLModel.objects.get(pk=pk)
        params = model.get_method_params()
        return Response(data =params, status=status.HTTP_200_OK)

    @detail_route(methods=['get'],  permission_classes=[ModelPermission])
    def get_config(self, request, pk=None, project_pk=None):
        model = MLModel.objects.get(pk=pk)
        config = model.config
        return Response(data=config, status=status.HTTP_200_OK)


