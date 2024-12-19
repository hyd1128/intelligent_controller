#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/11 15:55
# @Author : limber
# @desc :
import json
from pathlib import Path
from typing import Any, Dict


class FileUtil:
    @staticmethod
    def read_file_content(file_path: Path | str) -> Dict:
        """从文件中读取dict格式的数据"""
        with open(file_path, mode="r", encoding="utf-8") as f:
            content_ = json.load(f)
        return content_

    @staticmethod
    def write_file_content(file_path: Path | str, file_content: dict) -> None:
        """向文件中写入dict格式的数据"""
        with open(file_path, mode="w", encoding="utf-8") as f:
            json.dump(file_content, f)

    @staticmethod
    def read_content(file_path: Path | str) -> str:
        """从文件中读取str类型的数据"""
        with open(file_path, mode="r", encoding="utf-8") as f:
            content_ = f.read()
        return content_

    @staticmethod
    def write_content(file_path: Path | str, file_content: str) -> None:
        """向文件中写入str类型的数据"""
        with open(file_path, mode="w", encoding="utf-8") as f:
            f.write(file_content)


if __name__ == '__main__':
    pass
