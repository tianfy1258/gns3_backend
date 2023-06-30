"""backend URL Configuration

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
from django.shortcuts import render

from django.views.generic import TemplateView
from django.urls import path, include, re_path
from aim.views import *
from aim.utils import DataQuery
import inspect
from aim import models
from backend.settings import DEBUG

# 所有Models的查询接口
database_query = [
    path(f'get{classname}', DataQuery.query_builder(
        class_
    ))
    for classname, class_ in inspect.getmembers(models, inspect.isclass)
]
# 所有Models的删除接口
database_delete = [
    path(f'delete{classname}', DataDelete.query_builder(
        class_
    ))
    for classname, class_ in inspect.getmembers(models, inspect.isclass)
]
# 所有Models的修改接口
database_update = [
    path(f'update{classname}', DataUpdate.query_builder(
        class_
    ))
    for classname, class_ in inspect.getmembers(models, inspect.isclass)
]

urlpatterns = [
    # 登录相关
    path('login', login),
    path('logout', logout),
    path('validToken', valid_token),
    path('allprojects', all_projects),
    path('project', ops_for_project),
    path('node', ops_for_node),
    path('start', start_node),
    path('stop', stop_node),
    path('startall', start_all_nodes),
    path('stopall', stop_all_nodes),
    path('link', ops_for_link),
    path('telnet', do_telnet)

    # 数据库查询相关, 名称为 get{ModelName}, 例如getDataset
    *database_query,
    # 数据库删除相关, 名称为 delete{ModelName}, 例如deleteDataset
    *database_delete,
    # 数据库修改相关, 名    称为 update{ModelName}, 例如updateDataset
    *database_update,


    # [DEBUG ONLY] GNS交互测试接口，名称为 aim.network.gns3的方法名称

]
