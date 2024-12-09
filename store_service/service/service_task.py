#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/9/28 16:20
# @Author : limber
# @desc :

from store_service.mapper.task_mapper import TaskMapper
from store_service.model.model_task import Task
from typing import List


class TaskService:

    def select_all(self, task_name: str = "", task_release_date: str = "") -> List[Task]:
        # 1、获取所有的任务
        task_list = TaskMapper().select_all()

        # 2、根据条件筛选出符合条件的任务
        suitable_task_list = []
        for task_ in task_list:
            condition_one = task_name == "" or task_.task_name == task_name
            condition_two = task_release_date == "" or task_.task_release_date == task_release_date
            if condition_one and condition_two:
                suitable_task_list.append(task_)

        # 3、返回符合条件的任务列表
        return suitable_task_list

    def delete_by_name(self, task_name: str) -> None:
        TaskMapper().delete_by_name(task_name)

    def add_task(self, task: Task) -> None:
        TaskMapper().insert(task)

    def select_by_date(self, date_: str) -> List[Task]:
        suitable_task = TaskMapper().select_by_date(date_)
        return suitable_task

    def select_all_no_condition(self) -> List[Task]:
        # 1、获取所有的任务
        task_list = TaskMapper().select_all()
        return task_list



