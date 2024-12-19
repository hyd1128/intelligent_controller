#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/18 16:11
# @Author : limber
# @desc :

from database_service.model.base_model import Base
from database_service.model.device_model import Device
from database_service.model.advertising_task_model import AdvertisingTask
from peewee import *


class AdvertisingTaskRecord(Base):
    """设备记录"""
    id = IntegerField(primary_key=True)
    execution_times = IntegerField()  # 执行次数
    start_execution_time = DateTimeField()  # 任务当日开始执行时间
    end_execution_time = DateTimeField()  # 任务当日结束执行时间
    specify_device_execution_time = IntegerField()  # 指定设备
    task_last_execution_time = DateTimeField()  # 任务上一次执行时间
    date = DateField()  # 记录时间
    device = ForeignKeyField(Device, backref="records")  # 记录关联的设备
    task = ForeignKeyField(AdvertisingTask, backref="records")  # 记录关联的任务

    class Meta:
        table_name = "tb_advertising_task_record"



