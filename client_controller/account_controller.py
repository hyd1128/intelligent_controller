#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/11/26 7:43
# @Author : limber
# @desc :
import os
import sys
import time

import requests
import json
from util.info_util import get_node_info, edit_node_info


class AccountController:
    @staticmethod
    def login(account: str, password: str):
        url = "http://127.0.0.1:8000/api/v1/top_accounts/user/normal_user_login"
        # 设置请求头
        headers = {
            'Content-Type': 'application/json'  # 指定发送 JSON 格式的数据
        }

        data = {
            "username": account,
            "password": password
        }

        # 发送 POST 请求，传递 JSON 数据
        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            print("登录成功")
            print(response.json())
            node_info = get_node_info(os.path.join(sys.path[1] + "/node_info/info.json"))
            node_info["normal_account"] = account
            node_info["password"] = password
            node_info["top_account"] = response.json()["top_accounts"]
        else:
            print("status code: " + str(response.status_code))


if __name__ == '__main__':
    AccountController.login("13611223344", "123456")
