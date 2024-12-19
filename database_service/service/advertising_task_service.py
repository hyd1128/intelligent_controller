#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/18 16:10
# @Author : limber
# @desc :

from database_service.mapper.advertising_task_mapper import AdvertisingTaskMapper
from datetime import date


class AdvertisingTaskService:
    @staticmethod
    def select_by_task_execution_date(date_: date):
        return AdvertisingTaskMapper.select_by_task_execution_date(date_)
