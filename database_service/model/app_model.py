#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/18 16:10
# @Author : limber
# @desc :

from database_service.model.base_model import Base
from peewee import *


class App(Base):
    """app 模型类"""
    id = IntegerField(primary_key=True)  # id
    app_name = CharField(unique=True, null=False)  # app名称
    package_name = CharField(unique=True, null=True)  # app包名
    version = CharField(null=True)  # app版本
    download_link = CharField(null=True)  # app下载链接
    download_method = CharField(null=True)  # app下载方法

    class Meta:
        table_name = "tb_app"
