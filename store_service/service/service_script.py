#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/9/28 16:20
# @Author : limber
# @desc :

from store_service.mapper.script_mapper import ScriptMapper
from store_service.model.model_script import Script
from typing import List


class ScriptService:

    def select(self, script_name: str = "", app_name: str = "") -> List[Script]:
        # 1、查询所有脚本
        script_list = ScriptMapper().select_all()

        # 2、选择符合条件的脚本
        suitable_script_list = []
        for script_ in script_list:
            condition_one = script_name == "" or script_.script_name == script_name
            condition_two = app_name == "" or script_.app == app_name
            if condition_one and condition_two:
                suitable_script_list.append(script_)

        # 3、返回符合条件的脚本列表
        return suitable_script_list

    def select_by_app(self, app_name: str) -> List[Script]:
        # 1、查询所有脚本
        script_list = ScriptMapper().select_all()

        # 2、选择符合条件的脚本
        suitable_script_list = []
        for script_ in script_list:
            condition_one = script_.app == app_name
            if condition_one:
                suitable_script_list.append(script_)

        # 3、返回符合条件的脚本列表
        return suitable_script_list


    def delete_by_name(self, script_name: str) -> None:
        ScriptMapper().delete_by_name(script_name)

    def insert_script(self, script: Script) -> None:
        ScriptMapper().insert(script)


