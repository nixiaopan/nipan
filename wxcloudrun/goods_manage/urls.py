# -*- coding: utf-8 -*-

from django.urls import path
from wxcloudrun.goods_manage import views

urlpatterns = [
    path('add_goods/', views.add_goods),
    path('update_goods/', views.update_goods),
    path('get_goods_info/', views.get_goods_info),
    path('get_store_goods_info/', views.get_store_goods_info),
]
