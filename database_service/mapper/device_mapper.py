#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/18 16:11
# @Author : limber
# @desc :
import json
from datetime import datetime
from typing import List

from database_service.model.device_model import Device


class DeviceMapper:
    @staticmethod
    def add(device: Device) -> int:
        """添加"""
        return device.save()

    @staticmethod
    def delete(device_id) -> int:
        """根据给定的id删除数据库记录"""
        device = Device.get(Device.id == device_id)
        return device.delete_instance()

    @staticmethod
    def update(device: Device) -> int:
        """根据id更新数据库记录"""
        return device.save()

    @staticmethod
    def select_by_id(device_id: int) -> Device | None:
        """根据id查找单条数据库记录"""
        return Device.get_or_none(Device.id == device_id)

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

    @staticmethod
    def select_by_device_id(device_id: str) -> Device | None:
        """根据device_id查询合适的设备"""
        return Device.get_or_none(Device.device_id == device_id)

    @staticmethod
    def select_by_online_state(online_state: int) -> List[Device]:
        """根据网络状态查询符合条件的设备"""
        query = Device.select().where(Device.online_state == online_state)
        return list(query)

    @staticmethod
    def select_by_online_task_paging(page: int, per_page: int, online_status: int,
                                     task_status: int):
        query = Device.select().where(
            (Device.online_state == online_status) &
            (Device.task_state == task_status)
        ).paginate(page, per_page)
        return list(query)

    @staticmethod
    def select_count() -> int:
        """获取设备总数"""
        return Device.select().count()


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
    # device_id = 4
    # result = DeviceMapper.select_by_id(device_id)
    # print(result)
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
    # result = DeviceMapper.select_all()
    # for i in result:
    #     print(type(i))
    #     print(i)

    # 根据device_id查询设备
    # result = DeviceMapper.select_by_device_id("abc4")
    # print(result)

    # 查询指定设备下载的软件
    # device = DeviceMapper.select_by_id(3)
    # for i in json.loads(device.download_app):
    #     print(i)
    #
    # download_app_list: list = json.loads(device.download_app)
    # download_app_list.append("com.itheima.java")
    # device.download_app = json.dumps(download_app_list)
    # DeviceMapper.update(device)

    # 移除指定设备的app
    # device = DeviceMapper.select_by_id(3)
    # for i in json.loads(device.download_app):
    #     print(i)
    #
    # download_app_list: list = json.loads(device.download_app)
    # download_app_list.remove("com.itheima.java")
    # device.download_app = json.dumps(download_app_list)
    # DeviceMapper.update(device)

