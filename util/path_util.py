#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/12 11:17
# @Author : limber
# @desc :
import os
import sys
from pathlib import Path


class PathUtil:
    @staticmethod
    def get_current_file_absolute_path(file_name: str) -> Path:
        return Path(file_name)

    @staticmethod
    def get_root_path(file_path: str, depth: int) -> Path:
        """
        根据传递过来的文件绝对路径以及相对于工作目录的层级深度, 获得工作目录路径

        该方法既能够判断打包环境也能够判断开发环境
        :param file_path:
        :param depth:
        :return:
        """

        if getattr(sys, 'frozen', False):
            exe_dir = os.path.dirname(sys.executable)
            print("当前是打包环境")
            return Path(exe_dir)

        else:
            path = Path(file_path)
            print(path)
            for i in range(depth):
                path = path.parent
            return path


if __name__ == '__main__':
    path = PathUtil.get_root_path(__file__, 2)
    print(path)



