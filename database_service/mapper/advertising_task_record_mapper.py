#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/18 16:10
# @Author : limber
# @desc :

from datetime import datetime, time, date
from typing import List
from database_service.mapper.advertising_task_mapper import AdvertisingTaskMapper
from database_service.mapper.device_mapper import DeviceMapper
from database_service.model.advertising_task_model import AdvertisingTask
from database_service.model.advertising_task_record_model import AdvertisingTaskRecord
from database_service.model.device_model import Device


class AdvertisingTaskRecordMapper:
    @staticmethod
    def add(advertising_task_record: AdvertisingTaskRecord) -> int:
        """添加"""
        return advertising_task_record.save()

    @staticmethod
    def delete(advertising_task_record_id) -> int:
        """根据给定的id删除数据库记录"""
        advertising_task_record = AdvertisingTaskRecord.get(AdvertisingTaskRecord.id == advertising_task_record_id)
        return advertising_task_record.delete_instance()

    @staticmethod
    def update(advertising_task_record: AdvertisingTaskRecord) -> int:
        """根据id更新数据库记录"""
        return advertising_task_record.save()

    @staticmethod
    def select_by_id(advertising_task_record_id: int) -> AdvertisingTaskRecord:
        """根据id查找单条数据库记录"""
        return AdvertisingTaskRecord.get(AdvertisingTaskRecord.id == advertising_task_record_id)

    @staticmethod
    def select_list(page, per_page) -> List[AdvertisingTaskRecord]:
        """分页查找数据库记录"""
        query = AdvertisingTaskRecord.select().paginate(page, per_page)
        return list(query)

    @staticmethod
    def select_by_multiple_conditions(task_: AdvertisingTask, device_: Device, date_: date) -> AdvertisingTaskRecord:
        """多条件查询唯一广告记录"""
        return AdvertisingTaskRecord.get_or_none((AdvertisingTaskRecord.task == task_) &
                                                 (AdvertisingTaskRecord.device == device_) &
                                                 (AdvertisingTaskRecord.date == date_))

    @staticmethod
    def select_by_device_date(device_: Device, date_: date) -> List[AdvertisingTaskRecord]:
        """根据条件device date查询符合条件的广告运行记录"""
        query = AdvertisingTaskRecord.select().where((AdvertisingTaskRecord.device == device_) &
                                                     (AdvertisingTaskRecord.date == date_))
        return list(query)

    @staticmethod
    def select_by_date(task_: AdvertisingTask, date_: date) -> List[AdvertisingTaskRecord]:
        """根据日期查询符合条件的广告任务运行记录"""
        query = AdvertisingTaskRecord.select().where((AdvertisingTaskRecord.task == task_)
                                                     & (AdvertisingTaskRecord.date == date_))
        return list(query)

    @staticmethod
    def select_count() -> int:
        return AdvertisingTaskRecord.select().count()


if __name__ == '__main__':
    pass
    # 多条件查询唯一广告记录
    device = DeviceMapper.select_by_id(2)
    task = AdvertisingTaskMapper.select_by_id(1)
    date = date.today()
    result = AdvertisingTaskRecordMapper.select_by_multiple_conditions(task, device, date)
    if isinstance(result, AdvertisingTaskRecord):
        print(result.execution_times)

    # 添加
    # device = DeviceMapper.select_by_id(2)
    # task = AdvertisingTaskMapper.select_by_id(1)
    # advertising_task_record = AdvertisingTaskRecord(
    #     execution_times=1,
    #     start_execution_time=time(hour=12, minute=20, second=30),
    #     end_execution_time=time(hour=18, minute=30, second=20),
    #     specify_device_execution_time=20,
    #     task_last_execution_time=time(hour=15, minute=30, second=20),
    #     date=date.today().strftime("%Y-%m-%d"),
    #     device=device,
    #     task=task
    # )
    #
    # result = AdvertisingTaskRecordMapper.add(advertising_task_record)
    # print(result)

    # 删除
    # advertising_task_record_id = 4
    # result = AdvertisingTaskRecordMapper.delete(advertising_task_record_id)
    # print(result)

    # 查单个
    # advertising_task_record_id = 1
    # result = AdvertisingTaskRecordMapper.select_by_id(advertising_task_record_id)
    # print(type(result))
    # print(result.execution_times)

    # 分页查询
    # page = 1
    # per_page = 3
    # result = AdvertisingTaskRecordMapper.select_list(page, per_page)
    # for i in result:
    #     print(i)
    #     print(type(i))

    # 更新
    # advertising_task_record = AdvertisingTaskRecordMapper.select_by_id(1)
    # advertising_task_record.execution_times = advertising_task_record.execution_times + 1
    # result = AdvertisingTaskRecordMapper.update(advertising_task_record)
    # print(result)
