#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/18 16:10
# @Author : limber
# @desc :
from datetime import datetime

from database_service.db import database
from peewee import *


class Base(Model):
    create_time = DateTimeField(default=None, null=True)
    update_time = DateTimeField(default=None, null=True)

    def save(self, *args, **kwargs):
        if self.create_time is None:
            self.create_time = datetime.now()  # 如果是新记录，设置 create_time
            return super().save(*args, **kwargs)  # 调用父类的 save 方法
        else:
            self.update_time = datetime.now()  # 每次保存时更新 update_time
            return super().save(*args, **kwargs)  # 调用父类的 save 方法

    class Meta:
        database = database
