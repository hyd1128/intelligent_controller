#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/19 16:07
# @Author : limber
# @desc :


from PyQt6.QtCore import QThread, pyqtSignal
import time
from database_service.model.device_model import Device
from database_service.service.device_service import DeviceService
from logger_zk.logger_types import logger_watch
from util.adb_util import AdbUtil
from util.config_util import COORD_ONE, COORD_TWO
from util.device_queue import DeviceQueue
from util.general_util import GeneralUtil


# from adb.adb import device_list, info

class NewDeviceMonitor(QThread):
    new_device_signal = pyqtSignal(Device)

    def __init__(self):
        super().__init__()
        self.flag = False

    def run(self):
        """监控新增"""
        logger_watch.info("##### 监控新设备中.... #####")
        while True:
            if self.flag:
                break
            # 获取当前在线设备
            devices, _ = AdbUtil.device_list()
            # 获取系统已备份设备
            exist_devices = DeviceService.select_all()

            for device_ in devices:
                exist = False  # 是否存在
                for exist_device_ in exist_devices:
                    if device_ == exist_device_.device_id:
                        exist = True
                        break
                if not exist:
                    device_info, err = AdbUtil.info(device_)
                    if device_info is not None:
                        device_info["device_id"] = device_
                        device_info["coord"] = str(GeneralUtil.generate_coordinate(COORD_ONE, COORD_TWO))
                        device_info["online_state"] = 1
                        device_info["task_state"] = 0
                        device_info["locating_app_status"] = 0
                        # 查询该设备的device_id是否存在, 不存在则为新设备
                        result = DeviceService.select_by_device_id(device_info["device_id"])
                        # 判断是否为新设备
                        if result is None:
                            # 实例化一个Device对象
                            device_ = Device(**device_info)
                            DeviceService.add(device_)
                            # 将新设备添加到队列
                            new_device = DeviceService.select_by_device_id(device_.device_id)
                            DeviceQueue.put(new_device)

                            # 新设备触发信号
                            self.new_device_signal.emit(new_device)
            # 20秒查询一次
            time.sleep(10)

    def stop(self):
        self.flag = True
