import time

from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from adb.adb import device_list, info
from global_var import coord_1, coord_2
from modify_position.allocation_position import generate_coordinate
from logger_zk.logger_types import logger_watch
from store_service.service.service_device import DeviceService


class New(QThread):
    signal = QtCore.pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.flag = False

    # 监控是否有新增
    def run(self):
        logger_watch.info("开始监控新设备")
        while True:
            if self.flag:
                break

            # 获得当前在线设备
            devices, _ = device_list()

            # 获取当前文件记录的所有设备
            # current = DeviceStore().select()
            current = DeviceService().select()

            for item in devices:
                exist = False  # 是否存在
                for current_item in current:
                    if item == current_item.device_id:
                        exist = True
                        break

                if not exist:
                    device_info, err = info(item)
                    if device_info is not None:
                        device_info["device_id"] = item
                        device_info["coord"] = str(generate_coordinate(coord_1, coord_2))

                        self.signal.emit(device_info)
            time.sleep(20)  # 20秒查询一次

    def stop(self):
        self.flag = True


class Offline(QThread):
    signal = QtCore.pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.flag = False

    # 监控是否有掉线设备
    def run(self):
        logger_watch.info("开始监听掉线设备")
        while True:
            if self.flag:
                break
            # 当前实时在线设备
            devices, _ = device_list()

            # 文件中的在线设备（不具备实时性）
            current = DeviceService().select()

            for index, item in enumerate(current):
                online = False
                for device in devices:
                    if item.device_id == device:
                        online = True
                        break
                # 设备掉线，但是文件中显示为掉线或者设备在线但是设备在文件中显示是掉线
                if (not online and item.online_state == 1) or (online and item.online_state == 0):
                    if not online:
                        # 设备掉线，文件中更新设备
                        item.online_state = 0
                    else:
                        # 设备在线，文件中更新设备在线
                        item.online_state = 1

                    item.task_state = 0
                    DeviceService().update(item)
                    self.signal.emit(item)
            time.sleep(30)  # 30秒查询一次

    def stop(self):
        self.flag = True
