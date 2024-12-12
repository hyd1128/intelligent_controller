#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/4 17:02
# @Author : limber
# @desc :
import os
import sys

from PyQt6.QtCore import QObject, pyqtSlot, QVariant
from client_controller.account_controller import AccountController
from util.file_util import FileUtil
from util.path_util import PathUtil


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
            root_path = PathUtil.get_current_file_absolute_path(__file__).parent.parent
            current_user_detail_path = root_path.joinpath("node_info").joinpath("current_user_detail.json")
            current_user_detail = FileUtil.read_file_content(current_user_detail_path)

            return {
                "code": 200,
                "data": current_user_detail,
                "msg": ""
            }
        except Exception as e:
            return {
                "code": 400,
                "data": "",
                "msg": str(e)
            }
