#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/18 16:11
# @Author : limber
# @desc :

from database_service.model.base_model import Base
from peewee import *


class Device(Base):
    id = IntegerField(primary_key=True)  # id
    device_id = CharField(unique=True, null=False)  # 设备id
    brand = CharField()  # 品牌
    manufacturer = CharField()  # 厂商
    resolution_ration = CharField()  # 分辨率
    online_state = SmallIntegerField(default=0)  # 在线状态
    task_state = SmallIntegerField(default=0)  # 任务状态
    coord = CharField()  # 经纬度坐标
    locating_app_status = SmallIntegerField(default=0)  # 定位app状态
    locating_app_last_reload_time = DateTimeField(null=True)  # 定位app上一次重启时间

    class Meta:
        table_name = "tb_device"
