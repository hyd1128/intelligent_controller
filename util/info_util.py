#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/11 15:55
# @Author : limber
# @desc :
import json


def get_node_info(path: str) -> dict:
    with open(path, mode="r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def edit_node_info(path: str, data: dict) -> None:
    with open(path, mode="w", encoding="utf-8") as f:
        json.dump(data, f)


if __name__ == '__main__':
    path = "../node_info/info.json"
    data = get_node_info(path)
    # print(data)
    data["node_id"] = "abcdef"
    data["normal_account"] = "123"
    data["password"] = "abcdef"
    data["top_account"] = "4567"
    edit_node_info(path, data)
