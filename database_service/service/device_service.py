#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/18 16:10
# @Author : limber
# @desc :
from database_service.mapper.device_mapper import DeviceMapper


class DeviceService:
    @staticmethod
    def select_all():
        """查询全部"""
        return DeviceMapper.select_all()


