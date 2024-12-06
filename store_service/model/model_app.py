#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/9/27 11:43
# @Author : limber
# @desc :

class App:
    """
    app模型类
    """
    def __init__(self, id_=None, app_name=None):
        self.id = id_
        self.app = app_name

    def to_tuple(self):
        return self.__dict__.values()

    def to_dict(self):
        return self.__dict__

    def __str__(self):
        return f"App(id={self.id}, app={self.app})"
