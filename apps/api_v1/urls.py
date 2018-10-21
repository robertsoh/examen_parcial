from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^clientes$', views.ClienteCreateAPIView.as_view(), name='crear_cliente'),
]
