#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/18 16:11
# @Author : limber
# @desc :

from database_service.model.base_model import Base
from database_service.model.app_model import App
from peewee import *


class Script(Base):
    id = IntegerField(primary_key=True)  # id
    script_name = CharField(unique=True)  # 脚本名称
    script_content = TextField()  # 脚本内容
    script_type = CharField(null=True)  # 脚本类型 广告任务相关的脚本或者app操作相关的脚本
    app = ForeignKeyField(App, backref="scripts")  # 脚本关联的app

    class Meta:
        table_name = "tb_script"
