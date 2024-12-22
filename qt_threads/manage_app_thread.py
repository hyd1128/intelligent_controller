#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/22 21:37
# @Author : limber
# @desc :
from PyQt6.QtCore import QThread


class ManageAppThread(QThread):
    def __init__(self):
        super().__init__()
        self.flag = False

    def run(self):
        while True:

            # 停止管理app线程
            if self.flag:
                break

    def stop(self):
        self.flag = True
