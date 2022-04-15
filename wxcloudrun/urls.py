"""wxcloudrun URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from wxcloudrun import views
from django.conf.urls import url,include

urlpatterns = (
    # 计数器接口
    url(r'^^api/count(/)?$', views.counter),
    url(r'np/', include('wxcloudrun.np_test.urls')),
    url(r'user_manage/', include('wxcloudrun.user_manage.urls')),
    url(r'store_manage/', include('wxcloudrun.store_manage.urls')),
    url(r'goods_manage/', include('wxcloudrun.goods_manage.urls')),
    url(r'cooperation_manage/', include('wxcloudrun.cooperation_manage.urls')),
    # 获取主页
    # url(r'(index/)?$', views.index),
)
