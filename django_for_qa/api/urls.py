"""django_for_qa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'v1/testqa/',views.qarobot,name="qarobot"),#问答系统
    url(r'v1/downloads/',views.downloads,name="downloads"),#问答系统
    url(r'(?P<version>[v1|v2]+)/qa/',views.Qarobots.as_view(),name="qaqa"),#问答
    url(r'index/',views.index,name="index"),#问答
    url(r'cebianlan/',views.cebianlan,name="cebianlan"),#问答
    url(r'xiugai/',views.xiugai,name="xiugai"),#问答
    url(r'wendaceshi/',views.wendaceshi,name="wendaceshi"),#问答
    url(r'bumanyiwenti/',views.bumanyiwenti,name="bumanyiwenti"),#问答
    url(r'bumanyidaan/',views.bumanyidaan,name="bumanyidaan"),#问答
    url(r'tianjiaxinwenti/',views.tianjiaxinwenti,name="tianjiaxinwenti"),#问答
    url(r'changerji/',views.changerji,name="changerji"),#问答
    url(r'tianjia/',views.tianjia,name="tianjia"),#问答
    url(r'xuexi/',views.xuexi,name="xuexi"),#问答
    url(r'cnmd/(?P<pk>.+)',views.cnmd,name="cnmd"),#问答
    url(r'cnmd1/(?P<pk>.+)',views.cnmd1,name="cnmd1"),#问答
    url(r'cnmd2/(?P<pk>.+)',views.cnmd2,name="cnmd2"),#问答
    url(r'cnmd3/',views.cnmd3,name="cnmd3"),#问答
    url(r'cnmd12345/',views.cnmd12345,name="cnmd12345"),#问答
]
