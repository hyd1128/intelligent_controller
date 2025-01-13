#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/18 16:10
# @Author : limber
# @desc :
from datetime import date
from typing import List

from database_service.mapper.app_task_record_mapper import AppTaskRecordMapper
from database_service.model.app_task_model import AppTask
from database_service.model.app_task_record_model import AppTaskRecord


class AppTaskRecordService:
    @staticmethod
    def select_by_app_task_date(app_task: AppTask, date_: date) -> List[AppTaskRecord]:
        return AppTaskRecordMapper.select_by_app_task_date(app_task, date_)

    @staticmethod
    def add(app_task_record: AppTaskRecord) -> int:
        return AppTaskRecordMapper.add(app_task_record)

    @staticmethod
    def delete(app_task_record_id) -> int:
        return AppTaskRecordMapper.delete(app_task_record_id)

    @staticmethod
    def select_count() -> int:
        return AppTaskRecordMapper.select_count()

    @staticmethod
    def select_list(page, per_page) -> List[AppTaskRecord]:
        return AppTaskRecordMapper.select_list(page, per_page)

