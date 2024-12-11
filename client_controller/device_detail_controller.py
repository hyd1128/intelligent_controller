#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/11/26 7:43
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


class DeviceDetailController(QThread):
    # signal = QtCore.pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.flag = False

    # 监控是否有新增
    def run(self):
        while True:
            if self.flag:
                break

            node_info = get_node_info(os.path.join(sys.path[1] + "/node_info/info.json"))
            # 要发送的 JSON 数据
            suitable_devices = DeviceService().select(online_state="online", task_state="all")
            suitable_device_data = []
            for device_ in suitable_devices:
                suitable_device_data.append({
                    "device": device_.device_id,
                    "node": node_info["node_id"],
                    "normal_accounts": node_info["normal_account"]
                })

            # 接口URL（替换为你要发送数据的实际接口地址）
            url = 'http://127.0.0.1:8000/api/v1/root_accounts/device/add_device_details'

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
            time.sleep(60)

    def stop(self):
        self.flag = True


if __name__ == '__main__':
    device_detail = {
        "device": "device_02",
        "node": "node_1",
        "normal_account": "123"
    }

    # 接口URL（替换为你要发送数据的实际接口地址）
    url = 'http://127.0.0.1:8000/api/v1/root_accounts/device/add_device_details'

    # 设置请求头
    headers = {
        'Content-Type': 'application/json'  # 指定发送 JSON 格式的数据
    }

    # 发送 POST 请求，传递 JSON 数据
    response = requests.post(url, data=json.dumps(device_detail), headers=headers)

    # 获取返回的 JSON 数据
    if response.status_code == 200:
        response_data = response.json()  # 解析返回的 JSON 数据
        print("上传成功，返回的数据：", response_data)
    else:
        print(f"请求失败，状态码: {response.status_code}")
