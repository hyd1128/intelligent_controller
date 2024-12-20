#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/6 13:43
# @Author : limber
# @desc :
from typing import Optional
# from store_service.model.model_device import Device
# from store_service.service.service_device import DeviceService
from PyQt6.QtCore import QObject, pyqtSlot

from database_service.service.device_service import DeviceService


class DeviceHandler(QObject):
    def __init__(self):
        super().__init__()

    @pyqtSlot(int, int, int, int, result="QVariant")
    def condition_device_list_slot(self,
                                   page_number: int,
                                   total_items: int,
                                   task_status: int,
                                   online_status: int
                                   ) -> dict:
        try:
            suitable_device = DeviceService.select_by_online_task_paging(page=page_number,
                                                                         per_page=total_items,
                                                                         task_status=task_status,
                                                                         online_status=online_status)
            for i in range(len(suitable_device)):
                suitable_device[i] = suitable_device[i].to_dict()

            return {
                "code": 200,
                "data": suitable_device,
                "msg": ""
            }
        except Exception as e:
            return {
                "code": "400",
                "data": "",
                "msg": str(e)
            }

    @pyqtSlot(int, int, result="QVariant")
    def device_list_slot(self,
                         page_number: int,
                         total_items: int,
                         ) -> dict:
        try:
            suitable_device = DeviceService.select_list(page=page_number,
                                                       per_page=total_items)
            for i in range(len(suitable_device)):
                suitable_device[i] = suitable_device[i].to_dict()

            return {
                "code": 200,
                "data": suitable_device,
                "msg": ""
            }
        except Exception as e:
            return {
                "code": "400",
                "data": "",
                "msg": str(e)
            }
