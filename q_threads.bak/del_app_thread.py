#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/11/1 16:16
# @Author : limber
# @desc :
from PyQt6 import QtCore
from PyQt6.QtCore import QThread
from store_service.service.service_device import DeviceService
from q_threads.module_varchar import prism_package_name, youtube_package_name
from adb.adb import del_app_package


class DeleteAppThread(QThread):
    signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.flag = True

    def run(self):
        # 添加逻辑
        # 遍历当前在线的所有device 并获得其device_id
        # 获取在线且不在任务中的device
        suitable_device = DeviceService().select(online_state="online", task_state="no")
        suitable_device_id = []
        for device_ in suitable_device:
            suitable_device_id.append(device_.device_id)

        for i_ in range(len(suitable_device_id)):
            del_app_package(suitable_device_id[i_], youtube_package_name)
            self.signal.emit(f"设备 {suitable_device_id[i_]} 删除app-{youtube_package_name}-成功")

    def stop(self):
        self.flag = False