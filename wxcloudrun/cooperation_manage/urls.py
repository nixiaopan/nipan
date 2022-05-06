# -*- coding: utf-8 -*-

from django.urls import path
from wxcloudrun.cooperation_manage import views

urlpatterns = [
    path('new_cooperation/', views.new_cooperation),
    path('update_cooperation_info/', views.update_cooperation_info),
    path('send_apply/', views.send_apply),
    path('apply_for_sample/', views.apply_for_sample),
    path('ignore_apply/', views.ignore_apply),
    path('send_sample/', views.send_sample),
    path('test_sample/', views.test_sample),
    path('get_cooperation_info_by_status_and_test_result/', views.get_cooperation_info_by_status_and_test_result),
]
