#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/9 13:49
# @Author : limber
# @desc :
from datetime import datetime, timedelta
import random

from PyQt6.QtCore import QObject, pyqtSlot
from store_service.service.service_device import DeviceService
from store_service.service.service_task import TaskService
from global_var import is_running


class BoardHandler(QObject):
    def __init__(self):
        super().__init__()

    @pyqtSlot(result="QVariant")
    def node_data_slot(self):
        """
        看板界面节点数据

        :return:
        """
        try:
            all_device_amount = len(DeviceService().select_all_devices())
            online_device_amount = len(DeviceService().select_online_state_devices(online_status=1))
            offline_device_amount = len(DeviceService().select_online_state_devices(online_status=0))
            # todo: 累计在线时长后期使用requests来写 当前写死
            total_online_times = 1090
            today_online_times = 90

            return {
                "code": 200,
                "data": {
                    "all_device_amount": all_device_amount,
                    "online_device_amount": online_device_amount,
                    "offline_device_amount": offline_device_amount,
                    "total_online_times": total_online_times,
                    "today_online_times": today_online_times
                },
                "msg": ""
            }
        except Exception as e:
            return {
                "code": 400,
                "data": "",
                "msg": str(e)
            }

    @pyqtSlot(result="QVariant")
    def task_status_slot(self):
        """
        看板界面 任务状态数据

        :return:
        """
        try:
            all_task = TaskService().select_all_no_condition()
            latest_task = all_task[-1]
            current_task_id = latest_task.task_name
            latest_task_id = latest_task.task_name
            # 是否更新到最新任务
            is_latest_task = latest_task.task_release_date == datetime.strftime(datetime.now(), "%Y-%m-%d")
            is_latest_task_status = True if is_latest_task else False
            last_update_task_date_time = datetime(2024, 12, 9, 13, 56, 58).strftime("%Y-%m-%d %H:%M:%S")
            running_status = True if not is_running else False
            return {
                "code": 200,
                "data": {
                    "current_task_id": current_task_id,
                    "latest_task_id": latest_task_id,
                    "is_latest_task": is_latest_task,
                    "last_update_task_date_time": last_update_task_date_time,
                    "running_status": running_status
                },
                "msg": ""
            }
        except Exception as e:
            return {
                "code": 400,
                "data": "",
                "msg": str(e)
            }

    @pyqtSlot(result="QVariant")
    def recently_seven_day_running_condition_slot(self):
        """
        看板界面近一周任务时长

        :return:
        """
        try:
            recently_seven_day_running = dict()
            today = datetime.today()
            for i in range(1, 8):
                past_date = datetime.strftime(today - timedelta(days=i), '%Y-%m-%d')
                recently_seven_day_running[past_date] = random.randint(50, 150)
            return {
                "code": 200,
                "data": recently_seven_day_running,
                "msg": ""
            }
        except Exception as e:
            return {
                "code": 400,
                "data": "",
                "msg": str(e)
            }

    @pyqtSlot(int, int, result="QVariant")
    def broad_notice_slot(self, page_number: int, total_items: int):
        """
        看板界面通知模块

        注:
        通知的数据类型
        {"notic_id", "notic_type": "", "notic_content": "", "notic_occur_time": ""}
        notice_type的类型有三种: local、system、task，分别对应本地通知、系统通知、任务通知
        :return:
        """
        notice_data = [
            {
                "notice_id": 1,
                "notice_type": "system",
                "notice_content": "发现新版本, 请及时更新群控终端",
                "notice_occur_time": "2024-11-08 08:00:00"
            },
            {
                "notice_id": 2,
                "notice_type": "local",
                "notice_content": "检测到设备RAYSLOCAL掉线",
                "notice_occur_time": "2024-11-09 08:00:00"
            },
            {
                "notice_id": 3,
                "notice_type": "task",
                "notice_content": "新任务已发放，任务ID: T00233, 请检查是否更新",
                "notice_occur_time": "2024-11-07 08:00:00"
            },
            {
                "notice_id": 4,
                "notice_type": "system",
                "notice_content": "发现新版本, 请及时更新群控终端",
                "notice_occur_time": "2024-11-08 08:00:00"
            },
            {
                "notice_id": 5,
                "notice_type": "local",
                "notice_content": "检测到设备RAYSLOCAL掉线",
                "notice_occur_time": "2024-11-09 08:00:00"
            },
            {
                "notice_id": 6,
                "notice_type": "task",
                "notice_content": "新任务已发放，任务ID: T00233, 请检查是否更新",
                "notice_occur_time": "2024-11-07 08:00:00"
            },
        ]

        try:
            first_ = (page_number - 1) * total_items
            last_ = first_ + total_items
            data_ = notice_data[first_:last_]
            return {
                "code": 200,
                "data": data_,
                "msg": ""
            }
        except Exception as e:
            return {
                "code": 2400,
                "data": "",
                "msg": str(e)
            }
