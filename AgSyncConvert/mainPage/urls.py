# mainPage/urls.py
from django.conf.urls import url
from mainPage import views
from django.urls import path, include
from django.http import HttpResponseRedirect
from .models import AgSyncCredential
import requests
import string
import random

urlpatterns = [
    url(r'^login/', views.HomePageView.as_view()),
    url(r'^recCode/$', views.recCode.as_view()),
    url(r'^getOrders/$', views.GetOrders.as_view(), name='getOrders'),
    path('setCred/', views.CredCreate.as_view()),
]
