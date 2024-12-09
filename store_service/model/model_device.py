#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/9/27 11:43
# @Author : limber
# @desc :


class Device:
    """
    设备模型类
    """

    def __init__(self,
                 id_=None,
                 device_id=None,  # 设置id
                 brand=None,  # 品牌
                 manufacturer=None,  # 厂商
                 android_version=None,  # 安卓版本
                 resolution_ratio=None,  # 分辨率
                 online_state=None,  # 在线状态(adb连接状态) 1表示连接 0表示未连接
                 task_state=None,  # 任务状态 1表示正在执行任务 0表示未执行任务
                 coord=None,  # 坐标
                 locating_app_status=None,  # 定位软件状态  1表示已重启 0表示未重启
                 locating_app_last_reload_time=None  # 上一次重启定位软件时间
                 ):
        self.id = id_
        self.device_id = device_id
        self.brand = brand
        self.manufacturer = manufacturer
        self.android_version = android_version
        self.resolution_ratio = resolution_ratio
        self.online_state = online_state
        self.task_state = task_state
        self.coord = coord
        self.locating_app_status = locating_app_status
        self.locating_app_last_reload_time = locating_app_last_reload_time

    def to_tuple(self):
        return self.__dict__.values()

    def to_dict(self):
        return self.__dict__

    def __str__(self):
        return (f"Device("
                f"id_={self.id}, "
                f"device_id={self.device_id}, "
                f"brand={self.brand}, "
                f"manufacturer={self.manufacturer}, "
                f"android_version={self.android_version}, "
                f"resolution_ratio={self.resolution_ratio}, "
                f"online_state={self.online_state}, "
                f"task_state={self.task_state}, "
                f"coord={self.coord}), "
                f"locating_app_status={self.locating_app_last_reload_time},"
                f"locating_app_last_reload_time={self.locating_app_last_reload_time}"
                )


if __name__ == '__main__':
    # 实例化一台设备
    device = {
        "device_id": "abcdefg",
        "brand": "xiaomi",
        "manufacturer": "xiaomi",
        "android_version": 14,
        "resolution_ratio": "1080 x 2400",
        "online_state": 1,
        "task_state": 0,
        "coord": "[]",
        "locating_app_status": 1,
        "locating_app_last_reload_time": "2024-12-6 10:00:00"
    }

    device_demo = Device(**device)
    print(device_demo)
