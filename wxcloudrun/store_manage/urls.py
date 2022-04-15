# -*- coding: utf-8 -*-

from django.urls import path
from wxcloudrun.store_manage import views

urlpatterns = [
    path('new_store/', views.new_store),
    path('update_store_info/', views.update_store_info),
    path('get_store_info/', views.get_store_info),
    path('delete_store/', views.delete_store),
]
