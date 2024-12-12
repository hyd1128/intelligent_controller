#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/11/26 7:43
# @Author : limber
# @desc :

import time
from PyQt6 import QtCore
from PyQt6.QtCore import QThread
from store_service.service.service_device import DeviceService
from util.file_util import FileUtil
from util.path_util import PathUtil
from util.http_util import HttpUtils


class NodeController(QThread):
    signal = QtCore.pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.flag = False

    # 监控是否有新增
    def run(self):
        URI = "/api/v1/root_accounts/device/node"
        while True:
            if self.flag:
                break
            print("节点接口执行了一次")
            root_path = PathUtil.get_current_file_absolute_path(__file__).parent.parent
            node_info_path = root_path.joinpath("node_info").joinpath("info.json")
            node_info = FileUtil.read_file_content(node_info_path)

            # 定时更新节点信息
            suitable_devices = DeviceService().select(online_state="online", task_state="all")
            online_device = len(suitable_devices)

            # 当前节点信息
            node_data = {
                "uuid": node_info["node_id"],   # 节点ID
                "node_version": node_info["node_version"],  # 节点版本
                "normal_accounts": node_info["normal_account"],     # 当前登录节点的普通账号
                "top_accounts": node_info["top_account"],   # 普通账号所属的顶级账号
                "online_device": online_device,     # 在线设备数
                "status": 1,  # 1:节点在线  0:节点离线
                "task_version": "2024_1211_001",  # 当前执行的任务版本
                "update_task": 1  # 1: 已更新最新任务 0: 未更新最新任务
            }

            response_data = HttpUtils.post(URI, json_data=node_data)

            if response_data["code"] == 200 and response_data["data"]["code"] == 200:
                print("定时上传设备数据成功")
                print(response_data["data"]["data"])
            else:
                print("定时上传设备数据失败")
                print(response_data["data"]["data"])

            time.sleep(45)

    def stop(self):
        self.flag = True


if __name__ == "__main__":
    # 当前节点信息
    # node_data = {"node_version": "v1.0",
    #              "uuid": "node_4",
    #              "normal_accounts": "13611223344",
    #              "top_accounts": "13812345678",
    #              "online_device": "100",
    #              "status": 1,
    #              "task_version": "2024_1128_001",
    #              "update_task": 1
    #              }
    pass
