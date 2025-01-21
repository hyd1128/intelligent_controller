#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/19 16:07
# @Author : limber
# @desc :
import json
import time
from PyQt6.QtCore import QThread, pyqtSignal

from database_service.model.device_model import Device
from database_service.service.app_service import AppService
from util.adb_util import AdbUtil
from database_service.service.device_service import DeviceService
from logger_zk.logger_types import logger_watch
from util.uiautomotor_util import UIAutoMotorUtil


# from adb.adb import device_list

class OfflineDeviceMonitor(QThread):
    device_online_signal = pyqtSignal(Device)
    device_offline_signal = pyqtSignal(Device)

    def __init__(self):
        super().__init__()
        self.flag = False

    # 监控是否有掉线设备
    def run(self):
        logger_watch.info("##### 监听掉线设备.... #####")
        while True:
            if self.flag:
                break
            # 当前实时在线设备
            devices, _ = AdbUtil.device_list()
            # 已备份的设备
            exist_devices = DeviceService.select_all()
            for index, item in enumerate(exist_devices):
                online = False
                for device in devices:
                    if item.device_id == device:
                        online = True
                        break
                # 设备掉线但当前数据库中显示该设备在线
                # 或设备在线但当前数据库中显示该设备掉线
                if (not online and item.online_state == 1) or (online and item.online_state == 0):
                    if not online:
                        # 当前设备掉线
                        item.online_state = 0
                        item.task_state = 0
                        DeviceService.update(item)
                        self.device_offline_signal.emit(item)
                    else:
                        # 当前设备在线
                        item.online_state = 1
                        item.task_state = 0
                        # 判断设备具有哪些终端已注册的app
                        app_name_list = [app.package_name for app in AppService.select_all()]
                        download_app_list = []
                        for package_name in app_name_list:
                            if UIAutoMotorUtil.is_download_app(item.device_id, package_name):
                                download_app_list.append(package_name)
                        item.download_app = json.dumps(download_app_list)
                        DeviceService.update(item)
                        self.device_online_signal.emit(item)

            time.sleep(10)  # 30秒查询一次

    def stop(self):
        self.flag = True
