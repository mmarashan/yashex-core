from rest_framework import serializers
from message_port_app.models import Message
from rest_framework.compat import unicode_to_repr


class CurrentProjectDefault(object):
    def set_context(self, serializer_field):
        self.message = Message.objects.get(pk=serializer_field.context['project_pk'])
    def __call__(self):
        return self.message
    def __repr__(self):
        return unicode_to_repr('%s()' % self.__class__.__name__)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'file', 'extract_path', 'created_at', 'created_by')
        read_only_fields = ('id', 'extract_path', 'created_at', 'created_by')