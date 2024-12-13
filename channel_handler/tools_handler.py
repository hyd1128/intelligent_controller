#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/9 16:04
# @Author : limber
# @desc :
from PyQt6.QtCore import QObject, pyqtSlot
from adb.adb import change_volume, change_luminance
import global_var
from client_controller.task_controller import TaskController


class ToolsHandler(QObject):
    def __init__(self):
        super().__init__()

    @pyqtSlot(str, str, result="QVariant")
    def adjust_volume_slot(self, device_id: str, action_: str):
        """
        调节指定设备声音的槽函数

        :param device_id:
        :param action_:
        :return:
        """
        try:
            change_volume(device_id, action_)
            return {
                "code": 200,
                "data": True,
                "msg": ""
            }
        except Exception as e:
            return {
                "code": "400",
                "data": False,
                "msg": str(e)
            }

    @pyqtSlot(str, str, result="QVariant")
    def adjust_luminance_slot(self, device_id: str, action_: str):
        """
        调节指定设备亮度的槽函数

        :param device_id:
        :param action_:
        :return:
        """
        try:
            change_luminance(device_id, action_)
            return {
                "code": 200,
                "data": True,
                "msg": ""
            }
        except Exception as e:
            return {
                "code": "400",
                "data": False,
                "msg": str(e)
            }

    @pyqtSlot(bool, result="QVariant")
    def open_switch_slot(self, action_: bool):
        """
        开启或者关闭开关槽函数

        :return:
        """
        if action_:
            global_var.is_running = True
            return {
                "code": 200,
                "data": "开始执行",
                "msg": "开启开关，开始执行任务"
            }
        else:
            global_var.is_running = False
            return {
                "code": 200,
                "data": "暂停执行",
                "msg": "关闭开关，暂停执行任务"
            }

    @pyqtSlot(result="QVariant")
    def update_tasks(self):
        update_task_result = TaskController.pull_task()
        if update_task_result["result"]:
            return {
                "code": 200,
                "data": "",
                "msg": update_task_result["msg"]
            }
        else:
            return {
                "code": 400,
                "data": "",
                "msg": update_task_result["msg"]
            }
