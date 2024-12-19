#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/18 16:10
# @Author : limber
# @desc :
from typing import List

from database_service.model.app_model import App


class AppMapper:
    @staticmethod
    def add(app: App) -> int:
        """添加"""
        return app.save()

    @staticmethod
    def delete(app_id) -> int:
        """根据给定的id删除数据库记录"""
        app = App.get(App.id == app_id)
        return app.delete_instance()

    @staticmethod
    def update(app: App) -> int:
        """根据id更新数据库记录"""
        return app.save()

    @staticmethod
    def select_by_id(app_id: int) -> App:
        """根据id查找单条数据库记录"""
        return App.get(App.id == app_id)

    @staticmethod
    def select_list(page, per_page) -> List[App]:
        """分页查找数据库记录"""
        query = App.select().paginate(page, per_page)
        return list(query)


if __name__ == '__main__':
    pass

    # 添加
    # app = App(app_name="prism_5",
    #           package_name="com.ziqi.prism5",
    #           version="0.0.1",
    #           download_link="http://example.com",
    #           download_method="store")
    #
    # result = AppMapper.add(app)
    # print(result)

    # 删除
    # app_id = 1
    # result = AppMapper.delete(app_id)
    # print(result)

    # 查单个
    # app_id = 2
    # result = AppMapper.select_by_id(app_id)
    # print(type(result))
    # print(result.app_name)

    # 分页查询
    # page = 1
    # per_page = 3
    # result = AppMapper.select_list(page, per_page)
    # for i in result:
    #     print(i)
    #     print(type(i))

    # 更新
    # app = AppMapper.select_by_id(2)
    # app.version = "0.02"
    # result = AppMapper.update(app)
    # print(result)

