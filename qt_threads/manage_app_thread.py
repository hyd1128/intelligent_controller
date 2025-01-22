#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/22 21:37
# @Author : limber
# @desc :
import json
import math
import queue
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from PyQt6.QtCore import QThread

from database_service.model.device_model import Device
from database_service.service.app_task_service import AppTaskService
from database_service.service.device_service import DeviceService
from util.device_queue import DeviceQueue
from util.manage_app_util import ManageAppUtil
from util import config_util


class ManageAppThread(QThread):
    def __init__(self):
        super().__init__()
        self.flag = False

    def run(self):
        while True:
            # 每隔1个小时检测是否有处理app任务
            time.sleep(1 * 60 * 60)

            # 停止管理app线程
            if self.flag:
                break

            # 查询今日app 下载 更新 删除任务
            date_ = datetime.now().date()
            is_execution = 0  # 未执行的任务
            today_app_tasks = AppTaskService.select_by_multi_condition_one(date_, is_execution)

            if today_app_tasks:
                try:
                    config_util.SWITCH = 0  # 停止广告任务的执行
                    for app_task in today_app_tasks:
                        # 获取该节点当前在线的设备数量
                        total_device_count = len(DeviceService.select_by_online_state(online_state=1))
                        if total_device_count > 0:
                            # 提供一个容错数值 避免以外掉线设备
                            total_device_count = math.floor(total_device_count * 0.9)
                            device_list = []
                            while len(device_list) < total_device_count:
                                device_list.append(self.get_device())

                            actual_running_device_count = math.floor(total_device_count * app_task.ratio)
                            device_no_app_list = []
                            device_have_app_list = []
                            if app_task.task_type == "download" or app_task.task_type == "update":
                                for device in device_list:
                                    device_download_app = json.loads(device.download_app)
                                    if app_task.app.package_name not in device_download_app:
                                        device_no_app_list.append(device)
                                    if len(device_no_app_list) >= actual_running_device_count:
                                        break
                            else:
                                for device in device_list:
                                    device_download_app = json.loads(device.download_app)
                                    if app_task.app.package_name in device_download_app:
                                        device_have_app_list.append(device)
                                    if len(device_no_app_list) >= actual_running_device_count:
                                        break

                            if app_task.task_type == "download":
                                # 创建线程池，这里使用最大线程数为3作为示例
                                with ThreadPoolExecutor(max_workers=20) as executor:
                                    # 遍历列表，为每个元素提交任务
                                    for device in device_no_app_list:
                                        executor.submit(ManageAppUtil.download_app, device, app_task)

                            elif app_task.task_type == "update":
                                # 创建线程池，这里使用最大线程数为3作为示例
                                with ThreadPoolExecutor(max_workers=20) as executor:
                                    # 遍历列表，为每个元素提交任务
                                    for device in device_no_app_list:
                                        executor.submit(ManageAppUtil.update_app, device, app_task)

                            elif app_task.task_type == "delete":
                                # 创建线程池，这里使用最大线程数为3作为示例
                                with ThreadPoolExecutor(max_workers=20) as executor:
                                    # 遍历列表，为每个元素提交任务
                                    for device in device_no_app_list:
                                        executor.submit(ManageAppUtil.download_app, device, app_task)

                            else:
                                pass
                except Exception as e:
                    print(str(e))
                finally:
                    # 最后开启广告执行开关
                    config_util.SWITCH = 1

    def stop(self):
        self.flag = True

    @staticmethod
    def get_device():
        """
        以阻塞的方式从队列中获取设备

        :return:
        """
        try:
            while True:
                device = DeviceQueue.get()
                # 1.获取队列设备的device_id, 并查询数据库对应设备
                device_from_db = DeviceService.select_by_device_id(device_id=device.device_id)
                # 2.判断数据库中是否有对应设备, 判断该设备最新在线状态是否在线
                if device_from_db is not None:
                    if device_from_db.online_state == 1:
                        if device_from_db.online_state != device.online_state:
                            device.online_state = 1
                        return device

                    else:
                        if device_from_db.online_state != device.online_state:
                            device.online_state = device_from_db.online_state

                        # 将设备放回队列
                        DeviceQueue.put(device)
                        time.sleep(1)
        except queue.Empty:
            return None

    @staticmethod
    def put_device(device: Device):
        """
        将设备对象存放回队列中

        :param device:
        :return:
        """
        DeviceQueue.put(device)
