#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/11 14:38
# @Author : limber
# @desc :
import json

import requests


class HttpUtils:
    """
    封装一个http请求工具类
    """
    base_url = "http://127.0.0.1:8000"

    @classmethod
    def post(cls, uri: str, json_data: dict | list = None, headers: dict = None):
        """
        post请求传递传递json数据

        :param uri: 资源定位符 以/开头
        :param json_data:
        :param headers:
        :return:
        """

        try:
            if headers is None:
                headers = {"Content-Type": "application/json"}

            response_ = requests.post(
                url=cls.base_url + uri,
                json=json_data,
                headers=headers
            )

            if 200 <= response_.status_code <= 299:
                # 响应返回结果的dict对象
                return {
                    "code": response_.status_code,
                    "data": response_.json()
                }
            else:
                return {
                    "code": response_.status_code,
                    "data": response_.json()
                }
        except requests.exceptions.RequestException as e:
            return {
                "code": 500,
                "data": str(e)
            }


if __name__ == '__main__':
    json_data = {
        "username": "13611223344",
        "password": "123456"
    }

    result = HttpUtils.post("/api/v1/top_accounts/user/normal_user_login", json_data=json_data)
    print(result)
