from rest_framework import serializers
from message_port_app.models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        #fields = '__all__'
        fields = ('id', 'sender_address', 'reciever_address', 'text', 'date_created', 'type')
        read_only_fields = ('id', 'date_created')

        def create(self, validated_data):
            """
            Create and return a new `Message` instance, given the validated data.
            """
            return Message.objects.create(**validated_data)