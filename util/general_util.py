#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/19 16:25
# @Author : limber
# @desc :
import math
import random
from datetime import date, timedelta, time, datetime
from typing import List, Any, Sequence

from database_service.model.advertising_task_model import AdvertisingTask
from database_service.model.advertising_task_record_model import AdvertisingTaskRecord


class GeneralUtil:
    @staticmethod
    def generate_coordinate(coord_1, coord_2) -> List[float]:
        """
        采用GCJ02坐标系，实用于高德地图，微信地图由于该查询坐标接口支持小数点后六位查询，
        所以在生成新坐标前将每一个坐标扩大1000000，使用新坐标的时候再缩小1000000

        :param coord_1: 坐标1
        :param coord_2: 坐标2
        :return:
        """
        coord_1_ = [i * 1000000 for i in coord_1]
        coord_2_ = [i * 1000000 for i in coord_2]

        # 生成新的经度坐标
        if coord_1_[0] < coord_2_[0]:
            longitude1, longitude2 = coord_1_[0], coord_2_[0]
        else:
            longitude1, longitude2 = coord_2_[0], coord_1_[0]
        new_longitude = random.randint(longitude1, longitude2)

        # 生成新的纬度坐标
        if coord_1_[1] < coord_2_[1]:
            latitude1, latitude2 = coord_1_[1], coord_2_[1]
        else:
            latitude1, latitude2 = coord_2_[1], coord_1_[1]
        new_latitude = random.randint(latitude1, latitude2)

        new_coord = [new_longitude, new_latitude]
        new_coord = [i / 1000000 for i in new_coord]

        return new_coord

    @staticmethod
    def get_date(before: bool = False, n: int = 1) -> str | date:
        """
        获取当前或者之前的某一天日期 日期格式为 YYYY-mm-dd

        :param before:
        :param n:
        :return:
        """
        today = date.today()
        # 默认获取当日日期
        if not before:
            return today
        else:
            return today - timedelta(days=n)

    @staticmethod
    def generate_start_execution_time(iso_time_: str) -> str:
        """
        获取一个iso格式的时间 时间格式为HH:MM:SS 返回一个24小时制的时间
        返回的24小时时间制+传入24小时时间制 < 24:00:00

        :param iso_time_:
        :return:
        """
        duration_time = time.fromisoformat(iso_time_)
        remain_hour = time.max.hour - duration_time.hour
        remain_minute = time.max.minute - duration_time.minute
        remain_second = time.max.minute - duration_time.second

        start_hour = random.randint(0, remain_hour)
        start_minute = random.randint(0, remain_minute)
        start_second = random.randint(0, remain_second)

        start_run_task_time = time(hour=start_hour, minute=start_minute, second=start_second)
        return start_run_task_time.isoformat(timespec="seconds")

    @staticmethod
    def generate_end_execution_time(iso_start_time_: str, iso_duration_time_: str) -> str:
        start_execution_time = time.fromisoformat(iso_start_time_)
        duration_execution_time = time.fromisoformat(iso_duration_time_)
        end_execution_time = time(
            hour=start_execution_time.hour + duration_execution_time.hour,
            minute=start_execution_time.minute + duration_execution_time.minute,
            second=start_execution_time.second + duration_execution_time.second
        )
        return end_execution_time.isoformat(timespec="seconds")

    @staticmethod
    def compare_time(start_: str, end_: str) -> bool:
        """
        传入两个24小时制，格式HH:MM:SS的时间，并判断当前时间是否位于传入时间的区间内

        :param start_:
        :param end_:
        :return:
        """
        now_time = datetime.now().time()
        if (time.fromisoformat(start_) < now_time) and (now_time < time.fromisoformat(end_)):
            return True
        else:
            return False

    @staticmethod
    def is_suitable_interval(task_: AdvertisingTask, record_: AdvertisingTaskRecord) -> bool:
        """
        根据当前时间 判断同一任务的当此执行和上次执行的时间间隔时长是否符合

        :param task_:
        :param record_:
        :return:
        """

        if record_.task_last_execution_time is None:
            return True

        else:
            task_duration_time = time.fromisoformat(task_.task_execution_duration)
            task_duration_total_second = timedelta(hours=task_duration_time.hour,
                                                   minutes=task_duration_time.minute,
                                                   seconds=task_duration_time.second).total_seconds()
            # 最小间隔时长
            min_duration_time = task_duration_total_second // task_.max_execution_times
            suitable_interval_time = random.randint(min_duration_time - 100 if min_duration_time > 100 else 1,
                                                    min_duration_time + 100)
            last_execution_time = datetime.combine(date=date.today(),
                                                   time=time.fromisoformat(record_.task_last_execution_time))
            now_time = datetime.now()
            interval_time = (now_time - last_execution_time).total_seconds()
            if interval_time >= suitable_interval_time:
                return True
            else:
                return False

    @staticmethod
    def probability_tool(probability: float) -> bool:
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

    @staticmethod
    def calculate_distance(coord_1: Sequence[int], coord_2: Sequence[int]) -> int:
        """
            给定两个坐标 计算两个坐标之间的距离

            :param coord_1:
            :param coord_2:
            :return:
            """
        return int(math.sqrt((coord_1[0] - coord_2[0]) ** 2 + (coord_1[1] - coord_2[1]) ** 2))
