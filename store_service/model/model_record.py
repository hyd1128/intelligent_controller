#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/9/27 11:44
# @Author : limber
# @desc :


class Record:
    """
    设备-任务记录数据模型
    """

    def __init__(self,
                 _id=None,
                 device_id=None,    # 设备id
                 task_name=None,    # 任务名称
                 execution_times=None,    # 任务已执行次数
                 today_execution_time=None,   # 今日任务开始执行时间
                 date=None,    # 记录生成日期
                 deleted=0,    # 是否逻辑删除
                 specify_device_execution_times=0,    # 指定设备执行次数
                 task_last_execution_time=None,    # 任务上一次执行时间
                 today_end_execution_time=None    # 今日任务结束执行时间
                 ):
        self.id = _id
        self.device_id = device_id
        self.task_name = task_name
        self.execution_times = execution_times
        self.today_execution_time = today_execution_time
        self.date = date
        self.deleted = deleted
        self.specify_device_execution_times = specify_device_execution_times
        self.task_last_execution_time = task_last_execution_time
        self.today_end_execution_time = today_end_execution_time

    def to_tuple(self):
        return self.__dict__.values()

    def to_dict(self):
        return self.__dict__

    def __str__(self):
        return (f"Record("
                f"id={self.id}, "
                f"device_id={self.device_id}, "
                f"task_name={self.task_name}, "
                f"execution_times={self.execution_times}, "
                f"today_execution_time={self.today_execution_time}, "
                f"date={self.date}, "
                f"deleted={self.deleted}, "
                f"specify_device_execution_times={self.specify_device_execution_times}, "
                f"task_last_execution_time={self.task_last_execution_time}, "
                f"today_end_execution_time={self.today_end_execution_time})"
                )


if __name__ == '__main__':
    record_info = {"device_id": "abcdhy",
                   "task_name": "prism_task_1",
                   "execution_times": 5,
                   "today_execution_time": "08:00:00",
                   "date": "2024-9-28",
                   "deleted": 0,
                   "specify_device_execution_times": 15,
                   "task_last_execution_time": "10:50:55"
                   }

    record_obj = Record(**record_info)
    print(record_obj)

