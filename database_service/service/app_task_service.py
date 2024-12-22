#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/18 16:10
# @Author : limber
# @desc :
from datetime import date
from typing import List

from database_service.mapper.app_task_mapper import AppTaskMapper
from database_service.model.app_task_model import AppTask


class AppTaskService:

    @staticmethod
    def select_by_date(date_: date) -> List[AppTask]:
        return AppTaskMapper.select_by_date(date_)
