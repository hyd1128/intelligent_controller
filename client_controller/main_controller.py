#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/11 16:39
# @Author : limber
# @desc :

import time
import global_var
from PyQt6.QtCore import QThread
from client_controller.node_contrller import NodeController
from client_controller.device_controller import DeviceController
from client_controller.device_detail_controller import DeviceDetailController


class MainController(QThread):
    def __init__(self):
        super().__init__()
        self.flog = False
        self.device_thread = DeviceController()
        self.device_detail_thread = DeviceDetailController()
        self.node_thread = NodeController()

    def run(self):
        while True:
            if self.flog:
                break
            if global_var.is_running and not self.device_thread.isRunning():
                self.device_thread.start()
                self.device_detail_thread.start()
                self.node_thread.start()
            elif not global_var.is_running and self.device_thread.isRunning():
                self.device_thread.stop()
                self.device_detail_thread.stop()
                self.node_thread.stop()
            time.sleep(30)

    def stop(self):
        self.flog = True
