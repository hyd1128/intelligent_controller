#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/18 16:11
# @Author : limber
# @desc :
from database_service.model.base_model import Base
from peewee import *
from database_service.model.app_model import App


class AdvertisingTask(Base):
    """广告任务"""
    id = IntegerField(primary_key=True)  # id
    task_name = CharField(unique=True)  # 任务名称
    task_execution_duration = CharField()  # 任务执行时长
    min_execution_times = IntegerField()  # 任务最少执行次数
    max_execution_times = IntegerField()  # 任务最多执行次数
    task_release_date = DateField()  # 任务发布时间
    task_execution_date = DateField()  # 任务执行时间
    app = ForeignKeyField(App, backref="tasks")  # 任务关联的app

    class Meta:
        table_name = "tb_advertising_task"
