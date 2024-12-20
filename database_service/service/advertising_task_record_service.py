#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/18 16:10
# @Author : limber
# @desc :
from datetime import date

from database_service.mapper.advertising_task_record_mapper import AdvertisingTaskRecordMapper
from database_service.model.advertising_task_model import AdvertisingTask
from database_service.model.advertising_task_record_model import AdvertisingTaskRecord
from database_service.model.device_model import Device


class AdvertisingTaskRecordService:
    @staticmethod
    def select_by_multiple_conditions(task_: AdvertisingTask, device_: Device, date_: date):
        return AdvertisingTaskRecordMapper.select_by_multiple_conditions(task_, device_, date_)

    @staticmethod
    def add(advertising_task_record: AdvertisingTaskRecord) -> int:
        return AdvertisingTaskRecordMapper.add(advertising_task_record)

    @staticmethod
    def select_by_device_date(device_: Device, date_: date):
        return AdvertisingTaskRecordMapper.select_by_device_date(device_, date_)

    @staticmethod
    def update(advertising_task_record: AdvertisingTaskRecord) -> int:
        return AdvertisingTaskRecordMapper.update(advertising_task_record)
