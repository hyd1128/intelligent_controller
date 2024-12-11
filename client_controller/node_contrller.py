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


class NodeController(QThread):
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
            suitable_devices = DeviceService().select(online_state="online", task_state="all")
            online_device = len(suitable_devices)

            # 当前节点信息
            node_data = {"node_version": node_info["node_version"],
                         "uuid": node_info["node_id"],
                         "normal_accounts": node_info["normal_account"],
                         "top_accounts": node_info["top_account"],
                         "online_device": online_device,
                         "status": 1,   # 1 节点在线 0 节点离线
                         "task_version": "2024_1211_001",   # 当前执行的任务版本
                         "update_task": 1   # 是否更新最新任务
                         }

            # 接口URL（替换为你要发送数据的实际接口地址）
            url = 'http://127.0.0.1:8000/api/v1/root_accounts/device/node'

            # 设置请求头
            headers = {
                'Content-Type': 'application/json'  # 指定发送 JSON 格式的数据
            }

            # 发送 POST 请求，传递 JSON 数据
            response = requests.post(url, data=json.dumps(node_data), headers=headers)

            # 获取返回的 JSON 数据
            if response.status_code == 200:
                response_data = response.json()  # 解析返回的 JSON 数据
                print("上传成功，返回的数据：", response_data)
            else:
                print(f"请求失败，状态码: {response.status_code}")

            time.sleep(30)

    def stop(self):
        self.flag = True


if __name__ == "__main__":
    # 当前节点信息
    node_data = {"node_version": "v1.0",
                 "uuid": "node_4",
                 "normal_accounts": "13611223344",
                 "top_accounts": "13812345678",
                 "online_device": "100",
                 "status": 1,
                 "task_version": "2024_1128_001",
                 "update_task": 1
                 }

    # 接口URL（替换为你要发送数据的实际接口地址）
    url = 'http://127.0.0.1:8000/api/v1/root_accounts/device/node'

    # 设置请求头
    headers = {
        'Content-Type': 'application/json'  # 指定发送 JSON 格式的数据
    }

    # 发送 POST 请求，传递 JSON 数据
    response = requests.post(url, data=json.dumps(node_data), headers=headers)

    # 获取返回的 JSON 数据
    if response.status_code == 200:
        response_data = response.json()  # 解析返回的 JSON 数据
        print("上传成功，返回的数据：", response_data)
    else:
        print(f"请求失败，状态码: {response.status_code}")
        print(f"fail detail: {response.json()}")
