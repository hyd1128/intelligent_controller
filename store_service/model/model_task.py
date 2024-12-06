#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/9/27 11:44
# @Author : limber
# @desc :

class Task:
    """
    任务模型类
    """

    def __init__(self,
                 _id=None,
                 task_name=None,  # 任务名称
                 task_execution_duration=None,  # 任务持续执行时长
                 min_execution_times=None,  # 任务最少执行次数
                 max_execution_times=None,  # 任务最多执行次数
                 task_release_date=None,  # 任务发布日期
                 app=None  # 脚本所作用app
                 ):
        self.id = _id
        self.task_name = task_name
        self.task_execution_duration = task_execution_duration
        self.min_execution_times = min_execution_times
        self.max_execution_times = max_execution_times
        self.task_release_date = task_release_date
        self.app = app

    def to_tuple(self):
        return self.__dict__.values()

    def to_dict(self):
        return self.__dict__

    def __str__(self):
        return (f"Task("
                f"id={self.id}, "
                f"task_name={self.task_name}, "
                f"task_execution_duration={self.task_execution_duration}, "
                f"min_execution_times={self.min_execution_times}, "
                f"max_execution_times={self.max_execution_times}, "
                f"task_release_date={self.task_release_date}, "
                f"app={self.app})"
                )


if __name__ == '__main__':
    from datetime import time, datetime, date

    # time = time(8, 25, 30)
    # time.strftime("%H:%M:%S")
    # date = date(2024, 12, 15)
    # date.strftime("%Y-%m-%d")
    # print(time)
    # print(date)
    # print(datetime.now().strftime(f"%Y-%m-%d %H:%M:%S"))

    # 持续时长
    # time1 = time(8, 0, 0).strftime("%H:%M:%S")
    # print(type(time1))
    # time2 = time(9, 0, 0).strftime("%H:%M:%S")
    # print(type(time2))
    # time_obj_1 = datetime.strptime(time1, "%H:%M:%S")
    # print(type(time_obj_1))
    # time_obj_2 = datetime.strptime(time2, "%H:%M:%S")
    # print(type(time_obj_2))
    # print(time_obj_2 > time_obj_1)

    # 创建一个持续时间
    duratio_time = time(8, 0, 0).strftime("%H:%M:%S")
    # 任务发布时间
    release_task_date = datetime.now().strftime("%Y-%m-%d")

    task_info_1 = {"task_name": "prism_task_1", "task_execution_duration": duratio_time,
                   "min_execution_times": 5, "max_execution_times": 10,
                   "task_release_date": release_task_date, "app": "prism"}

    task_obj_1 = Task(**task_info_1)
    print(task_obj_1)
