from rest_framework import serializers
from message_port_app.models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        #fields = ('id', 'file', 'extract_path', 'created_at', 'created_by')
        #read_only_fields = ('id', 'extract_path', 'created_at', 'created_by')