#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/18 16:11
# @Author : limber
# @desc :
from datetime import datetime
from typing import List

from database_service.model.device_model import Device


class DeviceMapper:
    @staticmethod
    def add(device: Device) -> int:
        """添加"""
        return device.save()

    @staticmethod
    def delete(app_id) -> int:
        """根据给定的id删除数据库记录"""
        device = Device.get(Device.id == app_id)
        return device.delete_instance()

    @staticmethod
    def update(device: Device) -> int:
        """根据id更新数据库记录"""
        return device.save()

    @staticmethod
    def select_by_id(app_id: int) -> Device:
        """根据id查找单条数据库记录"""
        return Device.get(Device.id == app_id)

    @staticmethod
    def select_list(page, per_page) -> List[Device]:
        """分页查找数据库记录"""
        query = Device.select().paginate(page, per_page)
        return list(query)

    @staticmethod
    def select_all() -> List[Device]:
        """查询全部设备"""
        query = Device.select()
        return [device_ for device_ in query]


if __name__ == '__main__':
    pass

    # 添加
    # device = Device(device_id="abc5",
    #                 brand="xiaomi",
    #                 manufacturer="xiaomi",
    #                 resolution_ration="1920 X 1040",
    #                 online_state=0,
    #                 task_state=0,
    #                 coord="[12.0001,13.0001]",
    #                 locating_app_status=1,
    #                 locating_app_last_reload_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    #
    # result = DeviceMapper.add(device)
    # print(result)

    # 删除
    # device_id = 1
    # result = DeviceMapper.delete(device_id)
    # print(result)

    # 查单个
    # app_id = 2
    # result = DeviceMapper.select_by_id(app_id)
    # print(type(result))
    # print(result.device_id)

    # 分页查询
    # page = 1
    # per_page = 3
    # result = DeviceMapper.select_list(page, per_page)
    # for i in result:
    #     print(i)
    #     print(type(i))

    # 更新
    # device = DeviceMapper.select_by_id(2)
    # device.brand = "honor"
    # device.manufacturer = "honor"
    # result = DeviceMapper.update(device)
    # print(result)

    # 查询全部设备
    result = DeviceMapper.select_all()
    for i in result:
        print(type(i))
        print(i)
