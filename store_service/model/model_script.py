#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/9/27 11:44
# @Author : limber
# @desc :


class Script:
    """
    脚本模型类
    """

    def __init__(self, _id=None, script_name=None, script_content=None, app=None):
        self.id = _id
        self.script_name = script_name
        self.script_content = script_content
        self.app = app

    def to_tuple(self):
        return self.__dict__.values()

    def to_dict(self):
        return self.__dict__

    def __str__(self):
        return (f"Script(id={self.id}, script_name={self.script_name}, "
                f"script_content={self.script_content}, app={self.app}")


if __name__ == '__main__':
    script_info = {"_id": 1,
                   "script_name": "prism_task_1",
                   "script_content": "['home']",
                   "app": "prism"
                   }

    script_1 = Script(**script_info)
    print(script_1)
    print(script_1.to_dict())
    print(script_1.to_tuple())