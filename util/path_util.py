#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/12 11:17
# @Author : limber
# @desc :

from pathlib import Path


class PathUtil:
    @staticmethod
    def get_current_file_absolute_path(file_name: str) -> Path:
        return Path(file_name)
