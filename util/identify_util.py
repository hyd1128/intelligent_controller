#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/11 14:37
# @Author : limber
# @desc :
import hashlib
import uuid


def generate_unique_node_token():
    # 获取机器的 MAC 地址
    mac = uuid.getnode()
    mac_str = f"{mac}"

    # 使用 MAC 地址生成固定哈希值
    unique_string = hashlib.sha256(mac_str.encode()).hexdigest()[:50]

    return unique_string


if __name__ == '__main__':
    token = generate_unique_node_token()
    print(token)
