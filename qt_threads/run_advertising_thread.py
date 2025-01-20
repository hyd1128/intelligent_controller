#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/19 17:07
# @Author : limber
# @desc :
import random
from typing import List

from PyQt6.QtCore import QThread
from util import config_util
from util.adb_util import AdbUtil
from util.comment_util import CommentUtil
from util.config_util import RESOURCES, POOL_FILE_NAME, THREAD_POOL_SIZE, LOCATING_APP_PACKAGE_NAME, DATE_TIME_FORMAT, \
    ADVERTISING_TEMPLATE, CHROME_PACKAGE_NAME, PRISM_PACKAGE_NAME, LOCATING_APP_RELOAD_INTERVAL_TIME
from util.device_queue import DeviceQueue
from util.file_util import FileUtil
from util.general_util import GeneralUtil
from util.image_util import ImageUtil
from util.locating_util import LocatingUtil
from util.path_util import PathUtil
from datetime import datetime, date
from concurrent.futures import ThreadPoolExecutor
from logger_zk.logger_types import logger_run

from database_service.service.device_service import DeviceService
from database_service.service.advertising_task_service import AdvertisingTaskService
from database_service.service.advertising_task_record_service import AdvertisingTaskRecordService
from database_service.service.script_service import ScriptService

from database_service.model.device_model import Device
from database_service.model.advertising_task_record_model import AdvertisingTaskRecord
from database_service.model.advertising_task_model import AdvertisingTask
from database_service.model.script_model import Script

import time
import queue
import json

from util.uiautomotor_util import UIAutoMotorUtil


class RunAdvertisingThread(QThread):
    def __init__(self):
        super().__init__()
        self.flag = False

    def run(self):
        logger_run.info("##### 广告线程启动... #####")
        self.__set_task()

    def __set_task(self):
        """筛选任务"""

        def task_worker(_device: Device):
            tasks = self.__task(_device)

            # 无符合条件任务,设备放回队列,线程结束,线程池回收线程
            if not tasks:
                time.sleep(30)
                DeviceQueue.put(_device)
                return

            else:
                suitable_task_list = []
                # 1、判断符合条件的任务是否已初始化到对应设备当日record,如果未初始化,则初始化
                for task_ in tasks:
                    # 查询符合条件的记录
                    suitable_record = AdvertisingTaskRecordService.select_by_multiple_conditions(task_,
                                                                                                 _device,
                                                                                                 date.today())
                    # 3、如果没有符合条件的记录，则初始化该条记录，并初始化当前手机当日执行对应任务的开始时间
                    if suitable_record is None:
                        # 获取该任务的开始执行时间
                        today_start_execution_time = GeneralUtil.generate_start_execution_time(
                            task_.task_execution_duration)
                        today_end_execution_time = GeneralUtil.generate_end_execution_time(
                            today_start_execution_time, task_.task_execution_duration)

                        # 初始化一个Record对象
                        advertising_record_ = AdvertisingTaskRecord(
                            execution_times=0,
                            date=date.today(),
                            device=_device,
                            task=task_,
                            start_execution_time=today_start_execution_time,
                            end_execution_time=today_end_execution_time,
                            specify_device_execution_time=random.randint(task_.min_execution_times,
                                                                         task_.max_execution_times),
                        )
                        # 将record对象存入数据库
                        AdvertisingTaskRecordService.add(advertising_record_)
                        suitable_record = advertising_record_

                    # 4、判断当前时间是否符合任务执行时间
                    condition_one = GeneralUtil.compare_time(suitable_record.start_execution_time,
                                                             suitable_record.end_execution_time)

                    # 5、判断当前设备对该任务的执行次数是否符合条件
                    condition_two = suitable_record.execution_times < suitable_record.specify_device_execution_time
                    # 6、判断当前设备选中任务当次执行与上次执行的间隔时长是否符合
                    condition_three = GeneralUtil.is_suitable_interval(task_, suitable_record)
                    if condition_one and condition_two and condition_three:
                        suitable_task_list.append(task_)

                if suitable_task_list:
                    logger_run.info(f"##### 当前符合条件的任务: {suitable_task_list} #####")
                    task = random.choice(suitable_task_list)
                    self.__run_task(task, _device)
                else:
                    """
                    以上条件都不满足：
                        1、休眠一定时间，看是否有新任务发布
                        2、当天已连接手机需要执行的任务已经执行完成，所以此时就需要更换手机，将已选定的手机放回队列
                    """
                    time.sleep(30)
                    DeviceQueue.put(_device)

        # 创建的线程池
        root_path = PathUtil.get_root_path(__file__, 2)
        target_file_path = root_path.joinpath(RESOURCES).joinpath(POOL_FILE_NAME)
        content = FileUtil.read_file_content(target_file_path)
        thread_pool_size = content[THREAD_POOL_SIZE]
        logger_run.info(f"##### 当前线程数: {thread_pool_size} #####<-----***")

        with ThreadPoolExecutor(max_workers=thread_pool_size) as executor:
            while True:
                # 控制线程关闭
                if self.flag:
                    break

                logger_run.info(f"##### switch status: {config_util.SWITCH} #####")
                if config_util.SWITCH:
                    # 获取device
                    device = self.__queue_device()
                    if device:
                        logger_run.info(f"##### 当前设备: {device} #####")

                        # 提交任务到线程池
                        executor.submit(task_worker, device)

                        # 两个提交的任务之间间隔10秒
                        time.sleep(10)
                    else:
                        logger_run.info("##### 无设备可用，等待设备... #####")
                        time.sleep(10)  # 如果没有设备可用，等待2秒后重试

                else:
                    logger_run.info("##### 任务暂停中 #####")
                    # 等待开关再次打开
                    while not config_util.SWITCH:
                        time.sleep(2)

    def __run_task(self, task: AdvertisingTask, device: Device):
        """任务执行"""

        try:
            logger_run.info(f"##### 开始执行 {task.task_name} 任务 #####")

            # 随机选取脚本
            script = self.__script(task.app)
            if device is not None and script is not None:

                # 更新设备为任务中
                device.task_state = 1

                """
                重启定位软件需要满足以下两个条件之一:
                    - 条件1: 该设备当日第一次执行任务, 当日该设备在广告运行记录表中的运行记录为1且执行次数为0
                    - 条件2: 该设备的定位软件状态为未开启状态
                """
                record_data = AdvertisingTaskRecordService.select_by_device_date(device_=device, date_=date.today())
                condition_one = len(record_data) == 1 and record_data[0].execution_times == 0
                condition_two = device.locating_app_status == 0
                if condition_one or condition_two:
                    if LocatingUtil.enable_positioning(device.device_id, LOCATING_APP_PACKAGE_NAME):
                        logger_run.info(f"##### 设备 {device.device_id} 目标位置设置成功 #####")
                        device.locating_app_status = 1
                        # 获取当前时间 存入格式为 YYYY:mm:dd HH:MM:SS
                        device.locating_app_last_reload_time = datetime.now().strftime(DATE_TIME_FORMAT)
                    else:
                        logger_run.info(f"##### 设备 {device.device_id} 目标位置设置失败 #####")
                DeviceService.update(device)

                # 任务开始执行，对任务执行次数+1
                # 获取当前日期
                day_ = date.today()
                current_record = AdvertisingTaskRecordService.select_by_multiple_conditions(task_=task,
                                                                                            device_=device,
                                                                                            date_=day_)
                current_record.execution_times += 1
                # 更新上一次执行时间
                current_record.task_last_execution_time = datetime.now().strftime("%H:%M:%S")
                AdvertisingTaskRecordService.update(current_record)
                self.__run_device(device, script)
            else:
                DeviceQueue.put(device)
        except Exception as e:
            logger_run.error(f"{e}")

    def stop(self):
        self.flag = True

    # 设备执行
    @staticmethod
    def __run_device(device: Device, script: Script):
        """
            设备执行

            当前程序写的一些脚本命令:
                - click
                - home
                - back
                - start_app
                - stop_app
                - delete_app
                - wait
                - swipe
                - input
                - enter
                - browse
                - comment
        """
        logger_run.info(f"##### 设备 {device.device_id} 开始执行 {script.script_name} 脚本 #####")
        # 按步骤执行
        script.script_content = json.loads(script.script_content)

        # 统计脚本步骤
        total_steps = len(script.script_content)
        ############################################################################################
        # 新版本执行脚本程序
        ##################
        try:
            for current_step, current_script in enumerate(script.script_content):
                # 每一个步骤之间停顿两秒
                time.sleep(2)

                """
                    current_script: {
                        "action": "",  # 动作
                        "pattern": "",    # 执行方式
                        "dat`a": "",     # 具体数据
                        "wait_time": 0, # 睡眠时间
                        "execute_probability": 1   # 执行概率
                    }
                """

                ######################################
                # 点击操作
                ########
                if current_script["action"] == 'click':
                    if GeneralUtil.probability_tool(current_script["execute_probability"]):

                        ########
                        # 模板匹配
                        ########
                        if current_script["pattern"] == "IM":
                            """
                               "data": "模板图片文件名" 
                            """
                            # 截屏
                            AdbUtil.screen_cap(device.device_id)
                            # 拉取截图
                            screen_image = AdbUtil.screen_cap_pull(device.device_id)
                            template_image_path = (PathUtil.get_root_path(__file__, 2)
                                                   .joinpath(RESOURCES)
                                                   .joinpath("advertising_template").
                                                   joinpath("train_account").
                                                   joinpath(current_script["data"]))
                            point = ImageUtil.match(screen_image, str(template_image_path))
                            if point:
                                AdbUtil.click(device.device_id, point[0], point[1])
                            else:
                                retry = 2
                                while retry <= 3:
                                    AdbUtil.screen_cap(device.device_id)
                                    screen_image = AdbUtil.screen_cap_pull(device.device_id)
                                    template_image_path = (PathUtil.get_root_path(__file__, 2)
                                                           .joinpath(RESOURCES)
                                                           .joinpath("advertising_template").
                                                           joinpath("train_account").
                                                           joinpath(current_script["data"]))
                                    point = ImageUtil.match(screen_image, str(template_image_path))
                                    if point:
                                        AdbUtil.click(device.device_id, point[0], point[1])
                                        break
                                    retry += 1
                                    time.sleep(2)
                                raise Exception("坐标未找到")

                        ########
                        # UI定位
                        ########
                        elif current_script["pattern"] == "UD":
                            """
                                "data": "该元素的xpath定位"
                            """
                            UIAutoMotorUtil.click_by_xpath(device.device_id, current_script["data"])

                        ########
                        # 绝对定位
                        ########
                        elif current_script["pattern"] == "SRC":
                            """
                                "data": {
                                    "分辨率": ["横坐标", "纵坐标"],
                                    ...
                                } 
                                
                            """
                            if isinstance(current_script["data"], dict):
                                key_list = list(current_script["data"])
                                if device.resolution_ratio in key_list:
                                    position = current_script["data"][device.resolution_ratio]
                                    AdbUtil.click(device.device_id, position[0], position[1])
                        else:
                            pass
                    else:
                        # 该动作为概率动作 如果这一次的概率不在默认概率中 则认为后续步骤不再继续执行
                        break
                    # if current_script["wait_time"] >= 0:
                    #     wait_time = int(current_script["wait_time"])
                    #     if isinstance(wait_time, int):
                    #         time.sleep(wait_time)
                ######################################

                ######################################
                # 输入操作
                ########
                elif current_script["action"] == 'input':
                    if GeneralUtil.probability_tool(current_script["execute_probability"]):
                        """
                            "data": "输入的内容"
                        """
                        UIAutoMotorUtil.input_text(device.device_id, current_script["data"])
                    else:
                        break
                    # if current_script["wait_time"] >= 0:
                    #     wait_time = int(current_script["wait_time"])
                    #     if isinstance(wait_time, int):
                    #         time.sleep(wait_time)
                ######################################

                ######################################
                # 返回桌面
                ########
                elif current_script["action"] == 'home':
                    if GeneralUtil.probability_tool(current_script["execute_probability"]):
                        """
                            "data": ""
                        """
                        UIAutoMotorUtil.home(device.device_id)
                    else:
                        break
                    # if current_script["wait_time"] >= 0:
                    #     wait_time = int(current_script["wait_time"])
                    #     if isinstance(wait_time, int):
                    #         time.sleep(wait_time)
                ######################################

                ######################################
                # 返回
                ########
                elif current_script["action"] == 'back':
                    if GeneralUtil.probability_tool(current_script["execute_probability"]):
                        """
                            "data": "输入的内容"
                        """
                        UIAutoMotorUtil.back(device.device_id)
                    else:
                        break
                    # if current_script["wait_time"] >= 0:
                    #     wait_time = int(current_script["wait_time"])
                    #     if isinstance(wait_time, int):
                    #         time.sleep(wait_time)
                ######################################

                ######################################
                # 关闭软件
                ########
                elif current_script["action"] == 'stop_app':
                    if GeneralUtil.probability_tool(current_script["execute_probability"]):
                        """
                            "data": "app_package_name"
                        """
                        UIAutoMotorUtil.stop_app(device.device_id, current_script["data"])
                    else:
                        break
                    # if current_script["wait_time"] >= 0:
                    #     wait_time = int(current_script["wait_time"])
                    #     if isinstance(wait_time, int):
                    #         time.sleep(wait_time)

                ######################################
                # 启动软件
                ########
                elif current_script["action"] == 'start_app':
                    if GeneralUtil.probability_tool(current_script["execute_probability"]):
                        """
                            "data": "app包名"
                        """
                        UIAutoMotorUtil.start_app(device.device_id, current_script["data"])
                    else:
                        break
                    # if current_script["wait_time"] >= 0:
                    #     wait_time = int(current_script["wait_time"])
                    #     if isinstance(wait_time, int):
                    #         time.sleep(wait_time)
                ######################################

                ######################################
                # 删除软件
                ########
                elif current_script["action"] == 'delete_app':
                    """
                        "data": "app包名"
                    """
                    if GeneralUtil.probability_tool(current_script["execute_probability"]):
                        UIAutoMotorUtil.delete_app(device.device_id, current_script["data"])
                    else:
                        break
                    # if current_script["wait_time"] >= 0:
                    #     wait_time = int(current_script["wait_time"])
                    #     if isinstance(wait_time, int):
                    #         time.sleep(wait_time)
                ######################################

                ######################################
                # 滑动操作
                ########
                elif current_script["action"] == 'swipe':
                    """
                        "data": {
                            "position": [["开始x", "开始y"], ["结束x", "结束y"]]，
                            "duration": float
                        }
                    """
                    if GeneralUtil.probability_tool(current_script["execute_probability"]):
                        if isinstance(current_script["data"], dict):
                            position = [
                                tuple(current_script["data"]["position"][0]),
                                tuple(current_script["data"]["position"][1])
                            ]
                            UIAutoMotorUtil.swipe_by_coord(device.device_id, position,
                                                           current_script["data"]["duration"])
                    else:
                        break
                    # if current_script["wait_time"] >= 0:
                    #     wait_time = int(current_script["wait_time"])
                    #     if isinstance(wait_time, int):
                    #         time.sleep(wait_time)
                ######################################

                ######################################
                # 确认操作
                ########
                elif current_script["action"] == 'enter':
                    if GeneralUtil.probability_tool(current_script["execute_probability"]):
                        """
                            "data": ""
                        """
                        UIAutoMotorUtil.enter(device.device_id)
                    else:
                        break
                    # if current_script["wait_time"] >= 0:
                    #     wait_time = int(current_script["wait_time"])
                    #     if isinstance(wait_time, int):
                    #         time.sleep(wait_time)
                ######################################

                ######################################
                # 等待操作
                ########
                elif current_script["action"] == 'wait':
                    """
                        "data": int
                    """
                    if GeneralUtil.probability_tool(current_script["execute_probability"]):
                        time.sleep(current_script["data"])
                    else:
                        break
                    # if current_script["wait_time"] >= 0:
                    #     wait_time = int(current_script["wait_time"])
                    #     if isinstance(wait_time, int):
                    #         time.sleep(wait_time)
                ######################################

                ######################################
                # 刷短视频操作
                ########
                elif current_script["action"] == 'browse':
                    """
                        当前默认为的操作流程为 滑动短视频 概率评论 概率点赞 概率收藏
                        "data": {
                            "app_name": str,
                            "mode": str, "xpath" or "tradition"
                            "browse_type": "", # 可选值 vedio和place 1. 短视频类 2.地图索引类
                            "total_duration_time": int, # 秒为单位
                            "once_duration_time": int, # 秒为单位
                            "review_probability": float, # 0-1
                            "like_probability": float, # 0-1
                            "collect_probability": float, # 0-1
                        }
                    """
                    if GeneralUtil.probability_tool(current_script["execute_probability"]):
                        start_browse_time = datetime.now()
                        duration_browse_time = 0
                        if current_script["data"]["app_name"] == "youtube":
                            print(type(current_script["data"]))
                            print(current_script["data"])
                            print(current_script["data"]["total_duration_time"])
                            total_browse_time = current_script["data"]["total_duration_time"]
                            while duration_browse_time <= total_browse_time:
                                time.sleep(current_script["data"]["once_duration_time"])

                                if GeneralUtil.probability_tool(current_script["data"]["review_probability"]):
                                    time.sleep(2)
                                    d = UIAutoMotorUtil().generate_uam(device.device_id)
                                    d(className="android.widget.FrameLayout",
                                      resourceId="com.google.android.youtube:id/elements_button_bar_container").child(
                                        className="android.widget.ImageView")[2].click()
                                    time.sleep(2)
                                    d(className="android.widget.FrameLayout",
                                      resourceId="com.google.android.youtube:id/footer").child(
                                        className="android.widget.EditText")[0].click()

                                    if current_script["data"]["browse_type"] == "vedio":
                                        text_ = CommentUtil.multi_media_review()
                                        d.send_keys(text_)
                                        time.sleep(2)
                                        d(className="android.widget.FrameLayout",
                                          resourceId="com.google.android.youtube:id/interstitials_container").child(
                                            className="android.widget.ImageView")[1].click()
                                        time.sleep(2)
                                        AdbUtil.back(device.device_id)

                                    else:
                                        text_ = CommentUtil.place_review()
                                        d.send_keys(text_)
                                        d(className="android.widget.FrameLayout",
                                          resourceId="com.google.android.youtube:id/interstitials_container").child(
                                            className="android.widget.ImageView")[1].click()
                                        time.sleep(2)
                                        # d(className="android.widget.ImageView", resourceId="com.google.android.youtube:id/close_button").click()
                                        # UIAutoMotorUtil.click_by_xpath(device.device_id, '//*[@resource-id="com.google.android.youtube:id/close_button"]')
                                        # UIAutoMotorUtil.back(device.device_id)
                                        AdbUtil.back(device.device_id)

                                if GeneralUtil.probability_tool(current_script["data"]["like_probability"]):
                                    time.sleep(2)
                                    d = UIAutoMotorUtil().generate_uam(device.device_id)
                                    d(className="android.widget.FrameLayout",
                                      resourceId="com.google.android.youtube:id/elements_button_bar_container").child(
                                        className="android.widget.ImageView")[0].click()

                                # if GeneralUtil.probability_tool(current_script["data"]["collect_probability"]):
                                #     UIAutoMotorUtil.click_by_xpath(device.device_id,
                                #                                    '//android.view.ViewGroup[@text="Subscribe"]')

                                UIAutoMotorUtil.swipe_by_coord(device.device_id, [(584, 1630), (584, 240)], 0.2)
                                duration_browse_time = (datetime.now() - start_browse_time).total_seconds()
                        else:
                            pass

                    else:
                        break
                # if current_script["wait_time"] >= 0:
                #     wait_time = int(current_script["wait_time"])
                #     if isinstance(wait_time, int):
                #         time.sleep(wait_time)

                ######################################

                ######################################
                # 评论操作
                ########
                elif current_script["action"] == 'comment':
                    """
                        "data": ""
                    """
                    if GeneralUtil.probability_tool(current_script["execute_probability"]):
                        text_ = CommentUtil.place_review()
                        UIAutoMotorUtil.input_text(device.device_id, text_)
                    else:
                        break
                # if current_script["wait_time"] >= 0:
                #     wait_time = int(current_script["wait_time"])
                #     if isinstance(wait_time, int):
                #         time.sleep(wait_time)
                ######################################

                ######################################
                # 未知操作
                ########
                else:
                    if GeneralUtil.probability_tool(current_script["execute_probability"]):
                        pass
                    else:
                        pass
                if current_script["wait_time"] >= 0:
                    wait_time = int(current_script["wait_time"])
                    if isinstance(wait_time, int):
                        time.sleep(wait_time)
                ######################################

        except Exception as e:
            # 如果是在执行任务的过程中出现了异常, 则需要停止app并返回到手机主界面
            UIAutoMotorUtil.home(device.device_id)
            UIAutoMotorUtil.stop_app(device.device_id, script.app.package_name)
            print(f"error: {str(e)}")
            logger_run.error(str(e))

        finally:
            # 更新手机任务状态
            device.task_state = 0
            # 判断当前是否需要关闭定位软件
            last_reload_time = datetime.strptime(str(device.locating_app_last_reload_time), DATE_TIME_FORMAT)
            now_time = datetime.now()
            interval_second = (now_time - last_reload_time).total_seconds()
            if (LOCATING_APP_RELOAD_INTERVAL_TIME * 3600) < interval_second:
                AdbUtil.stop_app(device.device_id, LOCATING_APP_PACKAGE_NAME)
                device.locating_app_status = 0
            # 更新设备信息
            DeviceService.update(device)
            # 将设备重新放回到全局设备队列中
            DeviceQueue.put(device)

        ############################################################################################

        ############################################################################################
        # 老版本执行脚本流程
        ###################
        # # 点击广告下载应用的概率小于等于5%
        # is_execute_all_steps = GeneralUtil.probability_tool(random.randint(1, 30) / 100)
        # is_click_adv_button = False
        # if is_execute_all_steps:
        #     is_click_adv_button = True
        #
        # step = 0
        # while step < total_steps:
        #     # 返回主界面
        #     if script.script_content[step] == "home":
        #         AdbUtil.back_home(device.device_id)
        #         time.sleep(3)
        #         step += 1
        #
        #     # 广告时间等待功能
        #     elif script.script_content[step] == "waiting":
        #         # 范围随机广告等待时间
        #         adv_time = random.randint(45, 70)
        #         logger_run.info(f"##### 广告时间 {adv_time}s ######")
        #         time.sleep(adv_time)
        #         # 步骤+1
        #         step += 1
        #
        #     # 匹配广告图标并退出广告界面
        #     elif script.script_content[step] == "adv":
        #         # 截屏
        #         AdbUtil.screen_cap(device.device_id)
        #         time.sleep(2)
        #         logger_run.info("##### 已截屏 #####")
        #         # 拉取屏幕图片
        #         screen_image = AdbUtil.screen_cap_pull(device.device_id)
        #         time.sleep(5)
        #         logger_run.info("##### 已拉取图片到电脑端 #####")
        #         root_path = PathUtil.get_root_path(__file__, 2)
        #         if not is_click_adv_button:
        #             # 1、写死两种广告的匹配图标，后期优化
        #             adv_icon_path = ["icon_1.png", "icon_2.png"]
        #             # 2、通过匹配不同广告的退出坐标，获得一个最合适的坐标
        #             best_distance = 250  # 定义的一个范围阀值
        #             best_point = None
        #             device_h_resolution = int(device.resolution_ratio.split("x")[0])  # 获取设备横向分辨率
        #             device_top_right_corner = [device_h_resolution, 0]  # 获取设备右上角坐标
        #             # 匹配
        #             logger_run.info("##### 正在进行模板匹配... #####")
        #             for icon_path in adv_icon_path:
        #                 icon_path_ = str(root_path.joinpath(ADVERTISING_TEMPLATE).joinpath(icon_path))
        #                 point_ = ImageUtil.match(screen_image, icon_path_)
        #                 if point_ is not None:
        #                     distance_ = GeneralUtil.calculate_distance(point_, device_top_right_corner)
        #                     if distance_ < best_distance:
        #                         best_distance = distance_
        #                         best_point = point_
        #
        #             # 获得广告退出坐标按钮
        #             if best_point is not None:
        #                 AdbUtil.click(device.device_id, best_point[0], best_point[1])
        #             # 未获得广告退出坐标按钮
        #             else:
        #                 # 点击返回按钮关闭广告
        #                 AdbUtil.back(device.device_id)
        #             time.sleep(3)
        #             step += 1
        #         else:
        #             adv_button_type_one = str(root_path.joinpath(ADVERTISING_TEMPLATE).joinpath("icon_3.png"))
        #             adv_button_type_two = str(root_path.joinpath(ADVERTISING_TEMPLATE).joinpath("icon_4.png"))
        #             match_point = None
        #             point_one = ImageUtil.match(screen_image, adv_button_type_one)
        #             if point_one:
        #                 match_point = point_one
        #             else:
        #                 point_two = ImageUtil.match(screen_image, adv_button_type_two)
        #                 if point_two:
        #                     match_point = point_two
        #
        #             if match_point:
        #                 AdbUtil.click(device.device_id, match_point[0], match_point[1])
        #                 time.sleep(3)
        #                 AdbUtil.stop_app(device.device_id, CHROME_PACKAGE_NAME)
        #                 step = total_steps - 3
        #             else:
        #                 # 点击返回按钮关闭广告
        #                 AdbUtil.back_home(device.device_id)
        #                 time.sleep(3)
        #                 step = total_steps - 3
        #
        #     # 滑动页面
        #     elif script.script_content[step] == "swipe":
        #         start_coord = [540, 1600]
        #         end_coord = [540, 800]
        #         duration_time = 100  # ms
        #         AdbUtil.swipe(device.device_id, start_coord, end_coord, duration_time)
        #         time.sleep(3)
        #         step += 1
        #
        #     # back 返回上一级或者退出广告界面
        #     elif script.script_content[step] == "back":
        #         if not is_click_adv_button:
        #             AdbUtil.back(device.device_id)
        #             step += 1
        #         else:
        #             # 截屏
        #             AdbUtil.screen_cap(device.device_id)
        #             time.sleep(2)
        #             logger_run.info("##### 已截屏 #####")
        #             screen_image = AdbUtil.screen_cap_pull(device.device_id)
        #             time.sleep(5)
        #             logger_run.info("##### 已拉取图片到电脑端 #####")
        #             root_path = PathUtil.get_root_path(__file__, 2)
        #             adv_button_type_one = str(root_path.joinpath(ADVERTISING_TEMPLATE).joinpath("icon_3.png"))
        #             adv_button_type_two = str(root_path.joinpath(ADVERTISING_TEMPLATE).joinpath("icon_4.png"))
        #             match_point = None
        #             point_one = ImageUtil.match(screen_image, adv_button_type_one)
        #             if point_one:
        #                 match_point = point_one
        #             else:
        #                 point_two = ImageUtil.match(screen_image, adv_button_type_two)
        #                 if point_two:
        #                     match_point = point_two
        #
        #             if match_point:
        #                 AdbUtil.click(device.device_id, match_point[0], match_point[1])
        #                 time.sleep(3)
        #                 AdbUtil.stop_app(device.device_id, CHROME_PACKAGE_NAME)
        #                 step = total_steps - 3
        #             else:
        #                 # 点击返回按钮关闭广告
        #                 AdbUtil.back_home(device.device_id)
        #                 time.sleep(3)
        #                 step = total_steps - 3
        #
        #     # kill进程
        #     elif script.script_content[step] == "kill":
        #         if script.app.app_name == "prism":
        #             AdbUtil.stop_app(device.device_id, PRISM_PACKAGE_NAME)
        #             step += 1
        #         else:
        #             step += 1
        #
        #     else:
        #         retry_count = 1
        #         # 截屏
        #         AdbUtil.screen_cap(device.device_id)
        #         time.sleep(2)
        #         logger_run.info("##### 已截屏 #####")
        #
        #         # 拉取屏幕图片
        #         screen_image = AdbUtil.screen_cap_pull(device.device_id)
        #         time.sleep(5)
        #         logger_run.info("##### 已拉取图片到电脑端 #####")
        #
        #         # 匹配
        #         point = ImageUtil.match(screen_image, script.script_content[step])
        #         if point:
        #             logger_run.info(
        #                 f"当前匹配次数: {retry_count}---匹配结果: {point}---{script.script_content[step]}")
        #         else:
        #             logger_run.info(
        #                 f"当前匹配次数: {retry_count}---匹配结果: 无匹配坐标---{script.script_content[step]}")
        #
        #         # 未匹配到则再重复匹配4次后结束
        #         while point is None and retry_count < 5:
        #             retry_count += 1
        #             # 截屏
        #             AdbUtil.screen_cap(device.device_id)
        #             time.sleep(1)
        #             # 拉取屏幕图片
        #             screen_image = AdbUtil.screen_cap_pull(device.device_id)
        #             time.sleep(2)
        #             point = ImageUtil.match(screen_image, script.script_content[step])
        #             if point:
        #                 logger_run.info(
        #                     f"当前匹配次数: {retry_count}---匹配结果: {point}---{script.script_content[step]}")
        #             else:
        #                 logger_run.info(
        #                     f"当前匹配次数: {retry_count}---匹配结果: 无匹配坐标---{script.script_content[step]}")
        #
        #         # 未匹配到则不再执行且返回首页
        #         if point is None:
        #             """
        #             此时这种情况已经无法匹配对应点，后续步骤已经无法按计划进行，所以这个脚本暂停执行
        #                   1、返回桌面
        #                   2、更新手机状态，并将手机放回到全局队列中
        #                   3、关闭模拟定位后台进程
        #                   4、关闭被操作软件进程
        #             """
        #             AdbUtil.back_home(device.device_id)
        #             # 更新手机任务状态
        #             device.task_state = 0  # 将设备重新放回到全局设备队列中
        #             DeviceQueue.put(device)
        #             # 更新设备信息
        #             DeviceService.update(device)
        #             # 当前手机的任务执行完之后 关闭模拟定位应用进程
        #             AdbUtil.stop_app(device.device_id, LOCATING_APP_PACKAGE_NAME)
        #             # 判断包名kill进程
        #             if script.app.app_name == "prism":
        #                 AdbUtil.stop_app(device.device_id, PRISM_PACKAGE_NAME)
        #             return
        #         # 已匹配到则点击
        #         AdbUtil.click(device.device_id, point[0], point[1])
        #         time.sleep(5)
        #         # 执行下一步
        #         step += 1

        # # 更新手机任务状态
        # device.task_state = 0
        # # 当前手机的任务执行完之后 关闭模拟定位应用进程
        # # 判断当前是否需要关闭定位软件
        # last_reload_time = datetime.strptime(str(device.locating_app_last_reload_time), DATE_TIME_FORMAT)
        # now_time = datetime.now()
        # interval_second = (now_time - last_reload_time).total_seconds()
        # if (LOCATING_APP_RELOAD_INTERVAL_TIME * 3600) < interval_second:
        #     AdbUtil.stop_app(device.device_id, LOCATING_APP_PACKAGE_NAME)
        #     device.locating_app_status = 0
        # # 更新设备信息
        # DeviceService.update(device)
        # # 将设备重新放回到全局设备队列中
        # DeviceQueue.put(device)
        ############################################################################################

    @staticmethod
    def __task(device: Device) -> List[AdvertisingTask] | None:
        """筛选符合条件的任务并随机返回一个"""
        today = GeneralUtil.get_date()  # 获得当天日期
        tasks = AdvertisingTaskService.select_by_task_execution_date(today)
        ############# 新需求: 任务的执行有比例要求 #############
        download_app_list_ = json.loads(device.download_app)

        if not download_app_list_:
            return None

        # 条件1: 该任务未满足今日的执行比例
        online_devices_amounts = len(DeviceService.select_by_online_state(online_state=1))
        suitable_tasks = []
        for task in tasks:
            eligible_record_ = len(AdvertisingTaskRecordService.select_by_task_date(task, date.today()))
            if eligible_record_ / online_devices_amounts <= task.ratio:
                suitable_tasks.append(task)
            elif AdvertisingTaskRecordService.select_by_device_date(device, date.today()):
                suitable_tasks.append(task)
            else:
                pass
        tasks = suitable_tasks
        # 条件2: 在该台设备上安装了该task对应的app
        tasks = [task for task in tasks if task.app.package_name in download_app_list_]
        ##############################################################
        if not tasks:
            logger_run.warning(f"##### {today} 没有发布新任务 #####")

        # 当日无最新发布任务，查询历史任务并执行
        date_ = 1
        while not tasks and date_ < 3650:
            yesterday = GeneralUtil.get_date(before=True, n=date_)
            tasks = AdvertisingTaskService.select_by_task_execution_date(yesterday)
            ############# 新需求: 任务的执行有比例要求 #############
            download_app_list_ = json.loads(device.download_app)
            # 条件1: 该任务未满足今日的执行比例
            online_devices_amounts = len(DeviceService.select_by_online_state(online_state=1))
            suitable_tasks = []
            for task in tasks:
                eligible_record_ = len(AdvertisingTaskRecordService.select_by_task_date(task, date.today()))
                if eligible_record_ / online_devices_amounts <= task.ratio:
                    suitable_tasks.append(task)
                elif AdvertisingTaskRecordService.select_by_device_date(device, date.today()):
                    suitable_tasks.append(task)
                else:
                    pass
            tasks = suitable_tasks
            # 条件2: 在该台设备上安装了该task对应的app
            tasks = [task for task in tasks if task.app.package_name in download_app_list_]
            ##############################################################
            if not tasks:
                logger_run.info(f"##### {yesterday} 没有发布新任务 #####")
                date_ += 1
        if not tasks:
            logger_run.info("##### 无任务 #####")
            return tasks
        return tasks

    # 随机选取一个脚本
    @staticmethod
    def __script(app):
        scripts = ScriptService.select_by_app(app)
        if len(scripts) > 0:
            return random.choice(scripts)
        return None

    @staticmethod
    def __queue_device():
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
                logger_run.info("##### 获取设备 #####")
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


if __name__ == '__main__':
    pass
