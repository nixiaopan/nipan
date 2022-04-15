# -*- coding: utf-8 -*-

from django.urls import path
from wxcloudrun.np_test import views

urlpatterns = [
    path('test1/', views.test1),
]
