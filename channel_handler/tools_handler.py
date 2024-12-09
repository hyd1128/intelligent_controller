#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/9 16:04
# @Author : limber
# @desc :
from PyQt6.QtCore import QObject, pyqtSlot
from adb.adb import change_volume, change_luminance


class ToolsHandler(QObject):
    def __init__(self):
        super().__init__()

    @pyqtSlot(str, str, result="QVariant")
    def adjust_volume(self, device_id: str, action_: str):
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
    def adjust_luminance(self, device_id: str, action_: str):
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





