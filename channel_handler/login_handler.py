#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/4 17:02
# @Author : limber
# @desc :
from PyQt6.QtCore import QObject, pyqtSlot, QVariant


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
        if username == "admin" and password == "admin":
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
