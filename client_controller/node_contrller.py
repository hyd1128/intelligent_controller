#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/11/26 7:43
# @Author : limber
# @desc :

import time
from datetime import datetime
from PyQt6 import QtCore
from PyQt6.QtCore import QThread
from database_service.service.advertising_task_service import AdvertisingTaskService
from database_service.service.device_service import DeviceService
from util.config_util import NODE_DATA
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
            time.sleep(10)
            if self.flag:
                break
            print("节点接口执行了一次")
            root_path = PathUtil.get_current_file_absolute_path(__file__).parent.parent
            node_info_path = root_path.joinpath(NODE_DATA)
            node_info = FileUtil.read_file_content(node_info_path)

            # 定时更新节点信息
            suitable_devices = DeviceService.select_by_online_state(online_status=1)
            latest_task = AdvertisingTaskService.select_all()[-1]
            latest_task_release_date = datetime.strptime(latest_task.task_release_date, "%Y-%m-%d").date()
            today_ = datetime.now().date()
            is_update_latest = 1 if today_ == latest_task_release_date else 0
            online_device = len(suitable_devices)

            # 当前节点信息
            node_data = {
                "uuid": node_info["node_id"],  # 节点ID
                "node_version": node_info["node_version"],  # 节点版本
                "normal_accounts": node_info["normal_account"],  # 当前登录节点的普通账号
                "top_accounts": node_info["top_account"],  # 普通账号所属的顶级账号
                "online_device": str(online_device),  # 在线设备数
                "status": 1,  # 1:节点在线  0:节点离线
                "task_version": latest_task.task_release_date,  # 当前执行的任务版本
                "update_task": is_update_latest  # 1: 已更新最新任务 0: 未更新最新任务
            }

            response_data = HttpUtils.post(URI, json_data=node_data)

            if response_data["code"] == 200 and response_data["data"]["code"] == 200:
                print("定时上传设备数据成功")
                print(response_data["data"]["data"])
            else:
                print("定时上传设备数据失败")
                print(response_data["data"]["data"])

    def stop(self):
        self.flag = True


if __name__ == "__main__":
    pass
