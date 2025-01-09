#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/18 16:10
# @Author : limber
# @desc :
from typing import List

from database_service.mapper.app_mapper import AppMapper
from database_service.model.app_model import App


class AppService:
    @staticmethod
    def add(app: App) -> int:
        return AppMapper.add(app)

    @staticmethod
    def select_by_name(app_name: str) -> App:
        return AppMapper.select_by_name(app_name)

    @staticmethod
    def select_list(page, per_page) -> List[App]:
        return AppMapper.select_list(page, per_page)

    @staticmethod
    def select_count() -> int:
        return AppMapper.select_count()

    @staticmethod
    def delete_app(app_id: int) -> int:
        return AppMapper.delete(app_id)
