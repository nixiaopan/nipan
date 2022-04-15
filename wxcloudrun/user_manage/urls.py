# -*- coding: utf-8 -*-

from django.urls import path
from wxcloudrun.user_manage import views

urlpatterns = [
    path('user_register/', views.user_register),
    path('update_user_info/', views.update_user_info),
    path('get_user_info/', views.get_user_info),
]
