#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/18 16:10
# @Author : limber
# @desc :
from typing import List

from database_service.mapper.device_mapper import DeviceMapper
from database_service.model.device_model import Device


class DeviceService:
    @staticmethod
    def select_all() -> List[Device]:
        """
        查询全部

        :return:
        """
        return DeviceMapper.select_all()

    @staticmethod
    def select_by_id(device_id: int) -> Device | None:
        """
        根据id查询指定设备

        :param device_id:
        :return:
        """
        return DeviceMapper.select_by_id(device_id)

    @staticmethod
    def select_by_device_id(device_id: str) -> Device | None:
        """
        根据device_id查询指定设备

        :param device_id:
        :return:
        """
        return DeviceMapper.select_by_device_id(device_id)

    @staticmethod
    def add(device: Device) -> int:
        """
        添加一台设备
        :param device:
        :return:
        """
        return DeviceMapper.add(device)

    @staticmethod
    def update(device: Device) -> int:
        """
        更新设备信息

        :param device:
        :return:
        """
        return DeviceMapper.update(device)

    @staticmethod
    def select_by_online_state(online_state: int) -> List[Device]:
        return DeviceMapper.select_by_online_state(online_state)

    @staticmethod
    def select_by_online_task_paging(page: int, per_page: int,
                                     online_status: int, task_status: int):
        return DeviceMapper.select_by_online_task_paging(page,
                                                         per_page,
                                                         online_status,
                                                         task_status)

    @staticmethod
    def select_list(page: int, per_page: int) -> List[Device]:
        return DeviceMapper.select_list(page=page, per_page=per_page)

    @staticmethod
    def select_count() -> int:
        return DeviceMapper.select_count()

    @staticmethod
    def delete_device(id: int) -> int:
        return DeviceMapper.delete(id)

