from django.urls import path
from . import views

urlpatterns = [
    path('', views.crop_profit, name='crop_profit'),
]
