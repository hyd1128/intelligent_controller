#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/11/26 7:43
# @Author : limber
# @desc :

import time
from PyQt6.QtCore import QThread
from database_service.service.device_service import DeviceService
from util.http_util import HttpUtils
from util.file_util import FileUtil
from util.path_util import PathUtil


class DeviceDetailController(QThread):

    def __init__(self):
        super().__init__()
        self.flag = False

    def run(self):
        # 统一资源定位符
        URI = "/api/v1/root_accounts/device/add_device_details"
        while True:
            time.sleep(30)
            if self.flag:
                break
            print("上传设备详细接口执行了一次")
            root_path = PathUtil.get_current_file_absolute_path(__file__).parent.parent
            node_info_path = root_path.joinpath("node_info").joinpath("info.json")
            node_info = FileUtil.read_file_content(node_info_path)

            # 每小时发送一次设备运行任务详细, 只上传设备状态是在线的, 任务状态可以暂时忽略
            # 在线状态: 1: 在线  0: 离线
            suitable_devices = DeviceService.select_by_online_state(online_state=1)
            suitable_device_data = []
            for device_ in suitable_devices:
                suitable_device_data.append({
                    "device": device_.device_id,
                    "node": node_info["node_id"],
                    "normal_accounts": node_info["normal_account"]
                })

            response_data = HttpUtils.post(URI, suitable_device_data)

            if response_data["code"] == 200 and response_data["data"]["code"] == 200:
                print("定时上传设备运行详细数据成功")
                print(response_data["data"]["data"])
            else:
                print("定时上传设备详细数据失败")
                print(response_data["data"]["data"])

    def stop(self):
        self.flag = True


if __name__ == '__main__':
    pass
