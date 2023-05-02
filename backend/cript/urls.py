from django.views.generic import TemplateView
from django.urls import path
from . import views


urlpatterns = [
    path('', TemplateView.as_view(template_name="home.html"), name='home'),
    path('adfgx/encode', views.ADFGXEncodeView.as_view(), name='adfgx_encode'),
    path('adfgx/decode', views.ADFGXDecodeView.as_view(), name='adfgx_decode'),
    path('playfair/encode', views.PlayfairEncodeView.as_view(), name='playfair_encode'),
    path('playfair/decode', views.PlayfairDecodeView.as_view(), name='playfair_decode'),
    path('salsa/encode', views.SalsaEncodeView.as_view(), name='salsa_encode'),
    path('salsa/decode', views.SalsaDecodeView.as_view(), name='salsa_decode'),
    path('des/encode', views.DesEncodeView.as_view(), name='des_encode'),
    path('des/decode', views.DesDecodeView.as_view(), name='des_decode'),
    path('sha', views.ShaView.as_view(), name='sha_encode'),
]
