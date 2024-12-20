#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/9/9 15:53
# @Author : limber
# @desc :
import os
import random
import math
from datetime import datetime, timedelta

from typing import Union, List, Set, Tuple, Dict, Sequence
from util.device_queue import DeviceQueue
from logger_zk.logger_types import logger_main
from store_service.service.service_device import DeviceService
from store_service.model.model_record import Record
from store_service.model.model_task import Task


def queue_store_device_detail_config() -> None:
    """
    新版本：将所有的设备对象储存到队列中

    :return:
    """
    device_list = DeviceService().select()
    for device_obj in device_list:
        DeviceQueue.put(device_obj)

    logger_main.info("初始化全局队列完毕")


def get_date(before_today: bool = False, n: int = 1) -> str:
    """
    获取当天或之前某一天的日期

    :param before_today: 是否获取today之前的日期,默认为False
    :param n: 获取之前某一天的日期 1表示昨天 2表示前天 3表示大前天 以此类推
    :return:
    """
    current = datetime.now()
    # 默认是获得当天的日期
    if not before_today:
        return datetime.now().strftime("%Y-%m-%d")
    else:
        # 已处理处理bug, 月初的时候获取的日期不正确
        # 如果before_today为True,且指定了n,就获取该天日期,默认是获取昨天日期
        year, month, day = current.year, current.month, current.day
        if current.day <= n:
            month_days_list = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            days = day - n
            if month - 1 > 0:
                # 2-12月
                day = month_days_list[month - 2] + days
                month -= 1
            else:
                # 1月
                day = month_days_list[-1] + days
                month = 12
        else:
            day = day - n

        # 日期格式：YYYY-mm-dd
        month = str(month) if len(str(month)) > 1 else str(0) + str(month)
        day = str(day) if len(str(day)) > 1 else str(0) + str(day)
        return f"{year}-{month}-{day}"


def in_dir(directory: str, target_file: str) -> bool:
    """
    获取目录下的所有文件名,返回的是一个bool类型

    :param directory:
    :param target_file:
    :return:
    """
    file_list = os.listdir(directory)

    return target_file in file_list


def get_current_time():
    """
    获取当前时间 格式为: HH:MM:SS

    :return:
    """
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time


def compare_times(start_time: str, end_time: str) -> bool:
    """
    传入两个24小时制，格式HH:MM:SS的时间，并判断当前时间是否位于传入时间的区间内

    :param start_time:
    :param end_time:
    :return:
    """
    time_format = "%H:%M:%S"
    start_time = datetime.strptime(start_time, time_format)
    end_time = datetime.strptime(end_time, time_format)
    now_time = datetime.strptime(datetime.now().strftime(time_format), time_format)
    condition_one = now_time >= start_time
    condition_two = now_time <= end_time
    return condition_one and condition_two


def is_suitable_interval(task: Task, record: Record) -> bool:
    """
    通过当前时间，判断同一任务的当次执行和上次执行的时间间隔时长是否符合

    :param task:
    :param record:
    :return:
    """
    # 1、判断任务是否第一次执行，第一次执行直接返回True
    if record.task_last_execution_time is None:
        return True

    # 2、任务非第一次执行，获取当次执行任务的合理间隔时长
    else:
        time_format_ = "%H:%M:%S"
        duration_time_obj_ = datetime.strptime(task.task_execution_duration, time_format_)
        duration_total_second_ = duration_time_obj_.hour * 3600 + duration_time_obj_.minute * 60 + duration_time_obj_.second
        # 最大间隔时长
        # max_duration_time_ = duration_total_second_ // task.min_execution_times
        # 最小间隔时长
        min_duration_time_ = duration_total_second_ // task.max_execution_times
        # 当次合理的随机间隔时长
        suitable_interval_time_ = random.randint(min_duration_time_ - 100 if min_duration_time_ - 100 > 0 else 1,
                                                 min_duration_time_ + 100)

        # 3、判断当前时间与上次任务执行时间的间隔时长是否大于当此任务执行的合理间隔时长
        last_execution_datetime_object_ = datetime.strptime(record.task_last_execution_time, time_format_)
        now_datetime_object_ = datetime.strptime(datetime.now().strftime(time_format_), time_format_)
        interval_time_ = (now_datetime_object_ - last_execution_datetime_object_).total_seconds()

        if interval_time_ >= suitable_interval_time_:
            # 4、符合，返回True
            return True
        else:
            # 5、不符合，返回False
            return False


def calculate_distance(coord_1: Sequence[int], coord_2: Sequence[int]) -> int:
    """
        给定两个坐标 计算两个坐标之间的距离

        :param coord_1:
        :param coord_2:
        :return:
        """

    return int(math.sqrt((coord_1[0] - coord_2[0]) ** 2 + (coord_1[1] - coord_2[1]) ** 2))


def workspace_absolute_path(filename: str, n: int) -> str:
    """
    获取工作目录的绝对路径

    :param filename: 文件绝对路径
    :param n: 获得当前文件的几级父目录绝对路径，1表示当前文件直接父目录绝对路径，2级表示获得当前文件直接父目录的直接父目录绝对路径，以此类推
    :return:
    """
    current_file_path = os.path.abspath(filename)

    ancestor_absolute_path = "\\".join(current_file_path.split(".")[:-1])
    split_path = ancestor_absolute_path.split("\\")

    # 获得当前执行文件n级父目录绝对路径
    dir_absolute_path = "/".join(split_path[:(len(split_path) - n + 1)])

    return dir_absolute_path


def generate_start_execution_time(time_: str) -> str:
    """
    获取一个24小时制的时间 时间格式为HH:MM:SS 返回一个24小时制的时间
    返回的24小时时间制+传入24小时时间制 < 24:00:00
    :param time_:
    :return:
    """
    _list = time_.split(":")
    _list = [int(i) for i in _list]
    duration_hour = _list[0]
    duration_minute = _list[1]
    duration_second = _list[2]
    selection_interval_hour = 23 - duration_hour
    selection_interval_minute = 59 - duration_minute
    selection_interval_second = 60 - duration_second

    start_hour = random.randint(0, selection_interval_hour)
    start_hour = str(start_hour) if len(str(start_hour)) == 2 else str(0) + str(start_hour)
    start_minute = random.randint(0, selection_interval_minute)
    start_minute = str(start_minute) if len(str(start_minute)) == 2 else str(0) + str(start_minute)
    start_second = random.randint(0, selection_interval_second)
    start_second = str(start_second) if len(str(start_second)) == 2 else str(0) + str(start_second)

    # 生成符合条件的随机的时间戳
    template_ = f"{start_hour}:{start_minute}:{start_second}"
    return template_


def generate_end_execution_time(task_today_start_execution_time: str, task_duration_execution_time: str) -> str:
    """
    根据今日任务开始执行时间和任务持续时间生成今日任务结束时间

    注: 今日任务开始时间+任务持续时间<=24:00:00
    :param task_today_start_execution_time:
    :param task_duration_execution_time:
    :return:
    """
    time_format = "%H:%M:%S"
    start_dt_obj = datetime.strptime(task_today_start_execution_time, time_format)
    duration_dt_obj = datetime.strptime(task_duration_execution_time, time_format)
    duration_td_obj = timedelta(hours=duration_dt_obj.hour, minutes=duration_dt_obj.minute,
                                seconds=duration_dt_obj.second)
    end_dt_obj = start_dt_obj + duration_td_obj
    standard_end_time = end_dt_obj.time().isoformat("seconds")
    return standard_end_time


def probabilistic_output(probability: float) -> bool:
    """
    传入一个0-1之间的概率值 随机生成的概率值如果小于或者等于该概率值 则返回True 否则返回False

    :param probability:
    :return:
    """
    if probability < 0:
        probability = 0
    elif probability > 1:
        probability = 1
    return True if random.random() <= probability else False


if __name__ == '__main__':
    pass
