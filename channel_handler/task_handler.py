#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/6 13:42
# @Author : limber
# @desc :
from datetime import datetime

from PyQt6.QtCore import QObject, pyqtSlot

from database_service.service.advertising_task_service import AdvertisingTaskService


# from store_service.service.service_task import TaskService


class TaskHandler(QObject):
    def __init__(self):
        super().__init__()

    @pyqtSlot(int, int, result="QVariant")
    def device_list_slot(self, page_number: int, total_item: int):
        """
        任务列表分页槽函数

        :param page_number:
        :param total_item:
        :return:
        """
        """status: 0表示已运行 1表示正在运行 2表示未运行"""
        task_data = []
        tasks_ = AdvertisingTaskService.select_all()
        for task_ in tasks_:
            template_ = {"task_id": task_.task_name,
                         "task_content": (
                             f"任务运行时长: {task_.task_execution_duration}, "
                             f"任务最多运行{task_.max_execution_times}次, "
                             f"最少运行{task_.min_execution_times}次")}

            today_ = datetime.now()
            task_release_day = datetime.strptime(task_.task_release_date, "%Y-%m-%d")
            interval_timedelta = today_ - task_release_day
            task_data.append(template_)
            if interval_timedelta.days > 0:
                template_["status"] = 0
            elif interval_timedelta.days == 0:
                template_["status"] = 1
            else:
                template_["status"] = 2

        try:
            first_ = (page_number - 1) * total_item
            last_ = first_ + total_item
            data_ = task_data[first_:last_]
            return {
                "code": 200,
                "data": data_,
                "msg": ""
            }
        except Exception as e:
            return {
                "code": 400,
                "data": "",
                "msg": str(e)
            }
