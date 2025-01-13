#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/18 16:11
# @Author : limber
# @desc :

from typing import List

# from database_service.mapper.advertising_task_mapper import AdvertisingTaskMapper
from database_service.model.script_model import Script
from database_service.model.app_model import App
from database_service.mapper.app_mapper import AppMapper


class ScriptMapper:
    @staticmethod
    def add(script: Script) -> int:
        """添加"""
        return script.save()

    @staticmethod
    def delete(app_id) -> int:
        """根据给定的id删除数据库记录"""
        script = Script.get(Script.id == app_id)
        return script.delete_instance()

    @staticmethod
    def update(script: Script) -> int:
        """根据id更新数据库记录"""
        return script.save()

    @staticmethod
    def select_by_id(app_id: int) -> Script:
        """根据id查找单条数据库记录"""
        return Script.get(Script.id == app_id)

    @staticmethod
    def select_list(page, per_page) -> List[Script]:
        """分页查找数据库记录"""
        query = Script.select().paginate(page, per_page)
        return list(query)

    @staticmethod
    def select_by_app(app: App) -> List[Script]:
        query = Script.select().where(Script.app == app)
        return list(query)

    @staticmethod
    def select_count() -> int:
        result = Script.select().count()
        return result


if __name__ == '__main__':
    pass

    # 添加
    # app = AppMapper.select_by_id(2)
    # script = Script(
    #     script_name="2024_11_12_prism_task",
    #     script_content="[]",
    #     script_type="app",
    #     app=app
    # )
    #
    # result = ScriptMapper.add(script)
    # print(result)

    # 删除
    # device_id = 1
    # result = ScriptMapper.delete(device_id)
    # print(result)

    # 查单个
    # script_id = 3
    # result = ScriptMapper.select_by_id(script_id)
    # print(type(result))
    # print(result.script_name)

    # 分页查询
    # page = 1
    # per_page = 3
    # result = ScriptMapper.select_list(page, per_page)
    # for i in result:
    #     print(i)
    #     print(type(i))

    # 更新
    # script = ScriptMapper.select_by_id(2)
    # script.script_content = "[1]"
    #
    # result = ScriptMapper.update(script)
    # print(result)

    # 根据app获取脚本
    # task = AdvertisingTaskMapper.select_by_id(1)
    # task.app.id = 3
    # scripts = ScriptMapper.select_by_app(task.app)
    # print(scripts)

    # app = AppMapper.select_by_id(2)
    # for i in app.scripts:
    #     print(i)
