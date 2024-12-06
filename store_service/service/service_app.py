#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/9/28 16:20
# @Author : limber
# @desc :

from store_service.mapper.app_mapper import AppMapper
from store_service.model.model_app import App
from typing import List


class AppService:

    def select(self, app_name="") -> List[App]:
        # 1、查询所有app的名称
        app_list = AppMapper().select_all()

        # 2、选择符合条件的app
        suitable_app_list = []
        for app_ in app_list:
            condition_one = app_name == "" or app_.app == app_name
            if condition_one:
                suitable_app_list.append(app_)

        # 3、返回符合条件的app
        return suitable_app_list

    def delete_by_name(self, app_name) -> None:
        AppMapper().delete_by_name(app_name)

    def add_app(self, app: App) -> None:
        AppMapper().insert(app)



if __name__ == '__main__':
    result = AppService().select("twitter")
    for i in result:
        print(i)



