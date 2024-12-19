#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/18 16:10
# @Author : limber
# @desc :
from datetime import datetime
from typing import List

from database_service.mapper.app_task_mapper import AppTaskMapper
from database_service.mapper.device_mapper import DeviceMapper
from database_service.model.app_task_record_model import AppTaskRecord


class AppTaskRecordMapper:
    @staticmethod
    def add(app_task_record: AppTaskRecord) -> int:
        """添加"""
        return app_task_record.save()

    @staticmethod
    def delete(app_task_record_id) -> int:
        """根据给定的id删除数据库记录"""
        app_task_record = AppTaskRecord.get(AppTaskRecord.id == app_task_record_id)
        return app_task_record.delete_instance()

    @staticmethod
    def update(app_task_record: AppTaskRecord) -> int:
        """根据id更新数据库记录"""
        return app_task_record.save()

    @staticmethod
    def select_by_id(app_task_record_id: int) -> AppTaskRecord:
        """根据id查找单条数据库记录"""
        return AppTaskRecord.get(AppTaskRecord.id == app_task_record_id)

    @staticmethod
    def select_list(page, per_page) -> List[AppTaskRecord]:
        """分页查找数据库记录"""
        query = AppTaskRecord.select().paginate(page, per_page)
        return list(query)


if __name__ == '__main__':
    pass

    # 添加
    # device = DeviceMapper.select_by_id(2)
    # app_task = AppTaskMapper.select_by_id(2)
    # app_task_record = AppTaskRecord(
    #     device=device,
    #     app_task=app_task,
    # )
    #
    # result = AppTaskRecordMapper.add(app_task_record)
    # print(result)

    # 删除
    # app_task_record_id = 4
    # result = AppTaskRecordMapper.delete(app_task_record_id)
    # print(result)

    # 查单个
    # app_task_record_id = 1
    # result = AppTaskRecordMapper.select_by_id(app_task_record_id)
    # print(type(result))
    # print(result.device.device_id)

    # 分页查询
    # page = 1
    # per_page = 3
    # result =  AppTaskRecordMapper.select_list(page, per_page)
    # for i in result:
    #     print(i)
    #     print(type(i))

    # 更新
    app_task_record = AppTaskRecordMapper.select_by_id(1)
    device = DeviceMapper.select_by_id(3)
    app_task_record.device = device
    result = AppTaskRecordMapper.update(app_task_record)
    print(result)
