#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/19 15:46
# @Author : limber
# @desc :

from database_service.service.device_service import DeviceService
from logger_zk.logger_types import logger_main
from util.device_queue import DeviceQueue


class DeviceQueueUtil:
    @staticmethod
    def initialize_device_queue():
        """
        启动项目时，将数据库中的所有设备储存到队列中

        :return:
        """
        device_list = DeviceService.select_all()
        for device_ in device_list:
            DeviceQueue.put(device_)

        logger_main.info("##### 初始化队列完毕 #####")




