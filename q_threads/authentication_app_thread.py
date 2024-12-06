#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/11/1 16:18
# @Author : limber
# @desc :
from PyQt6.QtCore import QThread, pyqtSignal

from q_threads.utils.run_app_tool import run_run_app
from store_service.service.service_device import DeviceService


class AuthenticationAppThread(QThread):
    signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.flag = True

    def run(self):
        # # 查找当前在线且未执行任务的设备
        # # 1、根据app图标获取图标所在位置， 进入应用，
        # # 2、完整执行一遍脚本程序（鉴权脚本程序）
        # # 1、查找所有当前在线且未在执行任务的应用
        # suitable_devices = DeviceService().select(online_state="online", task_state="no")
        # suitable_device_ids = []
        # for device_ in suitable_devices:
        #     suitable_device_ids.append(device_.device_id)
        #
        # authentication_app_script = []
        # for s1 in range(len(authentication_app_script)):
        #     for d1 in range(len(suitable_device_ids)):
        #         run_run_app(authentication_app_script[s1], suitable_device_ids[d1])
        #         self.signal.emit(f"设备 {d1} 已鉴权app prism")

        for i in range(20):
            self.signal.emit("update")
            self.msleep(10)


    def stop(self):
        self.flag = False
