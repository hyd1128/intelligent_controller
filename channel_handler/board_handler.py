#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/9 13:49
# @Author : limber
# @desc :
from datetime import datetime, timedelta
import random

from PyQt6.QtCore import QObject, pyqtSlot

from database_service.service.advertising_task_service import AdvertisingTaskService
from database_service.service.device_service import DeviceService
# from store_service.service.service_device import DeviceService
# from store_service.service.service_task import TaskService
from util import config_util
from util.config_util import NODE_DATA
from util.http_util import HttpUtils
from util.path_util import PathUtil
from util.file_util import FileUtil


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
            all_device_amount = len(DeviceService.select_all())
            online_device_amount = len(DeviceService.select_by_online_state(online_state=1))
            offline_device_amount = len(DeviceService().select_by_online_state(online_state=0))
            # todo: 累计在线时长后期使用requests来写 当前写死
            root_path = PathUtil.get_current_file_absolute_path(__file__).parent.parent
            node_info_path = root_path.joinpath(NODE_DATA)
            node_info = FileUtil.read_file_content(node_info_path)
            total_online_times = 0
            today_online_times = 0
            URI = f"/api/v1/root_accounts/accounts/get_total_task_duration/{node_info['normal_account']}"
            response_data = HttpUtils.get(URI)
            if response_data["code"] == 200 and response_data["data"]["code"] == 200:
                total_online_times = response_data["data"]["data"]["total_task_duration"]
                today_online_times = response_data["data"]["data"]["today_task_duration"]

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
            all_task = AdvertisingTaskService.select_all()
            latest_task = all_task[-1]
            current_task_id = latest_task.task_name
            latest_task_id = latest_task.task_name
            # 是否更新到最新任务
            latest_task_date = datetime.strptime(latest_task.task_release_date, "%Y-%m-%d").date()
            today_date = datetime.now().date()
            is_latest_task = 1 if latest_task_date == today_date else 0
            last_update_task_date_time = datetime.strptime(latest_task.task_release_date, "%Y-%m-%d").strftime(
                "%Y-%m-%d")
            running_status = True if not config_util.SWITCH else False
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
            recently_seven_day_running = []
            today = datetime.today()
            for i in range(1, 8):
                object_ = {}
                past_date = datetime.strftime(today - timedelta(days=i), '%Y-%m-%d')
                object_["date"] = past_date
                object_["time"] = random.randint(50, 150)
                recently_seven_day_running.append(object_)
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
