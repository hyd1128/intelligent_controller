#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/11/27 16:13
# @Author : limber
# @desc :

import time
from PyQt6 import QtCore
from PyQt6.QtCore import QThread

from database_service.service.device_service import DeviceService
from util.config_util import NODE_DATA
from util.file_util import FileUtil
from util.path_util import PathUtil
from util.http_util import HttpUtils


class DeviceController(QThread):
    signal = QtCore.pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.flag = False

    # 监控是否有新增
    def run(self):

        # 远程资源定位符
        uri = "/api/v1/root_accounts/device/add_device"

        while True:
            time.sleep(20)
            if self.flag:
                break
            print("上传设备接口执行了一次")
            root_path = PathUtil.get_current_file_absolute_path(__file__).parent.parent
            node_info_path = root_path.joinpath(NODE_DATA)
            node_info = FileUtil.read_file_content(node_info_path)
            # 要发送的 JSON 数据
            suitable_devices = DeviceService.select_all()
            suitable_device_data = []
            for device_ in suitable_devices:
                suitable_device_data.append({"uuid": device_.device_id,
                                             "top_accounts": node_info["top_account"],
                                             "normal_accounts": node_info["normal_account"],
                                             "device_model": device_.manufacturer,
                                             "node": node_info["node_id"],
                                             "network": device_.online_state,
                                             "status": device_.task_state
                                             })
            response_data = HttpUtils.post(uri, json_data=suitable_device_data)

            if response_data["code"] == 200 and response_data["data"]["code"] == 200:
                print("定时上传设备数据成功")
                print(response_data["data"]["data"])
            else:
                print("定时上传设备数据失败")
                print(response_data["data"]["data"])

    def stop(self):
        self.flag = True


if __name__ == '__main__':
    pass
