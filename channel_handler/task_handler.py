#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/6 13:42
# @Author : limber
# @desc :
from PyQt6.QtCore import QObject, pyqtSlot


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
        task_data = [
            {
                "task_id": "12341",
                "task_content": "content",
                "status": 0,
            },
            {
                "task_id": "12342",
                "task_content": "content",
                "status": 0,
            },
            {
                "task_id": "12343",
                "task_content": "content",
                "status": 0,
            },
            {
                "task_id": "12344",
                "task_content": "content",
                "status": 0,
            },
            {
                "task_id": "12345",
                "task_content": "content",
                "status": 0,
            },
            {
                "task_id": "12346",
                "task_content": "content",
                "status": 0,
            },
        ]

        try:
            first_ = page_number * total_item
            last_ = page_number * total_item + total_item
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
