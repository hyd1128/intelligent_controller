#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/22 21:37
# @Author : limber
# @desc :
import json
import queue
import time
from datetime import datetime

from PyQt6.QtCore import QThread

from database_service.db import database
from database_service.model.app_task_record_model import AppTaskRecord
from database_service.model.device_model import Device
from database_service.service.app_task_record_service import AppTaskRecordService
from database_service.service.app_task_service import AppTaskService
from database_service.service.device_service import DeviceService
from util.adb_util import AdbUtil
from util.config_util import APP_TASK_TYPE_ONE, APP_TASK_TYPE_TWO, DOWNLOAD_APP_ICON
from util.device_queue import DeviceQueue
from util.image_util import ImageUtil
from util.path_util import PathUtil


class ManageAppThread(QThread):
    def __init__(self):
        super().__init__()
        self.flag = False

    def run(self):
        while True:

            # 停止管理app线程
            if self.flag:
                break

            # 1. 查询今日app任务
            have_app_task = AppTaskService.select_by_date(datetime.now().date())
            if have_app_task:
                # 2. 今日有AppTask, 获取设备
                while True:
                    # 循环结束条件
                    # 当满足今日的所有AppTask任务后退出循环
                    today_app_tasks = AppTaskService.select_by_date(datetime.now().date())
                    online_devices_amount = len(DeviceService.select_by_online_state(online_state=1))
                    is_satisfy = True
                    for app_task_ in today_app_tasks:
                        eligible_record_amount = len(AppTaskRecordService.select_by_app_task_date(app_task_,
                                                                                                  datetime.now().date()))
                        if not ((eligible_record_amount / online_devices_amount) >= app_task_.ratio):
                            is_satisfy = False
                    if is_satisfy:
                        break

                    while True:
                        device_ = self.get_device()
                        if device_ is not None:
                            break
                        else:
                            time.sleep(10)
                    # 3. 获取到设备后, 查询数据库中的任务
                    today_ = datetime.now().date()
                    today_app_tasks = AppTaskService.select_by_date(today_)
                    for app_task_ in today_app_tasks:
                        # 4. 获取到符合条件的设备, 判断AppTask的任务类型, 根据任务类型执行对应的操作
                        if app_task_.task_type == APP_TASK_TYPE_ONE:  # 下载任务
                            """
                                下载任务流程:
                                    判断该设备是否是否已下载该app
                                        已下载
                                            跳过该AppTask
                                        未下载
                                            到应用商店下载该app 
                                            添加一条AppTaskRecord
                                            向设备中添加该app的包名
                            """
                            if app_task_.app.package_name in json.loads(device_.download_app):
                                continue
                            else:
                                AdbUtil.skip_to_app_page(app_task_.app.package_name)
                                time.sleep(3)
                                AdbUtil.screen_cap(device_.device_id)
                                time.sleep(3)
                                screen_image = AdbUtil.screen_cap_pull(device_.device_id)
                                time.sleep(3)
                                root_path = PathUtil.get_current_file_absolute_path(__file__).parent.parent
                                icon_path_ = str(root_path.joinpath(DOWNLOAD_APP_ICON))
                                point_ = ImageUtil.match(screen_image, icon_path_)
                                if point_:
                                    AdbUtil.click(device_.device_id, point_[0], point_[1])
                                    time.sleep(3)
                                    try:
                                        with database.atomic():
                                            app_task_record = AppTaskRecord(
                                                device=device_,
                                                app_task=app_task_
                                            )
                                            AppTaskRecordService.add(app_task_record)
                                            download_app_list_: list = json.loads(device_.download_app)
                                            download_app_list_.append(app_task_.app.package_name)
                                            device_.download_app = json.dumps(download_app_list_)
                                            DeviceService.update(device_)
                                    except Exception as e:
                                        pass
                                    finally:
                                        AdbUtil.back_home(device_.device_id)

                        elif app_task_.task_type == APP_TASK_TYPE_TWO:  # 更新任务

                        else:
                            pass
                    # 5. 该台设备今日任务执行完毕, 将其放入任务队列中
                    self.put_device(device_)

            # 每隔1个小时检测是否有处理app任务
            time.sleep(1 * 60 * 60)

    def stop(self):
        self.flag = True

    @staticmethod
    def get_device():
        """
        一个使用队列的设备选择器
        1. 队列中的device都是未在执行任务的,只需要判断该设备是否在线
        2. 判断设备是否在线: 从队列中获取设备，并查看队列中储存的信息是否与数据库设备信息一致,队列中的设备信息需对齐数据库设备信息
        3. 存在以下情况:
            1、设备在队列中的时候, 设备从在线变为掉线
            2、设备在队列中的时候, 设备从掉线变为在线

        :return:
        """
        try:
            while True:
                device = DeviceQueue.get_nowait()
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
                        time.sleep(5)
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
