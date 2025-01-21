#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/18 18:45
# @Author : limber
# @desc :

from database_service.model.base_model import Base
from database_service.model.app_model import App
from peewee import *


class AppTask(Base):
    """app任务列列表"""
    id = IntegerField(primary_key=True)
    task_type = CharField()  # App任务类型: 下载/更新 设备需要已下载该软件后才可以更新软件
    ratio = FloatField(default=1)  # 当前节点执行该任务的设备比率(0 - 1)
    execution_date = DateField()    # app 任务执行时间
    app = ForeignKeyField(App, backref="appTask")

    class Meta:
        table_name = "tb_app_task"
