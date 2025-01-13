#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/18 16:10
# @Author : limber
# @desc :
from typing import List

from database_service.model.app_model import App
from database_service.mapper.script_mapper import ScriptMapper
from database_service.model.script_model import Script


class ScriptService:
    @staticmethod
    def select_by_app(app: App) -> List[Script]:
        return ScriptMapper.select_by_app(app)

    @staticmethod
    def add(script: Script) -> int:
        return ScriptMapper.add(script)

    @staticmethod
    def select_count() -> int:
        return ScriptMapper.select_count()

    @staticmethod
    def select_list(page, per_page) -> List[Script]:
        return ScriptMapper.select_list(page, per_page)

    @staticmethod
    def delete(script_id) -> int:
        return ScriptMapper.delete(script_id)
