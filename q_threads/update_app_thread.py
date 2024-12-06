#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/11/1 16:17
# @Author : limber
# @desc :
from PyQt6.QtCore import QThread, pyqtSignal

from q_threads.utils.download_app_tool import run_download_app
from store_service.service.service_device import DeviceService
from q_threads.module_varchar import update_script


class UpdateAppThread(QThread):
    signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.flag = True

    def run(self):
        # 1、查找所有当前在线且未在执行任务的应用
        suitable_devices = DeviceService().select(online_state="online", task_state="no")
        suitable_device_ids = []
        for device_ in suitable_devices:
            suitable_device_ids.append(device_.device_id)

        update_app_script = update_script
        for s1 in range(len(update_app_script)):
            for d1 in range(len(suitable_device_ids)):
                # 封装一个执行脚本该脚本的函数
                # 2、查找google应用在屏幕上的坐标
                # 3、进入google store
                # 4、查找应用搜索栏坐标
                # 5、点击搜索栏并输入被下载应用名称
                # 6、根据搜索结果进行查找图标并获得坐标位置
                # 7、点击进入应用界面
                # 8、匹配下载图标并点击更新应用
                run_download_app(update_app_script[s1], suitable_device_ids[d1])
            self.signal.emit(f"所有设备执行完步骤 {int(s1) + 1}")

        # 9、待上一个步骤完全执行完之后 等待10分钟（这一步是所有符合条件的设备都在下载应用 并等待应用下载完成）
        self.sleep(60 * 10)

        # for i in range(20):
        #     self.signal.emit("update")
        #     self.msleep(10)

    def stop(self):
        self.flag = False
