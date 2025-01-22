#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/18 18:45
# @Author : limber
# @desc :

from database_service.model.app_task_model import AppTask
from database_service.model.device_model import Device
from database_service.model.base_model import Base
from peewee import *


class AppTaskRecord(Base):
    """app任务运行记录"""
    id = IntegerField(primary_key=True)  # id
    device = ForeignKeyField(Device, backref="appRecords", on_delete="RESTRICT")  # app任务运行记录关联的设备
    app_task = ForeignKeyField(AppTask, backref="appRecords", on_delete="RESTRICT")  # app任务运行记录关联的app任务

    class Meta:
        table_name = "tb_app_task_record"
