from django.views.generic import TemplateView
from django.urls import path
from . import views


urlpatterns = [
    path('', TemplateView.as_view(template_name="home.html"), name='home'),
    path('encode', views.EncodeView.as_view(), name='encode'),
    path('decode', views.DecodeView.as_view(), name='decode'),
]
