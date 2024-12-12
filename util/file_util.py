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
        with open(file_path, mode="r", encoding="utf-8") as f:
            content_ = json.load(f)
        return content_

    @staticmethod
    def write_file_content(file_path: Path | str, file_content: dict) -> None:
        with open(file_path, mode="w", encoding="utf-8") as f:
            json.dump(file_content, f)


if __name__ == '__main__':
    pass
