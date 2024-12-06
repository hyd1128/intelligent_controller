#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/9/27 11:43
# @Author : limber
# @desc :


class Device:
    """
    设备模型类
    """
    def __init__(self, id_=None, device_id=None, brand=None, manufacturer=None,
                 android_version=None, resolution_ratio=None, online_state=None,
                 task_state=None, coord=None, locating_app_status=None, locating_app_last_reload_time=None):

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
        return (f"Device(id_={self.id}, device_id={self.device_id}, brand={self.brand}, "
                f"manufacturer={self.manufacturer}, android_version={self.android_version}, "
                f"resolution_ratio={self.resolution_ratio}, online_state={self.online_state}, "
                f"task_state={self.task_state}, coord={self.coord}), "
                f"locating_app_status={self.locating_app_last_reload_time},"
                f"locating_app_last_reload_time={self.locating_app_last_reload_time}")


