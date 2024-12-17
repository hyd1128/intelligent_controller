import time

from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from adb.adb import device_list, info
from global_var import coord_1, coord_2
from modify_position.allocation_position import generate_coordinate
from logger_zk.logger_types import logger_watch
from store_service.model.model_device import Device
from store_service.service.service_device import DeviceService
from util.device_queue import DeviceQueue


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

                        ###################
                        device_info["online_state"] = 1
                        device_info["task_state"] = 0
                        device_info["locating_app_status"] = 0
                        # 查询该设备的device_id是否存在, 不存在则为新设备
                        result = DeviceService().select_by_device_id(device_info["device_id"])
                        # 判断是否为新设备
                        if result is None:
                            # 实例化一个Device对象
                            device_ = Device(**device_info)
                            DeviceService().add_device(device_)
                            # 将新设备添加到队列
                            new_device = DeviceService().select_by_device_id(device_.device_id)
                            DeviceQueue.put(new_device)
                        ##################
            time.sleep(10)  # 20秒查询一次

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
                # 设备掉线但当前数据库中显示该设备在线
                # 或设备在线但当前数据库中显示该设备掉线
                if (not online and item.online_state == 1) or (online and item.online_state == 0):
                    if not online:
                        # 设备掉线，文件中更新设备
                        item.online_state = 0
                    else:
                        # 设备在线，文件中更新设备在线
                        item.online_state = 1
                    item.task_state = 0
                    DeviceService().update(item)
            time.sleep(10)  # 30秒查询一次

    def stop(self):
        self.flag = True
