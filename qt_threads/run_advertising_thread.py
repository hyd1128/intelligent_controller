#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/19 17:07
# @Author : limber
# @desc :


from PyQt6.QtCore import QThread
from modify_position.allocation_position import appoint_position, kill_specified_process
from image.image import ImageMatch
from adb.adb import *
from util import config_util
from util.config_util import RESOURCES, POOL_FILE_NAME, THREAD_POOL_SIZE
from util.file_util import FileUtil
from util.general_util import GeneralUtil
from util.path_util import PathUtil
from util.utils import *
from datetime import datetime
from global_var import *
from concurrent.futures import ThreadPoolExecutor
from logger_zk.logger_types import logger_run

# from store_service.service.service_device import DeviceService
# from store_service.service.service_task import TaskService
# from store_service.service.service_record import RecordService
# from store_service.service.service_script import ScriptService
#
# from store_service.model.model_device import Device
# from store_service.model.model_record import Record
# from store_service.model.model_task import Task
# from store_service.model.model_script import Script

from database_service.service.device_service import DeviceService
from database_service.service.advertising_task_service import AdvertisingTaskService
from database_service.service.advertising_task_record_service import AdvertisingTaskRecordService
from database_service.service.script_service import ScriptService

from database_service.model.device_model import Device
from database_service.model.advertising_task_record_model import AdvertisingTaskRecord
from database_service.model.advertising_task_model import AdvertisingTask
from database_service.model.script_model import Script

import time
import global_var
import queue
import json


class Run(QThread):
    def __init__(self):
        super().__init__()
        self.flag = False

    def run(self):
        logger_run.info("##### 广告线程启动... #####")
        self.__set_task()

    def __set_task(self):
        """筛选任务"""

        def task_worker(_device: Device):
            tasks = self.__task()

            # 无符合条件任务,设备放回队列,线程结束,线程池回收线程
            if not tasks:
                time.sleep(30)
                DeviceQueue.put(_device)
                return

            ##############################
            else:
                suitable_task_list = []
                # 1、判断符合条件的任务是否已初始化到对应设备当日record,如果未初始化,则初始化
                for task_ in tasks:
                    device_id = _device.device_id
                    # 2、获取当日日期
                    record_date = get_date()
                    task_name = task_.task_name
                    suitable_record = RecordService().select_record(device_id, task_name, record_date)
                    # 3、如果没有符合条件的记录，则初始化该条记录，并初始化当前手机当日执行对应任务的开始时间
                    if suitable_record is None:
                        # 获取该任务的开始执行时间
                        today_execution_time = generate_start_execution_time(task_.task_execution_duration)

                        # 初始化一个Record对象
                        record_ = Record(
                            device_id=device_id,
                            task_name=task_name,
                            execution_times=0,
                            today_execution_time=today_execution_time,
                            date=record_date,
                            specify_device_execution_times=random.randint(task_.min_execution_times,
                                                                          task_.max_execution_times),
                            today_end_execution_time=generate_end_execution_time(today_execution_time,
                                                                                 task_.task_execution_duration)
                        )
                        # 将record对象存入数据库
                        RecordService().add_record(record_)
                        suitable_record = record_
                    # 4、判断当前时间是否符合任务执行时间
                    condition_one = compare_times(suitable_record.today_execution_time,
                                                  suitable_record.today_end_execution_time)
                    # 5、判断当前设备对该任务的执行次数是否符合条件
                    condition_two = suitable_record.execution_times < suitable_record.specify_device_execution_times
                    # 6、判断当前设备选中任务当次执行与上次执行的间隔时长是否符合
                    condition_three = is_suitable_interval(task_, suitable_record)
                    # condition_three = True
                    if condition_one and condition_two and condition_three:
                        suitable_task_list.append(task_)

                if suitable_task_list:
                    logger_run.info(f"当前符合条件的任务: {suitable_task_list}")
                    task = random.choice(suitable_task_list)
                    self.__run_task(task, _device)
                else:
                    """
                    以上条件都不满足：
                        1、休眠一定时间，看是否有新任务发布
                        2、当天已连接手机需要执行的任务已经执行完成，所以此时就需要更换手机，将已选定的手机放回队列
                    """
                    time.sleep(60)
                    DeviceQueue.put(_device)

        # 创建的线程池
        root_path = PathUtil.get_current_file_absolute_path(__file__).parent.parent
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
                        logger_run.info("无设备可用，等待设备...")
                        time.sleep(10)  # 如果没有设备可用，等待2秒后重试

                else:
                    logger_run.info("*** 任务暂停中 ***")
                    # 等待开关再次打开
                    while not global_var.is_running:
                        time.sleep(2)

    def __run_task(self, task: Task, device: Device):
        """任务执行"""

        try:
            logger_run.info(f"开始执行 {task.task_name} 任务")

            # 随机选取脚本
            script = self.__script(task.app)
            if device is not None and script is not None:

                # 更新设备为任务中
                device.task_state = 1

                # 重新定位软件需要满足以下条件之一
                # 1、条件1: 该设备当日第一次执行任务 Record中搜索device_id 和 date获得的结果为None
                record_data = RecordService().select_record_two(device_id=device.device_id, date=get_date())
                condition_one = len(record_data) == 1 and record_data[0].execution_times == 0
                # 2、条件2: 该设备的定位软件状态为未开启状态
                condition_two = device.locating_app_status == 0
                if condition_one or condition_two:
                    package_name = "com.ziqi.luloc"

                    if appoint_position(device.device_id, package_name):
                        logger_run.info(f"设备 {device.device_id} 目标位置设置成功")
                        device.locating_app_status = 1
                        # 获取当前时间 存入格式为 YYYY:mm:dd HH:MM:SS
                        device.locating_app_last_reload_time = datetime.now().strftime(global_var.DATE_TIME_FORMAT)
                    else:
                        logger_run.info(f"设备 {device.device_id} 目标位置设置失败")
                DeviceService().update(device)
                # 任务开始执行，对任务执行次数+1
                # 获取当前日期
                that_day = datetime.now().strftime("%Y-%m-%d")
                current_record = RecordService().select_record(device.device_id, task.task_name, that_day)
                current_record.execution_times += 1
                # 更新上一次执行时间
                current_record.task_last_execution_time = datetime.now().strftime("%H:%M:%S")
                RecordService().update_record(current_record)

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
                - home：返回主界面
                - waiting: 等待广告时间
                - adv: 广告退出坐标匹配
                - swipe: 滑动
                - back: 返回上一级
                - kill: 杀死对应程序进程
        """
        logger_run.info(f"设备 {device.device_id} 开始执行 {script.script_name} 脚本")
        # 按步骤执行
        script_content = json.loads(script.script_content)
        script.script_content = script_content
        # 统计脚本步骤
        total_steps = len(script.script_content)

        # 添加一个需求, 一个脚本点击任务的概率不大于5%
        is_execute_all_steps = probabilistic_output(random.randint(1, 5) / 100)
        is_click_adv_button = False
        if is_execute_all_steps:
            # 有95%概率该软件只执行1到5步骤
            is_click_adv_button = True
        else:
            pass

        # 执行步骤
        step = 0
        while step < total_steps:
            # 返回主界面
            if script.script_content[step] == "home":
                back_home(device.device_id)
                time.sleep(3)
                step += 1

            # 广告时间等待功能
            elif script.script_content[step] == "waiting":
                # 范围随机广告等待时间
                adv_time = random.randint(45, 70)
                logger_run.info(f"广告时间 {adv_time}s")
                time.sleep(adv_time)
                # 步骤+1
                step += 1

            # 匹配广告图标并退出广告界面
            elif script.script_content[step] == "adv":
                # 截屏
                screen_cap(device.device_id)
                time.sleep(2)
                logger_run.info("已截屏")
                # 拉取屏幕图片
                # screen_image = None
                screen_image = screen_cap_pull(device.device_id)
                time.sleep(5)
                logger_run.info("已拉取图片到电脑端")
                if not is_click_adv_button:
                    # 1、写死两种广告的匹配图标，后期优化
                    adv_icon_path = ["app/adv_icon/icon_1.png", "app/adv_icon/icon_2.png"]
                    # 2、通过匹配不同广告的退出坐标，获得一个最合适的坐标
                    best_distance = 250  # 定义的一个范围阀值
                    best_point = None
                    device_h_resolution = int(device.resolution_ratio.split("x")[0])  # 获取设备横向分辨率
                    device_top_right_corner = [device_h_resolution, 0]  # 获取设备右上角坐标
                    # 匹配
                    logger_run.info("正在进行模板匹配")
                    for icon_path in adv_icon_path:
                        point_ = ImageMatch(icon_path, screen_image).match()
                        if point_ is not None:
                            distance_ = calculate_distance(point_, device_top_right_corner)
                            if distance_ < best_distance:
                                best_distance = distance_
                                best_point = point_

                    # 获得广告退出坐标按钮
                    if best_point is not None:
                        click(device.device_id, best_point[0], best_point[1])
                    # 未获得广告退出坐标按钮
                    else:
                        # 点击返回按钮关闭广告
                        back(device.device_id)
                    time.sleep(3)
                    step += 1
                else:
                    adv_button_type_one = "app/adv_icon/icon_3.png"
                    adv_button_type_two = "app/adv_icon/icon_4.png"
                    match_point = None
                    point_one = ImageMatch(adv_button_type_one, screen_image).match()
                    if point_one:
                        match_point = point_one
                    else:
                        point_two = ImageMatch(adv_button_type_two, screen_image).match()
                        if point_two:
                            match_point = point_two

                    if match_point:
                        click(device.device_id, match_point[0], match_point[1])
                        time.sleep(3)
                        kill_specified_process(device.device_id, global_var.CHROME_PACKAGE_NAME)
                        step = total_steps - 3
                    else:
                        # 点击返回按钮关闭广告
                        back_home(device.device_id)
                        time.sleep(3)
                        step = total_steps - 3

            # 滑动页面
            elif script.script_content[step] == "swipe":
                start_coord = [540, 1600]
                end_coord = [540, 800]
                duration_time = 100  # ms
                swipe(device.device_id, start_coord, end_coord, duration_time)
                time.sleep(3)
                step += 1

            # back 返回上一级或者退出广告界面
            elif script.script_content[step] == "back":
                # back(device.device_id)
                # step += 1
                if not is_click_adv_button:
                    back(device.device_id)
                    step += 1
                else:
                    # 截屏
                    screen_cap(device.device_id)
                    time.sleep(2)
                    logger_run.info("已截屏")
                    # 拉取屏幕图片
                    # screen_image = None
                    screen_image = screen_cap_pull(device.device_id)
                    time.sleep(5)
                    logger_run.info("已拉取图片到电脑端")
                    adv_button_type_one = "app/adv_icon/icon_3.png"
                    adv_button_type_two = "app/adv_icon/icon_4.png"
                    match_point = None
                    point_one = ImageMatch(adv_button_type_one, screen_image).match()
                    if point_one:
                        match_point = point_one
                    else:
                        point_two = ImageMatch(adv_button_type_two, screen_image).match()
                        if point_two:
                            match_point = point_two

                    if match_point:
                        click(device.device_id, match_point[0], match_point[1])
                        time.sleep(3)
                        kill_specified_process(device.device_id, global_var.CHROME_PACKAGE_NAME)
                        step = total_steps - 3
                    else:
                        # 点击返回按钮关闭广告
                        back_home(device.device_id)
                        time.sleep(3)
                        step = total_steps - 3

            # kill进程
            elif script.script_content[step] == "kill":
                if script.app == "prism":
                    stop_app(device.device_id, package_prism)
                    step += 1
                elif script.app == "innova":
                    stop_app(device.device_id, package_innova)
                    step += 1
                # 添加删除计算器进程的代码
                elif script.app == "calculator":
                    stop_app(device.device_id, package_calculator)
                else:
                    step += 1

            else:
                # 当前状况为模板匹配并根据图标进行点击
                # 重试时长
                retry_duration = 0

                # 截屏
                screen_cap(device.device_id)
                time.sleep(2)
                logger_run.info("已截屏")

                # 拉取屏幕图片
                screen_image = screen_cap_pull(device.device_id)
                time.sleep(5)
                logger_run.info("已拉取图片到电脑端")

                # 匹配
                logger_run.info("正在进行模板匹配")
                point = ImageMatch(script.script_content[step], screen_image).match()
                if point:
                    logger_run.info(
                        f"目标图上模板图坐标匹配结果为: {point}, 当前匹配次数为第1次---{script.script_content[step]}")
                else:
                    logger_run.info(f"未在目标图上找到模板图坐标, 当前匹配次数为第1次---{script.script_content[step]}")

                # 未匹配到则重复匹配-每次等待10秒钟且总等待时间不超过40秒钟
                while point is None and retry_duration <= 30:
                    retry_duration += 10
                    logger_run.info(
                        f"再次匹配, 当前第 {retry_duration // 10 + 1} 次, 最多匹配 5 次, 当前任务: {script.script_name}, 当前步骤: {step}, {script.script_content[step]}")
                    # 截屏
                    screen_cap(device.device_id)
                    time.sleep(1)
                    # 拉取屏幕图片
                    screen_image = screen_cap_pull(device.device_id)
                    time.sleep(2)
                    point = ImageMatch(script.script_content[step], screen_image).match()
                    if point:
                        logger_run.info(
                            f"目标图上模板图坐标匹配结果为: {point}, 当前匹配次数为第 {retry_duration // 10 + 1} 次")
                    else:
                        logger_run.info(f"未在目标图上找到模板图坐标, 当前匹配次数为第 {retry_duration // 10 + 1} 次")

                # 未匹配到则不再执行且返回首页
                if point is None:
                    # 此时这种情况已经无法匹配对应点，后续步骤已经无法按计划进行，所以这个脚本暂停执行
                    #   1、返回桌面
                    #   2、更新手机状态，并将手机放回到全局队列中
                    #   3、关闭模拟定位后台进程
                    #   4、关闭被操作软件包进程
                    back_home(device.device_id)
                    # 更新手机任务状态
                    device.task_state = 0  # 将设备重新放回到全局设备队列中
                    DeviceQueue.put(device)
                    # 更新设备信息
                    DeviceService().update(device)
                    # 当前手机的任务执行完之后 杀死模拟定位应用进程
                    package_name = "com.ziqi.luloc"
                    kill_specified_process(device.device_id, package_name)
                    # 判断包名kill进程
                    if script.app == "prism":
                        stop_app(device.device_id, package_prism)
                    elif script.app == "innova":
                        stop_app(device.device_id, package_innova)
                    # 添加删除计算器进程的代码
                    elif script.app == "calculator":
                        stop_app(device.device_id, package_calculator)
                    else:
                        pass
                    return
                # 已匹配到则点击
                click(device.device_id, point[0], point[1])
                time.sleep(5)
                # 执行下一步
                step += 1

        # 更新手机任务状态
        device.task_state = 0
        # 当前手机的任务执行完之后 杀死模拟定位应用进程
        # 判断当前是否需要关闭定位软件
        last_reload_time = datetime.strptime(device.locating_app_last_reload_time, global_var.DATE_TIME_FORMAT)
        now_time = datetime.strptime(datetime.now().strftime(global_var.DATE_TIME_FORMAT), global_var.DATE_TIME_FORMAT)
        interval_second = (now_time - last_reload_time).total_seconds()
        if (global_var.LOCATING_APP_RELOAD_INTERVAL_TIME * 3600) < interval_second:
            package_name = "com.ziqi.luloc"
            kill_specified_process(device.device_id, package_name)
            device.locating_app_status = 0
        # 更新设备信息
        DeviceService().update(device)
        # 将设备重新放回到全局设备队列中
        DeviceQueue.put(device)

    @staticmethod
    def __task() -> List[Task]:
        """筛选符合条件的任务并随机返回一个"""
        today = GeneralUtil.get_date()  # 获得当天日期
        tasks = AdvertisingTaskService.select_by_task_execution_date(today)
        if not tasks:
            logger_run.warning(f"##### {today} 没有发布新任务 #####")

        # 当日无最新发布任务，查询历史任务并执行，最多查询前7天任务
        date_ = 1
        while not tasks and date_ < 3650:
            yesterday = GeneralUtil.get_date(before=True, n=date_)
            tasks = AdvertisingTaskService.select_by_task_execution_date(yesterday)
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
        scripts = ScriptService().select_by_app(app)
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
