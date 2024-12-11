#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/4 17:02
# @Author : limber
# @desc :
import os
import sys

from PyQt6.QtCore import QObject, pyqtSlot, QVariant
from client_controller.account_controller import AccountController
from util.info_util import get_node_info


class LoginHandler(QObject):
    def __init__(self):
        super().__init__()

    @pyqtSlot(str, str, result="QVariant")
    def login_slot(self, username: str, password: str) -> dict:
        """
        登录槽函数板块

        :param username:
        :param password:
        :return:
        """
        login_result = AccountController.login(username, password)
        if login_result:
            return {
                "code": 200,
                "data": True,
                "msg": ""
            }
        else:
            return {
                "code": 401,
                "data": "",
                "msg": "用户名或密码错误"
            }

    @pyqtSlot(result="QVariant")
    def get_current_user_detail(self):
        try:
            current_user_detail = get_node_info(os.path.join(sys.path[1] + "/node_info/current_user_detail.json"))
            return {
                "code": 200,
                "data": current_user_detail,
                "msag": ""
            }
        except Exception as e:
            return {
                "code": 400,
                "data": "",
                "msg": str(e)
            }
