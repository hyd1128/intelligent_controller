#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/18 16:10
# @Author : limber
# @desc :
from datetime import date
from typing import List

from peewee import fn

from database_service.model.app_task_model import AppTask


class AppTaskMapper:
    @staticmethod
    def add(app_task: AppTask) -> int:
        """添加"""
        return app_task.save()

    @staticmethod
    def delete(app_task_id) -> int:
        """根据给定的id删除数据库记录"""
        app_task = AppTask.get(AppTask.id == app_task_id)
        return app_task.delete_instance()

    @staticmethod
    def update(app_task: AppTask) -> int:
        """根据id更新数据库记录"""
        return app_task.save()

    @staticmethod
    def select_by_id(app_task_id: int) -> AppTask:
        """根据id查找单条数据库记录"""
        return AppTask.get(AppTask.id == app_task_id)

    @staticmethod
    def select_list(page, per_page) -> List[AppTask]:
        """分页查找数据库记录"""
        query = AppTask.select().paginate(page, per_page)
        return list(query)

    @staticmethod
    def select_by_date(date_: date) -> List[AppTask]:
        """根据日期(格式为: YYYY-MM-DD)查询符合条件的数据"""
        query = AppTask.select().where(fn.Date(AppTask.create_time) == date_)
        return list(query)

    @staticmethod
    def select_count() -> int:
        return AppTask.select().count()

    @staticmethod
    def select_by_multi_condition_one(date_: date, is_execution: int) -> List[AppTask]:
        """根据执行日期和执行状态查找符合条件的app任务"""
        query = AppTask.select().where((fn.Date(AppTask.execution_date) == date_) &
                                       (AppTask.is_execution == is_execution))
        return list(query)




if __name__ == '__main__':
    pass

    # 添加
    # app = AppMapper.select_by_id(2)
    # app_task = AppTask(
    #     task_type="download",
    #     ratio="0.1",
    #     app=app
    # )
    # result = AppMapper.add(app_task)
    # print(result)

    # 删除
    # app_task_id = 4
    # result = AppTaskMapper.delete(app_task_id)
    # print(result)

    # 查单个
    # app_task_id = 1
    # result = AppTaskMapper.select_by_id(app_task_id)
    # print(type(result))
    # print(result.ratio)

    # 分页查询
    # page = 1
    # per_page = 3
    # result = AppTaskMapper.select_list(page, per_page)
    # for i in result:
    #     print(i)
    #     print(type(i))

    # 更新
    # app_task = AppTaskMapper.select_by_id(1)
    # app_task.ratio = 0.2
    #
    # result = AppMapper.update(app_task)
    # print(result)
