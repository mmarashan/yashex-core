from django.shortcuts import render
from .models import Message
# Create your views here.

def post_list(request):
    messages = Message.objects.order_by('-date_created')
    return render(request, 'message_port_app/message_list.html', {'messages':messages})