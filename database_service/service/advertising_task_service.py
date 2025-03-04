#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/18 16:10
# @Author : limber
# @desc :
from typing import List

from database_service.mapper.advertising_task_mapper import AdvertisingTaskMapper
from datetime import date

from database_service.model.advertising_task_model import AdvertisingTask


class AdvertisingTaskService:
    @staticmethod
    def select_by_task_execution_date(date_: date) -> List[AdvertisingTask]:
        return AdvertisingTaskMapper.select_by_task_execution_date(date_)

    @staticmethod
    def select_all() -> List[AdvertisingTask]:
        return AdvertisingTaskMapper.select_all()

    @staticmethod
    def add(advertising_task: AdvertisingTask) -> int:
        return AdvertisingTaskMapper.add(advertising_task)

    @staticmethod
    def select_list(page, per_page) -> List[AdvertisingTask]:
        return AdvertisingTaskMapper.select_list(page, per_page)

    @staticmethod
    def select_count() -> int:
        return AdvertisingTaskMapper.select_count()

    @staticmethod
    def delete(id) -> int:
        return AdvertisingTaskMapper.delete(id)

