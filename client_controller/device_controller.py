#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/11/27 16:13
# @Author : limber
# @desc :
import os
import sys
import time

from PyQt6 import QtCore
from PyQt6.QtCore import QThread
import requests
import json

from store_service.service.service_device import DeviceService
from util.info_util import get_node_info


class DeviceController(QThread):
    signal = QtCore.pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.flag = False

    # 监控是否有新增
    def run(self):
        while True:
            if self.flag:
                break

            # node_info = get_node_info(os.path.join(sys.path[1] + "/node_info/info.json"))
            node_info = get_node_info("./node_info/info.json")
            # 要发送的 JSON 数据
            suitable_devices = DeviceService().select(online_state="all", task_state="all")
            suitable_device_data = []
            for device_ in suitable_devices:
                suitable_device_data.append({"uuid": device_.device_id,
                                             "device_model": device_.manufacturer,
                                             "network": device_.online_state,
                                             "status": device_.task_state,
                                             "node": node_info["node_id"],
                                             "normal_accounts": node_info["account"],
                                             "top_accounts": node_info["top_account"]
                                             })

            # 接口URL（替换为你要发送数据的实际接口地址）
            url = 'http://127.0.0.1:8000/api/v1/root_accounts/device/add_device'

            # 设置请求头
            headers = {
                'Content-Type': 'application/json'  # 指定发送 JSON 格式的数据
            }

            # 发送 POST 请求，传递 JSON 数据
            response = requests.post(url, data=json.dumps(suitable_device_data), headers=headers)

            # 获取返回的 JSON 数据
            if response.status_code == 200:
                response_data = response.json()  # 解析返回的 JSON 数据
                print("上传成功，返回的数据：", response_data)
            else:
                print(f"请求失败，状态码: {response.status_code}")

            time.sleep(45)

    def stop(self):
        self.flag = True


if __name__ == '__main__':
    device_data = {
        "uuid": "device_03",
        "top_accounts": "13812345678",
        "normal_accounts": "13611223344",
        "node": "node_1",
        "device_model": "xiaomi",
        "network": 1,
        "status": 1,
    }

    # 接口URL（替换为你要发送数据的实际接口地址）
    url = 'http://127.0.0.1:8000/api/v1/root_accounts/device/add_device'

    # 设置请求头
    headers = {
        'Content-Type': 'application/json'  # 指定发送 JSON 格式的数据
    }

    # 发送 POST 请求，传递 JSON 数据
    response = requests.post(url, data=json.dumps(device_data), headers=headers)

    # 获取返回的 JSON 数据
    if response.status_code == 200:
        response_data = response.json()  # 解析返回的 JSON 数据
        print("上传成功，返回的数据：", response_data)
    else:
        print(f"请求失败，状态码: {response.status_code}")
