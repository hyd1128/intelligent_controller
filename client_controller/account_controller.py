#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/11/26 7:43
# @Author : limber
# @desc :
from util.config_util import NODE_DATA, CURRENT_USER_DETAIL
from util.http_util import HttpUtils
from util.path_util import PathUtil
from util.file_util import FileUtil


class AccountController:
    @staticmethod
    def login(account: str, password: str):
        uri = "/api/v1/top_accounts/user/normal_user_login"
        data = {
            "username": account,
            "password": password
        }

        # 发送 POST 请求，传递 JSON 数据
        response_data = HttpUtils.post(uri, json_data=data)

        if response_data["code"] == 200 and response_data["data"]["code"] == 200:
            print(f"用户 {account} 登录成功")
            root_path = PathUtil.get_root_path(__file__, 2)
            node_info_path = root_path.joinpath(NODE_DATA)
            node_info = FileUtil.read_file_content(node_info_path)
            update_node_info = {
                "normal_account": account,
                "password": password,
                "top_account": response_data["data"]["data"]["top_accounts"]
            }
            node_info = {**node_info, **update_node_info}
            FileUtil.write_file_content(node_info_path, node_info)
            current_user_info_path = root_path.joinpath(CURRENT_USER_DETAIL)
            FileUtil.write_file_content(current_user_info_path, response_data["data"]["data"])
            return True
        else:
            print("登录失败" +
                  "\n失败状态码: " + str(response_data["data"]["code"]) +
                  "\nstatus msg: " + str(response_data["data"]))
            return False


if __name__ == '__main__':
    AccountController.login("13611223344", "12346")
