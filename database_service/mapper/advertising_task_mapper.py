#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/18 16:10
# @Author : limber
# @desc :

from datetime import date, timedelta
from typing import List
from database_service.mapper.app_mapper import AppMapper
from database_service.model.advertising_task_model import AdvertisingTask


class AdvertisingTaskMapper:
    @staticmethod
    def add(advertising_task: AdvertisingTask) -> int:
        """添加"""
        return advertising_task.save()

    @staticmethod
    def delete(advertising_task_id) -> int:
        """根据给定的id删除数据库记录"""
        advertising_task = AdvertisingTask.get(AdvertisingTask.id == advertising_task_id)
        return advertising_task.delete_instance()

    @staticmethod
    def update(advertising_task: AdvertisingTask) -> int:
        """根据id更新数据库记录"""
        return advertising_task.save()

    @staticmethod
    def select_by_id(advertising_task_id: int) -> AdvertisingTask:
        """根据id查找单条数据库记录"""
        return AdvertisingTask.get(AdvertisingTask.id == advertising_task_id)

    @staticmethod
    def select_list(page, per_page) -> List[AdvertisingTask]:
        """分页查找数据库记录"""
        query = AdvertisingTask.select().paginate(page, per_page)
        return list(query)

    @staticmethod
    def select_by_task_execution_date(date_: date) -> AdvertisingTask | None:
        """根据日期查询任务"""
        return AdvertisingTask.get_or_none(AdvertisingTask.task_execution_date == date_)

    @staticmethod
    def select_all() -> List[AdvertisingTask]:
        """查询全部任务"""
        return list(AdvertisingTask.select())


if __name__ == '__main__':
    pass

    # 添加
    # app = AppMapper.select_by_id(2)
    # advertising_task = AdvertisingTask(task_name="2024-12-11-prism",
    #                                    task_execution_duration="08:00:00",
    #                                    min_execution_times=10,
    #                                    max_execution_times=20,
    #                                    task_release_date=date.today(),
    #                                    task_execution_date=date.today()+timedelta(days=1),
    #                                    app=app)
    #
    # result = AdvertisingTaskMapper.add(advertising_task)
    # print(result)

    # 删除
    # advertising_task_id = 3
    # result = AdvertisingTaskMapper.delete(advertising_task_id)
    # print(result)

    # 查单个
    # advertising_task_id = 1
    # result = AdvertisingTaskMapper.select_by_id(advertising_task_id)
    # print(type(result))
    # print(result.task_name)

    # 分页查询
    # page = 1
    # per_page = 3
    # result = AdvertisingTaskMapper.select_list(page, per_page)
    # for i in result:
    #     print(i)
    #     print(type(i))

    # 更新
    # advertising_task = AdvertisingTaskMapper.select_by_id(1)
    # advertising_task.task_execution_date = date.today() + timedelta(days=10)
    # result = AdvertisingTaskMapper.update(advertising_task)
    # print(result)

    # 根据日期查询任务
    # date = date(year=2024, month=12, day=31)
    # result = AdvertisingTaskMapper.select_by_task_execution_date(date)
    # print(result)
