from rest_framework_nested import routers

from django.conf.urls import url, include
from . import views

app_name = "message_port_app"

router = routers.SimpleRouter()
router.register(r'messages', views.AttachmentViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
